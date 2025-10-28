#!/usr/bin/env python3
"""
Stock Forensic Analysis Tool - Main Entry Point

This tool performs comprehensive forensic analysis on stocks using:
- Yahoo Finance API for financial data
- You.com API for news and articles
- Advanced forensic indicators (Beneish M-Score, Altman Z-Score)
- Pattern detection and risk analysis
"""

import sys
import argparse
from datetime import datetime

from config import Config
from src.data_fetcher import DataAggregator
from src.forensic_analyzer import ForensicAnalyzer
from src.news_analyzer import NewsAnalyzer
from src.pattern_detector import PatternDetector
from src.report_generator import ReportGenerator


def print_banner():
    """Print application banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║          STOCK FORENSIC ANALYSIS TOOL                         ║
    ║          Advanced Financial Fraud Detection                   ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def analyze_stock(symbol: str, period: str = '1y', you_api_key: str = None) -> dict:
    """
    Perform complete forensic analysis on a stock
    
    Args:
        symbol: Stock ticker symbol
        period: Historical data period
        you_api_key: You.com API key (optional)
        
    Returns:
        Dictionary containing complete analysis results
    """
    print(f"\n{'='*70}")
    print(f"Starting forensic analysis for {symbol}")
    print(f"{'='*70}\n")
    
    # Step 1: Fetch all data
    print("STEP 1: Fetching data from APIs...")
    print("-" * 70)
    
    aggregator = DataAggregator(symbol, you_api_key)
    data = aggregator.fetch_all_data(period)
    
    if not data.get('stock_info'):
        print(f"\n❌ Error: Could not fetch data for {symbol}")
        print("Please verify the ticker symbol is correct.")
        return None
    
    print(f"✓ Data fetched successfully for {data['stock_info'].get('company_name', symbol)}")
    
    # Step 2: Perform forensic analysis
    print("\nSTEP 2: Performing forensic analysis...")
    print("-" * 70)
    
    forensic_analyzer = ForensicAnalyzer(data)
    forensic_report = forensic_analyzer.generate_forensic_report()
    
    print(f"✓ Forensic analysis completed")
    print(f"  - Beneish M-Score: {forensic_report['beneish_m_score'].get('score', 'N/A')} "
          f"({forensic_report['beneish_m_score'].get('risk_level', 'UNKNOWN')})")
    print(f"  - Altman Z-Score: {forensic_report['altman_z_score'].get('score', 'N/A')} "
          f"({forensic_report['altman_z_score'].get('risk_level', 'UNKNOWN')})")
    print(f"  - Red Flags Detected: {forensic_report['financial_red_flags'].get('total_flags', 0)}")
    
    # Step 3: Analyze news
    print("\nSTEP 3: Analyzing news articles...")
    print("-" * 70)
    
    news_data = data.get('news', []) + data.get('financial_analysis', [])
    news_analyzer = NewsAnalyzer(news_data)
    news_report = news_analyzer.summarize_news()
    
    # Get critical news
    critical_news = news_analyzer.get_critical_news()
    news_report['critical_news'] = critical_news
    
    print(f"✓ News analysis completed")
    print(f"  - Articles Analyzed: {news_report['total_articles_analyzed']}")
    print(f"  - Sentiment: {news_report['sentiment_analysis'].get('sentiment', 'NEUTRAL')}")
    print(f"  - Risk Level: {news_report['risk_signals'].get('risk_level', 'UNKNOWN')}")
    print(f"  - Critical News Items: {len(critical_news)}")
    
    # Step 4: Detect patterns
    print("\nSTEP 4: Detecting price and volume patterns...")
    print("-" * 70)
    
    historical_data = data.get('historical_data')
    pattern_detector = PatternDetector(historical_data)
    pattern_report = pattern_detector.generate_pattern_report()
    
    print(f"✓ Pattern detection completed")
    print(f"  - Volume Spikes: {pattern_report['volume_spikes'].get('spikes_detected', 0)}")
    print(f"  - Price Anomalies: {pattern_report['price_anomalies'].get('anomalies_detected', 0)}")
    print(f"  - Volatility: {pattern_report['volatility_metrics'].get('annualized_volatility', 0):.2f}%")
    
    # Step 5: Calculate overall risk
    print("\nSTEP 5: Calculating overall risk assessment...")
    print("-" * 70)
    
    # Aggregate risk scores
    risk_scores = []
    
    # Forensic risk
    forensic_risk = forensic_report.get('overall_risk_score', 0.5)
    risk_scores.append(forensic_risk)
    
    # News risk
    news_risk = news_report['risk_signals'].get('risk_score', 0)
    risk_scores.append(news_risk)
    
    # Pattern risk
    pattern_risk = pattern_report.get('overall_pattern_risk_score', 0)
    risk_scores.append(pattern_risk)
    
    # Calculate weighted average (forensic analysis weighted more heavily)
    overall_risk_score = (
        forensic_risk * 0.5 +  # 50% weight
        news_risk * 0.3 +       # 30% weight
        pattern_risk * 0.2      # 20% weight
    )
    
    overall_risk_level = 'HIGH' if overall_risk_score > 0.6 else 'MEDIUM' if overall_risk_score > 0.3 else 'LOW'
    
    print(f"✓ Overall risk assessment completed")
    print(f"  - Overall Risk Score: {overall_risk_score:.2f}")
    print(f"  - Overall Risk Level: {overall_risk_level}")
    
    # Compile complete analysis
    complete_analysis = {
        'symbol': symbol,
        'analysis_timestamp': datetime.now().isoformat(),
        'stock_info': data.get('stock_info', {}),
        'key_ratios': data.get('key_ratios', {}),
        'forensic_analysis': forensic_report,
        'news_analysis': news_report,
        'pattern_analysis': pattern_report,
        'overall_risk_score': round(overall_risk_score, 2),
        'overall_risk_level': overall_risk_level,
    }
    
    return complete_analysis


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Stock Forensic Analysis Tool - Advanced financial fraud detection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py AAPL                    # Analyze Apple stock
  python main.py TSLA --period 2y        # Analyze Tesla with 2 years of data
  python main.py MSFT --json-only        # Generate only JSON report
  python main.py GOOGL --html-only       # Generate only HTML report
        """
    )
    
    parser.add_argument(
        'symbol',
        type=str,
        help='Stock ticker symbol (e.g., AAPL, TSLA, MSFT)'
    )
    
    parser.add_argument(
        '--period',
        type=str,
        default='1y',
        choices=['1m', '3m', '6m', '1y', '2y', '5y'],
        help='Historical data period (default: 1y)'
    )
    
    parser.add_argument(
        '--api-key',
        type=str,
        help='You.com API key (overrides environment variable)'
    )
    
    parser.add_argument(
        '--json-only',
        action='store_true',
        help='Generate only JSON report'
    )
    
    parser.add_argument(
        '--html-only',
        action='store_true',
        help='Generate only HTML report'
    )
    
    parser.add_argument(
        '--no-reports',
        action='store_true',
        help='Skip report generation (console output only)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default=None,
        help='Output directory for reports (default: reports/)'
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Validate API key
    api_key = args.api_key or Config.YOU_API_KEY
    if not api_key:
        print("⚠️  WARNING: You.com API key not configured.")
        print("   News analysis will be limited. Set YOU_API_KEY in .env file or use --api-key option.\n")
    
    try:
        # Perform analysis
        analysis_result = analyze_stock(args.symbol, args.period, api_key)
        
        if not analysis_result:
            sys.exit(1)
        
        # Generate reports
        if not args.no_reports:
            print("\nSTEP 6: Generating reports...")
            print("-" * 70)
            
            report_gen = ReportGenerator(analysis_result)
            
            # Print summary to console
            print("\n" + report_gen.generate_summary_text())
            
            # Generate JSON report
            if not args.html_only:
                json_path = report_gen.generate_json_report(args.output_dir)
                print(f"\n✓ JSON report generated: {json_path}")
            
            # Generate HTML report
            if not args.json_only:
                html_path = report_gen.generate_html_report(args.output_dir)
                print(f"✓ HTML report generated: {html_path}")
        
        print(f"\n{'='*70}")
        print("✓ Analysis completed successfully!")
        print(f"{'='*70}\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
