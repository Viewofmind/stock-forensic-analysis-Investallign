# You.com News API - Quick Reference Guide

## 🚀 Quick Start

### API Endpoint
```
GET https://api.ydc-index.io/livenews
```

### Authentication
```bash
X-API-Key: ydc-sk-cbcc06d5aba62f1a-XrV8UuulJwSjyQ3QRB5rAbg1EHCvBETl-9ac89f3e
```

### Basic Request
```bash
curl --request GET \
  --url 'https://api.ydc-index.io/livenews?q=AAPL+stock+news&count=10' \
  --header 'X-API-Key: your-api-key-here'
```

## 📋 Parameters

| Parameter | Type | Required | Range | Example |
|-----------|------|----------|-------|---------|
| `q` | string | ✅ Yes | - | "AAPL stock news" |
| `count` | integer | ❌ No | 1-40 | 10 |

## 📦 Response Structure

```json
{
  "news": {
    "results": [
      {
        "title": "Article Title",
        "description": "Article description...",
        "url": "https://example.com/article",
        "age": "6h",
        "page_age": "2025-10-28T10:00:00",
        "source_name": "WSJ",
        "article_id": "unique-id",
        "thumbnail": {
          "src": "https://example.com/image.jpg"
        },
        "meta_url": {
          "hostname": "www.wsj.com",
          "netloc": "wsj.com",
          "scheme": "https"
        }
      }
    ]
  }
}
```

## 🐍 Python Usage

### Using the Updated Class

```python
from src.data_fetcher import YouComNewsDataFetcher

# Initialize
fetcher = YouComNewsDataFetcher(api_key="your-api-key")

# Search news
news = fetcher.search_news("AAPL Apple stock news", num_results=10)

# Access results
for article in news:
    print(f"{article['title']} - {article['source_name']} ({article['age']})")
```

### Direct API Call

```python
import requests

url = "https://api.ydc-index.io/livenews"
headers = {"X-API-Key": "your-api-key"}
params = {"q": "AAPL stock news", "count": 10}

response = requests.get(url, headers=headers, params=params)
data = response.json()

articles = data['news']['results']
```

## 🔑 Available Fields

### Article Fields
- `title` - Article headline
- `description` - Article summary
- `url` - Full article URL
- `age` - Human-readable age (e.g., "6h", "2d")
- `page_age` - ISO 8601 datetime
- `source_name` - News source (e.g., "WSJ", "Bloomberg")
- `article_id` - Unique identifier
- `type` - Article type (usually "news_result")

### Metadata Fields
- `thumbnail.src` - Thumbnail image URL
- `meta_url.hostname` - Source hostname
- `meta_url.netloc` - Network location
- `meta_url.scheme` - URL scheme (http/https)

## ⚠️ Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 200 | Success | ✅ Request successful |
| 401 | Unauthorized | Check API key |
| 403 | Forbidden | Request early access (api@you.com) |
| 429 | Rate Limited | Reduce request frequency |
| 500 | Server Error | Retry later |

## 🧪 Testing

### Test with cURL
```bash
curl -X GET "https://api.ydc-index.io/livenews?q=AAPL%20stock%20news&count=5" \
  -H "X-API-Key: your-api-key-here" \
  -H "Content-Type: application/json"
```

### Test with Python Script
```bash
python3 test_news_api_simple.py
```

## 💡 Best Practices

1. **Query Construction**: Be specific with queries
   - ✅ Good: "AAPL Apple stock earnings report Q3 2025"
   - ❌ Bad: "apple"

2. **Count Parameter**: Start with smaller counts
   - Use 5-10 for quick updates
   - Use 20-40 for comprehensive analysis

3. **Error Handling**: Always check response status
   ```python
   if response.status_code == 200:
       # Process data
   elif response.status_code == 403:
       # Request API access
   ```

4. **Rate Limiting**: Cache results when possible
   ```python
   # Cache news for 15 minutes
   cache_duration = 900  # seconds
   ```

## 🔄 Migration from Old API

### Old Code (Search API)
```python
endpoint = f"{base_url}/search"
params = {'query': query, 'num_web_results': 10}
results = data['hits']
```

### New Code (News API)
```python
endpoint = f"{base_url}/livenews"
params = {'q': query, 'count': 10}
results = data['news']['results']
```

## 📞 Support

- **Early Access**: api@you.com
- **Documentation**: https://documentation.you.com/api-reference/news
- **API Key**: Provided in your request (see above)

## ✅ Checklist

Before using the API:
- [ ] API key configured in `.env` file
- [ ] Updated to `/livenews` endpoint
- [ ] Using `q` parameter (not `query`)
- [ ] Using `count` parameter (not `num_web_results`)
- [ ] Parsing `news.results` (not `hits`)
- [ ] Error handling for 403 (early access required)

---

**Your API Key**: `ydc-sk-cbcc06d5aba62f1a-XrV8UuulJwSjyQ3QRB5rAbg1EHCvBETl-9ac89f3e`

**Note**: Store this securely in your `.env` file!
