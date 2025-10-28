"""
Utility functions for data processing and analysis
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


def clean_financial_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and prepare financial data for analysis
    
    Args:
        df: Raw financial dataframe
        
    Returns:
        Cleaned dataframe
    """
    if df is None or df.empty:
        return pd.DataFrame()
    
    # Remove rows with all NaN values
    df = df.dropna(how='all')
    
    # Forward fill missing values (common in financial data)
    df = df.fillna(method='ffill', limit=2)
    
    return df


def calculate_percentage_change(current: float, previous: float) -> float:
    """
    Calculate percentage change between two values
    
    Args:
        current: Current value
        previous: Previous value
        
    Returns:
        Percentage change
    """
    if previous == 0 or pd.isna(previous) or pd.isna(current):
        return 0.0
    
    return ((current - previous) / abs(previous)) * 100


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default if denominator is zero
    
    Args:
        numerator: Numerator value
        denominator: Denominator value
        default: Default value to return if division fails
        
    Returns:
        Division result or default value
    """
    if denominator == 0 or pd.isna(denominator) or pd.isna(numerator):
        return default
    
    return numerator / denominator


def get_date_range(period: str = '1y') -> tuple:
    """
    Get start and end dates for a given period
    
    Args:
        period: Period string (e.g., '1y', '6m', '3m')
        
    Returns:
        Tuple of (start_date, end_date)
    """
    end_date = datetime.now()
    
    period_map = {
        '1m': 30,
        '3m': 90,
        '6m': 180,
        '1y': 365,
        '2y': 730,
        '5y': 1825
    }
    
    days = period_map.get(period, 365)
    start_date = end_date - timedelta(days=days)
    
    return start_date, end_date


def calculate_moving_average(data: pd.Series, window: int) -> pd.Series:
    """
    Calculate moving average for a series
    
    Args:
        data: Data series
        window: Window size for moving average
        
    Returns:
        Moving average series
    """
    return data.rolling(window=window, min_periods=1).mean()


def detect_outliers(data: pd.Series, threshold: float = 3.0) -> pd.Series:
    """
    Detect outliers using z-score method
    
    Args:
        data: Data series
        threshold: Z-score threshold for outlier detection
        
    Returns:
        Boolean series indicating outliers
    """
    if len(data) < 2:
        return pd.Series([False] * len(data), index=data.index)
    
    z_scores = np.abs((data - data.mean()) / data.std())
    return z_scores > threshold


def format_currency(value: float, currency: str = 'USD') -> str:
    """
    Format a number as currency
    
    Args:
        value: Numeric value
        currency: Currency code
        
    Returns:
        Formatted currency string
    """
    if pd.isna(value):
        return "N/A"
    
    if abs(value) >= 1e9:
        return f"${value/1e9:.2f}B"
    elif abs(value) >= 1e6:
        return f"${value/1e6:.2f}M"
    elif abs(value) >= 1e3:
        return f"${value/1e3:.2f}K"
    else:
        return f"${value:.2f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format a number as percentage
    
    Args:
        value: Numeric value
        decimals: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    if pd.isna(value):
        return "N/A"
    
    return f"{value:.{decimals}f}%"


def get_risk_level(score: float, high_threshold: float = 0.7, 
                   medium_threshold: float = 0.4) -> str:
    """
    Determine risk level based on score
    
    Args:
        score: Risk score (0-1)
        high_threshold: Threshold for high risk
        medium_threshold: Threshold for medium risk
        
    Returns:
        Risk level string
    """
    if score >= high_threshold:
        return "HIGH"
    elif score >= medium_threshold:
        return "MEDIUM"
    else:
        return "LOW"


def extract_financial_value(value: Any) -> float:
    """
    Extract numeric value from various financial data formats
    
    Args:
        value: Value to extract (can be string, int, float, etc.)
        
    Returns:
        Numeric value
    """
    if pd.isna(value):
        return 0.0
    
    if isinstance(value, (int, float)):
        return float(value)
    
    if isinstance(value, str):
        # Remove common currency symbols and formatting
        value = value.replace('$', '').replace(',', '').replace('%', '')
        value = value.replace('(', '-').replace(')', '')
        
        try:
            return float(value)
        except ValueError:
            return 0.0
    
    return 0.0


def calculate_growth_rate(values: list) -> float:
    """
    Calculate compound annual growth rate (CAGR)
    
    Args:
        values: List of values over time
        
    Returns:
        CAGR as percentage
    """
    if len(values) < 2:
        return 0.0
    
    values = [v for v in values if not pd.isna(v) and v > 0]
    
    if len(values) < 2:
        return 0.0
    
    start_value = values[0]
    end_value = values[-1]
    periods = len(values) - 1
    
    if start_value <= 0:
        return 0.0
    
    cagr = (pow(end_value / start_value, 1 / periods) - 1) * 100
    return cagr
