# Stock Forensic Analysis Tool

A comprehensive Python tool for advanced stock forensic analysis using financial fraud detection techniques, pattern recognition, and news sentiment analysis.

## 🎯 Features

### Data Sources
- **Yahoo Finance API**: Historical prices, financial statements, ratios, shareholding patterns
- **You.com Live News API**: Real-time news articles and financial analysis from across the web

### Forensic Analysis
- **Beneish M-Score**: Detects potential earnings manipulation using 8 financial variables
- **Altman Z-Score**: Predicts bankruptcy risk using 5 financial ratios
- **Promoter Pledge Analysis**: Analyzes insider and institutional ownership patterns
- **Financial Red Flags**: Identifies concerning patterns in financial statements
- **Unusual Patterns**: Detects abnormal price/volume movements

### Report Generation
- **JSON Format**: Machine-readable structured data
- **HTML Format**: Beautiful, interactive reports with visualizations
- **Console Output**: Quick summary for command-line usage

## 📋 Requirements

- Python 3.8 or higher
- You.com API key (for news analysis)

## 🚀 Installation

1. **Clone or download the project**
   ```bash
   cd stock-forensic-analysis
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys**
   
   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your You.com API key:
   ```
   YOU_API_KEY=your_you_api_key_here
   ```
   
   **Getting a You.com API Key:**
   - Visit https://documentation.you.com/
   - Contact api@you.com to request early access to the Live News API
   - See `YOU_API_INTEGRATION.md` for detailed setup instructions

## 📖 Usage

### Basic Usage

Analyze a stock with default settings (1 year of data):
```bash
python main.py AAPL
```

### Advanced Usage

```bash
# Analyze with 2 years of historical data
python main.py TSLA --period 2y

# Generate only JSON report
python main.py MSFT --json-only

# Generate only HTML report
python main.py GOOGL --html-only

# Specify custom output directory
python main.py AMZN --output-dir ./my_reports

# Use custom API key
python main.py NVDA --api-key your_api_key_here

# Console output only (no report files)
python main.py META --no-reports
```

### Command-Line Options

```
positional arguments:
  symbol                Stock ticker symbol (e.g., AAPL, TSLA, MSFT)

optional arguments:
  -h, --help            Show help message
  --period {1m,3m,6m,1y,2y,5y}
                        Historical data period (default: 1y)
  --api-key API_KEY     You.com API key (overrides environment variable)
  --json-only           Generate only JSON report
  --html-only           Generate only HTML report
  --no-reports          Skip report generation (console output only)
  --output-dir DIR      Output directory for reports (default: reports/)
```

## 📊 Understanding the Analysis

### Beneish M-Score
- **Score > -2.22**: Suggests possible earnings manipulation
- **Score ≤ -2.22**: Lower likelihood of manipulation
- Uses 8 variables: DSRI, GMI, AQI, SGI, DEPI, SGAI, LVGI, TATA

### Altman Z-Score
- **Z > 2.99**: Safe Zone (low bankruptcy risk)
- **1.81 < Z < 2.99**: Grey Zone (moderate risk)
- **Z < 1.81**: Distress Zone (high bankruptcy risk)
- Uses 5 ratios based on working capital, retained earnings, EBIT, market value, and sales

### Risk Levels
- **HIGH**: Significant concerns detected, requires immediate attention
- **MEDIUM**: Some concerns present, warrants monitoring
- **LOW**: No major concerns identified

## 📁 Project Structure

```
stock-forensic-analysis/
├── main.py                      # Main entry point
├── config.py                    # Configuration management
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── README.md                    # This file
├── src/
│   ├── __init__.py
│   ├── data_fetcher.py         # API integrations
│   ├── forensic_analyzer.py    # Forensic calculations
│   ├── news_analyzer.py        # News sentiment analysis
│   ├── pattern_detector.py     # Pattern detection
│   ├── report_generator.py     # Report generation
│   └── utils.py                # Helper functions
└── reports/                     # Generated reports (auto-created)
```

## 🔍 Example Output

### Console Output
```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║          STOCK FORENSIC ANALYSIS TOOL                         ║
║          Advanced Financial Fraud Detection                   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

======================================================================
Starting forensic analysis for AAPL
======================================================================

STEP 1: Fetching data from APIs...
----------------------------------------------------------------------
✓ Data fetched successfully for Apple Inc.

