# Release Notes - v1.0.0 (General Availability)

We are thrilled to announce the v1.0.0 release of the **Strategic Decision Intelligence Platform (SDIP)**. 

## What is SDIP?
SDIP acts as a junior strategy analyst that continuously collects, filters, scores, classifies, and summarizes startup intelligence into a structured knowledge base. It is a production-grade AI platform designed to replace manual market research.

## Key Features in v1.0.0
* **Automated Data Ingestion**: Plug-and-play collectors for NewsAPI, Google News, and customizable sources.
* **LLM Provider Abstraction**: Switch seamlessly between OpenAI, Anthropic, or Local models using our Provider architecture.
* **Intelligent Enrichment**: Extracts business events (Funding, Hiring, Layoffs, Acquisition, Expansion) and scores them by business impact.
* **FastAPI Backend**: A robust, dependency-injected backend ensuring low-latency data access.
* **Next.js Dashboard**: A beautiful, modern React application for analyzing the generated market intelligence.

## Technical Highlights
* Achieved **> 70% Test Coverage**.
* Eliminated vendor lock-in via strict architectural boundaries.
* Dockerized architecture for immediate deployment.

For upgrading from pre-release versions, please reset your `app.db` file as the schema has been significantly expanded to support auditing and compound indexing.
