# Data Pipeline

The SDIP Data Pipeline is the beating heart of the platform. It handles the continuous influx of unstructured and semi-structured data from the web, turning it into structured intelligence.

## Pipeline Architecture

```mermaid
graph LR
    A[Collectors] --> B[Preprocessing]
    B --> C[Deduplication]
    C --> D[Intelligence Enrichment]
    D --> E[Database Sink]
```

### 1. Collectors
Collectors are Python scripts orchestrated by Airflow. They pull data on a schedule or via webhooks.
- **Crunchbase Collector**: Pulls funding rounds, investor lists, and basic company metadata.
- **LinkedIn Collector**: Scrapes founder history, employee headcount growth, and hiring velocity.
- **Twitter/X Collector**: Monitors social sentiment, announcements, and developer engagement.
- **News/Web Collector**: Crawls PR Newswire, TechCrunch, and company blogs.

### 2. Preprocessing
Raw data is normalized into a standard JSON schema.
- Dates are converted to ISO 8601.
- Currency amounts are standardized to USD.
- Text is stripped of HTML tags and normalized.

### 3. Deduplication
Crucial for maintaining data integrity. We use a combination of deterministic matching (domain names, exact names) and probabilistic matching (fuzzy string matching, locality-sensitive hashing) to merge records referring to the same startup.

### 4. Intelligence Enrichment
This is where the raw data becomes valuable:
- **LLM Summarization**: Unstructured news and descriptions are sent to an LLM to generate a concise "Executive Summary".
- **Vector Embeddings**: Text descriptions are passed through an embedding model (e.g., `text-embedding-3-small`) and stored in Qdrant for semantic search.
- **Scoring**: The engine calculates:
  - `Growth Velocity Score`: Based on headcount growth, social traction, and funding frequency.
  - `Founder Capability Score`: Based on previous exits, top-tier university/employer affiliations, and network density.

### 5. Database Sink
The final enriched payload is distributed across the storage layer:
- Relational data to PostgreSQL.
- Graph relationships (e.g., Founder X works at Startup Y) to Neo4j.
- Embeddings to Qdrant.
