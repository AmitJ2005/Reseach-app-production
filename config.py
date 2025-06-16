# Production configuration
import os
from datetime import timedelta

class Config:
    # App settings
    APP_NAME = "TradingView Pro Stock Analysis"
    VERSION = "1.0.0"
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Cache settings
    CACHE_TTL = int(os.getenv('CACHE_TTL', 300))  # 5 minutes default
    
    # API settings
    API_RATE_LIMIT = float(os.getenv('API_RATE_LIMIT', 1.0))  # seconds between calls
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    
    # Data settings
    MAX_DATA_POINTS = int(os.getenv('MAX_DATA_POINTS', 10000))
    DEFAULT_PERIOD = os.getenv('DEFAULT_PERIOD', '1y')
    
    # UI settings
    CHART_HEIGHT = int(os.getenv('CHART_HEIGHT', 580))
    
    # File paths
    STOCK_NAMES_FILE = os.getenv('STOCK_NAMES_FILE', 'stock_names.json')
    
    # Streamlit specific
    STREAMLIT_CONFIG = {
        'server.maxUploadSize': 200,
        'server.enableCORS': False,
        'server.enableXsrfProtection': False,
        'browser.gatherUsageStats': False
    }
