#!/usr/bin/env python3
"""
Test script for You.com News API integration
Tests the updated /livenews endpoint implementation
"""

from src.data_fetcher import YouComNewsDataFetcher
from config import Config
import json

def test_news_api():
    """Test the You.com News API with the updated implementation"""
    
    print("=" * 70)
    print("Testing You.com News API Integration")
    print("=" * 70)
    print()
    
    # Check if API key is configured
    if not Config.YOU_API_KEY:
        print("❌ ERROR: YOU_API_KEY not configured in .env file")
        print("Please add your You.com API key to the .env file:")
        print("YOU_API_KEY=your_api_key_here")
        return
    
    print(f"✓ API Key configured: {Config.YOU_API_KEY[:10]}...")
    print(f"✓ API Base URL: {Config.YOU_API_BASE_URL}")
    print(f"✓ News Endpoint: {Config.YOU_API_NEWS_ENDPOINT}")
    print()
    
    # Initialize the news fetcher
    news_fetcher = YouComNewsDataFetcher(Config.YOU_API_KEY)
    
    # Test 1: Search for general stock news
    print("-" * 70)
    print("TEST 1: Searching for Apple (AAPL) stock news")
    print("-" * 70)
    
    news_results = news_fetcher.search_news("AAPL Apple stock news financial", num_results=5)
    
    if news_results:
        print(f"✓ Successfully fetched {len(news_results)} news articles")
        print()
        
        for i, article in enumerate(news_results, 1):
            print(f"Article {i}:")
            print(f"  Title: {article.get('title', 'N/A')}")
            print(f"  Source: {article.get('source_name', 'N/A')}")
            print(f"  Age: {article.get('age', 'N/A')}")
            print(f"  Published: {article.get('page_age', 'N/A')}")
            print(f"  URL: {article.get('url', 'N/A')[:80]}...")
            print(f"  Description: {article.get('description', 'N/A')[:100]}...")
            print(f"  Thumbnail: {article.get('thumbnail_url', 'N/A')[:80]}...")
            print()
    else:
        print("❌ No news results returned")
        print("This could mean:")
        print("  1. Invalid API key")
        print("  2. API access not granted (News API requires early access)")
        print("  3. Network connectivity issues")
        print()
        print("Note: You.com News API is available to exclusive early access partners only.")
        print("Contact api@you.com to request access.")
    
    print()
    
    # Test 2: Get stock-specific news
    print("-" * 70)
    print("TEST 2: Getting stock-specific news for Tesla (TSLA)")
    print("-" * 70)
    
    stock_news = news_fetcher.get_stock_news("TSLA", "Tesla Inc", num_results=3)
    
    if stock_news:
        print(f"✓ Successfully fetched {len(stock_news)} stock news articles")
        print()
        
        for i, article in enumerate(stock_news, 1):
            print(f"Article {i}:")
            print(f"  Title: {article.get('title', 'N/A')}")
            print(f"  Source: {article.get('source_name', 'N/A')}")
            print(f"  Age: {article.get('age', 'N/A')}")
            print()
    else:
        print("❌ No stock news results returned")
    
    print()
    
    # Test 3: Get financial analysis
    print("-" * 70)
    print("TEST 3: Getting financial analysis for Microsoft (MSFT)")
    print("-" * 70)
    
    analysis = news_fetcher.get_financial_analysis("MSFT", "Microsoft Corporation")
    
    if analysis:
        print(f"✓ Successfully fetched {len(analysis)} financial analysis articles")
        print()
        
        for i, article in enumerate(analysis, 1):
            print(f"Article {i}:")
            print(f"  Title: {article.get('title', 'N/A')}")
            print(f"  Source: {article.get('source_name', 'N/A')}")
            print()
    else:
        print("❌ No financial analysis results returned")
    
    print()
    print("=" * 70)
    print("Testing completed!")
    print("=" * 70)

if __name__ == '__main__':
    test_news_api()
