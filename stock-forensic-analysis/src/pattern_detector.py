"""
Pattern detection module for identifying unusual price and volume patterns
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta

from src.utils import calculate_moving_average, detect_outliers


class PatternDetector:
    """Detect unusual patterns in stock price and volume data"""
    
    def __init__(self, historical_data: pd.DataFrame):
        """
        Initialize the pattern detector
        
        Args:
            historical_data: DataFrame with historical price and volume data
        """
        self.data = historical_data
        self.has_data = not historical_data.empty
    
    def detect_volume_spikes(self, threshold: float = 2.0) -> Dict[str, Any]:
        """
        Detect unusual volume spikes
        
        Args:
            threshold: Multiplier for average volume to consider as spike
            
        Returns:
            Dictionary with volume spike analysis
        """
        if not self.has_data or 'Volume' not in self.data.columns:
            return {
                'spikes_detected': 0,
                'spike_dates': [],
                'average_volume': 0,
                'risk_level': 'UNKNOWN'
            }
        
        # Calculate average volume
        avg_volume = self.data['Volume'].mean()
        
        # Detect spikes
        volume_spikes = self.data[self.data['Volume'] > avg_volume * threshold]
        
        spike_dates = []
        for date, row in volume_spikes.iterrows():
            spike_dates.append({
                'date': date.strftime('%Y-%m-%d'),
                'volume': int(row['Volume']),
                'multiplier': round(row['Volume'] / avg_volume, 2),
                'close_price': round(row['Close'], 2)
            })
        
        # Sort by multiplier (highest first)
        spike_dates.sort(key=lambda x: x['multiplier'], reverse=True)
        
        # Determine risk level
        risk_level = 'LOW'
        if len(spike_dates) > 10:
            risk_level = 'HIGH'
        elif len(spike_dates) > 5:
            risk_level = 'MEDIUM'
        
        return {
            'spikes_detected': len(spike_dates),
            'spike_dates': spike_dates[:10],  # Return top 10
            'average_volume': int(avg_volume),
            'risk_level': risk_level,
            'interpretation': f'Detected {len(spike_dates)} volume spikes above {threshold}x average volume'
        }
    
    def detect_price_anomalies(self, window: int = 20) -> Dict[str, Any]:
        """
        Detect unusual price movements
        
        Args:
            window: Window size for moving average calculation
            
        Returns:
            Dictionary with price anomaly analysis
        """
        if not self.has_data or 'Close' not in self.data.columns:
            return {
                'anomalies_detected': 0,
                'anomaly_dates': [],
                'risk_level': 'UNKNOWN'
            }
        
        # Calculate moving average and standard deviation
        ma = calculate_moving_average(self.data['Close'], window)
        std = self.data['Close'].rolling(window=window).std()
        
        # Detect anomalies (price deviates more than 2 standard deviations)
        upper_band = ma + (2 * std)
        lower_band = ma - (2 * std)
        
        anomalies = self.data[
            (self.data['Close'] > upper_band) | 
            (self.data['Close'] < lower_band)
        ]
        
        anomaly_dates = []
        for date, row in anomalies.iterrows():
            price = row['Close']
            ma_value = ma.loc[date]
            deviation = ((price - ma_value) / ma_value) * 100
            
            anomaly_dates.append({
                'date': date.strftime('%Y-%m-%d'),
                'price': round(price, 2),
                'moving_average': round(ma_value, 2),
                'deviation_percent': round(deviation, 2),
                'type': 'SPIKE' if price > ma_value else 'DROP'
            })
        
        # Sort by absolute deviation
        anomaly_dates.sort(key=lambda x: abs(x['deviation_percent']), reverse=True)
        
        # Determine risk level
        risk_level = 'LOW'
        if len(anomaly_dates) > 15:
            risk_level = 'HIGH'
        elif len(anomaly_dates) > 8:
            risk_level = 'MEDIUM'
        
        return {
            'anomalies_detected': len(anomaly_dates),
            'anomaly_dates': anomaly_dates[:10],  # Return top 10
            'risk_level': risk_level,
            'interpretation': f'Detected {len(anomaly_dates)} price anomalies beyond 2 standard deviations'
        }
    
    def detect_gap_movements(self, gap_threshold: float = 5.0) -> Dict[str, Any]:
        """
        Detect significant gap up or gap down movements
        
        Args:
            gap_threshold: Percentage threshold for gap detection
            
        Returns:
            Dictionary with gap movement analysis
        """
        if not self.has_data or 'Open' not in self.data.columns or 'Close' not in self.data.columns:
            return {
                'gaps_detected': 0,
                'gap_dates': [],
                'risk_level': 'UNKNOWN'
            }
        
        # Calculate gap percentage
        prev_close = self.data['Close'].shift(1)
        gap_percent = ((self.data['Open'] - prev_close) / prev_close) * 100
        
        # Detect significant gaps
        significant_gaps = self.data[abs(gap_percent) > gap_threshold]
        
        gap_dates = []
        for date, row in significant_gaps.iterrows():
            gap_pct = gap_percent.loc[date]
            
            gap_dates.append({
                'date': date.strftime('%Y-%m-%d'),
                'gap_percent': round(gap_pct, 2),
                'open_price': round(row['Open'], 2),
                'previous_close': round(prev_close.loc[date], 2),
                'type': 'GAP_UP' if gap_pct > 0 else 'GAP_DOWN'
            })
        
        # Sort by absolute gap percentage
        gap_dates.sort(key=lambda x: abs(x['gap_percent']), reverse=True)
        
        # Determine risk level
        risk_level = 'LOW'
        gap_down_count = sum(1 for g in gap_dates if g['type'] == 'GAP_DOWN')
        
        if gap_down_count > 5:
            risk_level = 'HIGH'
        elif gap_down_count > 2:
            risk_level = 'MEDIUM'
        
        return {
            'gaps_detected': len(gap_dates),
            'gap_dates': gap_dates[:10],  # Return top 10
            'gap_up_count': sum(1 for g in gap_dates if g['type'] == 'GAP_UP'),
            'gap_down_count': gap_down_count,
            'risk_level': risk_level,
            'interpretation': f'Detected {len(gap_dates)} significant gaps (>{gap_threshold}%)'
        }
    
    def detect_price_volume_divergence(self) -> Dict[str, Any]:
        """
        Detect divergence between price and volume trends
        
        Returns:
            Dictionary with divergence analysis
        """
        if not self.has_data or 'Close' not in self.data.columns or 'Volume' not in self.data.columns:
            return {
                'divergence_detected': False,
                'risk_level': 'UNKNOWN',
                'interpretation': 'Insufficient data for divergence analysis'
            }
        
        # Calculate recent trends (last 20 days)
        recent_data = self.data.tail(20)
        
        if len(recent_data) < 10:
            return {
                'divergence_detected': False,
                'risk_level': 'UNKNOWN',
                'interpretation': 'Insufficient recent data for divergence analysis'
            }
        
        # Calculate price trend
        price_start = recent_data['Close'].iloc[0]
        price_end = recent_data['Close'].iloc[-1]
        price_trend = ((price_end - price_start) / price_start) * 100
        
        # Calculate volume trend
        volume_ma_start = recent_data['Volume'].iloc[:5].mean()
        volume_ma_end = recent_data['Volume'].iloc[-5:].mean()
        volume_trend = ((volume_ma_end - volume_ma_start) / volume_ma_start) * 100
        
        # Detect divergence
        divergence_detected = False
        divergence_type = None
        risk_level = 'LOW'
        
        # Bearish divergence: Price up, Volume down
        if price_trend > 5 and volume_trend < -20:
            divergence_detected = True
            divergence_type = 'BEARISH'
            risk_level = 'MEDIUM'
        
        # Bullish divergence: Price down, Volume up
        elif price_trend < -5 and volume_trend > 20:
            divergence_detected = True
            divergence_type = 'BULLISH'
            risk_level = 'LOW'
        
        interpretation = 'No significant price-volume divergence detected'
        if divergence_detected:
            if divergence_type == 'BEARISH':
                interpretation = 'Bearish divergence: Price rising on declining volume - potential weakness'
            else:
                interpretation = 'Bullish divergence: Price falling on rising volume - potential accumulation'
        
        return {
            'divergence_detected': divergence_detected,
            'divergence_type': divergence_type,
            'price_trend_percent': round(price_trend, 2),
            'volume_trend_percent': round(volume_trend, 2),
            'risk_level': risk_level,
            'interpretation': interpretation
        }
    
    def calculate_volatility_metrics(self) -> Dict[str, Any]:
        """
        Calculate volatility metrics
        
        Returns:
            Dictionary with volatility analysis
        """
        if not self.has_data or 'Close' not in self.data.columns:
            return {
                'volatility': 0,
                'risk_level': 'UNKNOWN'
            }
        
        # Calculate daily returns
        returns = self.data['Close'].pct_change().dropna()
        
        # Calculate volatility (standard deviation of returns)
        volatility = returns.std() * np.sqrt(252) * 100  # Annualized
        
        # Calculate recent volatility (last 30 days)
        recent_returns = returns.tail(30)
        recent_volatility = recent_returns.std() * np.sqrt(252) * 100
        
        # Determine risk level
        risk_level = 'LOW'
        if volatility > 50:
            risk_level = 'HIGH'
        elif volatility > 30:
            risk_level = 'MEDIUM'
        
        return {
            'annualized_volatility': round(volatility, 2),
            'recent_volatility': round(recent_volatility, 2),
            'max_daily_gain': round(returns.max() * 100, 2),
            'max_daily_loss': round(returns.min() * 100, 2),
            'risk_level': risk_level,
            'interpretation': f'Annualized volatility of {volatility:.1f}% indicates {"high" if risk_level == "HIGH" else "moderate" if risk_level == "MEDIUM" else "low"} price fluctuation'
        }
    
    def generate_pattern_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive pattern detection report
        
        Returns:
            Dictionary with complete pattern analysis
        """
        print("Detecting volume spikes...")
        volume_spikes = self.detect_volume_spikes()
        
        print("Detecting price anomalies...")
        price_anomalies = self.detect_price_anomalies()
        
        print("Detecting gap movements...")
        gap_movements = self.detect_gap_movements()
        
        print("Detecting price-volume divergence...")
        divergence = self.detect_price_volume_divergence()
        
        print("Calculating volatility metrics...")
        volatility = self.calculate_volatility_metrics()
        
        # Calculate overall pattern risk score
        risk_scores = []
        
        if volume_spikes['risk_level'] == 'HIGH':
            risk_scores.append(0.8)
        elif volume_spikes['risk_level'] == 'MEDIUM':
            risk_scores.append(0.5)
        else:
            risk_scores.append(0.2)
        
        if price_anomalies['risk_level'] == 'HIGH':
            risk_scores.append(0.7)
        elif price_anomalies['risk_level'] == 'MEDIUM':
            risk_scores.append(0.4)
        else:
            risk_scores.append(0.2)
        
        if gap_movements['risk_level'] == 'HIGH':
            risk_scores.append(0.6)
        elif gap_movements['risk_level'] == 'MEDIUM':
            risk_scores.append(0.4)
        else:
            risk_scores.append(0.2)
        
        if divergence['risk_level'] == 'MEDIUM':
            risk_scores.append(0.5)
        else:
            risk_scores.append(0.2)
        
        if volatility['risk_level'] == 'HIGH':
            risk_scores.append(0.7)
        elif volatility['risk_level'] == 'MEDIUM':
            risk_scores.append(0.4)
        else:
            risk_scores.append(0.2)
        
        overall_risk_score = np.mean(risk_scores)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'volume_spikes': volume_spikes,
            'price_anomalies': price_anomalies,
            'gap_movements': gap_movements,
            'price_volume_divergence': divergence,
            'volatility_metrics': volatility,
            'overall_pattern_risk_score': round(overall_risk_score, 2),
            'overall_risk_level': 'HIGH' if overall_risk_score > 0.6 else 'MEDIUM' if overall_risk_score > 0.4 else 'LOW'
        }
