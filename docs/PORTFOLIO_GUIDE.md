# Portfolio Presentation Guide

Use this guide to effectively present the SDIP project on your resume, LinkedIn, and during engineering interviews.

## 1. Resume Bullet Points

*   **Architected and deployed an AI-driven Startup Intelligence Platform** using FastAPI, Next.js, and OpenAI, capable of autonomously ingesting, classifying, and scoring thousands of market events.
*   **Designed a modular LLM Provider pattern** to prevent vendor lock-in, enabling seamless switching between OpenAI, Anthropic, and local mock models for cost-effective development.
*   **Optimized data ingestion pipeline** using a custom two-pass RapidFuzz deduplicator and in-memory TTL caching, reducing API latency to < 10ms.
*   **Enforced strict architectural boundaries** (Repository Pattern, Dependency Injection) resulting in a highly decoupled system with > 74% test coverage in CI/CD.

## 2. 30-Second Elevator Pitch
"I built an open-source AI platform that acts like a junior strategy analyst. Instead of manually reading TechCrunch, the system automatically scrapes news, uses an LLM to extract business events like funding rounds or layoffs, scores their impact, and aggregates them into a unified market dashboard using FastAPI and Next.js. I built it with strict dependency injection so you can run the whole pipeline offline with zero API keys."

## 3. Interview Walkthrough (5-Minute Technical Demo)

1.  **Start at the UI**: Show the Dashboard. Point out the Market Snapshot and the Top Companies list. Explain that this data is generated entirely by AI.
2.  **Show the Backend Pipeline**: Open `orchestrator.py`. Explain the 5-step pipeline: Collect -> Deduplicate -> Classify -> Extract -> Score.
3.  **Explain the Provider Pattern**: Open `llm_analyzer.py`. Show how `BaseProvider` guarantees that the business logic never knows whether it's talking to OpenAI or a mock.
4.  **Show the Tests**: Run `pytest tests/ --cov=src`. Show how the entire pipeline runs in 2 seconds because of the mock architecture.

## 4. Expected Recruiter/Hiring Manager Questions

**Q: Why didn't you use LangChain?**
**A:** "I evaluated LangChain, but for this specific use case—extracting structured JSON from unstructured text—it added unnecessary abstraction. By writing the prompts and using Pydantic directly, I retained full control over the AI's output, optimized token usage, and kept the dependency tree extremely light."

**Q: How does it scale?**
**A:** "Currently, it uses SQLite and a synchronous orchestrator for simplicity. To scale, I would replace the SQLite Repository with PostgreSQL, and move the Orchestrator loop into an asynchronous Celery worker queue to process articles in parallel."

**Q: What was the hardest bug you fixed?**
**A:** "When running parallel tests, SQLite threw 'database is locked' errors. I realized the global `Repository` was sharing state across tests. I fixed this by implementing proper Dependency Injection and patching the Repository during pipeline tests."
