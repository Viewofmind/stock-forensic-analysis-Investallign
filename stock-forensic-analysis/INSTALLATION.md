# Installation Guide

Complete step-by-step installation instructions for the Stock Forensic Analysis Tool.

## 📋 Prerequisites

- **Python**: Version 3.8 or higher
- **pip**: Python package installer
- **Internet Connection**: Required for data fetching
- **You.com API Key**: Optional but recommended for news analysis

## 🔍 Check Python Version

```bash
python --version
# or
python3 --version
```

If Python is not installed or version is below 3.8, download from [python.org](https://www.python.org/downloads/)

## 📦 Installation Steps

### Step 1: Navigate to Project Directory

```bash
cd /Users/gunjanchokshi/Desktop/stock-forensic-analysis
```

### Step 2: Create Virtual Environment (Recommended)

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- yfinance (Yahoo Finance data)
- pandas (data manipulation)
- numpy (numerical computations)
- requests (HTTP requests)
- python-dotenv (environment variables)
- jinja2 (HTML templates)
- scipy (scientific computing)
- matplotlib (plotting)
- beautifulsoup4 (HTML parsing)

### Step 4: Configure API Key

1. **Get You.com API Key**:
   - Visit https://api.you.com
   - Sign up for an account
   - Generate an API key

2. **Add to .env file**:
   ```bash
   # Edit the .env file
   nano .env
   # or use any text editor
   ```
   
   Replace `your_you_api_key_here` with your actual API key:
   ```
   YOU_API_KEY=your_actual_api_key_here
   ```

### Step 5: Verify Installation

```bash
python main.py --help
```

You should see the help message with all available options.

## ✅ Test Installation

### Quick Test

```bash
python main.py AAPL --no-reports
```

This will:
- Fetch data for Apple (AAPL)
- Run complete analysis
- Display results in console
- Skip report generation

### Full Test

```bash
python main.py AAPL
```

This will:
- Fetch data for Apple
- Run complete analysis
- Generate JSON and HTML reports
- Save reports to `reports/` directory

### Check Reports

```bash
ls -la reports/
```

You should see generated report files.

## 🔧 Troubleshooting

### Issue: "Command not found: python"

**Solution**: Try `python3` instead:
```bash
python3 main.py AAPL
```

### Issue: "No module named 'yfinance'"

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
# or
pip3 install -r requirements.txt
```

### Issue: "Permission denied"

**Solution**: Make scripts executable:
```bash
chmod +x main.py example_usage.py
```

### Issue: Virtual environment not activating

**macOS/Linux Solution**:
```bash
source venv/bin/activate
```

**Windows Solution**:
```bash
venv\Scripts\activate
```

### Issue: "Could not fetch data for symbol"

**Possible Causes**:
1. Invalid ticker symbol
2. No internet connection
3. Yahoo Finance API temporarily unavailable

**Solution**:
- Verify ticker symbol is correct
- Check internet connection
- Try again after a few minutes

### Issue: "You.com API key not configured"

**Solution**:
1. Get API key from https://api.you.com
2. Add to `.env` file
3. Or use command line: `python main.py AAPL --api-key YOUR_KEY`

**Note**: Tool works without API key, but news analysis will be limited.

## 🔄 Updating

To update dependencies:

```bash
pip install --upgrade -r requirements.txt
```

## 🗑️ Uninstallation

### Remove Virtual Environment

```bash
deactivate  # Exit virtual environment
rm -rf venv  # Remove virtual environment directory
```

### Remove Project

```bash
cd ..
rm -rf stock-forensic-analysis
```

## 🐳 Docker Installation (Optional)

If you prefer Docker:

### Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "main.py"]
```

### Build and Run

```bash
# Build image
docker build -t stock-forensic-analysis .

# Run analysis
docker run -v $(pwd)/reports:/app/reports stock-forensic-analysis AAPL
```

## 📱 Platform-Specific Notes

### macOS

- Use `python3` and `pip3` commands
- May need to install Xcode Command Line Tools:
  ```bash
  xcode-select --install
  ```

### Windows

- Use `python` and `pip` commands
- May need to enable script execution:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

### Linux

- Use `python3` and `pip3` commands
- May need to install python3-venv:
  ```bash
  sudo apt-get install python3-venv  # Ubuntu/Debian
  sudo yum install python3-venv      # CentOS/RHEL
  ```

## 🎓 Next Steps

After successful installation:

1. **Read Documentation**:
   - [QUICKSTART.md](QUICKSTART.md) - Quick start guide
   - [README.md](README.md) - Comprehensive documentation
   - [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Project overview

2. **Try Examples**:
   ```bash
   python main.py AAPL
   python main.py TSLA --period 2y
   python example_usage.py
   ```

3. **Explore Reports**:
   - Open HTML reports in browser
   - Review JSON data structure
   - Understand risk indicators

4. **Customize**:
   - Edit `config.py` for custom thresholds
   - Modify report templates
   - Add custom analysis

## 📞 Support

If you encounter issues:

1. Check this installation guide
2. Review [README.md](README.md) troubleshooting section
3. Verify all prerequisites are met
4. Ensure internet connection is stable
5. Check Python and pip versions

## ✅ Installation Checklist

- [ ] Python 3.8+ installed
- [ ] Project directory accessible
- [ ] Virtual environment created (optional but recommended)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] You.com API key configured in `.env`
- [ ] Test run successful (`python main.py AAPL --no-reports`)
- [ ] Reports generated successfully
- [ ] Documentation reviewed

---

**Congratulations! You're ready to start analyzing stocks! 🎉**
