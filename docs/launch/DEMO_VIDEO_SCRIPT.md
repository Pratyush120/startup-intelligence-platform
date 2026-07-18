# Demo Video Script

Use this script to record a 5-minute Loom or YouTube video demonstrating SDIP for your portfolio or LinkedIn.

## Setup
*   Ensure the Next.js app is running on `localhost:3000`.
*   Ensure the FastAPI backend is running on `localhost:8000`.
*   Have the SQLite database pre-populated using the MockProvider.
*   Have your IDE open to `orchestrator.py` and `repository.py`.

## The Script

### 0:00 - 1:00 | The Hook & The Problem
**[Screen: The Dashboard (localhost:3000) - Market Snapshot]**
"Hi everyone, I’m [Your Name], and I want to show you the Strategic Decision Intelligence Platform—an autonomous AI agent I built to automate startup market research. Usually, strategy analysts read hundreds of articles to figure out market trends. SDIP does this automatically. Every hour, it ingests news, uses an LLM to extract business events, and calculates the overall market health you see right here on this dashboard."

### 1:00 - 2:00 | The Timeline & Data Aggregation
**[Screen: Scroll down to the Timeline and Top Companies]**
"Instead of a raw news feed, SDIP generates a structured timeline. It extracted the fact that [Company X] raised [Amount] in Series B. It then aggregates these events to score individual companies on Momentum, Risk, and Investment Potential. This turns qualitative news into quantitative data."

### 2:00 - 3:00 | The Architecture & Provider Pattern
**[Screen: Switch to IDE -> `llm_analyzer.py` and `orchestrator.py`]**
"Let’s look under the hood. The pipeline is built in Python. The biggest risk in AI engineering is vendor lock-in, so I built a strict Provider Pattern. The business logic never talks directly to OpenAI. It talks to this `BaseProvider` interface. This allowed me to build a `MockProvider`, meaning I can run and test this entire pipeline locally without spending a dime on API tokens."

### 3:00 - 4:00 | Database & API Layer
**[Screen: Switch to IDE -> `repository.py` and FastAPI Swagger UI (`localhost:8000/docs`)]**
"To keep the architecture clean, I used the Repository Pattern to isolate the SQLite database. The frontend talks to this FastAPI backend, which serves data in under 10 milliseconds thanks to an in-memory TTL cache I implemented in the Repository layer."

### 4:00 - 5:00 | Testing & Conclusion
**[Screen: Terminal -> Run `pytest`]**
"Because the database and LLMs are completely decoupled, I can run my entire test suite—achieving over 70% coverage—in just 2 seconds. The entire stack is dockerized and open source. Check out the link in the description for the GitHub repo and a deep dive into the architecture decisions. Thanks for watching!"
