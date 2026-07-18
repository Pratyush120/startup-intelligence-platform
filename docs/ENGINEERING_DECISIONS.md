# Engineering Decisions & Trade-offs

This document outlines the major technical decisions, rejected alternatives, and identified technical debt within SDIP.

## 1. Major Decisions & Rejected Alternatives

### Rejected: LangChain / LlamaIndex
**Why:** While popular, these frameworks introduce heavy abstraction layers that obscure prompt engineering (our core IP).
**Decision:** We built a custom `LLMAnalyzer` with a strict `Provider` interface. This keeps the codebase lightweight and guarantees we understand exactly what is sent to the LLM.

### Rejected: NoSQL (MongoDB)
**Why:** Intelligence data is highly relational. We need to aggregate funding events by company, calculate momentum scores, and map market snapshots. 
**Decision:** SQLite. We enforce strict schemas, foreign keys, and compound indices to enable rapid analytics queries that would be difficult to perform reliably in a schema-less NoSQL DB.

## 2. Performance Optimizations

*   **In-Memory API Caching:** Implemented `SimpleCache` (a TTL-based caching layer) in the Repository. This drops API latency from ~50ms to ~5ms for hot endpoints like `/market/snapshot` and `/companies`.
*   **Two-Pass Deduplication:** Before hitting expensive LLM APIs, the `Deduplicator` filters articles using an O(1) hash check, followed by an O(N) RapidFuzz similarity check.
*   **Pydantic Parsing:** We use Pydantic `model_validate` for instant parsing and validation of LLM outputs, failing fast if the LLM hallucinates an invalid schema.

## 3. Testing Strategy
*   **Mock-First CI/CD:** We achieve 74% test coverage without a single network call. `MockProvider` and `MockCollector` simulate real-world payloads.
*   **Dependency Injection:** `PipelineOrchestrator` is tested by injecting a `MockRepo` via `unittest.mock.patch`, preventing test database pollution.

## 4. Technical Debt & Future Improvements
*   **LLM Hallucinations:** Currently, if the LLM hallucinates a completely wrong schema, the pipeline logs an error and skips the article. *Improvement*: Implement an automatic retry mechanism with the LLM error fed back into the prompt.
*   **Single-Threaded Orchestrator:** The pipeline currently processes records sequentially. *Improvement*: Implement `asyncio.gather` for parallel LLM API calls.
*   **Frontend State Management:** We rely heavily on React Query. If the application grows to include real-time WebSockets, we will need a centralized store like Zustand.
