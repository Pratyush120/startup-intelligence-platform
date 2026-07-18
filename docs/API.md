# API Documentation

The SDIP API is built with FastAPI and follows RESTful principles. It returns JSON responses and uses standard HTTP status codes.

## Base URL
`/api/v1`

## Authentication
All endpoints require a Bearer token in the `Authorization` header.

`Authorization: Bearer <your_token>`

## Endpoints

### 1. Startups

#### GET `/startups`
List all tracked startups.

**Query Parameters:**
- `page` (int, default: 1): Page number.
- `limit` (int, default: 20, max: 100): Items per page.
- `sector` (string, optional): Filter by industry sector.
- `min_score` (float, optional): Filter by minimum SDIP score.

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": "uuid-1234",
      "name": "Acme AI",
      "sector": "Artificial Intelligence",
      "sdip_score": 88.5,
      "founded_year": 2024
    }
  ],
  "meta": {
    "page": 1,
    "total_pages": 45,
    "total_items": 900
  }
}
```

#### GET `/startups/{id}`
Get detailed information for a specific startup, including LLM summaries and vector similarity results.

#### GET `/startups/{id}/graph`
Get the local knowledge graph neighborhood for a startup (Founders, Investors, Competitors).

### 2. Search

#### POST `/search/semantic`
Perform a semantic search across the startup database using Qdrant vector embeddings.

**Request Body:**
```json
{
  "query": "B2B SaaS companies focused on supply chain optimization in Europe",
  "top_k": 5
}
```

**Response (200 OK):**
```json
{
  "results": [
    {
      "startup_id": "uuid-5678",
      "name": "LogisTech",
      "similarity_score": 0.92,
      "description_snippet": "LogisTech is a B2B SaaS platform that optimizes..."
    }
  ]
}
```

## Pagination
List endpoints utilize cursor-based or offset-based pagination. The `meta` object in the response will always include `page`, `total_pages`, and `total_items`.

## Rate Limiting
The API enforces a rate limit of 100 requests per minute per IP address. Exceeding this will return a `429 Too Many Requests` status.