STEP 2: Performing forensic analysis...
----------------------------------------------------------------------
✓ Forensic analysis completed
  - Beneish M-Score: -2.45 (LOW)
  - Altman Z-Score: 3.85 (LOW)
  - Red Flags Detected: 1

STEP 3: Analyzing news articles...
----------------------------------------------------------------------
✓ News analysis completed
  - Articles Analyzed: 10
  - Sentiment: POSITIVE
  - Risk Level: LOW
  - Critical News Items: 0

STEP 4: Detecting price and volume patterns...
----------------------------------------------------------------------
✓ Pattern detection completed
  - Volume Spikes: 5
  - Price Anomalies: 3
  - Volatility: 28.45%

STEP 5: Calculating overall risk assessment...
----------------------------------------------------------------------
✓ Overall risk assessment completed
  - Overall Risk Score: 0.25
  - Overall Risk Level: LOW
```

### Generated Reports

1. **JSON Report**: `AAPL_forensic_analysis_20240115_143022.json`
   - Complete structured data
   - All calculations and metrics
   - Machine-readable format

2. **HTML Report**: `AAPL_forensic_analysis_20240115_143022.html`
   - Beautiful, interactive report
   - Color-coded risk indicators
   - Charts and visualizations
   - Easy to share and present

## 🔧 Configuration

Edit `config.py` or set environment variables in `.env`:

```python
# API Keys
YOU_API_KEY=your_api_key

# Report Configuration
REPORT_OUTPUT_DIR=reports
DEFAULT_ANALYSIS_PERIOD=1y

# Risk Thresholds
RISK_THRESHOLD_HIGH=0.7
RISK_THRESHOLD_MEDIUM=0.4

# Forensic Thresholds
BENEISH_M_SCORE_THRESHOLD=-2.22
ALTMAN_Z_SCORE_SAFE=2.99
ALTMAN_Z_SCORE_DISTRESS=1.81

# Pattern Detection
VOLUME_SPIKE_THRESHOLD=2.0
PRICE_CHANGE_THRESHOLD=0.05
```

## 🎓 Forensic Indicators Explained

### Beneish M-Score Components

1. **DSRI** (Days Sales in Receivables Index): Measures receivables growth vs. sales growth
2. **GMI** (Gross Margin Index): Compares gross margins year-over-year
3. **AQI** (Asset Quality Index): Measures asset quality deterioration
4. **SGI** (Sales Growth Index): Measures sales growth
5. **DEPI** (Depreciation Index): Compares depreciation rates
6. **SGAI** (SG&A Index): Measures SG&A expense growth
7. **LVGI** (Leverage Index): Measures debt level changes
8. **TATA** (Total Accruals to Total Assets): Measures accrual quality

### Financial Red Flags Detected

- Negative or declining profit margins
- High debt-to-equity ratios
- Low liquidity ratios
- Negative return on equity
- Significant revenue declines
- Unusual accounting patterns

## 🛡️ Disclaimer

**IMPORTANT**: This tool is for informational and educational purposes only. It should NOT be considered as:
- Investment advice
- Financial advice
- A recommendation to buy or sell securities
- A guarantee of accuracy or completeness

Always consult with qualified financial professionals before making investment decisions. Past performance does not guarantee future results.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional forensic indicators
- More sophisticated pattern detection
- Enhanced visualization
- Support for international markets
- Real-time monitoring capabilities

## 📝 License

This project is provided as-is for educational purposes.

## 🆘 Troubleshooting

### Common Issues

1. **"Could not fetch data for symbol"**
   - Verify the ticker symbol is correct
   - Check your internet connection
   - Some symbols may not be available on Yahoo Finance

2. **"You.com API key not configured"**
   - Add your API key to the `.env` file
   - Or use `--api-key` command-line option
   - News analysis will be limited without API key

3. **"Insufficient data for calculation"**
   - Some stocks may not have complete financial data
   - Try a different time period
   - Newer companies may have limited historical data

4. **Module import errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Activate your virtual environment if using one

## 📧 Support

For issues, questions, or suggestions, please refer to the project documentation or create an issue in the project repository.

## 🙏 Acknowledgments

- Yahoo Finance for providing financial data
- You.com for news and article search capabilities
- The financial forensics community for research on fraud detection methods

---

**Happy Analyzing! 📊🔍**
