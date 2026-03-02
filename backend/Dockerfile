# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps for psycopg2-binary (pre-built wheel still needs libpq at runtime)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Install uv — fastest Python package installer
# Copies a single static binary from the official uv image
COPY --from=ghcr.io/astral-sh/uv:0.5.29 /uv /usr/local/bin/uv

# Install Python dependencies
# uv always fetches pre-built wheels — never compiles from source
COPY pyproject.toml .
RUN uv pip install --system --no-cache .

COPY . .

RUN mkdir -p /app/media /app/staticfiles

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
