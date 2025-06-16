# 📈 TradingView Pro Stock Analysis

A professional-grade stock analysis application built with Streamlit, featuring TradingView-style charts and comprehensive technical analysis tools.

## 🚀 Features

- **Interactive Charts**: TradingView-style candlestick charts with zoom and pan capabilities
- **Technical Indicators**: Moving Averages, RSI, MACD, Bollinger Bands, Volume Analysis
- **Multi-Timeframe Support**: 1m, 5m, 15m, 30m, 1h, 1d, 5d, 1w intervals
- **Intraday Analysis**: Custom time range filtering for detailed session analysis
- **Real-time Data**: Live stock data via Yahoo Finance API
- **Export Functionality**: Download data as CSV
- **Responsive Design**: Mobile-friendly interface

## 🛠️ Tech Stack

- **Frontend**: Streamlit, Lightweight Charts
- **Data**: Yahoo Finance (yfinance), Pandas, NumPy
- **Technical Analysis**: TA-Lib, Custom indicators
- **Deployment**: Docker, Docker Compose

## 📦 Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd Reseach-app-production

# Build and run with Docker Compose
docker-compose up --build

# Access the app at http://localhost:8501
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run working1.py
```

## 🚀 Deployment

### Streamlit Cloud (Easiest)
1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Deploy directly from the repository

### Railway
1. Connect your repository to Railway
2. Railway will automatically detect the Dockerfile
3. Deploy with one click

### Render
1. Create a new Web Service on Render
2. Connect your repository
3. Use Docker deployment option

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | `false` | Enable debug mode |
| `CACHE_TTL` | `300` | Cache timeout in seconds |
| `API_RATE_LIMIT` | `1.0` | Minimum seconds between API calls |
| `MAX_DATA_POINTS` | `10000` | Maximum data points to fetch |
| `CHART_HEIGHT` | `580` | Chart height in pixels |

### Production Settings

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
# Edit .env with your settings
```

## 📊 Supported Stocks

The application supports 2000+ Indian stocks listed on NSE. Stock symbols are loaded from `stock_names.json`.

## 🛡️ Production Features

- **Error Handling**: Comprehensive error handling and user feedback
- **Rate Limiting**: API call rate limiting to prevent abuse
- **Caching**: Intelligent data caching for improved performance
- **Health Checks**: Built-in health monitoring and system diagnostics
- **Logging**: Production-grade logging and monitoring
- **Security**: Non-root user execution, CORS protection

## 📈 Performance

- **Response Time**: < 2 seconds for data fetching
- **Memory Usage**: < 200MB typical usage
- **Concurrent Users**: Supports 10+ concurrent users
- **Cache Hit Rate**: 80%+ for repeated queries

## 🔍 Health Monitoring

The application includes built-in health checks:

- File dependency verification
- Memory and disk usage monitoring
- API connectivity testing
- System performance metrics

Access health info through the sidebar "System Info" checkbox.

## 🐛 Troubleshooting

### Common Issues

1. **"No data available"**: Check internet connection and stock symbol
2. **Rate limit exceeded**: Wait 1-2 minutes and try again
3. **Chart not loading**: Refresh the page or try a different timeframe
4. **Memory issues**: Reduce date range or use higher timeframes

### Logs

Application logs are available in:
- Development: Console output
- Production: `/app/app.log` (Docker container)

## 📝 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

For issues and support:
- Create an issue on GitHub
- Check the troubleshooting section
- Review application logs

---

**Built with ❤️ using Streamlit and Python**
