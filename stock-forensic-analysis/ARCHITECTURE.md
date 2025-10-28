# Architecture: You.com Live News API Integration

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Stock Forensic Analysis Tool                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
        ┌───────────────────┐  ┌──────────────────┐
        │  Yahoo Finance    │  │  You.com Live    │
        │      API          │  │    News API      │
        └───────────────────┘  └──────────────────┘
                    │                   │
                    │                   │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Data Aggregator │
                    └─────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
                ▼             ▼             ▼
        ┌──────────┐  ┌─────────────┐  ┌──────────┐
        │ Forensic │  │    News     │  │ Pattern  │
        │ Analyzer │  │  Analyzer   │  │ Detector │
        └──────────┘  └─────────────┘  └──────────┘
                │             │             │
                └─────────────┼─────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │     Report      │
                    │   Generator     │
                    └─────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
            ┌──────────┐        ┌──────────┐
            │   JSON   │        │   HTML   │
            │  Report  │        │  Report  │
            └──────────┘        └──────────┘
```

## Data Flow

### 1. User Request
```
User → main.py → DataAggregator
```

### 2. Data Fetching
```
DataAggregator
    ├─→ YahooFinanceDataFetcher
    │   ├─→ Stock Info
    │   ├─→ Historical Data
    │   ├─→ Financial Statements
    │   └─→ Key Ratios
    │
    └─→ YouComNewsDataFetcher (Live News API)
        ├─→ Stock News (20 articles)
        └─→ Financial Analysis (15 articles)
```

### 3. Analysis Pipeline
```
Raw Data
    │
    ├─→ ForensicAnalyzer
    │   ├─→ Beneish M-Score
    │   ├─→ Altman Z-Score
    │   └─→ Financial Red Flags
    │
    ├─→ NewsAnalyzer
    │   ├─→ Sentiment Analysis
    │   ├─→ Risk Signal Detection
    │   └─→ Critical News Identification
    │
    └─→ PatternDetector
        ├─→ Volume Spikes
        ├─→ Price Anomalies
        └─→ Volatility Metrics
```

### 4. Report Generation
```
Analysis Results
    │
    └─→ ReportGenerator
        ├─→ JSON Report (structured data)
        └─→ HTML Report (visual presentation)
```

## You.com Live News API Integration

### Request Flow

```
┌──────────────────────────────────────────────────────────────┐
│ 1. User initiates stock analysis                             │
│    python main.py AAPL                                        │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ 2. DataAggregator calls YouComNewsDataFetcher                │
│    - get_stock_news("AAPL", "Apple Inc", 20)                 │
│    - get_financial_analysis("AAPL", "Apple Inc")             │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ 3. YouComNewsDataFetcher constructs API request              │
│    GET https://api.ydc-index.io/livenews                     │
│    Headers: X-API-Key: {api_key}                             │
│    Params: q="Apple AAPL stock news", count=20               │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ 4. You.com Live News API processes request                   │
│    - Searches live news sources                              │
│    - Filters relevant articles                               │
│    - Returns structured JSON response                        │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ 5. Response parsing and mapping                              │
│    news.results[] → List[Dict]                               │
│    - title, description, url                                 │
│    - published_date, age, source                             │
│    - thumbnail_url, article_id                               │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ 6. NewsAnalyzer processes articles                           │
│    - Sentiment analysis                                      │
│    - Risk signal detection                                   │
│    - Critical news identification                            │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ 7. Results included in final report                          │
│    - News sentiment score                                    │
│    - Risk level from news                                    │
│    - Critical news items                                     │
└──────────────────────────────────────────────────────────────┘
```

## Component Details

### YouComNewsDataFetcher

```python
class YouComNewsDataFetcher:
    """Fetch news from You.com Live News API"""
    
    # Configuration
    base_url = "https://api.ydc-index.io"
    endpoint = "/livenews"
    max_count = 40
    
    # Methods
    ├─ search_news(query, count)
    │  └─ Core API interaction
    │
    ├─ get_stock_news(symbol, company, count=20)
    │  └─ Stock-specific news
    │
    └─ get_financial_analysis(symbol, company)
       └─ Financial analysis articles (count=15)
```

### API Request Structure

```
GET https://api.ydc-index.io/livenews
    ?q={query}
    &count={1-40}

Headers:
    X-API-Key: {your_api_key}
```

### API Response Structure

```json
{
  "news": {
    "query": {
      "original": "search query",
      "spellcheck_off": false
    },
    "results": [
      {
        "title": "string",
        "description": "string",
        "url": "string",
        "page_age": "ISO 8601 datetime",
        "age": "relative time",
        "source_name": "string",
        "meta_url": {
          "hostname": "string",
          "netloc": "string",
          "path": "string",
          "scheme": "string"
        },
        "thumbnail": {
          "src": "url"
        },
        "article_id": "string",
        "type": "news_result"
      }
    ],
    "type": "news",
    "metadata": {
      "request_uuid": "uuid"
    }
  }
}
```

## Error Handling Flow

```
API Request
    │
    ├─→ Success (200)
    │   └─→ Parse response → Return articles
    │
    ├─→ Unauthorized (401)
    │   └─→ Log error → Return empty list
    │
    ├─→ Rate Limit (429)
    │   └─→ Log warning → Return empty list
    │
    ├─→ Timeout
    │   └─→ Log timeout → Return empty list
    │
    └─→ Other Error
        └─→ Log error → Return empty list
