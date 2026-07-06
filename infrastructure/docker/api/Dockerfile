FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY apps/api/pyproject.toml .
COPY apps/api/README.md .

RUN uv sync

COPY apps/api .

EXPOSE 8000

CMD ["uv","run","uvicorn","app.main:app","--host","0.0.0.0","--port","8000","--app-dir","src"]