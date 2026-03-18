"""
Taiwan Voice AI — ASR Server Configuration
Pain Point AI Tech 🦞
"""

import os

# Model
MODEL_ID = os.getenv("ASR_MODEL_ID", "NUTN-KWS/Whisper-Taiwanese-model-v0.5")
MODEL_CACHE_DIR = os.getenv("ASR_MODEL_CACHE", os.path.expanduser("~/.cache/whisper-taiwanese"))
DEVICE = os.getenv("ASR_DEVICE", "cpu")  # "cpu" for dev, "cuda" for production

# Audio
SAMPLE_RATE = int(os.getenv("ASR_SAMPLE_RATE", "16000"))
TELEPHONY_SAMPLE_RATE = 8000  # Retell/telephony standard
MAX_AUDIO_LENGTH_SEC = int(os.getenv("ASR_MAX_LENGTH", "300"))
SUPPORTED_FORMATS = ["wav", "pcm", "mp3", "ogg", "flac", "webm"]

# Server
HOST = os.getenv("ASR_HOST", "0.0.0.0")
PORT = int(os.getenv("ASR_PORT", "8765"))
CORS_ORIGINS = os.getenv("ASR_CORS_ORIGINS", "*").split(",")

# Streaming
CHUNK_DURATION_MS = 500  # Process audio in 500ms chunks
STREAMING_BUFFER_SEC = 2.0  # Buffer before processing

# Logging
LOG_LEVEL = os.getenv("ASR_LOG_LEVEL", "INFO")
