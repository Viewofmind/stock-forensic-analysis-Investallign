# Changelog: You.com Live News API Integration

## Date: October 28, 2025

## Summary

Updated the Stock Forensic Analysis Tool to use You.com's **Live News API** (`/livenews` endpoint) for fetching real-time news articles. This replaces the previous generic search endpoint with a specialized news-focused API that provides better structured data and more relevant results.

---

## Changes Made

### 1. Configuration Updates (`config.py`)

**Added:**
- `YOU_API_LIVENEWS_ENDPOINT = "/livenews"` - New Live News API endpoint
- `YOU_API_MAX_NEWS_COUNT = 40` - Maximum results per request (API constraint)

**Removed:**
- `YOU_API_SEARCH_ENDPOINT = "/search"` - Old generic search endpoint

### 2. Data Fetcher Updates (`src/data_fetcher.py`)

#### Class: `YouComNewsDataFetcher`

**Updated `__init__` method:**
- Added `self.livenews_endpoint` configuration
- Added `self.max_news_count` configuration
- Simplified headers (removed unnecessary `Content-Type`)

**Updated `search_news` method:**
- Changed endpoint from `/search` to `/livenews`
- Updated request parameters:
  - `query` → `q` (required by Live News API)
  - `num_web_results` → `count` (1-40 constraint)
- Enhanced response parsing for new structure:
  - Parse `news.results[]` array
  - Extract all Live News API fields
  - Map to internal data structure
- Improved error handling:
  - 401 Unauthorized (invalid API key)
  - 429 Too Many Requests (rate limiting)
  - Timeout handling
  - Network error handling
- Added success message with article count

**Updated `get_stock_news` method:**
- Increased default results from 10 to 20
- Optimized query construction for live news
- Added check for valid company name

**Updated `get_financial_analysis` method:**
- Increased default results from 5 to 15
- Optimized query for earnings and analysis content
- Added check for valid company name

### 3. Response Structure Mapping

**New fields from Live News API:**

| API Field | Internal Field | Type | Description |
|-----------|----------------|------|-------------|
| `title` | `title` | string | Article headline |
| `description` | `description` | string | Article snippet/summary |
| `url` | `url` | string | Full article URL |
| `page_age` | `published_date` | string | ISO 8601 timestamp |
| `age` | `age` | string | Relative age (e.g., "2h", "1d") |
| `source_name` | `source` | string | News source name |
| `meta_url.hostname` | `source_hostname` | string | Source domain |
| `thumbnail.src` | `thumbnail_url` | string | Thumbnail image URL |
| `article_id` | `article_id` | string | Unique article identifier |
| `type` | `type` | string | Result type (e.g., "news_result") |

### 4. New Files Created

#### `test_you_api.py`
- Comprehensive test script for Live News API integration
- Tests 4 scenarios:
  1. General news search
  2. Stock-specific news
  3. Financial analysis articles
  4. Response structure validation
- Provides detailed output and error messages

#### `YOU_API_INTEGRATION.md`
- Complete documentation for Live News API integration
- API specifications and examples
- Implementation details
- Usage examples
- Troubleshooting guide
- Best practices

#### `CHANGELOG_YOU_API.md`
- This file - detailed changelog of all modifications

### 5. Documentation Updates

#### `README.md`
- Updated data sources description
- Added Live News API reference
- Added link to detailed integration guide
- Added instructions for obtaining API key

---

## API Endpoint Comparison

### Before (Generic Search API)

```bash
GET https://api.ydc-index.io/search
Parameters:
  - query: string
  - num_web_results: integer
```

### After (Live News API)

```bash
GET https://api.ydc-index.io/livenews
Parameters:
  - q: string (required)
  - count: integer (1-40, optional)
```

---

## Benefits of Live News API

1. **Specialized for News**: Designed specifically for news articles, not general web search
2. **Better Structure**: Consistent response format with news-specific metadata
3. **Real-time Data**: Live news articles from across the web
4. **Rich Metadata**: Includes source, age, thumbnails, and article IDs
5. **Optimized Results**: Better relevance for news queries

---

## Breaking Changes

### None for End Users

The changes are internal to the data fetcher module. The public API remains the same:

```python
# This still works exactly the same way
fetcher = YouComNewsDataFetcher()
news = fetcher.get_stock_news("AAPL", "Apple Inc")
```

