FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim


WORKDIR /app

ENV UV_COMPILE_BYTECODE=1

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

COPY pyproject.toml .
COPY uv.lock .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

ENV PATH="/app/.venv/bin:$PATH"

COPY movie-app/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
