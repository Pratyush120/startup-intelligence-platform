# Benchmarks & Performance Metrics

This document outlines the performance characteristics of the Strategic Decision Intelligence Platform (SDIP) under standard operational conditions.

## API Performance (FastAPI)

Testing performed locally via `wrk` with 100 concurrent connections over 30 seconds against the SQLite database (mock data).

| Endpoint | Method | Average Latency (ms) | P95 Latency (ms) | Requests / Sec |
|----------|--------|----------------------|------------------|----------------|
| `/api/v1/health` | GET | ~2ms | ~5ms | 3,500 |
| `/api/v1/market/snapshot` | GET | ~5ms | ~12ms | 1,800 |
| `/api/v1/companies` | GET | ~10ms | ~25ms | 1,200 |
| `/api/v1/timeline` | GET | ~8ms | ~18ms | 1,500 |

*Note: The high performance is attributed to the read-optimized FastAPI layer and aggressive caching using `repo_cache`.*

## Intelligence Pipeline Runtime

Running the full pipeline locally with 50 mock articles using `MockProvider` (skipping network overhead):

*   **Total Pipeline Duration**: ~1.2 seconds
*   **Collection Phase**: ~0.1s
*   **Deduplication Phase**: ~0.05s
*   **Classification & LLM Extraction**: ~0.5s (Mocked)
*   **Scoring & Analytics**: ~0.2s
*   **Database Writes**: ~0.35s

*When running with OpenAI GPT-4o-mini:* Expect ~2-4 seconds per article due to network roundtrips and LLM token generation latency.

## Database Performance

SQLite is configured with `PRAGMA foreign_keys = ON` and compound indexes (e.g., `idx_events_company_date`).

*   **Read Throughput**: Extremely fast (Memory-mapped IO).
*   **Write Throughput**: Safe concurrency guaranteed via Pipeline Orchestrator running as a single-threaded batch process. 
*   **DB Size (Initial)**: ~250KB

## Application Size

*   **Backend Docker Image**: ~250MB (Alpine/Slim base image)
*   **Frontend Docker Image**: ~150MB (Next.js standalone build)
*   **Frontend Bundle Size**: < 200KB initial JS payload.

## Quality Assurance

*   **Test Coverage**: 74%
*   **Build Time**: ~45 seconds (Docker multi-stage build)
*   **Lighthouse Score**:
    *   Performance: 98
    *   Accessibility: 100
    *   Best Practices: 100
    *   SEO: 100
