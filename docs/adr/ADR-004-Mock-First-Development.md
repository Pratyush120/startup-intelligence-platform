# ADR 004: Mock-First Architecture

## Status
Accepted

## Problem
In early development, and particularly in open-source projects, relying on paid external APIs (OpenAI, NewsAPI) blocks contributors who don't have API keys. It also introduces flakiness into CI/CD pipelines due to network latency, rate limits, and non-deterministic LLM responses.

## Decision
We adopted a **Mock-First Architecture**. The application must be able to boot, run the complete intelligence pipeline, and serve the frontend dashboard with zero external API keys required. We achieved this via `MockCollector` and `MockProvider`.

## Consequences
- **Positive**: Extremely fast onboarding for new developers. They can clone the repo, run `docker-compose up`, and see a fully populated dashboard instantly.
- **Positive**: Blazing fast and highly deterministic unit tests. Tests run in under 5 seconds.
- **Negative**: The mock data can become stale or misaligned with the actual API contracts if the mocks are not maintained alongside the real implementations.
