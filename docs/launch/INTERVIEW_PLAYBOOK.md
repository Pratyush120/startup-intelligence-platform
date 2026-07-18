# Interview Playbook: SDIP

Review this document 24 hours before a technical interview. It maps the engineering decisions in SDIP directly to standard FAANG interview signals (Architecture, Trade-offs, Testing, Behavioral).

## 1. System Design & Architecture

**The "Why" Behind the Patterns**
*   **Repository Pattern**: You didn't just write SQL queries in your routes. You built a `Repository` class. *Why?* To decouple the data persistence from the business logic. It allows you to mock the database entirely for unit testing and makes it trivial to swap SQLite for PostgreSQL later.
*   **Provider Pattern**: You didn't hardcode the `openai` SDK. You built an abstract `BaseProvider`. *Why?* To avoid vendor lock-in. AI moves fast; tomorrow Claude 4 might be better. By injecting the provider, changing the LLM is a one-line config change. It also enabled `MockProvider`, dropping API costs to $0 for local development.

## 2. Dealing with AI Unreliability (The Pydantic Shield)

**Interview Question**: *"LLMs hallucinate and return bad JSON. How did you handle that?"*
**Your Answer**: "Defense in depth. First, aggressive system prompts explicitly demanding JSON. Second, using OpenAI's `response_format` flag. But most importantly, the backend enforces a strict Pydantic model (`BusinessEvent`). If the LLM returns bad data, Pydantic throws a `ValidationError`. My pipeline catches this, logs the hallucination, and safely skips the article rather than corrupting the SQLite database."

## 3. Scaling & Trade-offs (The "What would you change?" Question)

**Interview Question**: *"If this got 100,000 users tomorrow, what breaks first?"*
**Your Answer**: 
1.  **The Database**: SQLite will hit concurrent write locks (`database is locked`). I would migrate the `Repository` implementation to PostgreSQL.
2.  **The Orchestrator**: Currently, it processes articles synchronously in a loop. I would decouple the ingestion from the LLM processing using a message queue like Celery or RabbitMQ, allowing horizontal scaling of the LLM worker nodes.
3.  **The Frontend**: The Next.js app fetches the whole snapshot. For millions of records, I'd need to implement pagination and server-side filtering on the FastAPI layer.

## 4. Behavioral Stories (STAR Format)

**Situation**: High LLM API costs and slow development loops.
**Task**: I needed a way to test the pipeline continuously without spending $5 a day on OpenAI tokens or waiting 30 seconds for test runs.
**Action**: I refactored the intelligence engine to use Dependency Injection. I created a `MockProvider` that returns deterministic, pre-written JSON responses instantly.
**Result**: Test coverage jumped to 74%, API costs dropped to zero during development, and the entire CI/CD test suite now executes in under 2 seconds.

## 5. Explaining the Deduplication Algorithm

**Interview Question**: *"How do you prevent processing the same news twice?"*
**Your Answer**: "A two-pass approach to save money. 
Pass 1 (O(1)): Hashing. I take the URL, hash it, and check it against the DB. If it exists, drop it.
Pass 2 (O(N)): Semantic overlap. If a different news outlet publishes the exact same story, the URL hash is different. So, I use RapidFuzz to do a fuzzy string match against recent article titles. If similarity > 85%, I flag it as a duplicate and don't send it to the LLM."
