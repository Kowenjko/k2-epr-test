
FROM python:3.14

WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir --upgrade pip wheel uv


COPY api/pyproject.toml api/uv.lock* ./


RUN uv sync --no-dev

COPY api/ ./

EXPOSE 8000

CMD ["uv", "run", "python", "run.py"]
