FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove gcc \
    && rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos "" appuser

RUN mkdir -p /app/logs && chown -R appuser:appuser /app/logs

USER appuser

COPY --chown=appuser:appuser . .

CMD ["python","app.py"]