#!/usr/bin/env python3
"""
Simple test script for You.com News API integration
Tests the updated /livenews endpoint without requiring all dependencies
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_news_api_direct():
    """Test the You.com News API directly"""
    
    print("=" * 70)
    print("Testing You.com News API Integration (Direct)")
    print("=" * 70)
    print()
    
    # Get API key from environment
    api_key = os.getenv('YOU_API_KEY', '')
    
    if not api_key:
        print("❌ ERROR: YOU_API_KEY not configured in .env file")
        print("Please add your You.com API key to the .env file:")
        print("YOU_API_KEY=your_api_key_here")
        print()
        print("Note: You.com News API is available to exclusive early access partners only.")
        print("Contact api@you.com to request access.")
        return
    
    print(f"✓ API Key configured: {api_key[:20]}...{api_key[-10:]}")
    print()
    
    # API configuration
    base_url = "https://api.ydc-index.io"
    endpoint = f"{base_url}/livenews"
    
    headers = {
        'X-API-Key': api_key,
        'Content-Type': 'application/json'
    }
    
    # Test query
    query = "AAPL Apple stock news financial"
    
    print("-" * 70)
    print(f"TEST: Fetching news for query: '{query}'")
    print("-" * 70)
    print(f"Endpoint: {endpoint}")
    print(f"Parameters: q={query}, count=5")
    print()
    
    try:
        params = {
            'q': query,
            'count': 5
        }
        
        response = requests.get(
            endpoint,
            headers=headers,
            params=params,
            timeout=10
        )
        
        print(f"Response Status Code: {response.status_code}")
        print()
        
        if response.status_code == 200:
            data = response.json()
            
            # Check response structure
            if 'news' in data:
                print("✓ Response contains 'news' object")
                
                if 'results' in data['news']:
                    results = data['news']['results']
                    print(f"✓ Found {len(results)} news articles")
                    print()
                    
                    # Display first few articles
                    for i, article in enumerate(results[:3], 1):
                        print(f"Article {i}:")
                        print(f"  Title: {article.get('title', 'N/A')}")
                        print(f"  Source: {article.get('source_name', 'N/A')}")
                        print(f"  Age: {article.get('age', 'N/A')}")
                        print(f"  Published: {article.get('page_age', 'N/A')}")
                        print(f"  URL: {article.get('url', 'N/A')[:80]}...")
                        print(f"  Description: {article.get('description', 'N/A')[:100]}...")
                        print()
                    
                    print("✓ API integration successful!")
                else:
                    print("❌ No 'results' found in news object")
                    print(f"Available keys: {list(data['news'].keys())}")
            else:
                print("❌ No 'news' object in response")
                print(f"Response keys: {list(data.keys())}")
                print(f"Response: {data}")
        
        elif response.status_code == 401:
            print("❌ Authentication failed (401 Unauthorized)")
            print("Please check your API key is correct.")
            
        elif response.status_code == 403:
            print("❌ Access forbidden (403 Forbidden)")
            print("You.com News API requires early access partnership.")
            print("Contact api@you.com to request access.")
            
        else:
            print(f"❌ Request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
    
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print()
    print("=" * 70)
    print("Testing completed!")
    print("=" * 70)

if __name__ == '__main__':
    test_news_api_direct()
