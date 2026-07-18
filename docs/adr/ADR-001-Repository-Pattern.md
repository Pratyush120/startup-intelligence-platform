# ADR 001: Repository Pattern for Database Access

## Status
Accepted

## Problem
The Intelligence Engine processes complex nested objects (Companies, Events) and needs to persist them to a SQLite database. Directly embedding SQL queries inside the pipeline orchestration code or business logic makes the code hard to test, couples the business rules to the schema, and duplicates database access code.

## Decision
We will use the **Repository Pattern**. We create a `Repository` class (`src/database/repository.py`) that acts as an abstraction layer over the SQLite database. All data access goes through this repository.

## Alternatives Considered
- **Direct SQLite Queries (sqlite3 module)**: Easiest to write initially but quickly becomes unmaintainable and impossible to unit test without standing up a real database.
- **Full ORM (SQLAlchemy)**: Offers robust object mapping but introduces high complexity and overhead for a project that relies on unstructured JSON payloads and dynamic dictionary serialization.

## Consequences
- **Positive**: Business logic (Pipeline Orchestrator, Analytics Engines) can be unit-tested seamlessly by patching or injecting a Mock Repository.
- **Positive**: We can swap out SQLite for PostgreSQL or Neo4j in the future by simply implementing a new Repository class matching the same interface.
- **Negative**: Requires maintaining explicit serialization/deserialization logic in the Repository layer to map tuples to dicts.
