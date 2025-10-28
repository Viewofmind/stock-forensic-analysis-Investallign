# Quick Start Guide

Get started with the Stock Forensic Analysis Tool in 5 minutes!

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
cd stock-forensic-analysis
pip install -r requirements.txt
```

### 2. Configure API Key

Edit the `.env` file and add your You.com API key:

```bash
# Open .env file and replace with your actual API key
YOU_API_KEY=your_actual_you_api_key_here
```

**Note**: If you don't have a You.com API key yet:
- Visit https://api.you.com to sign up
- The tool will still work without it, but news analysis will be limited

### 3. Run Your First Analysis

```bash
python main.py AAPL
```

That's it! The tool will:
- ✓ Fetch financial data from Yahoo Finance
- ✓ Fetch news from You.com
- ✓ Calculate forensic indicators (M-Score, Z-Score)
- ✓ Detect unusual patterns
- ✓ Analyze news sentiment
- ✓ Generate HTML and JSON reports

## 📊 Example Commands

### Analyze Different Stocks

```bash
# Apple
python main.py AAPL

# Tesla
python main.py TSLA

# Microsoft
python main.py MSFT

# Google
python main.py GOOGL
```

### Use Different Time Periods

```bash
# 3 months of data
python main.py AAPL --period 3m

# 2 years of data
python main.py TSLA --period 2y

# 5 years of data
python main.py MSFT --period 5y
```

### Generate Specific Report Types

```bash
# Only JSON report
python main.py AAPL --json-only

# Only HTML report
python main.py TSLA --html-only

# Console output only (no files)
python main.py MSFT --no-reports
```

## 📁 Where Are My Reports?

Reports are saved in the `reports/` directory:

```
stock-forensic-analysis/
└── reports/
    ├── AAPL_forensic_analysis_20240115_143022.json
    ├── AAPL_forensic_analysis_20240115_143022.html
    ├── TSLA_forensic_analysis_20240115_144530.json
    └── TSLA_forensic_analysis_20240115_144530.html
```

### Open HTML Report

**macOS:**
```bash
open reports/AAPL_forensic_analysis_*.html
```

**Windows:**
```bash
start reports\AAPL_forensic_analysis_*.html
```

**Linux:**
```bash
xdg-open reports/AAPL_forensic_analysis_*.html
```

## 🎯 Understanding the Output

### Console Output

```
✓ Forensic analysis completed
  - Beneish M-Score: -2.45 (LOW)      ← Earnings manipulation risk
  - Altman Z-Score: 3.85 (LOW)        ← Bankruptcy risk
  - Red Flags Detected: 1             ← Financial concerns

✓ News analysis completed
  - Sentiment: POSITIVE                ← Overall news sentiment
  - Risk Level: LOW                    ← News-based risk

✓ Pattern detection completed
  - Volume Spikes: 5                   ← Unusual trading volume
  - Volatility: 28.45%                 ← Price volatility
```

### Risk Levels

- 🟢 **LOW**: No major concerns
- 🟡 **MEDIUM**: Some concerns, monitor closely
- 🔴 **HIGH**: Significant concerns, investigate further

### Key Indicators

**Beneish M-Score:**
- Score > -2.22 = Possible earnings manipulation
- Score ≤ -2.22 = Lower manipulation risk

**Altman Z-Score:**
- Z > 2.99 = Safe (low bankruptcy risk)
- 1.81 < Z < 2.99 = Grey zone
- Z < 1.81 = Distress (high bankruptcy risk)

## 🔧 Troubleshooting

### "Could not fetch data"
- Check if the ticker symbol is correct
- Verify internet connection
- Try a different stock

### "API key not configured"
- Add your You.com API key to `.env` file
- Or use: `python main.py AAPL --api-key YOUR_KEY`

### "Module not found"
- Install dependencies: `pip install -r requirements.txt`
- Activate virtual environment if using one

## 💡 Pro Tips

1. **Compare Multiple Stocks**: Run analysis on competitors
   ```bash
   python main.py AAPL
   python main.py MSFT
   python main.py GOOGL
   ```

2. **Track Over Time**: Run weekly/monthly to track changes
   ```bash
   # Save with custom directory
   python main.py AAPL --output-dir ./weekly_reports
   ```

3. **Automate Analysis**: Create a script to analyze multiple stocks
   ```bash
   for symbol in AAPL MSFT GOOGL TSLA; do
       python main.py $symbol
   done
   ```

4. **Use Programmatically**: Import as a library
   ```python
   from src.data_fetcher import DataAggregator
   from src.forensic_analyzer import ForensicAnalyzer
   
   # Your custom analysis code
   ```

## 📚 Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Check [example_usage.py](example_usage.py) for programmatic usage
3. Customize thresholds in [config.py](config.py)
4. Explore the generated HTML reports for detailed insights

## 🆘 Need Help?

- Check the [README.md](README.md) for detailed documentation
- Review [example_usage.py](example_usage.py) for code examples
- Verify your `.env` configuration

---

**Happy Analyzing! 📊🔍**
