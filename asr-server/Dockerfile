FROM python:3.11-slim

WORKDIR /app

# Install system deps for audio processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Config
ENV ASR_DEVICE=cuda \
    ASR_PRELOAD=true \
    ASR_PORT=8765 \
    ASR_HOST=0.0.0.0

EXPOSE 8765

HEALTHCHECK --interval=30s --timeout=10s \
    CMD curl -f http://localhost:8765/health || exit 1

CMD ["python", "main.py"]
