# Build stage
FROM python:3.11.9-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Run stage
FROM python:3.11.9-slim

# Create a non-root user and install curl for healthchecks
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/* \
    && groupadd -r sdip && useradd -r -g sdip sdipuser

WORKDIR /app

# Copy wheels from builder and install
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy application code
COPY . .

# Ensure permissions for data and logs
RUN mkdir -p data/raw data/processed data/exports logs \
    && chown -R sdipuser:sdip /app \
    && chmod -R 755 /app

# Switch to non-root user
USER sdipuser

# Expose FastAPI port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/api/v1/health || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
