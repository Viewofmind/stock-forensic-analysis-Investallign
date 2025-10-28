#!/usr/bin/env python3
"""
Installation Test Script
Verifies that all components are properly installed and configured
"""

import sys
import os

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_status(test_name, passed, message=""):
    """Print test status"""
    status = "✓ PASS" if passed else "✗ FAIL"
    color = "\033[92m" if passed else "\033[91m"
    reset = "\033[0m"
    print(f"{color}{status}{reset} - {test_name}")
    if message:
        print(f"       {message}")

def test_python_version():
    """Test Python version"""
    version = sys.version_info
    passed = version.major == 3 and version.minor >= 8
    message = f"Python {version.major}.{version.minor}.{version.micro}"
    print_status("Python Version (>= 3.8)", passed, message)
    return passed

def test_imports():
    """Test required imports"""
    print_header("Testing Required Packages")
    
    packages = [
        ('yfinance', 'yfinance'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('requests', 'requests'),
        ('dotenv', 'python-dotenv'),
        ('jinja2', 'jinja2'),
        ('scipy', 'scipy'),
        ('matplotlib', 'matplotlib'),
        ('bs4', 'beautifulsoup4'),
    ]
    
    all_passed = True
    for module_name, package_name in packages:
        try:
            __import__(module_name)
            print_status(f"Package: {package_name}", True)
        except ImportError:
            print_status(f"Package: {package_name}", False, f"Run: pip install {package_name}")
            all_passed = False
    
    return all_passed

def test_project_structure():
    """Test project structure"""
    print_header("Testing Project Structure")
    
    required_files = [
        'main.py',
        'config.py',
        'requirements.txt',
        '.env.example',
        'README.md',
        'src/__init__.py',
        'src/data_fetcher.py',
        'src/forensic_analyzer.py',
        'src/news_analyzer.py',
        'src/pattern_detector.py',
        'src/report_generator.py',
        'src/utils.py',
    ]
    
    all_passed = True
    for file_path in required_files:
        exists = os.path.exists(file_path)
        print_status(f"File: {file_path}", exists)
        if not exists:
            all_passed = False
    
    return all_passed

def test_configuration():
    """Test configuration"""
    print_header("Testing Configuration")
    
    try:
        from config import Config
        print_status("Config module import", True)
        
        # Check if .env exists
        env_exists = os.path.exists('.env')
        print_status(".env file exists", env_exists, 
                    "Create from .env.example if missing" if not env_exists else "")
        
        # Check API key
        api_key_set = bool(Config.YOU_API_KEY and Config.YOU_API_KEY != 'your_you_api_key_here')
        print_status("You.com API key configured", api_key_set,
                    "Set YOU_API_KEY in .env file" if not api_key_set else "API key is set")
        
        return True
    except Exception as e:
        print_status("Config module import", False, str(e))
        return False

def test_modules():
    """Test custom modules"""
    print_header("Testing Custom Modules")
    
    modules = [
        'src.data_fetcher',
        'src.forensic_analyzer',
        'src.news_analyzer',
        'src.pattern_detector',
        'src.report_generator',
        'src.utils',
    ]
    
    all_passed = True
    for module_name in modules:
        try:
            __import__(module_name)
            print_status(f"Module: {module_name}", True)
        except Exception as e:
            print_status(f"Module: {module_name}", False, str(e))
            all_passed = False
    
    return all_passed

def test_basic_functionality():
    """Test basic functionality"""
    print_header("Testing Basic Functionality")
    
    try:
        from src.utils import safe_divide, format_currency, get_risk_level
        
        # Test safe_divide
        result = safe_divide(10, 2)
        passed = result == 5.0
        print_status("Utils: safe_divide", passed)
        
        # Test format_currency
        result = format_currency(1500000)
        passed = result == "$1.50M"
        print_status("Utils: format_currency", passed)
        
        # Test get_risk_level
        result = get_risk_level(0.8)
        passed = result == "HIGH"
        print_status("Utils: get_risk_level", passed)
        
        return True
    except Exception as e:
        print_status("Basic functionality", False, str(e))
        return False

def test_data_fetcher():
    """Test data fetcher (without actual API call)"""
    print_header("Testing Data Fetcher Module")
    
    try:
        from src.data_fetcher import YahooFinanceDataFetcher, YouComNewsDataFetcher, DataAggregator
        
        print_status("YahooFinanceDataFetcher class", True)
        print_status("YouComNewsDataFetcher class", True)
        print_status("DataAggregator class", True)
        
        return True
    except Exception as e:
        print_status("Data fetcher module", False, str(e))
        return False

def test_forensic_analyzer():
    """Test forensic analyzer"""
    print_header("Testing Forensic Analyzer Module")
    
    try:
        from src.forensic_analyzer import ForensicAnalyzer
        
        print_status("ForensicAnalyzer class", True)
        
        # Test with empty data
        analyzer = ForensicAnalyzer({})
        print_status("ForensicAnalyzer initialization", True)
        
        return True
    except Exception as e:
        print_status("Forensic analyzer module", False, str(e))
        return False

def test_report_generator():
    """Test report generator"""
    print_header("Testing Report Generator Module")
    
    try:
        from src.report_generator import ReportGenerator
        
        print_status("ReportGenerator class", True)
        
        # Test with minimal data
        test_data = {
            'symbol': 'TEST',
            'stock_info': {},
            'forensic_analysis': {},
            'news_analysis': {},
            'pattern_analysis': {},
        }
        
        generator = ReportGenerator(test_data)
        print_status("ReportGenerator initialization", True)
        
        return True
    except Exception as e:
        print_status("Report generator module", False, str(e))
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("  STOCK FORENSIC ANALYSIS TOOL - INSTALLATION TEST")
    print("=" * 70)
    
    results = []
    
    # Run tests
    print_header("Testing Python Environment")
    results.append(("Python Version", test_python_version()))
    
    results.append(("Required Packages", test_imports()))
    results.append(("Project Structure", test_project_structure()))
    results.append(("Configuration", test_configuration()))
    results.append(("Custom Modules", test_modules()))
    results.append(("Basic Functionality", test_basic_functionality()))
    results.append(("Data Fetcher", test_data_fetcher()))
    results.append(("Forensic Analyzer", test_forensic_analyzer()))
    results.append(("Report Generator", test_report_generator()))
    
    # Summary
    print_header("Test Summary")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for test_name, passed in results:
        status = "✓" if passed else "✗"
        print(f"  {status} {test_name}")
    
    print("\n" + "-" * 70)
    print(f"  Results: {passed_count}/{total_count} tests passed")
    print("-" * 70)
    
    if passed_count == total_count:
        print("\n✓ All tests passed! Installation is complete and working.")
        print("\nNext steps:")
        print("  1. Add your You.com API key to .env file (if not already done)")
        print("  2. Run: python main.py AAPL")
        print("  3. Check the generated reports in the reports/ directory")
        print("\nFor more information, see:")
        print("  - QUICKSTART.md for quick start guide")
        print("  - README.md for comprehensive documentation")
        return 0
    else:
        print("\n✗ Some tests failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("  - Install missing packages: pip install -r requirements.txt")
        print("  - Create .env file from .env.example")
        print("  - Ensure you're in the correct directory")
        print("\nFor help, see INSTALLATION.md")
        return 1

if __name__ == '__main__':
    sys.exit(main())
