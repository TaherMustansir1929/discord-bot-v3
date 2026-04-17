# ── Stage 1: dependency resolver ─────────────────────────────────────────────
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

WORKDIR /app

# Enable bytecode compilation and frozen lockfile installs for speed + correctness
ENV UV_COMPILE_BYTECODE=1 \
    UV_FROZEN=1

# Copy dependency files first (better layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies into /app/.venv — no project sources yet
RUN uv sync --no-install-project

# Copy source and do the final sync (installs the project itself)
COPY . .
RUN uv sync

# Strip bloat from the venv before copying to the runtime image:
#   - *.dist-info  → package metadata, not needed at runtime
#   - __pycache__  → already compiled to .pyc via UV_COMPILE_BYTECODE above
#   - *.pyi        → type stubs, only useful for IDEs/type checkers
#   - tests/       → test suites shipped inside third-party packages
RUN find .venv \( \
        -type d -name "*.dist-info" -o \
        -type d -name "__pycache__" -o \
        -type d -name "tests"       -o \
        -type d -name "test"        \
    \) -exec rm -rf {} + 2>/dev/null || true \
 && find .venv \( -name "*.pyi" -o -name "*.so.debug" \) \
    -delete 2>/dev/null || true


# ── Stage 2: minimal runtime image ───────────────────────────────────────────
FROM python:3.13-slim-bookworm

WORKDIR /app

# Don't run as root
RUN useradd --create-home botuser
USER botuser

# Copy the fully-built virtualenv and source from the builder
COPY --from=builder --chown=botuser:botuser /app /app

# Put the venv's Python on PATH
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

CMD ["python", "main.py"]

# ---- Run in terminal ----
# docker build -t discord-bot-v3 .
# docker run --env-file .env discord-bot-v3
