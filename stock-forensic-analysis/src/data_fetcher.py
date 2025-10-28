"""
Data fetching module for Yahoo Finance and You.com API
"""
import yfinance as yf
import requests
import pandas as pd
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import time

from config import Config


class YahooFinanceDataFetcher:
    """Fetch stock data from Yahoo Finance"""
    
    def __init__(self, symbol: str):
        """
        Initialize the data fetcher
        
        Args:
            symbol: Stock ticker symbol
        """
        self.symbol = symbol.upper()
        self.ticker = yf.Ticker(self.symbol)
    
    def get_stock_info(self) -> Dict[str, Any]:
        """
        Get basic stock information
        
        Returns:
            Dictionary containing stock info
        """
        try:
            info = self.ticker.info
            return {
                'symbol': self.symbol,
                'company_name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 0),
                'current_price': info.get('currentPrice', 0),
                'previous_close': info.get('previousClose', 0),
                'volume': info.get('volume', 0),
                'average_volume': info.get('averageVolume', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'forward_pe': info.get('forwardPE', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'beta': info.get('beta', 0),
                '52_week_high': info.get('fiftyTwoWeekHigh', 0),
                '52_week_low': info.get('fiftyTwoWeekLow', 0),
            }
        except Exception as e:
            print(f"Error fetching stock info: {e}")
            return {}
    
    def get_historical_data(self, period: str = '1y') -> pd.DataFrame:
        """
        Get historical price data
        
        Args:
            period: Time period (e.g., '1y', '6m', '3m')
            
        Returns:
            DataFrame with historical data
        """
        try:
            hist = self.ticker.history(period=period)
            return hist
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return pd.DataFrame()
    
    def get_financials(self) -> Dict[str, pd.DataFrame]:
        """
        Get financial statements
        
        Returns:
            Dictionary containing income statement, balance sheet, and cash flow
        """
        try:
            return {
                'income_statement': self.ticker.financials,
                'balance_sheet': self.ticker.balance_sheet,
                'cash_flow': self.ticker.cashflow,
                'quarterly_financials': self.ticker.quarterly_financials,
                'quarterly_balance_sheet': self.ticker.quarterly_balance_sheet,
                'quarterly_cashflow': self.ticker.quarterly_cashflow,
            }
        except Exception as e:
            print(f"Error fetching financials: {e}")
            return {}
    
    def get_key_ratios(self) -> Dict[str, float]:
        """
        Calculate and return key financial ratios
        
        Returns:
            Dictionary of financial ratios
        """
        try:
            info = self.ticker.info
            balance_sheet = self.ticker.balance_sheet
            income_stmt = self.ticker.financials
            
            ratios = {}
            
            # Profitability Ratios
            ratios['profit_margin'] = info.get('profitMargins', 0) * 100
            ratios['operating_margin'] = info.get('operatingMargins', 0) * 100
            ratios['roe'] = info.get('returnOnEquity', 0) * 100
            ratios['roa'] = info.get('returnOnAssets', 0) * 100
            
            # Liquidity Ratios
            if not balance_sheet.empty:
                try:
                    current_assets = balance_sheet.loc['Total Current Assets'].iloc[0]
                    current_liabilities = balance_sheet.loc['Total Current Liabilities'].iloc[0]
                    ratios['current_ratio'] = current_assets / current_liabilities if current_liabilities != 0 else 0
                except:
                    ratios['current_ratio'] = 0
            
            # Leverage Ratios
            ratios['debt_to_equity'] = info.get('debtToEquity', 0) / 100
            
            # Efficiency Ratios
            if not income_stmt.empty and not balance_sheet.empty:
                try:
                    revenue = income_stmt.loc['Total Revenue'].iloc[0]
                    total_assets = balance_sheet.loc['Total Assets'].iloc[0]
                    ratios['asset_turnover'] = revenue / total_assets if total_assets != 0 else 0
                except:
                    ratios['asset_turnover'] = 0
            
            return ratios
        except Exception as e:
            print(f"Error calculating ratios: {e}")
            return {}
    
    def get_shareholding_pattern(self) -> Dict[str, Any]:
        """
        Get shareholding pattern information
        
        Returns:
            Dictionary with shareholding details
        """
        try:
            info = self.ticker.info
            major_holders = self.ticker.major_holders
            institutional_holders = self.ticker.institutional_holders
            
            shareholding = {
                'insider_ownership': info.get('heldPercentInsiders', 0) * 100,
                'institutional_ownership': info.get('heldPercentInstitutions', 0) * 100,
                'float_shares': info.get('floatShares', 0),
                'shares_outstanding': info.get('sharesOutstanding', 0),
                'shares_short': info.get('sharesShort', 0),
                'short_ratio': info.get('shortRatio', 0),
                'major_holders': major_holders.to_dict() if major_holders is not None else {},
                'institutional_holders': institutional_holders.to_dict() if institutional_holders is not None else {},
            }
            
            return shareholding
        except Exception as e:
            print(f"Error fetching shareholding pattern: {e}")
            return {}
    
    def get_earnings_history(self) -> pd.DataFrame:
        """
        Get earnings history
        
        Returns:
            DataFrame with earnings data
        """
        try:
            return self.ticker.earnings_history
        except Exception as e:
            print(f"Error fetching earnings history: {e}")
            return pd.DataFrame()


class YouComNewsDataFetcher:
    """Fetch news and articles from You.com API"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the news fetcher
        
        Args:
            api_key: You.com API key
        """
        self.api_key = api_key or Config.YOU_API_KEY
        self.base_url = Config.YOU_API_BASE_URL
        self.headers = {
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json'
        }
    
    def search_news(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search for live news articles using You.com News API
        
        Args:
            query: Search query
            num_results: Number of results to return (1-40)
            
        Returns:
            List of news articles with rich metadata
        """
        if not self.api_key:
            print("Warning: You.com API key not configured. Returning empty results.")
            return []
        
        try:
            # Use the correct /livenews endpoint
            endpoint = f"{self.base_url}/livenews"
            
            # Limit count to valid range (1-40)
            count = min(max(num_results, 1), 40)
            
            params = {
                'q': query,  # Correct parameter name is 'q'
                'count': count,  # Correct parameter name is 'count'
            }
            
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract news results from the correct structure
                news_results = []
                
                # Parse news.results structure
                if 'news' in data and 'results' in data['news']:
                    for result in data['news']['results'][:num_results]:
                        # Extract meta_url information
                        meta_url = result.get('meta_url', {})
                        
                        # Extract thumbnail information
                        thumbnail = result.get('thumbnail', {})
                        
                        news_results.append({
                            'title': result.get('title', ''),
                            'description': result.get('description', ''),
                            'url': result.get('url', ''),
                            'age': result.get('age', ''),  # e.g., "6h", "2d"
                            'page_age': result.get('page_age', ''),  # ISO 8601 datetime
                            'source_name': result.get('source_name', ''),
                            'article_id': result.get('article_id', ''),
                            'type': result.get('type', ''),
                            'thumbnail_url': thumbnail.get('src', ''),
                            'hostname': meta_url.get('hostname', ''),
                            'netloc': meta_url.get('netloc', ''),
                            'scheme': meta_url.get('scheme', ''),
                        })
                
                return news_results
            else:
                print(f"Error fetching news: HTTP {response.status_code}")
                if response.status_code == 401:
                    print("Authentication failed. Please check your API key.")
                elif response.status_code == 403:
                    print("Access forbidden. You.com News API requires early access partnership.")
                    print("Contact api@you.com to request access.")
                return []
                
        except Exception as e:
            print(f"Error searching news: {e}")
            return []
    
    def get_stock_news(self, symbol: str, company_name: str = None, 
                       num_results: int = 10) -> List[Dict[str, Any]]:
        """
        Get news specifically about a stock
        
        Args:
            symbol: Stock ticker symbol
            company_name: Company name (optional)
            num_results: Number of results to return
            
        Returns:
            List of news articles about the stock
        """
        # Create search query
        if company_name:
            query = f"{symbol} {company_name} stock news financial"
        else:
            query = f"{symbol} stock news financial"
        
        return self.search_news(query, num_results)
    
    def get_financial_analysis(self, symbol: str, company_name: str = None) -> List[Dict[str, Any]]:
        """
        Get financial analysis articles about a stock
        
        Args:
            symbol: Stock ticker symbol
            company_name: Company name (optional)
            
        Returns:
            List of financial analysis articles
        """
        if company_name:
            query = f"{symbol} {company_name} financial analysis earnings report"
        else:
            query = f"{symbol} financial analysis earnings report"
        
        return self.search_news(query, num_results=5)


class DataAggregator:
    """Aggregate data from multiple sources"""
    
    def __init__(self, symbol: str, you_api_key: str = None):
        """
        Initialize the data aggregator
        
        Args:
            symbol: Stock ticker symbol
            you_api_key: You.com API key
        """
        self.symbol = symbol
        self.yahoo_fetcher = YahooFinanceDataFetcher(symbol)
        self.news_fetcher = YouComNewsDataFetcher(you_api_key)
    
    def fetch_all_data(self, period: str = '1y') -> Dict[str, Any]:
        """
        Fetch all available data for the stock
        
        Args:
            period: Historical data period
            
        Returns:
            Dictionary containing all fetched data
        """
        print(f"Fetching data for {self.symbol}...")
        
        # Fetch Yahoo Finance data
        stock_info = self.yahoo_fetcher.get_stock_info()
        company_name = stock_info.get('company_name', '')
        
        data = {
            'symbol': self.symbol,
            'fetch_timestamp': datetime.now().isoformat(),
            'stock_info': stock_info,
            'historical_data': self.yahoo_fetcher.get_historical_data(period),
            'financials': self.yahoo_fetcher.get_financials(),
            'key_ratios': self.yahoo_fetcher.get_key_ratios(),
            'shareholding': self.yahoo_fetcher.get_shareholding_pattern(),
            'earnings_history': self.yahoo_fetcher.get_earnings_history(),
        }
        
        # Fetch news data
        print("Fetching news articles...")
        data['news'] = self.news_fetcher.get_stock_news(self.symbol, company_name)
        data['financial_analysis'] = self.news_fetcher.get_financial_analysis(self.symbol, company_name)
        
        print(f"Data fetching completed for {self.symbol}")
        return data
