# Demo Script

Use this script when presenting SDIP via screen-share.

## 1. The 3-Minute Recruiter Demo
*(Goal: Show business value and UI polish immediately)*

1.  **Open Dashboard**: "This is the Strategic Decision Intelligence Platform. It's an automated AI analyst."
2.  **Show Market Snapshot**: "Every hour, it reads the news and updates this overall market health score. Right now, it sees a strong investment climate but high risk."
3.  **Show Timeline**: "Scroll down. Instead of a news feed, this is a structured timeline of Business Events. The AI read the news and extracted the exact funding amounts, companies, and event types."
4.  **Show Companies**: "It then aggregates those events to score companies on Momentum and Risk."
5.  **Conclusion**: "It runs completely autonomously via a Python pipeline, backed by FastAPI and Next.js."

## 2. The 5-Minute Engineering Demo
*(Goal: Show architecture and code quality)*

1.  *(Do the 3-minute demo first)*
2.  **Show FastAPI Swagger**: Open `localhost:8000/docs`. "The backend is fully typed via FastAPI and Pydantic."
3.  **Open Code (`orchestrator.py`)**: "Here is the pipeline. It collects, deduplicates, classifies, and extracts. Note how clean it is."
4.  **Open Code (`llm_analyzer.py`)**: "I built a custom Provider interface. We aren't locked into OpenAI. I can swap to a MockProvider instantly."
5.  **Run Tests**: Open terminal and run `pytest`. "Because of this decoupled architecture, I can run the entire test suite offline in under 3 seconds."

## 3. Anticipated Questions during Demo
- *Where is the data coming from?* "Currently NewsAPI and Google News RSS, but the Collector interface makes it trivial to plug in specialized APIs like Crunchbase."
- *How much does the LLM cost?* "We use GPT-4o-mini. Because of the RapidFuzz deduplicator and caching, we only send highly relevant, novel articles to the LLM, keeping costs to pennies per run."
