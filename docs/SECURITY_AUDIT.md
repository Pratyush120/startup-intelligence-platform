# Security Audit Report (v1.0.0 RC-1)

## Overview
This document outlines the security posture, best practices, and identified risks of the Strategic Decision Intelligence Platform (SDIP) prior to the v1.0.0 production release.

## 1. Secrets Management
*   **Environment Variables**: All sensitive API keys (e.g., `OPENAI_API_KEY`) are managed strictly via `.env` files. The `.env` file is excluded from version control via `.gitignore`.
*   **Validation**: The application uses `pydantic-settings` to strictly validate that required configuration variables are present at startup. If `ENVIRONMENT=production` is set but no `OPENAI_API_KEY` is found, the backend will refuse to start rather than failing silently later.

## 2. API Security
*   **CORS**: Cross-Origin Resource Sharing (CORS) is configured strictly in `src/main.py`. It is locked down to specific frontend origins (e.g., `http://localhost:3000` or production domains), preventing malicious cross-site requests.
*   **Data Validation**: Every incoming and outgoing API request is validated using strict Pydantic schemas. This ensures no malformed or oversized payloads can crash the FastAPI handlers.
*   **Rate Limiting**: (Planned for v1.1) Currently relying on the underlying reverse proxy (Nginx/Render) for DDoS protection.

## 3. Database Security
*   **SQL Injection Prevention**: We do not use raw string concatenation for SQL queries. Every query in the SQLite `Repository` uses parameterized queries (`execute(..., (val1, val2))`), completely neutralizing SQL injection risks.
*   **Data Integrity**: SQLite is enforced with `PRAGMA foreign_keys = ON`, guaranteeing relational integrity between companies, articles, and extracted events.
*   **LLM Hallucination Guardrails**: LLM outputs are treated as untrusted user input. They are pushed through Pydantic validators before ever touching the database logic.

## 4. Docker Security
*   **Non-Root Execution**: (Recommended adjustment) The base Dockerfiles currently run as root. A `USER appuser` should be added prior to enterprise deployment to prevent privilege escalation if a container is compromised.
*   **Minimal Base Images**: Both the frontend (Node Alpine) and backend (Python Slim) use minimal base images to reduce the attack surface area.

## 5. Dependency Audit
*   All dependencies in `requirements.txt` and `package.json` are pinned to specific versions to prevent supply-chain attacks via automatic minor version upgrades.

## Conclusion
The application is structurally secure for an open-source analytics platform. The primary requirement before transitioning to a multi-tenant SaaS is the implementation of an authentication layer (OAuth2/JWT) and applying non-root user execution in Docker.