### For Developers

If you were directly using the `search_news` method:
- Response structure has changed (see mapping table above)
- New fields are available (age, source_hostname, thumbnail_url, etc.)
- Error handling is more comprehensive

---

## Testing

### Run the Test Suite

```bash
# Test the Live News API integration
python test_you_api.py
```

### Expected Output

```
======================================================================
Testing You.com Live News API Integration
======================================================================

✓ API Key configured: abc123xyz...
✓ API Base URL: https://api.ydc-index.io
✓ Live News Endpoint: /livenews

----------------------------------------------------------------------
TEST 1: Fetching general tech news
----------------------------------------------------------------------
✓ Successfully fetched 5 articles

----------------------------------------------------------------------
TEST 2: Fetching Apple (AAPL) stock news
----------------------------------------------------------------------
✓ Successfully fetched 10 stock news articles

----------------------------------------------------------------------
TEST 3: Fetching financial analysis for Tesla (TSLA)
----------------------------------------------------------------------
✓ Successfully fetched 15 financial analysis articles

----------------------------------------------------------------------
TEST 4: Validating response structure
----------------------------------------------------------------------
✓ All required fields present in response
✓ Additional Live News API fields: age, source_hostname, thumbnail_url

======================================================================
✓ ALL TESTS PASSED!
======================================================================
```

---

## Migration Guide

### For Existing Users

1. **Update your code** (if using git):
   ```bash
   git pull origin main
   ```

2. **No configuration changes needed** - your existing `.env` file works as-is

3. **Test the integration**:
   ```bash
   python test_you_api.py
   ```

4. **Run analysis as usual**:
   ```bash
   python main.py AAPL
   ```

### For New Users

Follow the standard installation process in `README.md`. The Live News API is now the default.

---

## Error Handling Improvements

### New Error Messages

1. **Invalid API Key (401)**
   ```
   Error: Invalid API key. Please check your YOU_API_KEY in .env file.
   ```

2. **Rate Limit (429)**
   ```
   Error: Rate limit exceeded. Please wait before making more requests.
   ```

3. **Timeout**
   ```
   Error: Request timeout while fetching news from You.com API
   ```

4. **Network Error**
   ```
   Error: Network error while fetching news: {details}
   ```

---

## Performance Considerations

### Request Limits

- **Maximum results per request**: 40 articles
- **Default for stock news**: 20 articles
- **Default for financial analysis**: 15 articles

### Optimization Tips

1. Request only the number of articles you need
2. Cache results when possible
3. Handle rate limits gracefully
4. Use specific search queries for better relevance

---

## Future Enhancements

Potential improvements for future versions:

1. **Caching Layer**: Reduce API calls by caching recent results
2. **Date Filtering**: Add support for date range queries
3. **Source Filtering**: Filter by specific news sources
4. **Pagination**: Handle large result sets more efficiently
5. **Real-time Streaming**: WebSocket support for live updates
6. **Advanced Sentiment**: ML-based sentiment analysis
7. **Entity Recognition**: Extract companies, people, and events

---

## Compatibility

- **Python Version**: 3.8+
- **Dependencies**: No new dependencies added
- **Backward Compatible**: Yes (internal changes only)
- **API Version**: Live News API v1

---

## Support and Resources

### Documentation
- **Live News API Docs**: https://documentation.you.com/api-reference/news
- **Integration Guide**: `YOU_API_INTEGRATION.md`
- **Main README**: `README.md`

### Getting Help
- **You.com API Support**: api@you.com
- **Discord Community**: Via You.com documentation
- **Project Issues**: GitHub repository

### Testing
- **Test Script**: `python test_you_api.py`
- **Example Usage**: `python example_usage.py`
- **Full Analysis**: `python main.py AAPL`

---

## Contributors

- Integration implemented: October 28, 2025
- Based on You.com Live News API documentation
- Tested with multiple stock symbols

---

## Notes

1. **Early Access**: The Live News API is currently in early access. Contact api@you.com for access.

2. **Rate Limits**: Not specified in documentation. Monitor for 429 responses and implement appropriate backoff.

3. **Data Quality**: Live News API provides high-quality, real-time news from reputable sources.

4. **Cost**: Check with You.com for pricing details and usage limits.

---

**Status**: ✅ Complete and Tested
**Version**: 1.1.0
**Last Updated**: October 28, 2025
