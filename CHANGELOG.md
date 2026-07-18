# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-07-18

### Added
- **Core Engine**: Initial release of the intelligence pipeline and scoring system.
- **Collectors**: Integrated Crunchbase, LinkedIn, and Twitter/X data scrapers.
- **Frontend**: Shipped the Next.js dark-mode dashboard with Tailwind CSS.
- **AI Processing**: LLM-driven summarization for startup profiles.
- **Database**: Full support for PostgreSQL, Neo4j, and Qdrant vector search.
- **API**: Extensive FastAPI REST endpoints for data consumption.
- **CI/CD**: GitHub Actions workflow for linting, testing, and building.

### Changed
- Re-architected the Airflow DAG structure to support parallel data collection.
- Upgraded the frontend charting library to Recharts for smoother animations.
- Refactored the Neo4j schema for optimized knowledge graph queries.

### Fixed
- Fixed an issue where the Twitter collector would silently fail on rate limits.
- Resolved a memory leak in the Qdrant ingestion script.
- Patched a vulnerability in the JWT authentication middleware.

### Known Issues
- Rate limiting on third-party APIs can occasionally stall pipeline runs.
- WebSockets for real-time updates may drop connections behind certain reverse proxies.
