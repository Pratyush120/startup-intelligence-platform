<div align="center">
  <img src="assets/screenshots/logo.png" alt="SDIP Logo" width="120" />
  <h1>Startup Data Intelligence Platform (SDIP)</h1>
  <p><strong>The modern data intelligence platform for discovering, evaluating, and tracking high-growth startups.</strong></p>

  <p>
    <a href="https://github.com/startup-intelligence-platform/sdip/actions"><img src="https://img.shields.io/github/actions/workflow/status/startup-intelligence-platform/sdip/ci.yml?style=flat-square" alt="Build Status"></a>
    <a href="https://github.com/startup-intelligence-platform/sdip/blob/main/LICENSE"><img src="https://img.shields.io/github/license/startup-intelligence-platform/sdip?style=flat-square" alt="License"></a>
    <a href="https://github.com/startup-intelligence-platform/sdip/pulls"><img src="https://img.shields.io/github/issues-pr/startup-intelligence-platform/sdip?style=flat-square" alt="PRs Welcome"></a>
    <a href="https://github.com/startup-intelligence-platform/sdip/releases"><img src="https://img.shields.io/github/v/release/startup-intelligence-platform/sdip?style=flat-square" alt="Release"></a>
  </p>
</div>

---

## Overview

**SDIP (Startup Data Intelligence Platform)** is an open-source, end-to-end intelligence engine designed for Venture Capitalists, Angel Investors, and Market Researchers. It automates the discovery, ingestion, analysis, and scoring of startup data across the web, providing actionable insights through a stunning, modern web interface.

![Dashboard Overview](assets/screenshots/dashboard.png)

## ✨ Key Features

- **Automated Data Pipelines**: Seamlessly ingest data from Crunchbase, LinkedIn, Twitter/X, News APIs, and more.
- **AI-Powered Insights**: LLM-driven summaries, sentiment analysis, and risk assessment for every startup profile.
- **Dynamic Scoring Engine**: Proprietary growth velocity and founder capability scores.
- **Real-time Knowledge Graph**: Traverse connections between founders, investors, and competitors.
- **Modern Dashboard**: Built with Next.js, featuring dark mode, glassmorphism, and responsive design.
- **Extensible Architecture**: Easily plug in new data sources or scoring algorithms.

## 🛠️ Technology Stack

SDIP is built on a modern, robust, and scalable technology stack:

- **Frontend**: Next.js (React), Tailwind CSS, Framer Motion, Recharts
- **Backend**: Python, FastAPI
- **Database**: PostgreSQL (Relational), Neo4j (Knowledge Graph), Qdrant (Vector DB)
- **Data Pipeline**: Apache Airflow, Celery
- **AI/ML**: OpenAI / Anthropic APIs, LangChain, HuggingFace Transformers
- **Infrastructure**: Docker, Kubernetes, GitHub Actions

## 🚀 Quickstart

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- API Keys (OpenAI, Anthropic, etc. for full functionality)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/startup-intelligence-platform/sdip.git
   cd sdip
   ```

2. **Environment Setup**
   ```bash
   cp .env.example .env
   # Edit .env with your required API keys and database credentials
   ```

3. **Start the Infrastructure**
   ```bash
   docker-compose up -d db redis neo4j qdrant
   ```

4. **Start the Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

5. **Start the Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

Navigate to `http://localhost:3000` to access the SDIP dashboard.

## 🗺️ Architecture Overview

SDIP is divided into three primary components: Data Collectors, the Intelligence Engine, and the UI Application.

For a deep dive, see [ARCHITECTURE.md](docs/ARCHITECTURE.md) and [PIPELINE.md](docs/PIPELINE.md).

## ⚠️ Known Limitations

- **Rate Limits**: Heavy reliance on third-party APIs (e.g., Crunchbase, Twitter) may hit rate limits. Consider providing multiple API keys or configuring longer retry intervals in Airflow.
- **Vector DB Memory Usage**: Qdrant can consume significant memory for large datasets. Ensure your host machine has adequate RAM.
- **Real-time WebSocket Latency**: The live feed may experience latency under extreme load due to Redis Pub/Sub bottlenecks.

## 🤝 Contributing

We welcome contributions from the community! Whether it's a bug fix, a new data collector, or a UI enhancement, your help is appreciated.

Please read our [Contributing Guidelines](CONTRIBUTING.md) and our [Code of Conduct](CODE_OF_CONDUCT.md).

## 🛡️ Security

Security is a priority. For reporting vulnerabilities, please review our [Security Policy](SECURITY.md).

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---
<div align="center">
  Built with ❤️ by the open-source intelligence community.
</div>