```

## Configuration Hierarchy

```
Environment Variables (.env)
    │
    ├─→ YOU_API_KEY
    │
    └─→ REPORT_OUTPUT_DIR
            │
            ▼
        Config Class (config.py)
            │
            ├─→ YOU_API_BASE_URL
            ├─→ YOU_API_LIVENEWS_ENDPOINT
            ├─→ YOU_API_MAX_NEWS_COUNT
            │
            └─→ Risk Thresholds
                    │
                    ▼
            Application Components
                    │
                    ├─→ DataAggregator
                    ├─→ ForensicAnalyzer
                    ├─→ NewsAnalyzer
                    └─→ PatternDetector
```

## Module Dependencies

```
main.py
    │
    ├─→ config.py
    │   └─→ python-dotenv
    │
    └─→ src/
        │
        ├─→ data_fetcher.py
        │   ├─→ yfinance
        │   ├─→ requests
        │   ├─→ pandas
        │   └─→ config.py
        │
        ├─→ forensic_analyzer.py
        │   ├─→ pandas
        │   ├─→ numpy
        │   └─→ src/utils.py
        │
        ├─→ news_analyzer.py
        │   └─→ (standard library)
        │
        ├─→ pattern_detector.py
        │   ├─→ pandas
        │   ├─→ numpy
        │   └─→ src/utils.py
        │
        ├─→ report_generator.py
        │   ├─→ json
        │   ├─→ jinja2
        │   └─→ config.py
        │
        └─→ utils.py
            ├─→ pandas
            └─→ numpy
```

## API Integration Points

### 1. Initialization
```python
fetcher = YouComNewsDataFetcher(api_key)
# Loads config, sets up headers
```

### 2. Stock News Request
```python
news = fetcher.get_stock_news("AAPL", "Apple Inc", 20)
# Constructs query: "Apple Inc AAPL stock news"
# Calls Live News API with count=20
```

### 3. Financial Analysis Request
```python
analysis = fetcher.get_financial_analysis("AAPL", "Apple Inc")
# Constructs query: "Apple Inc AAPL earnings financial analysis"
# Calls Live News API with count=15
```

### 4. Response Processing
```python
# Parse news.results[] array
# Map fields to internal structure
# Return List[Dict] with article data
```

## Performance Characteristics

### Request Timing
```
API Request:     ~500-2000ms
Response Parse:  ~10-50ms
Total per call:  ~510-2050ms
```

### Data Volume
```
Stock News:      20 articles × ~2KB = ~40KB
Financial News:  15 articles × ~2KB = ~30KB
Total per stock: ~70KB
```

### Caching Strategy
```
Current:  No caching (always fresh data)
Future:   Consider caching with TTL
```

## Security Considerations

### API Key Protection
```
.env file (not committed)
    │
    └─→ Config.YOU_API_KEY
            │
            └─→ YouComNewsDataFetcher
                    │
                    └─→ X-API-Key header
```

### Data Validation
```
API Response
    │
    ├─→ Check status code
    ├─→ Validate JSON structure
    ├─→ Verify required fields
    └─→ Sanitize output
```

## Monitoring and Logging

### Success Logging
```python
print(f"✓ Fetched {len(news_results)} news articles from You.com Live News API")
```

### Error Logging
```python
print(f"Error: Invalid API key. Please check your YOU_API_KEY in .env file.")
print(f"Error: Rate limit exceeded. Please wait before making more requests.")
print(f"Error: Request timeout while fetching news from You.com API")
```

## Testing Strategy

### Unit Tests
```
test_you_api.py
    │
    ├─→ Test 1: General news search
    ├─→ Test 2: Stock-specific news
    ├─→ Test 3: Financial analysis
    └─→ Test 4: Response structure
```

### Integration Tests
```
example_usage.py
    │
    └─→ Full analysis pipeline with real API calls
```

### Manual Testing
```bash
python test_you_api.py      # API integration test
python main.py AAPL         # Full analysis test
```

## Deployment Considerations

### Environment Setup
1. Python 3.8+ required
2. Install dependencies: `pip install -r requirements.txt`
3. Configure `.env` with API key
4. Verify with `python test_you_api.py`

### Production Checklist
- ✅ API key configured
- ✅ Dependencies installed
- ✅ Tests passing
- ✅ Error handling in place
- ✅ Logging configured
- ✅ Documentation complete

---

**Architecture Version**: 1.1.0
**Last Updated**: October 28, 2025
**Integration Status**: ✅ Production Ready
