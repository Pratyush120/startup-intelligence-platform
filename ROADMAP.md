# Strategic Decision Intelligence Platform (SDIP) - Roadmap

## Phase 1: Core Intelligence Engine (Complete ✅)
- Data extraction framework (Collectors)
- LLM Provider Abstraction
- Article Classification & Scoring
- Repository Pattern implementation

## Phase 2: Production Readiness (Complete ✅)
- FastAPI Integration
- Docker & Docker Compose setup
- Performance optimizations and caching
- CI/CD setup, Test Coverage > 70%

## Phase 3: Advanced Intelligence (Target: Q4)
- **Graph Database Integration**: Migrate from SQLite to Neo4j to map complex entity relationships (investors, founders, subsidiaries).
- **Real-time Event Streaming**: Introduce Apache Kafka for streaming data ingestion.
- **Multi-modal LLM Support**: Analyze startup pitch decks and video transcripts using Gemini and GPT-4 Vision.

## Phase 4: Enterprise Scale (Target: Next Year)
- **SaaS Multi-Tenancy**: Allow different analyst teams to maintain separate intelligence contexts.
- **Custom Taxonomies**: Allow users to train custom classifiers for specific niche markets (e.g., SpaceTech).
- **Kubernetes Native**: Fully managed Helm charts for cloud-agnostic deployment.
