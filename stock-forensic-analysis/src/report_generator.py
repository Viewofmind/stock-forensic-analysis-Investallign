"""
Report generation module for creating structured analysis reports
"""
import json
import os
from typing import Dict, Any
from datetime import datetime
from jinja2 import Template

from config import Config


class ReportGenerator:
    """Generate analysis reports in various formats"""
    
    def __init__(self, analysis_data: Dict[str, Any]):
        """
        Initialize the report generator
        
        Args:
            analysis_data: Complete analysis data
        """
        self.data = analysis_data
        self.symbol = analysis_data.get('symbol', 'UNKNOWN')
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    def generate_json_report(self, output_dir: str = None) -> str:
        """
        Generate JSON format report
        
        Args:
            output_dir: Output directory for the report
            
        Returns:
            Path to the generated report
        """
        if output_dir is None:
            output_dir = Config.REPORT_OUTPUT_DIR
        
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{self.symbol}_forensic_analysis_{self.timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(self.data, f, indent=2, default=str)
        
        print(f"JSON report saved to: {filepath}")
        return filepath
    
    def generate_html_report(self, output_dir: str = None) -> str:
        """
        Generate HTML format report
        
        Args:
            output_dir: Output directory for the report
            
        Returns:
            Path to the generated report
        """
        if output_dir is None:
            output_dir = Config.REPORT_OUTPUT_DIR
        
        os.makedirs(output_dir, exist_ok=True)
        
        html_content = self._create_html_content()
        
        filename = f"{self.symbol}_forensic_analysis_{self.timestamp}.html"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(html_content)
        
        print(f"HTML report saved to: {filepath}")
        return filepath
    
    def _create_html_content(self) -> str:
        """
        Create HTML content for the report
        
        Returns:
            HTML string
        """
        template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stock Forensic Analysis - {{ symbol }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        
        h2 {
            color: #34495e;
            margin-top: 30px;
            margin-bottom: 15px;
            padding-left: 10px;
            border-left: 4px solid #3498db;
        }
        
        h3 {
            color: #555;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        
        .header-info {
            background: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        
        .risk-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 14px;
            margin-left: 10px;
        }
        
        .risk-high {
            background: #e74c3c;
            color: white;
        }
        
        .risk-medium {
            background: #f39c12;
            color: white;
        }
        
        .risk-low {
            background: #27ae60;
            color: white;
        }
        
        .risk-unknown {
            background: #95a5a6;
            color: white;
        }
        
        .metric-card {
            background: #f8f9fa;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid #3498db;
        }
        
        .metric-label {
            font-weight: bold;
            color: #555;
        }
        
        .metric-value {
            font-size: 18px;
            color: #2c3e50;
            margin-top: 5px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        th {
            background: #3498db;
            color: white;
            font-weight: bold;
        }
        
        tr:hover {
            background: #f5f5f5;
        }
        
        .red-flag {
            background: #ffe6e6;
            padding: 10px;
            margin: 5px 0;
            border-left: 4px solid #e74c3c;
            border-radius: 3px;
        }
        
        .news-item {
            background: #f8f9fa;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid #9b59b6;
        }
        
        .news-title {
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
        }
        
        .news-meta {
            font-size: 12px;
            color: #7f8c8d;
        }
        
        .summary-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        
        .summary-box h2 {
            color: white;
            border-left-color: white;
        }
        
        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #ecf0f1;
            text-align: center;
            color: #7f8c8d;
            font-size: 14px;
        }
        
        .component-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 15px 0;
        }
        
        .component-item {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
        }
        
        .component-name {
            font-size: 12px;
            color: #7f8c8d;
            margin-bottom: 5px;
        }
        
        .component-value {
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Stock Forensic Analysis Report</h1>
        
        <div class="header-info">
            <p><strong>Symbol:</strong> {{ symbol }}</p>
            <p><strong>Company:</strong> {{ company_name }}</p>
            <p><strong>Analysis Date:</strong> {{ analysis_date }}</p>
            <p><strong>Overall Risk Level:</strong> 
                <span class="risk-badge risk-{{ overall_risk_level|lower }}">{{ overall_risk_level }}</span>
            </p>
            <p><strong>Overall Risk Score:</strong> {{ overall_risk_score }} / 1.0</p>
        </div>
        
        <div class="summary-box">
            <h2>🎯 Executive Summary</h2>
            <p>{{ executive_summary }}</p>
        </div>
        
        <h2>📈 Stock Information</h2>
        <div class="component-grid">
            <div class="component-item">
                <div class="component-name">Current Price</div>
                <div class="component-value">${{ current_price }}</div>
            </div>
            <div class="component-item">
                <div class="component-name">Market Cap</div>
                <div class="component-value">{{ market_cap }}</div>
            </div>
            <div class="component-item">
                <div class="component-name">P/E Ratio</div>
                <div class="component-value">{{ pe_ratio }}</div>
            </div>
            <div class="component-item">
                <div class="component-name">Sector</div>
                <div class="component-value">{{ sector }}</div>
            </div>
        </div>
        
        <h2>🔍 Forensic Analysis</h2>
        
        <h3>Beneish M-Score (Earnings Manipulation Detection)</h3>
        <div class="metric-card">
            <div class="metric-label">M-Score</div>
            <div class="metric-value">{{ m_score }} 
                <span class="risk-badge risk-{{ m_score_risk|lower }}">{{ m_score_risk }}</span>
            </div>
            <p style="margin-top: 10px;">{{ m_score_interpretation }}</p>
        </div>
        
        {% if m_score_components %}
        <div class="component-grid">
            {% for key, value in m_score_components.items() %}
            <div class="component-item">
                <div class="component-name">{{ key }}</div>
                <div class="component-value">{{ value }}</div>
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        <h3>Altman Z-Score (Bankruptcy Prediction)</h3>
        <div class="metric-card">
            <div class="metric-label">Z-Score</div>
            <div class="metric-value">{{ z_score }} 
                <span class="risk-badge risk-{{ z_score_risk|lower }}">{{ z_score_risk }}</span>
            </div>
            <p style="margin-top: 10px;">{{ z_score_interpretation }}</p>
        </div>
        
        {% if z_score_components %}
        <div class="component-grid">
            {% for key, value in z_score_components.items() %}
            <div class="component-item">
                <div class="component-name">{{ key|replace('_', ' ')|title }}</div>
                <div class="component-value">{{ value }}</div>
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        <h2>🚩 Financial Red Flags</h2>
        {% if red_flags %}
            {% for flag in red_flags %}
            <div class="red-flag">
                <strong>{{ flag.category }}:</strong> {{ flag.flag }}
                <span class="risk-badge risk-{{ flag.severity|lower }}">{{ flag.severity }}</span>
                <br><small>Value: {{ flag.value }}</small>
            </div>
            {% endfor %}
        {% else %}
            <p>No significant red flags detected.</p>
        {% endif %}
        
        <h2>👥 Shareholding Analysis</h2>
        <div class="metric-card">
            <p><strong>Insider Ownership:</strong> {{ insider_ownership }}%</p>
            <p><strong>Institutional Ownership:</strong> {{ institutional_ownership }}%</p>
            <p><strong>Risk Level:</strong> 
                <span class="risk-badge risk-{{ shareholding_risk|lower }}">{{ shareholding_risk }}</span>
            </p>
            {% if shareholding_flags %}
            <div style="margin-top: 10px;">
                {% for flag in shareholding_flags %}
                <p style="color: #e74c3c;">⚠️ {{ flag }}</p>
                {% endfor %}
            </div>
            {% endif %}
        </div>
        
        <h2>📊 Price & Volume Patterns</h2>
        
        <h3>Volume Spikes</h3>
        <div class="metric-card">
            <p><strong>Spikes Detected:</strong> {{ volume_spikes_count }}</p>
            <p><strong>Risk Level:</strong> 
                <span class="risk-badge risk-{{ volume_risk|lower }}">{{ volume_risk }}</span>
            </p>
        </div>
        
        <h3>Price Anomalies</h3>
        <div class="metric-card">
            <p><strong>Anomalies Detected:</strong> {{ price_anomalies_count }}</p>
            <p><strong>Risk Level:</strong> 
                <span class="risk-badge risk-{{ price_anomaly_risk|lower }}">{{ price_anomaly_risk }}</span>
            </p>
        </div>
        
        <h3>Volatility Metrics</h3>
        <div class="metric-card">
            <p><strong>Annualized Volatility:</strong> {{ volatility }}%</p>
            <p><strong>Risk Level:</strong> 
                <span class="risk-badge risk-{{ volatility_risk|lower }}">{{ volatility_risk }}</span>
            </p>
        </div>
        
        <h2>📰 News Analysis</h2>
        
        <h3>Sentiment Analysis</h3>
        <div class="metric-card">
            <p><strong>Overall Sentiment:</strong> {{ news_sentiment }}</p>
            <p><strong>Sentiment Score:</strong> {{ news_sentiment_score }}</p>
            <p><strong>Articles Analyzed:</strong> {{ news_count }}</p>
        </div>
        
        <h3>Risk Signals in News</h3>
        <div class="metric-card">
            <p><strong>High Risk Signals:</strong> {{ high_risk_news_count }}</p>
            <p><strong>Medium Risk Signals:</strong> {{ medium_risk_news_count }}</p>
            <p><strong>News Risk Level:</strong> 
                <span class="risk-badge risk-{{ news_risk|lower }}">{{ news_risk }}</span>
            </p>
        </div>
        
        {% if critical_news %}
        <h3>Critical News Items</h3>
        {% for news in critical_news %}
        <div class="news-item">
            <div class="news-title">{{ news.title }}</div>
            <p>{{ news.description }}</p>
            <div class="news-meta">
                Keywords: {{ news.keywords|join(', ') }}
                {% if news.date %} | Date: {{ news.date }}{% endif %}
            </div>
        </div>
        {% endfor %}
        {% endif %}
        
        <h2>💡 Key Financial Ratios</h2>
        <table>
            <tr>
                <th>Ratio</th>
                <th>Value</th>
            </tr>
            {% for ratio_name, ratio_value in key_ratios.items() %}
            <tr>
                <td>{{ ratio_name|replace('_', ' ')|title }}</td>
                <td>{{ ratio_value }}</td>
            </tr>
            {% endfor %}
        </table>
        
        <div class="footer">
            <p>This report was generated using Stock Forensic Analysis Tool</p>
            <p>Report generated on {{ analysis_date }}</p>
            <p><strong>Disclaimer:</strong> This analysis is for informational purposes only and should not be considered as investment advice.</p>
        </div>
    </div>
</body>
</html>
        """
        
        # Prepare data for template
        stock_info = self.data.get('stock_info', {})
        forensic = self.data.get('forensic_analysis', {})
        patterns = self.data.get('pattern_analysis', {})
        news = self.data.get('news_analysis', {})
        
        # Format market cap
        market_cap = stock_info.get('market_cap', 0)
        if market_cap >= 1e9:
            market_cap_str = f"${market_cap/1e9:.2f}B"
        elif market_cap >= 1e6:
            market_cap_str = f"${market_cap/1e6:.2f}M"
        else:
            market_cap_str = f"${market_cap:,.0f}"
        
        # Generate executive summary
        executive_summary = self._generate_executive_summary()
        
        template_data = {
            'symbol': self.symbol,
            'company_name': stock_info.get('company_name', 'N/A'),
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'overall_risk_level': self.data.get('overall_risk_level', 'UNKNOWN'),
            'overall_risk_score': self.data.get('overall_risk_score', 0),
            'executive_summary': executive_summary,
            
            # Stock info
            'current_price': stock_info.get('current_price', 0),
            'market_cap': market_cap_str,
            'pe_ratio': stock_info.get('pe_ratio', 'N/A'),
            'sector': stock_info.get('sector', 'N/A'),
            
            # Forensic scores
            'm_score': forensic.get('beneish_m_score', {}).get('score', 'N/A'),
            'm_score_risk': forensic.get('beneish_m_score', {}).get('risk_level', 'UNKNOWN'),
            'm_score_interpretation': forensic.get('beneish_m_score', {}).get('interpretation', ''),
            'm_score_components': forensic.get('beneish_m_score', {}).get('components', {}),
            
            'z_score': forensic.get('altman_z_score', {}).get('score', 'N/A'),
            'z_score_risk': forensic.get('altman_z_score', {}).get('risk_level', 'UNKNOWN'),
            'z_score_interpretation': forensic.get('altman_z_score', {}).get('interpretation', ''),
            'z_score_components': forensic.get('altman_z_score', {}).get('components', {}),
            
            # Red flags
            'red_flags': forensic.get('financial_red_flags', {}).get('red_flags', []),
            
            # Shareholding
            'insider_ownership': forensic.get('promoter_pledge_analysis', {}).get('insider_ownership_percent', 0),
            'institutional_ownership': forensic.get('promoter_pledge_analysis', {}).get('institutional_ownership_percent', 0),
            'shareholding_risk': forensic.get('promoter_pledge_analysis', {}).get('risk_level', 'UNKNOWN'),
            'shareholding_flags': forensic.get('promoter_pledge_analysis', {}).get('red_flags', []),
            
            # Patterns
            'volume_spikes_count': patterns.get('volume_spikes', {}).get('spikes_detected', 0),
            'volume_risk': patterns.get('volume_spikes', {}).get('risk_level', 'UNKNOWN'),
            'price_anomalies_count': patterns.get('price_anomalies', {}).get('anomalies_detected', 0),
            'price_anomaly_risk': patterns.get('price_anomalies', {}).get('risk_level', 'UNKNOWN'),
            'volatility': patterns.get('volatility_metrics', {}).get('annualized_volatility', 0),
            'volatility_risk': patterns.get('volatility_metrics', {}).get('risk_level', 'UNKNOWN'),
            
            # News
            'news_sentiment': news.get('sentiment_analysis', {}).get('sentiment', 'NEUTRAL'),
            'news_sentiment_score': news.get('sentiment_analysis', {}).get('sentiment_score', 0),
            'news_count': news.get('total_articles_analyzed', 0),
            'high_risk_news_count': len(news.get('risk_signals', {}).get('high_risk', [])),
            'medium_risk_news_count': len(news.get('risk_signals', {}).get('medium_risk', [])),
            'news_risk': news.get('risk_signals', {}).get('risk_level', 'UNKNOWN'),
            'critical_news': news.get('critical_news', [])[:5],  # Top 5 critical news
            
            # Key ratios
            'key_ratios': self.data.get('key_ratios', {}),
        }
        
        # Render template
        tmpl = Template(template)
        return tmpl.render(**template_data)
    
    def _generate_executive_summary(self) -> str:
        """
        Generate executive summary based on analysis results
        
        Returns:
            Executive summary string
        """
        symbol = self.symbol
        overall_risk = self.data.get('overall_risk_level', 'UNKNOWN')
        
        forensic = self.data.get('forensic_analysis', {})
        m_score_risk = forensic.get('beneish_m_score', {}).get('risk_level', 'UNKNOWN')
        z_score_risk = forensic.get('altman_z_score', {}).get('risk_level', 'UNKNOWN')
        red_flags_count = forensic.get('financial_red_flags', {}).get('total_flags', 0)
        
        news = self.data.get('news_analysis', {})
        news_sentiment = news.get('sentiment_analysis', {}).get('sentiment', 'NEUTRAL')
        
        summary_parts = [
            f"Forensic analysis of {symbol} reveals an overall risk level of {overall_risk}."
        ]
        
        if m_score_risk == 'HIGH':
            summary_parts.append("The Beneish M-Score indicates potential earnings manipulation concerns.")
        
        if z_score_risk == 'HIGH':
            summary_parts.append("The Altman Z-Score suggests elevated bankruptcy risk.")
        
        if red_flags_count > 0:
            summary_parts.append(f"Analysis identified {red_flags_count} financial red flags requiring attention.")
        
        if news_sentiment == 'NEGATIVE':
            summary_parts.append("Recent news sentiment is predominantly negative, indicating market concerns.")
        elif news_sentiment == 'POSITIVE':
            summary_parts.append("Recent news sentiment is positive, reflecting favorable market perception.")
        
        return " ".join(summary_parts)
    
    def generate_summary_text(self) -> str:
        """
        Generate a text summary of the analysis
        
        Returns:
            Text summary string
        """
        lines = []
        lines.append("=" * 80)
        lines.append(f"STOCK FORENSIC ANALYSIS REPORT - {self.symbol}")
        lines.append("=" * 80)
        lines.append(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Overall Risk Level: {self.data.get('overall_risk_level', 'UNKNOWN')}")
        lines.append(f"Overall Risk Score: {self.data.get('overall_risk_score', 0):.2f}")
        lines.append("")
        
        # Forensic Analysis
        lines.append("FORENSIC ANALYSIS")
        lines.append("-" * 80)
        forensic = self.data.get('forensic_analysis', {})
        
        m_score = forensic.get('beneish_m_score', {})
        lines.append(f"Beneish M-Score: {m_score.get('score', 'N/A')} ({m_score.get('risk_level', 'UNKNOWN')})")
        
        z_score = forensic.get('altman_z_score', {})
        lines.append(f"Altman Z-Score: {z_score.get('score', 'N/A')} ({z_score.get('risk_level', 'UNKNOWN')})")
        
        red_flags = forensic.get('financial_red_flags', {})
        lines.append(f"Financial Red Flags: {red_flags.get('total_flags', 0)}")
        lines.append("")
        
        # News Analysis
        lines.append("NEWS ANALYSIS")
        lines.append("-" * 80)
        news = self.data.get('news_analysis', {})
        sentiment = news.get('sentiment_analysis', {})
        lines.append(f"Sentiment: {sentiment.get('sentiment', 'NEUTRAL')} (Score: {sentiment.get('sentiment_score', 0)})")
        lines.append(f"Articles Analyzed: {news.get('total_articles_analyzed', 0)}")
        
        risk_signals = news.get('risk_signals', {})
        lines.append(f"High Risk Signals: {len(risk_signals.get('high_risk', []))}")
        lines.append("")
        
        lines.append("=" * 80)
        
        return "\n".join(lines)
