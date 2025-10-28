# You.com Live News API Integration

## Overview

This document describes the integration of You.com's Live News API into the Stock Forensic Analysis Tool. The Live News API provides real-time news articles from across the web, which are used to analyze sentiment and detect risk signals for stock analysis.

## API Documentation

- **Official Documentation**: https://documentation.you.com/api-reference/news
- **Endpoint**: `GET https://api.ydc-index.io/livenews`
- **Authentication**: API Key via `X-API-Key` header
- **Early Access**: Currently available only to exclusive early access partners

## Getting an API Key

1. Visit https://documentation.you.com/
2. Contact api@you.com to request early access
3. Once approved, you'll receive your API key
4. Add it to your `.env` file:
   ```
   YOU_API_KEY=your_api_key_here
   ```

## API Specifications

### Request Parameters

| Parameter | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| `q` | string | Yes | - | Search query for news articles |
| `count` | integer | No | 1 ≤ x ≤ 40 | Maximum number of results (default: varies) |

### Request Headers

| Header | Value | Required |
|--------|-------|----------|
| `X-API-Key` | Your API key | Yes |

### Example Request

```bash
curl --request GET \
  --url 'https://api.ydc-index.io/livenews?q=Apple+stock+news&count=20' \
  --header 'X-API-Key: your_api_key_here'
```

### Response Structure

```json
{
  "news": {
    "query": {
      "original": "Apple stock news",
      "spellcheck_off": false
    },
    "results": [
      {
        "age": "2h",
        "description": "Article description...",
        "meta_url": {
          "hostname": "www.example.com",
          "netloc": "example.com",
          "path": "/article-path",
          "scheme": "https"
        },
        "page_age": "2025-10-28T10:30:00",
        "source_name": "Example News",
        "thumbnail": {
          "src": "https://example.com/image.jpg"
        },
        "title": "Article Title",
        "type": "news_result",
        "url": "https://example.com/article",
        "article_id": "unique-id"
      }
    ],
    "type": "news",
    "metadata": {
      "request_uuid": "uuid-here"
    }
  }
}
```

## Implementation Details

### Configuration (`config.py`)

```python
# You.com API Configuration
YOU_API_BASE_URL = "https://api.ydc-index.io"
YOU_API_LIVENEWS_ENDPOINT = "/livenews"
YOU_API_MAX_NEWS_COUNT = 40  # API limit: 1-40
```

### Data Fetcher (`src/data_fetcher.py`)

The `YouComNewsDataFetcher` class has been updated to use the Live News API:

#### Key Methods

1. **`search_news(query, num_results)`**
   - Searches for news articles using the Live News API
   - Validates count parameter (1-40)
   - Handles API errors (401, 429, etc.)
   - Returns structured news data

2. **`get_stock_news(symbol, company_name, num_results)`**
   - Fetches news specifically about a stock
   - Constructs optimized search queries
   - Default: 20 results

3. **`get_financial_analysis(symbol, company_name)`**
   - Fetches financial analysis articles
   - Focuses on earnings and analysis content
   - Default: 15 results

### Response Mapping

The API response is mapped to our internal structure:

| API Field | Internal Field | Description |
|-----------|----------------|-------------|
| `title` | `title` | Article headline |
| `description` | `description` | Article snippet |
| `url` | `url` | Full article URL |
| `page_age` | `published_date` | ISO 8601 timestamp |
| `age` | `age` | Relative age (e.g., "2h") |
| `source_name` | `source` | News source name |
| `meta_url.hostname` | `source_hostname` | Source domain |
| `thumbnail.src` | `thumbnail_url` | Thumbnail image URL |
| `article_id` | `article_id` | Unique article ID |
| `type` | `type` | Result type |

## Error Handling

The implementation includes comprehensive error handling:

### HTTP Status Codes

- **200 OK**: Success - articles returned
- **401 Unauthorized**: Invalid API key
- **429 Too Many Requests**: Rate limit exceeded
- **Other errors**: Network or server issues

