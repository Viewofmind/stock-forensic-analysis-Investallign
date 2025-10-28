"""
News analysis module for detecting risk signals in news articles
"""
import re
from typing import Dict, List, Any
from datetime import datetime
from collections import Counter


class NewsAnalyzer:
    """Analyze news articles for risk signals and sentiment"""
    
    # Risk keywords categorized by severity
    HIGH_RISK_KEYWORDS = [
        'fraud', 'scandal', 'investigation', 'lawsuit', 'bankruptcy', 'default',
        'criminal', 'sec investigation', 'accounting irregularities', 'restatement',
        'insider trading', 'manipulation', 'ponzi', 'embezzlement', 'corruption',
        'class action', 'delisting', 'going concern', 'chapter 11', 'insolvent'
    ]
    
    MEDIUM_RISK_KEYWORDS = [
        'warning', 'concern', 'decline', 'loss', 'layoff', 'restructuring',
        'downgrade', 'miss', 'disappointing', 'weak', 'struggle', 'challenge',
        'regulatory', 'compliance', 'violation', 'fine', 'penalty', 'dispute',
        'recall', 'controversy', 'criticism', 'probe', 'audit'
    ]
    
    LOW_RISK_KEYWORDS = [
        'caution', 'uncertainty', 'volatility', 'pressure', 'slowdown',
        'competition', 'headwind', 'risk', 'concern', 'question'
    ]
    
    POSITIVE_KEYWORDS = [
        'growth', 'profit', 'beat', 'exceed', 'strong', 'positive', 'upgrade',
        'expansion', 'innovation', 'success', 'record', 'breakthrough',
        'acquisition', 'partnership', 'award', 'leadership', 'momentum'
    ]
    
    def __init__(self, news_data: List[Dict[str, Any]]):
        """
        Initialize the news analyzer
        
        Args:
            news_data: List of news articles
        """
        self.news_data = news_data
    
    def analyze_sentiment(self) -> Dict[str, Any]:
        """
        Analyze overall sentiment from news articles
        
        Returns:
            Dictionary with sentiment analysis
        """
        if not self.news_data:
            return {
                'sentiment_score': 0.0,
                'sentiment': 'NEUTRAL',
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'total_articles': 0
            }
        
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        for article in self.news_data:
            text = f"{article.get('title', '')} {article.get('description', '')}".lower()
            
            # Count keyword matches
            high_risk_matches = sum(1 for keyword in self.HIGH_RISK_KEYWORDS if keyword in text)
            medium_risk_matches = sum(1 for keyword in self.MEDIUM_RISK_KEYWORDS if keyword in text)
            low_risk_matches = sum(1 for keyword in self.LOW_RISK_KEYWORDS if keyword in text)
            positive_matches = sum(1 for keyword in self.POSITIVE_KEYWORDS if keyword in text)
            
            # Calculate article sentiment
            negative_score = high_risk_matches * 3 + medium_risk_matches * 2 + low_risk_matches
            positive_score = positive_matches * 2
            
            if negative_score > positive_score:
                negative_count += 1
            elif positive_score > negative_score:
                positive_count += 1
            else:
                neutral_count += 1
        
        total = len(self.news_data)
        
        # Calculate overall sentiment score (-1 to 1)
        sentiment_score = (positive_count - negative_count) / total if total > 0 else 0
        
        # Determine sentiment category
        if sentiment_score > 0.3:
            sentiment = 'POSITIVE'
        elif sentiment_score < -0.3:
            sentiment = 'NEGATIVE'
        else:
            sentiment = 'NEUTRAL'
        
        return {
            'sentiment_score': round(sentiment_score, 2),
            'sentiment': sentiment,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'total_articles': total
        }
    
    def detect_risk_signals(self) -> Dict[str, Any]:
        """
        Detect risk signals in news articles
        
        Returns:
            Dictionary with detected risk signals
        """
        risk_signals = {
            'high_risk': [],
            'medium_risk': [],
            'low_risk': [],
            'risk_score': 0.0,
            'risk_level': 'LOW'
        }
        
        if not self.news_data:
            return risk_signals
        
        high_risk_count = 0
        medium_risk_count = 0
        low_risk_count = 0
        
        for article in self.news_data:
            title = article.get('title', '')
            description = article.get('description', '')
            text = f"{title} {description}".lower()
            url = article.get('url', '')
            published_date = article.get('published_date', '')
            
            # Check for high-risk keywords
            high_risk_found = []
            for keyword in self.HIGH_RISK_KEYWORDS:
                if keyword in text:
                    high_risk_found.append(keyword)
            
            if high_risk_found:
                risk_signals['high_risk'].append({
                    'title': title,
                    'keywords': high_risk_found,
                    'url': url,
                    'date': published_date
                })
                high_risk_count += len(high_risk_found)
            
            # Check for medium-risk keywords
            medium_risk_found = []
            for keyword in self.MEDIUM_RISK_KEYWORDS:
                if keyword in text:
                    medium_risk_found.append(keyword)
            
            if medium_risk_found and not high_risk_found:
                risk_signals['medium_risk'].append({
                    'title': title,
                    'keywords': medium_risk_found,
                    'url': url,
                    'date': published_date
                })
                medium_risk_count += len(medium_risk_found)
            
            # Check for low-risk keywords
            low_risk_found = []
            for keyword in self.LOW_RISK_KEYWORDS:
                if keyword in text:
                    low_risk_found.append(keyword)
            
            if low_risk_found and not high_risk_found and not medium_risk_found:
                risk_signals['low_risk'].append({
                    'title': title,
                    'keywords': low_risk_found,
                    'url': url,
                    'date': published_date
                })
                low_risk_count += len(low_risk_found)
        
        # Calculate risk score (0 to 1)
        total_articles = len(self.news_data)
        risk_score = (
            (high_risk_count * 0.5 + medium_risk_count * 0.3 + low_risk_count * 0.1) / 
            max(total_articles, 1)
        )
        risk_score = min(risk_score, 1.0)
        
        risk_signals['risk_score'] = round(risk_score, 2)
        
        # Determine risk level
        if risk_score > 0.6 or len(risk_signals['high_risk']) > 0:
            risk_signals['risk_level'] = 'HIGH'
        elif risk_score > 0.3 or len(risk_signals['medium_risk']) > 2:
            risk_signals['risk_level'] = 'MEDIUM'
        else:
            risk_signals['risk_level'] = 'LOW'
        
        return risk_signals
    
    def extract_key_topics(self, top_n: int = 5) -> List[Dict[str, Any]]:
        """
        Extract key topics from news articles
        
        Args:
            top_n: Number of top topics to return
            
        Returns:
            List of key topics with frequency
        """
        if not self.news_data:
            return []
        
        # Combine all text
        all_text = ' '.join([
            f"{article.get('title', '')} {article.get('description', '')}"
            for article in self.news_data
        ]).lower()
        
        # Remove common words and extract meaningful terms
        words = re.findall(r'\b[a-z]{4,}\b', all_text)
        
        # Common stop words to exclude
        stop_words = {
            'that', 'this', 'with', 'from', 'have', 'been', 'will', 'their',
            'about', 'which', 'were', 'said', 'what', 'when', 'where', 'more',
            'than', 'other', 'some', 'into', 'could', 'would', 'should', 'also'
        }
        
        # Filter out stop words
        filtered_words = [word for word in words if word not in stop_words]
        
        # Count word frequency
        word_counts = Counter(filtered_words)
        
        # Get top topics
        top_topics = [
            {'topic': word, 'frequency': count}
            for word, count in word_counts.most_common(top_n)
        ]
        
        return top_topics
    
    def summarize_news(self) -> Dict[str, Any]:
        """
        Generate a summary of news analysis
        
        Returns:
            Dictionary with news summary
        """
        sentiment = self.analyze_sentiment()
        risk_signals = self.detect_risk_signals()
        key_topics = self.extract_key_topics()
        
        # Get recent headlines
        recent_headlines = [
            {
                'title': article.get('title', ''),
                'date': article.get('published_date', ''),
                'url': article.get('url', '')
            }
            for article in self.news_data[:5]
        ]
        
        return {
            'total_articles_analyzed': len(self.news_data),
            'sentiment_analysis': sentiment,
            'risk_signals': risk_signals,
            'key_topics': key_topics,
            'recent_headlines': recent_headlines,
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def get_critical_news(self) -> List[Dict[str, Any]]:
        """
        Get news articles with critical risk signals
        
        Returns:
            List of critical news articles
        """
        critical_news = []
        
        for article in self.news_data:
            text = f"{article.get('title', '')} {article.get('description', '')}".lower()
            
            # Check for high-risk keywords
            critical_keywords = []
            for keyword in self.HIGH_RISK_KEYWORDS:
                if keyword in text:
                    critical_keywords.append(keyword)
            
            if critical_keywords:
                critical_news.append({
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'url': article.get('url', ''),
                    'published_date': article.get('published_date', ''),
                    'critical_keywords': critical_keywords,
                    'severity': 'HIGH'
                })
        
        return critical_news
