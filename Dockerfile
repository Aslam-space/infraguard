FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app/ ./app/
COPY scripts/ ./scripts/

# Set permissions on heal scripts
RUN chmod +x scripts/*.sh

# Create data directories
RUN mkdir -p data/model logs

# Expose port
EXPOSE 8080

# Start with gunicorn
CMD ["gunicorn", "app.routes:app", \
     "--bind", "0.0.0.0:8080", \
     "--worker-class", "eventlet", \
     "--workers", "1", \
     "--timeout", "120"]
