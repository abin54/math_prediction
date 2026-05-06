FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml .
RUN pip install --no-cache-dir .
COPY src/ ./src/
COPY models/ ./models/
RUN useradd -m appuser && mkdir -p /app/data && chown -R appuser:appuser /app/data
USER appuser
VOLUME ["/app/data"]
EXPOSE 8000
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "disable"]
