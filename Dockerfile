FROM python:3.11-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

RUN adduser --disabled-password --gecos "" appuser

COPY --chown=appuser:appuser . .

RUN mkdir -p /app/logs \
    && chown -R appuser:appuser /app/logs

USER appuser

CMD ["python", "app.py"]
