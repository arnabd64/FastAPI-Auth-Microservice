# Stage 1: Build virtual environment using the official uv Alpine image
FROM ghcr.io/astral-sh/uv:python3.12-alpine AS builder

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Install dependencies into the virtual environment
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-dev --no-install-project --no-cache


# Stage 2: Minimal runtime stage
FROM python:3.12-alpine

WORKDIR /app

# Copy the virtual environment and app from the builder
COPY --from=builder /app/.venv /app/.venv
COPY src/ /app/src

# Place the virtual environment on PATH
ENV PATH="/app/.venv/bin:$PATH" \
    UVICORN_HOST=0.0.0.0 \
    UVICORN_PORT=8000 \
    UVICORN_WORKERS=2

CMD ["uvicorn", "src.main:app"]