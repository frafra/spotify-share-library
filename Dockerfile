FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim
LABEL maintainer="fraph24@gmail.com"

WORKDIR /app
ADD pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project
ADD app.py .

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app:main", "--host", "0.0.0.0"]
