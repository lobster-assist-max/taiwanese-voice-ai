# Taiwan Voice AI — ASR Server

> Taiwanese Hokkien (台語) Automatic Speech Recognition powered by fine-tuned Whisper
>
> Built by Pain Point AI Tech 🦞

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run server (model loads on first request)
python main.py

# Or with uvicorn
uvicorn main:app --host 0.0.0.0 --port 8765
```

Server starts at `http://localhost:8765`

## API Endpoints

### `GET /` — Service info
### `GET /health` — Health check
### `GET /info` — Model info

### `POST /transcribe` — Batch transcription
```bash
curl -X POST http://localhost:8765/transcribe \
  -F "file=@test.wav"
```

Response:
```json
{
  "transcript": "你好，我想要問一下...",
  "language": "taiwanese",
  "confidence": 0.85,
  "audio_duration_sec": 5.2,
  "processing_time_sec": 1.3,
  "realtime_factor": 0.25
}
```

### `POST /retell/transcribe` — Retell-compatible endpoint
Same as `/transcribe` but returns Retell's expected format:
```json
{
  "text": "你好，我想要問一下...",
  "confidence": 0.85,
  "words": []
}
```

### `WebSocket /ws/transcribe` — Streaming transcription
```python
import websockets
import asyncio

async def stream():
    async with websockets.connect("ws://localhost:8765/ws/transcribe") as ws:
        # Send audio chunks (PCM 16-bit, 16kHz mono)
        with open("test.pcm", "rb") as f:
            while chunk := f.read(32000):  # 1 second chunks
                await ws.send(chunk)
                response = await asyncio.wait_for(ws.recv(), timeout=5)
                print(response)
        
        # Signal end
        await ws.send("END")
        final = await ws.recv()
        print(final)

asyncio.run(stream())
```

## Configuration

All settings via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `ASR_MODEL_ID` | `NUTN-KWS/Whisper-Taiwanese-model-v0.5` | HuggingFace model ID |
| `ASR_DEVICE` | `cpu` | `cpu` or `cuda` |
| `ASR_PORT` | `8765` | Server port |
| `ASR_SAMPLE_RATE` | `16000` | Default sample rate |
| `ASR_MAX_LENGTH` | `300` | Max audio length (seconds) |
| `ASR_PRELOAD` | `false` | Preload model on startup |
| `ASR_DEV` | `false` | Enable hot reload |
| `ASR_LOG_LEVEL` | `INFO` | Log level |
| `ASR_CORS_ORIGINS` | `*` | CORS origins (comma-separated) |

## Retell AI Integration

This server is designed to integrate with [Retell AI](https://retellai.com) as a custom STT provider.

### Setup in Retell
1. Deploy this server on a GPU instance (RunPod/Lambda Labs recommended)
2. Configure agent with `stt_mode: "custom"`
3. Point `custom_stt_config` to your server's `/retell/transcribe` endpoint

### Audio Format
- Retell sends telephony audio at **8kHz PCM**
- Server auto-resamples to 16kHz for Whisper
- Supports: WAV, PCM, MP3, OGG, FLAC, WebM

## Deployment

### Local (CPU, for testing)
```bash
python main.py
```

### GPU Server (Production)
```bash
ASR_DEVICE=cuda ASR_PRELOAD=true python main.py
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV ASR_DEVICE=cuda ASR_PRELOAD=true
EXPOSE 8765
CMD ["python", "main.py"]
```

### Recommended GPU Instances
| Provider | Instance | Price |
|----------|----------|-------|
| RunPod | A10G | ~$0.44/hr |
| Lambda Labs | A10 | ~$0.60/hr |
| AWS | g5.xlarge | ~$1.00/hr |

## Model

**NUTN-KWS/Whisper-Taiwanese-model-v0.5**
- Base: OpenAI Whisper Large V3 Turbo
- Fine-tuned for Taiwanese Hokkien (台語)
- By National University of Tainan (台南大學)
- HuggingFace: https://huggingface.co/NUTN-KWS/Whisper-Taiwanese-model-v0.5

---

Built by [Pain Point AI Tech](https://painpoint-ai.com) 🦞
