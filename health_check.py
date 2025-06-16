"""
Health check utilities for production deployment
"""
import streamlit as st
import yfinance as yf
import json
import os
from datetime import datetime
import psutil  # Add to requirements

def check_health():
    """Comprehensive health check for the application"""
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'checks': {}
    }
    
    try:
        # Check file dependencies
        health_status['checks']['stock_names_file'] = os.path.exists('stock_names.json')
        
        # Check memory usage
        memory_usage = psutil.virtual_memory().percent
        health_status['checks']['memory_usage'] = f"{memory_usage}%"
        health_status['checks']['memory_ok'] = memory_usage < 80
        
        # Check disk space
        disk_usage = psutil.disk_usage('/').percent
        health_status['checks']['disk_usage'] = f"{disk_usage}%"
        health_status['checks']['disk_ok'] = disk_usage < 80
        
        # Test yfinance connectivity
        try:
            test_ticker = yf.Ticker("AAPL")
            test_data = test_ticker.history(period="1d", interval="1d")
            health_status['checks']['yfinance_api'] = not test_data.empty
        except:
            health_status['checks']['yfinance_api'] = False
        
        # Overall status
        if not all([
            health_status['checks']['stock_names_file'],
            health_status['checks']['memory_ok'],
            health_status['checks']['disk_ok'],
            health_status['checks']['yfinance_api']
        ]):
            health_status['status'] = 'unhealthy'
            
    except Exception as e:
        health_status['status'] = 'error'
        health_status['error'] = str(e)
    
    return health_status

def display_health_info():
    """Display health information in sidebar for debugging"""
    if st.sidebar.checkbox("🔧 System Info", value=False):
        health = check_health()
        st.sidebar.json(health)
