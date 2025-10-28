#!/usr/bin/env python3
"""
Example usage script for Stock Forensic Analysis Tool
Demonstrates how to use the tool programmatically
"""

from src.data_fetcher import DataAggregator
from src.forensic_analyzer import ForensicAnalyzer
from src.news_analyzer import NewsAnalyzer
from src.pattern_detector import PatternDetector
from src.report_generator import ReportGenerator


def analyze_stock_programmatically(symbol: str):
    """
    Example of using the tool programmatically
    
    Args:
        symbol: Stock ticker symbol
    """
    print(f"Analyzing {symbol}...\n")
    
    # Step 1: Fetch data
    print("1. Fetching data...")
    aggregator = DataAggregator(symbol)
    data = aggregator.fetch_all_data(period='1y')
    
    # Step 2: Forensic analysis
    print("2. Running forensic analysis...")
    forensic_analyzer = ForensicAnalyzer(data)
    forensic_report = forensic_analyzer.generate_forensic_report()
    
    # Print M-Score
    m_score = forensic_report['beneish_m_score']
    print(f"\n   Beneish M-Score: {m_score.get('score', 'N/A')}")
    print(f"   Risk Level: {m_score.get('risk_level', 'UNKNOWN')}")
    print(f"   Interpretation: {m_score.get('interpretation', '')}")
    
    # Print Z-Score
    z_score = forensic_report['altman_z_score']
    print(f"\n   Altman Z-Score: {z_score.get('score', 'N/A')}")
    print(f"   Risk Level: {z_score.get('risk_level', 'UNKNOWN')}")
    print(f"   Interpretation: {z_score.get('interpretation', '')}")
    
    # Step 3: News analysis
    print("\n3. Analyzing news...")
    news_data = data.get('news', []) + data.get('financial_analysis', [])
    news_analyzer = NewsAnalyzer(news_data)
    news_report = news_analyzer.summarize_news()
    
    sentiment = news_report['sentiment_analysis']
    print(f"\n   Sentiment: {sentiment.get('sentiment', 'NEUTRAL')}")
    print(f"   Sentiment Score: {sentiment.get('sentiment_score', 0)}")
    print(f"   Articles Analyzed: {news_report['total_articles_analyzed']}")
    
    # Step 4: Pattern detection
    print("\n4. Detecting patterns...")
    pattern_detector = PatternDetector(data.get('historical_data'))
    pattern_report = pattern_detector.generate_pattern_report()
    
    print(f"\n   Volume Spikes: {pattern_report['volume_spikes'].get('spikes_detected', 0)}")
    print(f"   Price Anomalies: {pattern_report['price_anomalies'].get('anomalies_detected', 0)}")
    print(f"   Volatility: {pattern_report['volatility_metrics'].get('annualized_volatility', 0):.2f}%")
    
    # Step 5: Generate reports
    print("\n5. Generating reports...")
    
    # Compile complete analysis
    complete_analysis = {
        'symbol': symbol,
        'stock_info': data.get('stock_info', {}),
        'key_ratios': data.get('key_ratios', {}),
        'forensic_analysis': forensic_report,
        'news_analysis': news_report,
        'pattern_analysis': pattern_report,
        'overall_risk_score': forensic_report.get('overall_risk_score', 0),
        'overall_risk_level': forensic_report.get('overall_risk_level', 'UNKNOWN'),
    }
    
    report_gen = ReportGenerator(complete_analysis)
    
    # Generate JSON report
    json_path = report_gen.generate_json_report()
    print(f"\n   JSON report: {json_path}")
    
    # Generate HTML report
    html_path = report_gen.generate_html_report()
    print(f"   HTML report: {html_path}")
    
    print(f"\n✓ Analysis complete for {symbol}!")
    
    return complete_analysis


def main():
    """Main function"""
    # Example 1: Analyze Apple
    print("=" * 70)
    print("EXAMPLE 1: Analyzing Apple (AAPL)")
    print("=" * 70)
    analyze_stock_programmatically('AAPL')
    
    print("\n\n")
    
    # Example 2: Analyze Tesla
    print("=" * 70)
    print("EXAMPLE 2: Analyzing Tesla (TSLA)")
    print("=" * 70)
    analyze_stock_programmatically('TSLA')


if __name__ == '__main__':
    main()
