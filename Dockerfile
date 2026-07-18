# syntax=docker/dockerfile:1.7
# =============================================================================
# Startup Intelligence Platform — Production Dockerfile
#
# Strategy: Two-stage multi-architecture build
#   Stage 1 (builder): Compile and cache wheels
#   Stage 2 (runtime): Copy wheels and install; no compiler toolchain in prod
#
# Build:
#   DOCKER_BUILDKIT=1 docker build -t sdip-backend .
#
# Python: 3.11-slim (standardized; numpy 2.5+ requires 3.12, we pin 2.2.x)
# =============================================================================

# ── Stage 1: Build wheels ─────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

# Install only the minimum system packages needed to compile C extensions
# (numpy, pandas, rapidfuzz all have pre-built cp311 wheels so gcc is rarely
# needed, but we keep it here as a safety net for any sdist fallbacks)
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Upgrade pip + wheel + setuptools to latest before anything else
# Cached across rebuilds; only re-runs when pip itself changes
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip wheel setuptools

# Copy only requirements (not code) to maximise Docker layer cache hits.
# This layer is invalidated ONLY when requirements change, not on code edits.
COPY requirements.txt requirements.txt
COPY requirements/ requirements/

# Build all wheels. BuildKit pip cache persists across builds.
RUN --mount=type=cache,target=/root/.cache/pip \
    pip wheel \
        --no-deps \
        --wheel-dir /build/wheels \
        -r requirements/prod.txt


# ── Stage 2: Production runtime ───────────────────────────────────────────────
FROM python:3.11-slim AS runtime

# Metadata
LABEL maintainer="SDIP Platform Team" \
      version="1.0.0" \
      description="Startup Intelligence Platform — FastAPI Backend"

# Create non-root service user before copying anything
RUN groupadd --system sdip && \
    useradd --system --gid sdip --no-create-home --shell /sbin/nologin sdipuser

# Minimal runtime dependencies (curl for HEALTHCHECK only)
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install wheels — no network call, deterministic
COPY --from=builder /build/wheels /wheels

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-index --find-links /wheels /wheels/*.whl \
    && rm -rf /wheels

# Copy application source (code-only layer; does NOT invalidate pip cache)
COPY . .

# Create required runtime directories and assign ownership in one layer
RUN mkdir -p data/raw data/processed data/exports logs && \
    chown -R sdipuser:sdip /app && \
    chmod -R 755 /app

# ── Production environment ────────────────────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    ENVIRONMENT=production \
    PORT=8000

# Switch to non-root user for all subsequent commands
USER sdipuser

EXPOSE 8000

# Healthcheck: calls the /api/v1/health FastAPI endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Production server command.
# workers=1 on Render free tier to respect 512MB RAM limit.
# For paid instances, set via env: WEB_CONCURRENCY=2
CMD ["uvicorn", "src.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "1", \
     "--no-access-log"]