### Error Messages

```python
# Invalid API key
"Error: Invalid API key. Please check your YOU_API_KEY in .env file."

# Rate limit
"Error: Rate limit exceeded. Please wait before making more requests."

# Timeout
"Error: Request timeout while fetching news from You.com API"

# Network error
"Error: Network error while fetching news: {error}"
```

## Usage Examples

### Basic Usage

```python
from src.data_fetcher import YouComNewsDataFetcher

# Initialize fetcher
fetcher = YouComNewsDataFetcher()

# Search for news
news = fetcher.search_news("Tesla stock", num_results=10)

# Get stock-specific news
stock_news = fetcher.get_stock_news("AAPL", "Apple Inc", num_results=20)

# Get financial analysis
analysis = fetcher.get_financial_analysis("MSFT", "Microsoft")
```

### With Data Aggregator

```python
from src.data_fetcher import DataAggregator

# Fetch all data including news
aggregator = DataAggregator("AAPL")
data = aggregator.fetch_all_data(period='1y')

# Access news data
news_articles = data['news']
financial_analysis = data['financial_analysis']
```

## Testing

Run the test script to verify the integration:

```bash
python test_you_api.py
```

The test script validates:
1. API key configuration
2. General news search
3. Stock-specific news fetching
4. Financial analysis retrieval
5. Response structure

## Rate Limiting

**Note**: The API documentation does not specify rate limits. To avoid issues:

- Implement reasonable delays between requests
- Cache results when possible
- Monitor for 429 status codes
- Contact You.com support for rate limit details

## Best Practices

1. **Query Optimization**
   - Use specific, relevant search terms
   - Include company name and ticker symbol
   - Focus queries on financial topics

2. **Result Count**
   - Request only needed articles (1-40)
   - Default to 20 for stock news
   - Use 15 for financial analysis

3. **Error Handling**
   - Always check for API key presence
   - Handle network timeouts gracefully
   - Provide informative error messages

4. **Data Processing**
   - Validate response structure
   - Handle missing fields gracefully
   - Parse dates correctly (ISO 8601)

## Troubleshooting

### No API Key Error

```
WARNING: YOU_API_KEY not set. News analysis will be limited.
```

**Solution**: Add your API key to `.env`:
```
YOU_API_KEY=your_actual_api_key
```

### 401 Unauthorized

**Causes**:
- Invalid API key
- Expired API key
- Missing API key

**Solution**: Verify your API key is correct and active

### 429 Rate Limit

**Causes**:
- Too many requests in short time
- Exceeded daily/hourly quota

**Solution**: 
- Wait before retrying
- Reduce request frequency
- Contact You.com for limit increase

### Empty Results

**Causes**:
- No matching articles found
- Query too specific
- API temporarily unavailable

**Solution**:
- Broaden search query
- Check API status
- Verify network connectivity

## Integration with Analysis Pipeline

The Live News API integrates seamlessly with the forensic analysis pipeline:

1. **Data Fetching** → News articles retrieved via Live News API
2. **News Analysis** → Sentiment and risk signal detection
3. **Pattern Detection** → Correlation with price/volume patterns
4. **Report Generation** → News insights included in reports

## Future Enhancements

Potential improvements for the integration:

1. **Caching**: Implement local caching to reduce API calls
2. **Filtering**: Add date range and source filtering
3. **Pagination**: Handle large result sets efficiently
4. **Sentiment Analysis**: Enhanced NLP for better sentiment detection
5. **Real-time Updates**: WebSocket support for live news feeds

## Support

For issues or questions:

- **You.com API Support**: api@you.com
- **Discord Community**: Available via You.com documentation
- **Project Issues**: Create an issue in the project repository

## References

- [You.com API Documentation](https://documentation.you.com/api-reference/news)
- [Live News API Reference](https://documentation.you.com/api-reference/news)
- [Get API Key](https://documentation.you.com/)

---

**Last Updated**: October 28, 2025
**API Version**: Live News API v1
**Integration Status**: ✓ Active
