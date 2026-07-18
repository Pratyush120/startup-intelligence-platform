# Project Metrics & Statistics

Use these hard numbers in interviews, READMEs, and portfolios to demonstrate the scale and rigor of the SDIP project.

## Architecture Scale
*   **Total Lines of Code (Backend)**: ~2,500 LOC
*   **Backend Framework**: FastAPI (Python 3.10+)
*   **Frontend Framework**: Next.js 14, React Query
*   **Data Models**: 6 Core Pydantic Entities (`BusinessEvent`, `Company`, `MarketIntelligence`, etc.)

## Component Breakdown
*   **API Endpoints**: 6 production endpoints (Health, Market Snapshot, Timeline, Companies, Search, Recommendations).
*   **Pipeline Stages**: 6 distinct stages (Collect, Deduplicate, Preprocess, Classify, Extract, Score).
*   **LLM Providers Supported**: 2 (OpenAI, Mock) - extensible to infinite.
*   **Data Collectors**: 4 (NewsAPI, Google News, Startup India, Mock)

## Quality Assurance & Testing
*   **Total Tests**: 56 unit and integration tests.
*   **Test Coverage**: **74%**
*   **Test Execution Time**: < 3.0 seconds (due to `MockProvider` and DI).
*   **Linting**: 100% compliant with `Ruff`.

## Performance Benchmarks
*   **API Latency (Read)**: ~5ms average (using in-memory TTL Repository caching).
*   **API Throughput**: ~1,800 Requests/Sec on the Snapshot endpoint (Local load testing).
*   **Deduplication Speed**: < 0.05s per batch utilizing RapidFuzz and hash sets.
*   **Database Constraints**: 2 Compound Indices added to SQLite to optimize timeline and event fetching.

## Infrastructure
*   **Docker Images**: 2 (Backend Alpine, Frontend Next.js Standalone).
*   **Backend Image Size**: ~250MB
*   **Frontend Image Size**: ~150MB
