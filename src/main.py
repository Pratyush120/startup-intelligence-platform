import time
import uuid
import collections
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
import structlog
from config.config import Config

from src.api.response import error_response

from src.api.health import router as health_router
from src.api.executive import router as executive_router
from src.api.market import router as market_router
from src.api.companies import router as companies_router
from src.api.timeline import router as timeline_router
from src.api.recommendations import router as recommendations_router
from src.api.search import router as search_router
from src.api.pipeline import router as pipeline_router
from src.utils.logger import get_logger
from src.database.schema import SchemaManager
from src.database.seeder import seed_database_if_empty

logger = get_logger("fastapi")

app = FastAPI(
    title="SDIP Intelligence API",
    version=Config.VERSION,
    description="Strategic Decision Intelligence Platform API",
)

@app.on_event("startup")
async def startup_event():
    logger.info("Running database migrations...")
    SchemaManager().create_tables()
    logger.info("Database migrations complete.")
    logger.info("Seeding initial data if empty...")
    seed_database_if_empty()

# 1. CORS middleware (Strict)
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# 2. GZip Middleware for performance
app.add_middleware(GZipMiddleware, minimum_size=1000)


# 3. Simple In-Memory Rate Limiting
class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.history = collections.defaultdict(list)

    def check_rate_limit(self, ip: str) -> bool:
        now = time.time()
        # Clean up old history for this IP
        self.history[ip] = [t for t in self.history[ip] if now - t < 60]
        if len(self.history[ip]) >= self.requests_per_minute:
            return False
        self.history[ip].append(now)
        return True


rate_limiter = RateLimiter(requests_per_minute=100)


@app.middleware("http")
async def security_and_logging_middleware(request: Request, call_next):
    # Rate Limiting
    client_ip = request.client.host if request.client else "unknown"
    if not rate_limiter.check_rate_limit(client_ip):
        return JSONResponse(
            status_code=429, content=error_response(["Too Many Requests"]).model_dump()
        )

    # Structlog context
    request_id = str(uuid.uuid4())
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=request_id,
        path=request.url.path,
        method=request.method,
        ip=client_ip,
    )

    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logger.info(
            "Request completed",
            status_code=response.status_code,
            duration_ms=process_time,
        )

        # Security Headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response
    except Exception:
        logger.error("Unhandled exception", exc_info=True)
        return JSONResponse(
            status_code=500,
            content=error_response(["Internal Server Error"]).model_dump(),
        )


# Global Exception Handler (redundant to middleware catch, but covers routing exceptions)
@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    logger.error("Exception handled in global handler", exc_info=True)
    return JSONResponse(
        status_code=500, content=error_response([str(exc)]).model_dump()
    )


# Register routers
app.include_router(health_router, prefix="/api/v1")
app.include_router(executive_router, prefix="/api/v1")
app.include_router(market_router, prefix="/api/v1")
app.include_router(companies_router, prefix="/api/v1")
app.include_router(timeline_router, prefix="/api/v1")
app.include_router(recommendations_router, prefix="/api/v1")
app.include_router(search_router, prefix="/api/v1")
app.include_router(pipeline_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=False)
