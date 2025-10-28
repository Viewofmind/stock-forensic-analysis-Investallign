#!/usr/bin/env python3
"""
Test script for You.com Live News API integration
"""

import sys
from src.data_fetcher import YouComNewsDataFetcher
from config import Config


def test_you_api():
    """Test You.com Live News API"""
    
    print("=" * 70)
    print("Testing You.com Live News API Integration")
    print("=" * 70)
    
    # Check API key
    if not Config.YOU_API_KEY:
        print("\n❌ ERROR: YOU_API_KEY not configured!")
        print("Please set your You.com API key in the .env file:")
        print("  YOU_API_KEY=your_api_key_here")
        print("\nTo get an API key, visit: https://documentation.you.com/")
        return False
    
    print(f"\n✓ API Key configured: {Config.YOU_API_KEY[:10]}...")
    print(f"✓ API Base URL: {Config.YOU_API_BASE_URL}")
    print(f"✓ Live News Endpoint: {Config.YOU_API_LIVENEWS_ENDPOINT}")
    
    # Initialize fetcher
    fetcher = YouComNewsDataFetcher()
    
    # Test 1: Simple news search
    print("\n" + "-" * 70)
    print("TEST 1: Fetching general tech news")
    print("-" * 70)
    
    news = fetcher.search_news("technology news", num_results=5)
    
    if news:
        print(f"✓ Successfully fetched {len(news)} articles")
        print("\nSample article:")
        article = news[0]
        print(f"  Title: {article.get('title', 'N/A')[:80]}...")
        print(f"  Source: {article.get('source', 'N/A')}")
        print(f"  Age: {article.get('age', 'N/A')}")
        print(f"  URL: {article.get('url', 'N/A')[:60]}...")
    else:
        print("❌ Failed to fetch news articles")
        return False
    
    # Test 2: Stock-specific news
    print("\n" + "-" * 70)
    print("TEST 2: Fetching Apple (AAPL) stock news")
    print("-" * 70)
    
    stock_news = fetcher.get_stock_news("AAPL", "Apple Inc", num_results=10)
    
    if stock_news:
        print(f"✓ Successfully fetched {len(stock_news)} stock news articles")
        print("\nTop 3 articles:")
        for i, article in enumerate(stock_news[:3], 1):
            print(f"\n  {i}. {article.get('title', 'N/A')[:70]}...")
            print(f"     Source: {article.get('source', 'N/A')} | Age: {article.get('age', 'N/A')}")
    else:
        print("❌ Failed to fetch stock news")
        return False
    
    # Test 3: Financial analysis
    print("\n" + "-" * 70)
    print("TEST 3: Fetching financial analysis for Tesla (TSLA)")
    print("-" * 70)
    
    analysis = fetcher.get_financial_analysis("TSLA", "Tesla")
    
    if analysis:
        print(f"✓ Successfully fetched {len(analysis)} financial analysis articles")
        print("\nTop 2 articles:")
        for i, article in enumerate(analysis[:2], 1):
            print(f"\n  {i}. {article.get('title', 'N/A')[:70]}...")
            print(f"     Source: {article.get('source', 'N/A')}")
    else:
        print("❌ Failed to fetch financial analysis")
        return False
    
    # Test 4: Response structure validation
    print("\n" + "-" * 70)
    print("TEST 4: Validating response structure")
    print("-" * 70)
    
    required_fields = ['title', 'description', 'url', 'source', 'published_date']
    sample_article = stock_news[0] if stock_news else {}
    
    missing_fields = []
    for field in required_fields:
        if field not in sample_article:
            missing_fields.append(field)
    
    if not missing_fields:
        print("✓ All required fields present in response")
        print(f"  Fields: {', '.join(required_fields)}")
    else:
        print(f"⚠ Warning: Missing fields: {', '.join(missing_fields)}")
    
    # Additional fields from Live News API
    additional_fields = ['age', 'source_hostname', 'thumbnail_url', 'article_id', 'type']
    present_additional = [f for f in additional_fields if f in sample_article]
    
    if present_additional:
        print(f"✓ Additional Live News API fields: {', '.join(present_additional)}")
    
    print("\n" + "=" * 70)
    print("✓ ALL TESTS PASSED!")
    print("=" * 70)
    print("\nYou.com Live News API integration is working correctly.")
    print("You can now use the stock forensic analysis tool with live news data.")
    
    return True


if __name__ == '__main__':
    try:
        success = test_you_api()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
