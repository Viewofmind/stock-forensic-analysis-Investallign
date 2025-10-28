# Quick Start: You.com Live News API

## 🚀 Get Started in 3 Steps

### Step 1: Get Your API Key

1. Visit https://documentation.you.com/
2. Contact **api@you.com** to request early access
3. You'll receive your API key via email

### Step 2: Configure Your Environment

Create or edit `.env` file in the project root:

```bash
YOU_API_KEY=your_actual_api_key_here
```

### Step 3: Test the Integration

```bash
python test_you_api.py
```

Expected output:
```
✓ API Key configured
✓ Successfully fetched articles
✓ ALL TESTS PASSED!
```

---

## 📊 Run Your First Analysis

```bash
python main.py AAPL
```

This will:
- Fetch financial data from Yahoo Finance
- Get live news from You.com Live News API
- Perform forensic analysis
- Generate HTML and JSON reports

---

## 🔍 What's Different?

### Old API (Generic Search)
```python
# Old endpoint
GET /search?query=Apple+stock&num_web_results=10
```

### New API (Live News)
```python
# New endpoint - specialized for news
GET /livenews?q=Apple+stock&count=20
```

### Better Results
- ✅ Real-time news articles
- ✅ Better structured data
- ✅ News-specific metadata (age, source, thumbnails)
- ✅ More relevant results

---

## 📖 Key Features

### 1. Stock News
```python
from src.data_fetcher import YouComNewsDataFetcher

fetcher = YouComNewsDataFetcher()
news = fetcher.get_stock_news("AAPL", "Apple Inc", num_results=20)
```

### 2. Financial Analysis
```python
analysis = fetcher.get_financial_analysis("TSLA", "Tesla")
```

### 3. Custom Search
```python
articles = fetcher.search_news("tech earnings report", num_results=15)
```

---

## 🎯 Response Structure

Each article includes:

```python
{
    'title': 'Article headline',
    'description': 'Article summary',
    'url': 'https://...',
    'published_date': '2025-10-28T10:30:00',
    'age': '2h',
    'source': 'Source Name',
    'source_hostname': 'example.com',
    'thumbnail_url': 'https://...',
    'article_id': 'unique-id',
    'type': 'news_result'
}
```

---

## ⚠️ Common Issues

### Issue: "API key not configured"
**Solution**: Add `YOU_API_KEY=your_key` to `.env` file

### Issue: "401 Unauthorized"
**Solution**: Check your API key is correct and active

### Issue: "429 Rate Limit"
**Solution**: Wait a moment before making more requests

### Issue: No results returned
**Solution**: Try a broader search query

---

## 📚 Documentation

- **Full Integration Guide**: `YOU_API_INTEGRATION.md`
- **Changelog**: `CHANGELOG_YOU_API.md`
- **Main README**: `README.md`
- **Official API Docs**: https://documentation.you.com/api-reference/news

---

## 💡 Pro Tips

1. **Request only what you need** (1-40 articles)
2. **Use specific queries** for better results
3. **Include company name** in stock searches
4. **Check for errors** in API responses
5. **Cache results** to reduce API calls

---

## 🧪 Testing Commands

```bash
# Test API integration
python test_you_api.py

# Test with example stocks
python example_usage.py

# Full analysis
python main.py AAPL
python main.py TSLA --period 2y
python main.py MSFT --json-only
```

---

## 📞 Support

- **You.com API**: api@you.com
- **Documentation**: https://documentation.you.com/
- **Discord**: Available via You.com docs

---

**Ready to analyze? Run `python main.py AAPL` to get started! 🚀**
