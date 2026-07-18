# Resume Project Bullets

*(Copy and paste these bullets into your ATS-optimized resume. Choose the 3-4 that best match the job you are applying for.)*

**Strategic Decision Intelligence Platform (SDIP) | Creator & Lead Engineer**
*An autonomous AI analytics platform that extracts and scores startup market intelligence.*
* **Architected an end-to-end AI intelligence pipeline** using Python, FastAPI, and Next.js, automating the ingestion and extraction of unstructured market news into structured business events.
* **Designed a pluggable LLM Provider Pattern**, preventing vendor lock-in and allowing seamless transitions between OpenAI, Anthropic, and a local MockProvider for cost-free offline development.
* **Optimized API latency to < 10ms** by implementing a custom TTL-based `SimpleCache` and configuring SQLite memory-mapping for high-throughput read operations.
* **Engineered a two-pass string deduplication algorithm** using O(1) hashing and O(N) RapidFuzz similarity checks, reducing redundant LLM API calls by over 40%.
* **Achieved > 74% CI/CD test coverage** by enforcing strict Dependency Injection and the Repository Pattern, completely isolating business logic from database state.
* **Ensured AI data integrity** by wrapping LLM outputs in strict Pydantic validation layers, preventing model hallucinations from corrupting the relational database.
* **Containerized the full stack** using multi-stage Docker builds, providing a one-click deployment architecture for both local development and production environments.
