# Portfolio Page Content

*(Use this copy for your personal portfolio website)*

## Hero Section
**Headline:** Strategic Decision Intelligence Platform (SDIP)
**Sub-headline:** An autonomous AI strategy analyst that aggregates, scores, and visualizes the startup ecosystem in real-time.
**CTA Buttons:** [View Live Demo] [Read Case Study] [GitHub Repo]

## The Problem
Venture capitalists and strategy analysts spend thousands of hours manually reading news to gauge market sentiment and track competitors. This manual process is slow, subjective, and difficult to quantify.

## The Solution
SDIP acts as a Junior Analyst running 24/7. It ingests thousands of articles, uses Large Language Models to extract structured business events (Funding, Layoffs, Acquisitions), calculates objective Momentum and Risk scores, and serves the data through a high-performance Next.js dashboard. 

## Business Impact
- **Automated Research**: Replaces manual news scraping with automated, structured entity extraction.
- **Quantitative Signals**: Converts qualitative news into actionable, numeric Momentum and Risk scores.
- **Cost-Efficient**: Uses a two-pass deduplication algorithm and TTL caching to minimize expensive LLM API calls by 40%.

## Engineering Highlights
1. **Mock-First Architecture**: Built with a strict Provider Pattern, allowing the entire AI pipeline and test suite to run offline with zero API keys. 
2. **Dependency Injection**: Utilized the Repository Pattern and FastAPI's `Depends()` to completely decouple the database from business logic, achieving >70% test coverage.
3. **Resilient AI Pipelines**: Enforced strict Pydantic validation on LLM outputs to prevent hallucinations from corrupting the database.

## Tech Stack
- **Backend**: Python, FastAPI, Pydantic, RapidFuzz
- **Frontend**: TypeScript, Next.js, React Query, TailwindCSS
- **Database**: SQLite (Read-optimized)
- **AI**: OpenAI GPT-4o-mini (Pluggable architecture)
- **Infrastructure**: Docker, GitHub Actions
