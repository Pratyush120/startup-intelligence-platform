# System Architecture

The Startup Data Intelligence Platform (SDIP) is designed as a modular, highly scalable microservices architecture. This allows for resilient data scraping, intensive AI processing, and a snappy user experience.

## High-Level Design

```mermaid
graph TD
    subgraph Data Sources
        C[Crunchbase]
        L[LinkedIn]
        T[Twitter/X]
        N[News APIs]
    end

    subgraph Data Pipeline Engine
        A[Airflow / Celery]
        A --> |Collect| C
        A --> |Collect| L
        A --> |Collect| T
        A --> |Collect| N
    end

    subgraph Intelligence Engine
        LLM[LLM Processing - OpenAI/Anthropic]
        Score[Scoring Module]
        A --> |Raw Data| LLM
        A --> |Raw Data| Score
    end

    subgraph Storage Layer
        PG[(PostgreSQL)]
        N4J[(Neo4j - Graph)]
        Q[(Qdrant - Vector)]
        R[(Redis - Cache/PubSub)]
        
        LLM --> PG
        LLM --> Q
        Score --> PG
        A --> N4J
    end

    subgraph API Layer
        API[FastAPI Backend]
        API <--> PG
        API <--> N4J
        API <--> Q
        API <--> R
    end

    subgraph Client Layer
        UI[Next.js Dashboard]
        UI <--> |REST / WebSockets| API
    end
```

## Component Breakdown

### 1. Data Pipeline Engine (Apache Airflow / Celery)
Handles the orchestration of data collection tasks. It runs scheduled DAGs to pull data from various sources, handling retries, rate-limiting, and backoffs.

### 2. Intelligence Engine
- **LLM Processing**: Uses large language models to generate text summaries, classify sentiment, and parse unstructured news.
- **Scoring Module**: Applies deterministic and probabilistic models to rank startups based on team strength, momentum, and market size.

### 3. Storage Layer
SDIP uses a polyglot persistence strategy:
- **PostgreSQL**: Stores structured relational data (Users, Startups core details, Financials).
- **Neo4j**: Maps the complex relationships (Founder -> Investor -> Startup -> Competitor).
- **Qdrant**: Stores vector embeddings for semantic search across startup descriptions and news articles.
- **Redis**: Acts as a caching layer for the API and handles WebSocket message brokering for the live feed.

### 4. API Layer (FastAPI)
A high-performance Python backend that serves as the gateway for the frontend. It routes complex queries to the appropriate database and manages authentication/authorization.

### 5. Client Layer (Next.js)
A modern, responsive frontend built with React, Tailwind CSS, and Framer Motion to provide an exceptional user experience.
