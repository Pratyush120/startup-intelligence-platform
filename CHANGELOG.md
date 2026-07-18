# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-07-18
### Added
- **Core Engine**: Full Intelligence Pipeline (Extraction, Classification, LLM Analysis, Entity Resolution, Sparkline Generation).
- **Architecture**: Solidified Repository and Provider patterns for dependency injection.
- **API**: FastAPI implementation with production-ready endpoints (`/market/snapshot`, `/timeline`, `/search`, `/companies`).
- **UI**: Next.js React-Query frontend with dynamic dashboards and interactive market sentiment analysis.
- **Data Persistence**: SQLite schema with robust indexing, pipeline execution auditing, and snapshot histories.
- **Testing**: Reached > 74% coverage using Pytest.

### Fixed
- Fixed rate-limiting constraints by introducing robust offline Mock Collectors.
- Fixed database lock errors and concurrency bottlenecks via isolated repository instances.
- Re-architected `Deduplicator` to reduce dependency coupling.
