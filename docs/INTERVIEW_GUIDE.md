# Interview Preparation Guide

This guide provides suggested answers to common technical and behavioral questions an interviewer might ask after reviewing the SDIP repository.

## 1. System Design & Architecture

**Q: Can you draw the architecture of SDIP?**
*A:* "At the perimeter, we have cron-triggered Collectors fetching RSS/API feeds. These feed into a Preprocessor & Deduplicator. Clean records hit the Intelligence Engine, which orchestrates the LLM Analyzer (via a Provider interface) to classify and extract events. Those events are scored by the Analytics Engine and persisted via a Repository pattern to SQLite. The frontend is a Next.js React-Query app consuming a FastAPI JSON backend."

**Q: Why SQLite instead of PostgreSQL?**
*A:* "For v1.0, the goal was portability and a zero-configuration developer experience. Since this is an analytical read-heavy application, SQLite with compound indexing and memory-mapping is incredibly fast. The only downside is concurrent write locks, which we avoided by making the Pipeline Orchestrator a single-threaded batch process."

## 2. Backend & FastAPI

**Q: Why use Dependency Injection in FastAPI?**
*A:* "FastAPI's `Depends()` allowed me to inject the `Repository` and configuration dynamically into the route handlers. This decoupling made it trivial to write unit tests for the API endpoints by injecting a `MockRepo`, meaning my API tests run in milliseconds without hitting a database."

**Q: How do you handle errors in the pipeline?**
*A:* "The Pipeline Orchestrator uses a robust try-catch loop. If a collector fails, it falls back to the next available collector. If an LLM call fails due to rate limits, it logs the error, increments an error counter, and continues to the next article. This guarantees the pipeline never crashes mid-run."

## 3. LLMs & AI Integration

**Q: How do you prevent the LLM from returning invalid JSON?**
*A:* "First, I use aggressive prompt engineering, explicitly providing the required JSON schema in the system prompt. Second, I use the `response_format={ "type": "json_object" }` flag for OpenAI. Finally, the response is parsed through a Pydantic model (`BusinessEvent`). If it fails validation, the error is caught and logged."

## 4. Behavioral Questions

**Q: Tell me about a time you had to make a technical trade-off.**
*A:* "I had to choose between using LangChain or building a custom LLM provider interface. LangChain would have been faster to implement initially, but it obscured the prompts and added a massive dependency. I chose to build a custom `BaseProvider` and `OpenAIProvider`. It took a little longer upfront, but it resulted in a vastly lighter codebase and gave me total control over the exact prompt engineering."
