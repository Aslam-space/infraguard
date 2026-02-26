FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    bash \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY scripts/ ./scripts/
RUN chmod +x scripts/*.sh
RUN mkdir -p data/model logs

EXPOSE 8080

CMD ["gunicorn", "app.routes:app", \
     "--bind", "0.0.0.0:8080", \
     "--worker-class", "eventlet", \
     "--workers", "1", \
     "--timeout", "120"]
