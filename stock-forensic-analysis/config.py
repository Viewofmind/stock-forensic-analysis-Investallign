"""
Configuration management for Stock Forensic Analysis Tool
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the application"""
    
    # API Keys
    YOU_API_KEY = os.getenv('YOU_API_KEY', '')
    
    # Report Configuration
    REPORT_OUTPUT_DIR = os.getenv('REPORT_OUTPUT_DIR', 'reports')
    
    # Analysis Parameters
    DEFAULT_ANALYSIS_PERIOD = os.getenv('DEFAULT_ANALYSIS_PERIOD', '1y')
    RISK_THRESHOLD_HIGH = float(os.getenv('RISK_THRESHOLD_HIGH', '0.7'))
    RISK_THRESHOLD_MEDIUM = float(os.getenv('RISK_THRESHOLD_MEDIUM', '0.4'))
    
    # You.com API Configuration
    YOU_API_BASE_URL = "https://api.ydc-index.io"
    YOU_API_SEARCH_ENDPOINT = "/search"
    
    # Forensic Analysis Thresholds
    BENEISH_M_SCORE_THRESHOLD = -2.22  # Values > -2.22 suggest manipulation
    ALTMAN_Z_SCORE_SAFE = 2.99  # Z > 2.99 = Safe zone
    ALTMAN_Z_SCORE_DISTRESS = 1.81  # Z < 1.81 = Distress zone
    
    # Pattern Detection Parameters
    VOLUME_SPIKE_THRESHOLD = 2.0  # 2x average volume
    PRICE_CHANGE_THRESHOLD = 0.05  # 5% price change
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.YOU_API_KEY:
            print("WARNING: YOU_API_KEY not set. News analysis will be limited.")
        
        # Create reports directory if it doesn't exist
        os.makedirs(cls.REPORT_OUTPUT_DIR, exist_ok=True)
        
        return True

# Validate configuration on import
Config.validate()
