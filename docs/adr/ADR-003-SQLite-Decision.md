# ADR 003: SQLite Decision

## Status
Accepted

## Problem
We need a robust, low-maintenance way to persist intelligence records, market snapshots, pipeline execution logs, and entity relationship data. We want to minimize infrastructure overhead during the initial release while maintaining data integrity.

## Decision
We chose **SQLite** as the primary datastore for v1.0.

## Alternatives Considered
- **PostgreSQL**: Industry standard, extremely scalable, but requires a separate Docker container, volume management, and increased memory footprint. Overkill for early-stage intelligence gathering.
- **Neo4j / Graph Database**: Ideal for mapping complex relationships (Investors -> Startups -> Founders), but requires learning Cypher and managing a heavier JVM-based container.
- **NoSQL (MongoDB)**: Good for flexible JSON, but lacks the structured relational guarantees (foreign keys, compound indexes) we need for deterministic analytics.

## Consequences
- **Positive**: Zero configuration required. The database is a single file (`app.db`).
- **Positive**: Easy to backup and transfer.
- **Positive**: Extremely fast read performance for FastAPI.
- **Negative**: Concurrent writes can cause `database is locked` errors. We mitigated this by centralizing writes to the single-threaded pipeline orchestrator, treating the FastAPI backend as mostly read-only.
