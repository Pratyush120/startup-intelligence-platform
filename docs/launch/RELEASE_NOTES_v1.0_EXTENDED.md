# Release Notes: v1.0.0 (General Availability)

We are thrilled to announce the v1.0.0 release of the **Strategic Decision Intelligence Platform (SDIP)**! 🚀

## Highlights
* **Automated Data Ingestion**: Plug-and-play collectors for NewsAPI, Google News, and customizable sources.
* **LLM Provider Abstraction**: Switch seamlessly between OpenAI, Anthropic, or Local models using our Provider architecture without changing any business logic.
* **Intelligent Enrichment**: Automatically extracts business events (Funding, Hiring, Layoffs, Acquisition, Expansion) and scores them by business impact.
* **High-Performance FastAPI Backend**: A robust, dependency-injected backend ensuring < 10ms data access.
* **Next.js Dashboard**: A modern, interactive React application for analyzing generated market intelligence.

## Known Limitations
* **Concurrent Writes**: The SQLite database (`app.db`) is optimized for reads. Running the Pipeline Orchestrator simultaneously across multiple threads may result in `database is locked` errors. For now, the orchestrator should be run as a single-threaded cron job.
* **Frontend Filtering**: Large datasets (>50,000 events) may cause the Next.js client-side filtering to lag. Server-side pagination is planned for v1.1.

## Upgrade / Migration Notes
If you are upgrading from a pre-release version:
1. Delete your existing `app.db` file. The schema has been heavily modified to support compound indexing and the new `pipeline_runs` audit table.
2. Run `python -m src.scripts.run_pipeline` to regenerate the tables and fetch fresh data.
3. Update your `.env` file to include `OPENAI_API_KEY` if you are switching off the `MockProvider`.

## Future Roadmap (v2.0)
* **Graph Database Migration**: We plan to replace SQLite with Neo4j to properly model the complex relationships between Investors, Founders, and Startups.
* **Parallel Orchestration**: Moving the ingestion pipeline from a synchronous loop to an asynchronous Celery worker queue.
* **User Authentication**: Implementing OAuth2 / JWT to support multi-tenant SaaS deployments.

Thank you to all contributors who made this 1.0 release possible!
