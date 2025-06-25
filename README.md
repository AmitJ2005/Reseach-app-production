<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-Stock%20Analysis-blueviolet?style=for-the-badge&logo=streamlit" alt="Streamlit Badge" />
  <img src="https://img.shields.io/github/stars/AmitJ2005/Reseach-app-production?style=for-the-badge" alt="GitHub stars" />
  <img src="https://img.shields.io/github/license/AmitJ2005/Reseach-app-production?style=for-the-badge" alt="License" />
  <a href="https://researchstock.streamlit.app/">
    <img src="https://img.shields.io/badge/Live%20Demo-Online-green?style=for-the-badge&logo=streamlit" alt="Live Demo" />
  </a>
</p>

# 📈 Stock Chart Analysis

<p align="center">
  <b>A modern, professional-grade stock analysis app with TradingView-style charts, technical indicators, and real-time data.</b><br>
  <a href="https://researchstock.streamlit.app/">🌐 Live Demo</a> ·
  <a href="https://github.com/AmitJ2005/Reseach-app-production">GitHub</a>
</p>

---

## 🚀 Features

<div align="center">

| 📊 Interactive Charts | 🧮 Technical Indicators | ⏱️ Multi-Timeframe | 🔄 Real-time Data | 📥 Export CSV | 📱 Responsive |
|:---------------------:|:----------------------:|:------------------:|:-----------------:|:-------------:|:-------------:|
| Candlestick, Zoom/Pan | MA, RSI, MACD, BB, Vol | 1m–1w, Intraday    | Yahoo Finance API | Downloadable  | Mobile Ready  |

</div>

---

## 🛠️ Tech Stack

<details>
<summary><b>Show Details</b></summary>

- <b>Frontend:</b> Streamlit, Lightweight Charts
- <b>Data:</b> Yahoo Finance (yfinance), Pandas, NumPy
- <b>Technical Analysis:</b> TA-Lib, Custom indicators
- <b>Deployment:</b> Docker, Docker Compose

</details>

---

## 📦 Quick Start

### 🚢 Using Docker (Recommended)

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


## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | `false` | Enable debug mode |
| `CACHE_TTL` | `300` | Cache timeout in seconds |
| `API_RATE_LIMIT` | `1.0` | Minimum seconds between API calls |
| `MAX_DATA_POINTS` | `10000` | Maximum data points to fetch |
| `CHART_HEIGHT` | `580` | Chart height in pixels |



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

**Built with ❤️ by Amit 😊**