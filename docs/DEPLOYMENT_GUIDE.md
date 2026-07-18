# Deployment Guide

This guide covers deploying SDIP to a production environment using **Render** (Backend/Database) and **Vercel** (Frontend).

## Prerequisites
*   GitHub Repository with SDIP codebase.
*   OpenAI API Key (or Anthropic API Key).
*   Accounts on Render.com and Vercel.com.

---

## 1. Backend Deployment (Render)

We use Render because it natively supports Docker and provides persistent disks for our SQLite database.

1.  Log in to Render and create a new **Web Service**.
2.  Connect your GitHub repository.
3.  Set the environment to **Docker**.
4.  Under **Advanced**, add a **Persistent Disk**:
    *   Name: `sqlite_data`
    *   Mount Path: `/app/data` (You must update the `Config.DATABASE_PATH` in `config.py` to point to `/app/data/app.db`).
5.  Set the following **Environment Variables**:
    *   `ENVIRONMENT=production`
    *   `OPENAI_API_KEY=your-api-key`
    *   `MOCK_MODE=False`
6.  Click **Deploy**.

## 2. Frontend Deployment (Vercel)

Vercel is the optimal hosting provider for Next.js applications.

1.  Log in to Vercel and **Add New Project**.
2.  Connect your GitHub repository.
3.  Vercel will automatically detect the Next.js framework.
4.  Set the **Root Directory** to `frontend`.
5.  Set the following **Environment Variables**:
    *   `NEXT_PUBLIC_API_BASE_URL=https://your-render-app-url.onrender.com/api/v1`
6.  Click **Deploy**.

---

## 3. Database Migration & Rollbacks

### SQLite to PostgreSQL
If the SQLite database becomes a bottleneck (due to write locks), migrate to PostgreSQL:
1.  Spin up a managed PostgreSQL database on Render.
2.  Rewrite `src/database/repository.py` to use SQLAlchemy connecting to the `DATABASE_URL`.
3.  Update the FastAPI dependency injection to provide the Postgres repository.

### Rollback Strategy
If a deployment introduces a critical bug:
1.  **Frontend**: Open the Vercel dashboard, navigate to Deployments, and click the three dots next to the previous stable deployment -> **Promote to Production**. (Instant rollback).
2.  **Backend**: Open Render, navigate to the Web Service -> Manual Deploy -> Deploy specific commit.

## 4. Monitoring
*   Monitor FastAPI metrics using the built-in Swagger UI and Render logs.
*   Monitor pipeline execution health directly from the `/api/v1/health` endpoint.
*   All pipeline errors are logged securely using `structlog` as structured JSON, easily ingestible by Datadog or ELK stacks.
