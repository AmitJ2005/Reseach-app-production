import streamlit as st
import json
import yfinance as yf
import pandas as pd
import numpy as np
import traceback
import pytz
from datetime import datetime, timedelta
from streamlit_lightweight_charts import renderLightweightCharts

try:
    import ta
except ImportError:
    st.error("Please install TA library: pip install ta")
    ta = None

# Set page config
st.set_page_config(
    page_title="TradingView Pro | Stock Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load stock names from JSON file
@st.cache_data
def load_stock_names():
    with open('stock_names.json', 'r') as f:
        return json.load(f)

# Function to get stock data
@st.cache_data
def get_stock_data(symbol, start_date, end_date, interval):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(start=start_date, end=end_date, interval=interval)
        return data, stock.info
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None, None

# Technical Analysis Functions
def calculate_moving_averages(data):
    """Calculate various moving averages"""
    data['MA_20'] = data['Close'].rolling(window=20).mean()
    data['MA_50'] = data['Close'].rolling(window=50).mean()
    data['MA_200'] = data['Close'].rolling(window=200).mean()
    data['EMA_12'] = data['Close'].ewm(span=12).mean()
    data['EMA_26'] = data['Close'].ewm(span=26).mean()
    return data

def prepare_candlestick_data(data):
    """Convert pandas dataframe to format required by lightweight-charts"""
    candlestick_data = []
    
    for index, row in data.iterrows():
        # Format time properly for lightweight charts
        try:
            # Check if this is daily data (timezone-aware but at 00:00:00)
            if (hasattr(index, 'hour') and index.hour == 0 and 
                index.minute == 0 and index.second == 0):
                # For daily data, use date format (YYYY-MM-DD)
                time_value = index.strftime('%Y-%m-%d')
            else:
                # For intraday data, create timestamp that displays IST time correctly
                if hasattr(index, 'tz') and index.tz is not None:
                    # Method: Create a naive datetime with IST values and treat it as UTC
                    # This forces the chart to display the IST time correctly
                    naive_ist = index.replace(tzinfo=None)
                    # Convert to UTC datetime for timestamp calculation
                    utc_naive = datetime(naive_ist.year, naive_ist.month, naive_ist.day,
                                       naive_ist.hour, naive_ist.minute, naive_ist.second)
                    # Get timestamp treating the IST time as if it were UTC
                    time_value = int(utc_naive.replace(tzinfo=pytz.UTC).timestamp())
                else:
                    # If timezone-naive, assume it's already correct
                    time_value = int(index.timestamp())
        except Exception as e:
            # Fallback: extract date part
            time_value = str(index).split(' ')[0]
            
        candlestick_data.append({
            "time": time_value,
            "open": float(row['Open'].iloc[0] if hasattr(row['Open'], 'iloc') else row['Open']),
            "high": float(row['High'].iloc[0] if hasattr(row['High'], 'iloc') else row['High']),
            "low": float(row['Low'].iloc[0] if hasattr(row['Low'], 'iloc') else row['Low']),
            "close": float(row['Close'].iloc[0] if hasattr(row['Close'], 'iloc') else row['Close'])
        })
    
    return candlestick_data

def prepare_line_data(data, column):
    """Convert pandas series to format required by lightweight-charts"""
    line_data = []
    
    for index, value in data[column].dropna().items():
        try:
            # Check if this is daily data (timezone-aware but at 00:00:00)
            if (hasattr(index, 'hour') and index.hour == 0 and 
                index.minute == 0 and index.second == 0):
                # For daily data, use date format
                time_value = index.strftime('%Y-%m-%d')
            else:
                # For intraday data, create timestamp that displays IST time correctly
                if hasattr(index, 'tz') and index.tz is not None:
                    # Method: Create a naive datetime with IST values and treat it as UTC
                    # This forces the chart to display the IST time correctly
                    naive_ist = index.replace(tzinfo=None)
                    # Convert to UTC datetime for timestamp calculation
                    utc_naive = datetime(naive_ist.year, naive_ist.month, naive_ist.day,
                                       naive_ist.hour, naive_ist.minute, naive_ist.second)
                    # Get timestamp treating the IST time as if it were UTC
                    time_value = int(utc_naive.replace(tzinfo=pytz.UTC).timestamp())
                else:
                    # If timezone-naive, assume it's already correct
                    time_value = int(index.timestamp())
        except Exception as e:
            # Fallback
            time_value = str(index).split(' ')[0]
            
        line_data.append({
            "time": time_value,
            "value": float(value.iloc[0] if hasattr(value, 'iloc') else value)
        })
    
    return line_data

def prepare_volume_data(data):
    """Convert volume data to format required by lightweight-charts"""
    volume_data = []
    
    for index, row in data.iterrows():
        try:
            # Check if this is daily data (timezone-aware but at 00:00:00)
            if (hasattr(index, 'hour') and index.hour == 0 and 
                index.minute == 0 and index.second == 0):
                # For daily data, use date format
                time_value = index.strftime('%Y-%m-%d')
            else:
                # For intraday data, create timestamp that displays IST time correctly
                if hasattr(index, 'tz') and index.tz is not None:
                    # Method: Create a naive datetime with IST values and treat it as UTC
                    # This forces the chart to display the IST time correctly
                    naive_ist = index.replace(tzinfo=None)
                    # Convert to UTC datetime for timestamp calculation
                    utc_naive = datetime(naive_ist.year, naive_ist.month, naive_ist.day,
                                       naive_ist.hour, naive_ist.minute, naive_ist.second)
                    # Get timestamp treating the IST time as if it were UTC
                    time_value = int(utc_naive.replace(tzinfo=pytz.UTC).timestamp())
                else:
                    # If timezone-naive, assume it's already correct
                    time_value = int(index.timestamp())
        except Exception as e:
            # Fallback
            time_value = str(index).split(' ')[0]
            
        # Color volume bars based on price movement
        color = "#089981" if row['Close'] >= row['Open'] else "#f23645"
        
        volume_data.append({
            "time": time_value,
            "value": float(row['Volume'].iloc[0] if hasattr(row['Volume'], 'iloc') else row['Volume']),
            "color": color
        })
    
    return volume_data

def calculate_rsi(data, period=14):
    """Calculate RSI"""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    return data

def calculate_macd(data):
    """Calculate MACD"""
    exp1 = data['Close'].ewm(span=12).mean()
    exp2 = data['Close'].ewm(span=26).mean()
    data['MACD'] = exp1 - exp2
    data['MACD_Signal'] = data['MACD'].ewm(span=9).mean()
    data['MACD_Histogram'] = data['MACD'] - data['MACD_Signal']
    return data

def calculate_bollinger_bands(data, period=20, std_dev=2):
    """Calculate Bollinger Bands"""
    data['BB_Middle'] = data['Close'].rolling(window=period).mean()
    bb_std = data['Close'].rolling(window=period).std()
    data['BB_Upper'] = data['BB_Middle'] + (bb_std * std_dev)
    data['BB_Lower'] = data['BB_Middle'] - (bb_std * std_dev)
    return data

def calculate_volume_indicators(data):
    """Calculate volume-based indicators"""
    data['Volume_MA'] = data['Volume'].rolling(window=20).mean()
    data['Volume_Ratio'] = data['Volume'] / data['Volume_MA']
    return data

def filter_by_time_range(data, start_time, end_time):
    """Filter data by specific time range for intraday analysis"""
    if start_time is None or end_time is None:
        return data
    
    # Create a copy to avoid modifying original data
    filtered_data = data.copy()
    
    # Convert index to datetime if it's not already
    if not isinstance(filtered_data.index, pd.DatetimeIndex):
        filtered_data.index = pd.to_datetime(filtered_data.index)
    
    # Filter by time
    filtered_data = filtered_data.between_time(start_time, end_time)
    
    return filtered_data

def analyze_time_patterns(data, time_ranges):
    """Analyze trading patterns across different time ranges"""
    patterns = {}
    
    for range_name, (start_str, end_str) in time_ranges.items():
        start_time = datetime.strptime(start_str, "%H:%M").time()
        end_time = datetime.strptime(end_str, "%H:%M").time()
        
        range_data = filter_by_time_range(data, start_time, end_time)
        
        if not range_data.empty:
            patterns[range_name] = {
                'avg_volume': range_data['Volume'].mean(),
                'avg_price_change': ((range_data['Close'] - range_data['Open']) / range_data['Open'] * 100).mean(),
                'volatility': ((range_data['High'] - range_data['Low']) / range_data['Open'] * 100).mean(),
                'total_trades': len(range_data)
            }
    
    return patterns

def create_tradingview_chart(data, stock_name, indicators):
    """Create TradingView-style chart using lightweight-charts"""
    
    # Prepare data for different series
    candlestick_data = prepare_candlestick_data(data)
    volume_data = prepare_volume_data(data)
    
    # Chart configuration with proper height for no-scroll design
    chart_options = {
        "height": 580,  # Fixed height to prevent scrolling
        "layout": {
            "background": {"color": "#0D1421"},
            "textColor": "#D1D4DC"
        },
        "grid": {
            "vertLines": {"color": "#1E222D"},
            "horzLines": {"color": "#1E222D"}
        },
        "timeScale": {
            "borderColor": "#485C7B",
            "timeVisible": True,
            "secondsVisible": False,
            "rightOffset": 5,
            "barSpacing": 3,
            "fixLeftEdge": False,
            "lockVisibleTimeRangeOnResize": True,
            "rightBarStaysOnScroll": True,
            "visible": True,
            "borderVisible": True
        },
        "rightPriceScale": {
            "borderColor": "#485C7B",
            "visible": True,
            "borderVisible": True,
            "autoScale": True,
            "entireTextOnly": False
        },
        "leftPriceScale": {
            "visible": False
        },
        "crosshair": {
            "mode": 0,
            "vertLine": {
                "color": "#758696",
                "width": 1,
                "style": 3,
                "visible": True,
                "labelVisible": True
            },
            "horzLine": {
                "color": "#758696", 
                "width": 1,
                "style": 3,
                "visible": True,
                "labelVisible": True
            }
        },
        "handleScroll": {
            "mouseWheel": True,
            "pressedMouseMove": True,
            "horzTouchDrag": True,
            "vertTouchDrag": True
        },
        "handleScale": {
            "axisPressedMouseMove": {
                "time": True,
                "price": True
            },
            "axisDoubleClickReset": {
                "time": True,
                "price": True
            },
            "mouseWheel": True,
            "pinch": True
        }
    }
    
    # Series configuration
    series_config = []
    
    # Candlestick series
    candlestick_series = {
        "type": "Candlestick",
        "data": candlestick_data,
        "options": {
            "upColor": "#089981",
            "downColor": "#f23645",
            "borderVisible": False,
            "wickUpColor": "#089981",
            "wickDownColor": "#f23645"
        }
    }
    series_config.append(candlestick_series)
    
    # Moving averages
    if 'MA' in indicators:
        if 'MA_20' in data.columns:
            ma20_data = prepare_line_data(data, 'MA_20')
            ma20_series = {
                "type": "Line",
                "data": ma20_data,
                "options": {
                    "color": "#2962ff",
                    "lineWidth": 2,
                    "title": "MA20"
                }
            }
            series_config.append(ma20_series)
        
        if 'MA_50' in data.columns:
            ma50_data = prepare_line_data(data, 'MA_50')
            ma50_series = {
                "type": "Line",
                "data": ma50_data,
                "options": {
                    "color": "#ff6d00",
                    "lineWidth": 2,
                    "title": "MA50"
                }
            }
            series_config.append(ma50_series)
    
    # Volume series (on separate pane)
    if 'Volume' in indicators:
        volume_series = {
            "type": "Histogram",
            "data": volume_data,
            "options": {
                "priceFormat": {"type": "volume"},
                "priceScaleId": "volume"
            },
            "priceScale": {
                "scaleMargins": {"top": 0.8, "bottom": 0}
            }
        }
        series_config.append(volume_series)
        
        # Volume MA
        if 'Volume_MA' in data.columns:
            volume_ma_data = prepare_line_data(data, 'Volume_MA')
            volume_ma_series = {
                "type": "Line",
                "data": volume_ma_data,
                "options": {
                    "color": "#ff9800",
                    "lineWidth": 2,
                    "priceScaleId": "volume",
                    "title": "Volume MA"
                }
            }
            series_config.append(volume_ma_series)
    
    return chart_options, series_config

def create_enhanced_tooltip(data):
    """Create enhanced tooltip information"""
    if data.empty:
        return ""
    
    latest = data.iloc[-1]
    prev = data.iloc[-2] if len(data) > 1 else latest
    
    change = latest['Close'] - prev['Close']
    change_pct = (change / prev['Close']) * 100 if prev['Close'] != 0 else 0
    
    tooltip_info = f"""
    **Latest Data:**
    • Open: ₹{latest['Open']:.2f}
    • High: ₹{latest['High']:.2f}  
    • Low: ₹{latest['Low']:.2f}
    • Close: ₹{latest['Close']:.2f}
    • Volume: {latest['Volume']:,.0f}
    • Change: ₹{change:+.2f} ({change_pct:+.2f}%)
    """
    
    # Add technical indicator values if available
    if 'RSI' in data.columns:
        tooltip_info += f"\n• RSI: {latest['RSI']:.2f}"
    if 'MACD' in data.columns:
        tooltip_info += f"\n• MACD: {latest['MACD']:.4f}"
    
    return tooltip_info

# Main app
def main():    # TradingView-style CSS
    st.markdown("""
    <style>
    /* Remove all top margin/padding for Streamlit main container and body */
    .main .block-container, .block-container, .stApp, .stAppViewContainer, .stAppViewBlockContainer, .stAppViewBlockContainer > div:first-child {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    html, body {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    body {
        min-height: 100vh;
    }
    /* Try to force content up if Streamlit adds extra space */
    .main .block-container { margin-top: -1.5rem !important; }
    #MainMenu, footer, header {visibility: hidden;}
    .css-1d391kg {
        background-color: #0D1421;
        border-right: 1px solid #1E222D;
        width: 19rem;
    }
    .metric-container {
        background-color: #131722;
        padding: 6px 10px;
        border-radius: 5px;
        margin: 2px 0;
        border-left: 3px solid #2962FF;
    }
    .tradingview-header {
        background: linear-gradient(135deg, #0D1421 0%, #131722 100%);
        padding: 7px 15px;
        border-radius: 6px;
        margin-bottom: 4px;
        border: 1px solid #1E222D;
        display: flex;
        align-items: center;
        justify-content: space-between;
        min-height: 38px;
    }
    .tradingview-header h2 {
        color: #D1D4DC;
        margin: 0;
        font-size: 1.25rem;
        font-weight: 600;
        line-height: 1.2;
    }
    .tradingview-header .price {
        color: #089981;
        font-size: 1.1rem;
        font-weight: 600;
        margin-left: 1.5rem;
    }
    .stButton > button {
        background-color: #2962FF;
        color: white;
        border: none;
        border-radius: 5px;
        height: 36px;
        font-weight: 600;
        padding: 0 18px;
    }
    .stButton > button:hover {
        background-color: #1E53E5;
    }
    .stSelectbox > div > div {
        background-color: #1E222D;
        border: 1px solid #363C4E;
        border-radius: 5px;
    }
    .stMetric {
        background-color: #131722;
        padding: 5px 8px;
        border-radius: 5px;
        border-left: 3px solid #089981;
        margin-bottom: 0.2rem;
    }
    .element-container {
        margin-bottom: 0.2rem;
    }
    .stMarkdown, .stSelectbox label, .stMultiSelect label {
        color: #D1D4DC !important;
    }
    .sidebar .sidebar-content {
        background-color: #0D1421;
    }
    iframe[title="streamlit_lightweight_charts.frontend"] {
        border-radius: 8px;
        border: 1px solid #1E222D;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Load stock names
    stock_names = load_stock_names()
    
    # === SIDEBAR CONTROLS ===
    with st.sidebar:
        st.markdown("""
        <style>
        /* Ultra-compact sidebar: remove all vertical space, padding, and margins, flush to top */
        section[data-testid="stSidebar"] .block-container {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            min-height: 100vh !important;
        }
        section[data-testid="stSidebar"] {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        .stSidebar .stMarkdown, .stSidebar label, .stSidebar .stSelectbox, .stSidebar .stMultiSelect, .stSidebar .stDateInput, .stSidebar .stButton, .stSidebar .stCheckbox, .stSidebar .stInfo {
            margin-bottom: 0.01rem !important;
            margin-top: 0 !important;
            font-size: 0.90rem !important;
        }
        .stSidebar .stSelectbox > div > div, .stSidebar .stMultiSelect > div > div {
            min-height: 22px !important;
            font-size: 0.90rem !important;
        }
        .stSidebar .stButton > button {
            height: 22px !important;
            font-size: 0.90rem !important;
            padding: 0 2px !important;
            margin: 0 !important;
        }
        .stSidebar .stDateInput > div > input {
            min-height: 22px !important;
            font-size: 0.90rem !important;
        }
        .stSidebar .stCheckbox > label {
            font-size: 0.90rem !important;
        }
        .stSidebar .stInfo {
            font-size: 0.88rem !important;
            padding: 0.01rem 0.05rem !important;
            margin: 0 !important;
        }
        /* Remove all vertical space between Streamlit elements */
        .stSidebar [data-testid="stVerticalBlock"] > div {
            margin-bottom: 0 !important;
            margin-top: 0 !important;
        }
        .stSidebar [data-testid="stHorizontalBlock"] > div {
            margin-bottom: 0 !important;
            margin-top: 0 !important;
        }
        /* Remove top space above sidebar content */
        [data-testid="stSidebarNav"] {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        </style>
        """, unsafe_allow_html=True)

        # --- Compact Stock Select ---
        st.markdown("#### 🔍 Stock")
        stock_options = [f"{name} ({symbol})" for name, symbol in stock_names.items()]
        default_index = 0
        selected = st.selectbox(
            "",
            options=stock_options,
            index=default_index,
            key="stock_selectbox",
            help="Type to filter, then select with mouse or keyboard."
        )
        selected_stock_name = selected.split(" (")[0]
        selected_symbol = selected.split("(")[-1].replace(")", "")

        # --- Compact Date Range ---
        st.markdown("#### 📅 Date Range")
        col_date1, col_date2 = st.columns(2, gap="small")
        with col_date1:
            start_date = st.date_input(
                "From",
                value=datetime.now() - timedelta(days=30),
                max_value=datetime.now().date(),
                key="start_date"
            )
        with col_date2:
            end_date = st.date_input(
                "To",
                value=datetime.now().date(),
                max_value=datetime.now().date(),
                min_value=start_date,
                key="end_date"
            )

        # --- Compact Timeframe ---
        st.markdown("#### ⏱ Interval")
        timeframe = st.selectbox(
            "",
            options=["1m", "5m", "15m", "30m", "60m", "1d", "5d", "1wk"],
            index=2,
            format_func=lambda x: {
                "1m": "1 Min", "5m": "5 Min", "15m": "15 Min", 
                "30m": "30 Min", "60m": "1 Hour", "1d": "1 Day",
                "5d": "5 Days", "1wk": "1 Week"
            }[x],
            key="timeframe"
        )

        # --- Compact Indicators ---
        st.markdown("#### 📊 Indicators")
        indicators = st.multiselect(
            "",
            options=["MA", "RSI", "MACD", "Volume", "Bollinger Bands"],
            default=["MA", "Volume"],
            key="indicators"
        )

        # --- Compact Time Filter ---
        if timeframe in ["1m", "5m", "15m", "30m", "60m"]:
            st.markdown("#### 🕐 Time Filter")
            time_filter = st.checkbox("Custom Time Range", key="time_filter")
            if time_filter:
                col_t1, col_t2 = st.columns(2, gap="small")
                with col_t1:
                    start_time = st.time_input(
                        "From",
                        value=datetime.strptime("09:15", "%H:%M").time(),
                        key="start_time"
                    )
                with col_t2:
                    end_time = st.time_input(
                        "To",
                        value=datetime.strptime("15:30", "%H:%M").time(),
                        key="end_time"
                    )
                st.info(f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}")
            else:
                start_time = None
                end_time = None
        else:
            st.markdown("#### 🕐 Time Filter")
            st.info("Intraday only")
            time_filter = False
            start_time = None
            end_time = None

        # --- Compact Action Buttons ---
        fetch_data = st.button("📊 Get Data", type="primary", use_container_width=True, key="fetch_button")
        if fetch_data:
            st.session_state.fetch_data = True

        if hasattr(st.session_state, 'fetch_data') and st.session_state.fetch_data:
            if st.button("🔄 Refresh", use_container_width=True, key="refresh_button"):
                st.rerun()
    
    # === MAIN CONTENT AREA ===
    with st.container():
        st.markdown('<div style="height:0;margin:0;padding:0;"></div>', unsafe_allow_html=True)
        if hasattr(st.session_state, 'fetch_data') and st.session_state.fetch_data:
            # Fetch data
            with st.spinner("Loading data..."):
                data, info = get_stock_data(selected_symbol, start_date, end_date, timeframe)

            if data is not None and not data.empty:
                # Apply time filtering if enabled
                original_data = data.copy()
                if time_filter and start_time and end_time:
                    data = filter_by_time_range(data, start_time, end_time)
                    if data.empty:
                        st.warning("No data in selected time range")
                        data = original_data

                # Calculate indicators
                if indicators:
                    if 'MA' in indicators:
                        data = calculate_moving_averages(data)
                    if 'RSI' in indicators:
                        data = calculate_rsi(data)
                    if 'MACD' in indicators:
                        data = calculate_macd(data)
                    if 'Bollinger Bands' in indicators:
                        data = calculate_bollinger_bands(data)
                    if 'Volume' in indicators:
                        data = calculate_volume_indicators(data)

                # --- COMPACT HEADER: Name + Price ---
                current_price = data['Close'].iloc[-1]
                st.markdown(f"""
                <div class='tradingview-header' style='margin-top:0 !important;padding-top:0 !important;'>
                    <h2>{selected_stock_name} <span style='color:#758696;font-size:1rem;font-weight:400;'>({selected_symbol})</span></h2>
                    <span class='price'>₹{current_price:.2f}</span>
                </div>
                """, unsafe_allow_html=True)

                # --- CHART ---
                try:
                    chart_options, series_config = create_tradingview_chart(data, selected_stock_name, indicators)
                    renderLightweightCharts([
                        {
                            "chart": chart_options,
                            "series": series_config
                        }
                    ], 'tradingview_chart')
                except Exception as e:
                    st.error(f"Chart error: {str(e)}")
                    st.line_chart(data['Close'], height=400)

                # --- METRICS & ANALYSIS BELOW CHART ---
                prev_price = data['Close'].iloc[-2] if len(data) > 1 else current_price
                price_change = current_price - prev_price
                price_change_pct = (price_change / prev_price) * 100 if prev_price != 0 else 0

                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("Price", f"₹{current_price:.2f}", f"{price_change:+.2f} ({price_change_pct:+.2f}%)")
                with col2:
                    if info and info.get('fiftyTwoWeekHigh'):
                        st.metric("52W High", f"₹{info.get('fiftyTwoWeekHigh'):.2f}")
                    else:
                        high_52w = data['High'].max()
                        st.metric("52W High", f"₹{high_52w:.2f}")
                with col3:
                    if info and info.get('fiftyTwoWeekLow'):
                        st.metric("52W Low", f"₹{info.get('fiftyTwoWeekLow'):.2f}")
                    else:
                        low_52w = data['Low'].min()
                        st.metric("52W Low", f"₹{low_52w:.2f}")
                with col4:
                    volume = data['Volume'].iloc[-1]
                    st.metric("Volume", f"{volume:,.0f}")
                with col5:
                    if 'RSI' in data.columns and not pd.isna(data['RSI'].iloc[-1]):
                        rsi_val = data['RSI'].iloc[-1]
                        st.metric("RSI", f"{rsi_val:.1f}")
                    else:
                        st.metric("Data Points", f"{len(data):,}")

                # --- QUICK ANALYSIS ---
                if indicators and not data.empty:
                    analysis_cols = st.columns(3)
                    with analysis_cols[0]:
                        if 'RSI' in indicators and 'RSI' in data.columns:
                            rsi_val = data['RSI'].iloc[-1]
                            if not pd.isna(rsi_val):
                                if rsi_val > 70:
                                    st.info(f"🔴 RSI: {rsi_val:.1f} (Overbought)")
                                elif rsi_val < 30:
                                    st.info(f"🟢 RSI: {rsi_val:.1f} (Oversold)")
                                else:
                                    st.info(f"🟡 RSI: {rsi_val:.1f} (Neutral)")
                    with analysis_cols[1]:
                        if 'MACD' in indicators and 'MACD' in data.columns:
                            macd_val = data['MACD'].iloc[-1]
                            signal_val = data['MACD_Signal'].iloc[-1]
                            if not pd.isna(macd_val) and not pd.isna(signal_val):
                                if macd_val > signal_val:
                                    st.info("🟢 MACD: Bullish")
                                else:
                                    st.info("🔴 MACD: Bearish")
                    with analysis_cols[2]:
                        if 'MA' in indicators and 'MA_20' in data.columns:
                            ma20 = data['MA_20'].iloc[-1]
                            price = data['Close'].iloc[-1]
                            if not pd.isna(ma20):
                                if price > ma20:
                                    st.info("🟢 Above MA20")
                                else:
                                    st.info("🔴 Below MA20")

                # --- DATA TABLE ---
                with st.expander("📋 Data Table", expanded=False):
                    display_data = data.tail(20)[['Open', 'High', 'Low', 'Close', 'Volume']].round(2)
                    st.dataframe(display_data, use_container_width=True, height=260)
                    csv = data.to_csv()
                    st.download_button(
                        "📥 Download CSV",
                        data=csv,
                        file_name=f"{selected_symbol}_{start_date}_{end_date}.csv",
                        mime="text/csv"
                    )
            else:
                st.error("❌ No data available")
                st.info("Try different date range or stock symbol")
        else:
            # Only show welcome screen if 'fetch_data' is not in session state (never pressed Get Data)
            if not hasattr(st.session_state, 'fetch_data'):
                st.markdown("""
                <div class="tradingview-header" style="justify-content:center;">
                    <h1 style="color: #D1D4DC; text-align: center; margin: 0; font-size:1.5rem;">📈 TradingView Pro Stock Analysis</h1>
                </div>
                """, unsafe_allow_html=True)
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown("""
                    <div class="metric-container">
                        <h3 style="color: #D1D4DC; margin: 0; font-size:1.05rem;">📊 Advanced Charts</h3>
                        <p style="color: #758696; margin: 5px 0 0 0; font-size:0.95rem;">
                        • TradingView-style interface<br>
                        • Interactive candlestick charts<br>
                        • Multiple timeframes<br>
                        • Real-time data updates
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown("""
                    <div class="metric-container">
                        <h3 style="color: #D1D4DC; margin: 0; font-size:1.05rem;">📈 Technical Analysis</h3>
                        <p style="color: #758696; margin: 5px 0 0 0; font-size:0.95rem;">
                        • Moving averages (MA20, MA50)<br>
                        • RSI & MACD indicators<br>
                        • Bollinger Bands<br>
                        • Volume analysis
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown("""
                    <div class="metric-container">
                        <h3 style="color: #D1D4DC; margin: 0; font-size:1.05rem;">🕐 Intraday Tools</h3>
                        <p style="color: #758696; margin: 5px 0 0 0; font-size:0.95rem;">
                        • Custom time range filtering<br>
                        • 1m to 1d intervals<br>
                        • Session analysis<br>
                        • Pattern recognition
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("""
                <div style="text-align: center; padding: 12px; background-color: #131722; border-radius: 8px; border: 1px solid #1E222D;">
                    <h3 style="color: #2962FF; margin: 0; font-size:1.1rem;">🚀 Quick Start</h3>
                    <p style="color: #D1D4DC; margin: 10px 0; font-size:0.98rem;">
                        1. Select a stock from the sidebar<br>
                        2. Choose your date range and timeframe<br>
                        3. Pick technical indicators<br>
                        4. Click "📊 Get Data" to start analyzing
                    </p>
                </div>
                """, unsafe_allow_html=True)
if __name__ == "__main__":
    main()
