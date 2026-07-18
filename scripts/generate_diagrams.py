import urllib.request
import base64
import os

DIAGRAMS = {
    "architecture": """
graph TD
    A[Cron Job / Scripts] -->|Triggers| B(Pipeline Orchestrator)
    
    subgraph Data Ingestion
        B --> C[Collectors: NewsAPI/RSS]
        C --> D[Deduplicator]
    end

    subgraph Intelligence Engine
        D --> E{LLM Analyzer}
        E -.->|Provider Interface| F[OpenAI / Mock]
        F -.-> E
        E --> G[Scoring & Analytics]
    end
    
    subgraph Persistence Layer
        G --> H[(SQLite via Repository)]
    end
    
    subgraph Frontend Delivery
        H --> I[FastAPI Backend]
        I --> J[Next.js + React Query]
    end
""",
    "pipeline": """
sequenceDiagram
    participant Orchestrator
    participant Collector
    participant LLM
    participant Analytics
    participant DB
    
    Orchestrator->>Collector: fetch_news()
    Collector-->>Orchestrator: raw_articles[]
    
    loop For each article
        Orchestrator->>LLM: extract_events(text)
        LLM-->>Orchestrator: structured_json
        
        Orchestrator->>Analytics: calculate_impact(event)
        Analytics-->>Orchestrator: scored_event
        
        Orchestrator->>DB: save_event(event)
    end
    
    Orchestrator->>Analytics: aggregate_companies()
    Analytics-->>DB: save_company_metrics()
""",
    "database": """
erDiagram
    COMPANIES ||--o{ EVENTS : "has"
    ARTICLES ||--o{ EVENTS : "source of"
    
    COMPANIES {
        string company_name PK
        float momentum_score
        float growth_score
        float risk_score
        int total_funding
        string recommendation
    }
    
    EVENTS {
        int event_id PK
        int article_id FK
        string company_name FK
        string event_type
        float importance_score
        string ai_summary
    }
    
    ARTICLES {
        int article_id PK
        string url_hash
        string title
        datetime published_at
    }
    
    PIPELINE_RUNS {
        int run_id PK
        datetime started_at
        int records_processed
        string status
    }
""",
    "deployment": """
graph TD
    subgraph Docker Compose
        A[Next.js Frontend: Port 3000]
        B[FastAPI Backend: Port 8000]
        C[(SQLite Data Volume)]
    end
    
    User[Client Browser] -->|HTTP/REST| A
    A -->|React Query| B
    B -->|Read/Write| C
    
    Cron[System Cron] -->|Run pipeline.py| B
    B -->|API Calls| OpenAI[OpenAI API]
"""
}

def generate_svgs():
    os.makedirs("assets/diagrams", exist_ok=True)
    for name, code in DIAGRAMS.items():
        try:
            # Base64 encode the mermaid code
            b64_str = base64.b64encode(code.strip().encode("utf-8")).decode("utf-8")
            # Create the URL
            url = f"https://mermaid.ink/svg/{b64_str}"
            
            # Fetch the SVG
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                svg_data = response.read().decode('utf-8')
            
            # Save the SVG
            file_path = f"assets/diagrams/{name}.svg"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(svg_data)
            print(f"Generated {file_path}")
        except Exception as e:
            print(f"Failed to generate {name}: {e}")

if __name__ == "__main__":
    generate_svgs()
