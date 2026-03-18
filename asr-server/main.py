"""
Taiwan Voice AI — ASR Server
Taiwanese Hokkien Speech Recognition via Fine-tuned Whisper

Built by Pain Point AI Tech 🦞
https://painpoint-ai.com
"""

import io
import time
import logging
import asyncio
import tempfile
from pathlib import Path
from typing import Optional

import numpy as np
import soundfile as sf
from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import config

# ─── Logging ─────────────────────────────────────────────
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("asr-server")

# ─── App Setup ───────────────────────────────────────────
app = FastAPI(
    title="Taiwan Voice AI — ASR Server",
    description="Taiwanese Hokkien (台語) Automatic Speech Recognition powered by fine-tuned Whisper",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Model Loading ───────────────────────────────────────
model = None
processor = None
model_loaded = False
model_load_error = None


def load_model():
    """Load the Whisper model. Called on first request or startup."""
    global model, processor, model_loaded, model_load_error
    
    if model_loaded:
        return True
    
    try:
        logger.info(f"Loading model: {config.MODEL_ID}")
        logger.info(f"Device: {config.DEVICE}")
        logger.info(f"Cache dir: {config.MODEL_CACHE_DIR}")
        
        from transformers import WhisperProcessor, WhisperForConditionalGeneration
        
        processor = WhisperProcessor.from_pretrained(
            config.MODEL_ID,
            cache_dir=config.MODEL_CACHE_DIR,
        )
        model = WhisperForConditionalGeneration.from_pretrained(
            config.MODEL_ID,
            cache_dir=config.MODEL_CACHE_DIR,
        )
        
        if config.DEVICE == "cuda":
            import torch
            if torch.cuda.is_available():
                model = model.to("cuda")
                logger.info("Model loaded on CUDA GPU")
            else:
                logger.warning("CUDA requested but not available, using CPU")
        else:
            logger.info("Model loaded on CPU")
        
        model.eval()
        model_loaded = True
        logger.info("✅ Model loaded successfully")
        return True
        
    except Exception as e:
        model_load_error = str(e)
        logger.error(f"❌ Failed to load model: {e}")
        return False


def transcribe_audio(audio_data: np.ndarray, sample_rate: int) -> dict:
    """
    Transcribe audio using the loaded Whisper model.
    
    Args:
        audio_data: numpy array of audio samples
        sample_rate: sample rate of the audio
        
    Returns:
        dict with transcript, language, confidence, duration
    """
    import torch
    
    if not model_loaded:
        raise RuntimeError("Model not loaded")
    
    start_time = time.time()
    
    # Resample to 16kHz if needed (Whisper requires 16kHz)
    if sample_rate != 16000:
        import librosa
        audio_data = librosa.resample(
            audio_data.astype(np.float32),
            orig_sr=sample_rate,
            target_sr=16000
        )
        sample_rate = 16000
    
    # Ensure float32 and normalize
    audio_data = audio_data.astype(np.float32)
    if np.abs(audio_data).max() > 1.0:
        audio_data = audio_data / np.abs(audio_data).max()
    
    # Process
    input_features = processor(
        audio_data,
        sampling_rate=sample_rate,
        return_tensors="pt"
    ).input_features
    
    if config.DEVICE == "cuda" and torch.cuda.is_available():
        input_features = input_features.to("cuda")
    
    # Generate
    with torch.no_grad():
        predicted_ids = model.generate(
            input_features,
            language="zh",  # Chinese/Taiwanese
            task="transcribe",
        )
    
    # Decode
    transcript = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0].strip()
    
    elapsed = time.time() - start_time
    audio_duration = len(audio_data) / sample_rate
    
    return {
        "transcript": transcript,
        "language": "taiwanese",
        "confidence": 0.85,  # TODO: extract actual confidence from model
        "audio_duration_sec": round(audio_duration, 2),
        "processing_time_sec": round(elapsed, 3),
        "realtime_factor": round(elapsed / max(audio_duration, 0.01), 2),
    }


# ─── Endpoints ───────────────────────────────────────────

@app.get("/")
async def root():
    return {
        "service": "Taiwan Voice AI — ASR Server",
        "version": "0.1.0",
        "model": config.MODEL_ID,
        "status": "ready" if model_loaded else "model_not_loaded",
        "built_by": "Pain Point AI Tech 🦞",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model_loaded": model_loaded,
        "model_error": model_load_error,
        "device": config.DEVICE,
    }


@app.get("/info")
async def info():
    return {
        "model_id": config.MODEL_ID,
        "device": config.DEVICE,
        "sample_rate": config.SAMPLE_RATE,
        "max_audio_length_sec": config.MAX_AUDIO_LENGTH_SEC,
        "supported_formats": config.SUPPORTED_FORMATS,
        "model_loaded": model_loaded,
        "features": {
            "batch_transcribe": True,
            "streaming_transcribe": True,
            "retell_compatible": True,
        },
    }


@app.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    sample_rate: Optional[int] = None,
):
    """
    Transcribe an audio file to text.
    
    Accepts WAV, PCM, MP3, OGG, FLAC, WebM formats.
    For PCM/raw audio, specify sample_rate query param (default: 16000).
    
    Returns JSON with transcript and metadata.
    """
    # Load model on first request
    if not model_loaded:
        if not load_model():
            raise HTTPException(
                status_code=503,
                detail=f"Model not available: {model_load_error}"
            )
    
    try:
        # Read file
        content = await file.read()
        
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Empty audio file")
        
        # Determine format and read audio
        filename = file.filename or "audio.wav"
        ext = Path(filename).suffix.lower().lstrip(".")
        
        if ext == "pcm" or file.content_type == "audio/pcm":
            # Raw PCM: assume 16-bit signed integers
            sr = sample_rate or config.SAMPLE_RATE
            audio_data = np.frombuffer(content, dtype=np.int16).astype(np.float32) / 32768.0
        else:
            # Use soundfile for WAV, FLAC, OGG
            try:
                audio_data, sr = sf.read(io.BytesIO(content))
            except Exception:
                # Fallback: try librosa for MP3, WebM, etc.
                import librosa
                with tempfile.NamedTemporaryFile(suffix=f".{ext}", delete=True) as tmp:
                    tmp.write(content)
                    tmp.flush()
                    audio_data, sr = librosa.load(tmp.name, sr=None)
        
        if sample_rate:
            sr = sample_rate
        
        # Convert stereo to mono
        if len(audio_data.shape) > 1:
            audio_data = audio_data.mean(axis=1)
        
        # Check length
        duration = len(audio_data) / sr
        if duration > config.MAX_AUDIO_LENGTH_SEC:
            raise HTTPException(
                status_code=400,
                detail=f"Audio too long: {duration:.1f}s (max: {config.MAX_AUDIO_LENGTH_SEC}s)"
            )
        
        # Transcribe
        result = transcribe_audio(audio_data, sr)
        
        logger.info(
            f"Transcribed {duration:.1f}s audio -> '{result['transcript'][:50]}...' "
            f"({result['processing_time_sec']}s)"
        )
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Transcription error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws/transcribe")
async def ws_transcribe(websocket: WebSocket):
    """
    Streaming transcription via WebSocket.
    
    Protocol:
    1. Client connects
    2. Client sends audio chunks (binary frames, PCM 16-bit, 16kHz mono)
    3. Server sends back JSON with partial/final transcripts
    4. Client sends text "END" to finalize
    
    Message format from server:
    {
        "type": "partial" | "final",
        "transcript": "...",
        "timestamp_ms": 1234567890
    }
    """
    await websocket.accept()
    logger.info("WebSocket client connected")
    
    # Load model if needed
    if not model_loaded:
        if not load_model():
            await websocket.send_json({
                "type": "error",
                "message": f"Model not available: {model_load_error}"
            })
            await websocket.close()
            return
    
    audio_buffer = bytearray()
    
    try:
        while True:
            data = await websocket.receive()
            
            if "text" in data:
                text = data["text"]
                if text.upper() == "END":
                    # Process remaining buffer
                    if len(audio_buffer) > 0:
                        audio_data = np.frombuffer(
                            bytes(audio_buffer), dtype=np.int16
                        ).astype(np.float32) / 32768.0
                        
                        if len(audio_data) > 0:
                            result = transcribe_audio(audio_data, config.SAMPLE_RATE)
                            await websocket.send_json({
                                "type": "final",
                                "transcript": result["transcript"],
                                "confidence": result["confidence"],
                                "audio_duration_sec": result["audio_duration_sec"],
                                "timestamp_ms": int(time.time() * 1000),
                            })
                    
                    await websocket.send_json({
                        "type": "done",
                        "timestamp_ms": int(time.time() * 1000),
                    })
                    break
                    
                elif text.upper() == "PING":
                    await websocket.send_json({"type": "pong"})
                    
            elif "bytes" in data:
                audio_buffer.extend(data["bytes"])
                
                # Process every STREAMING_BUFFER_SEC worth of audio
                buffer_samples = len(audio_buffer) // 2  # 16-bit = 2 bytes per sample
                buffer_duration = buffer_samples / config.SAMPLE_RATE
                
                if buffer_duration >= config.STREAMING_BUFFER_SEC:
                    audio_data = np.frombuffer(
                        bytes(audio_buffer), dtype=np.int16
                    ).astype(np.float32) / 32768.0
                    
                    result = transcribe_audio(audio_data, config.SAMPLE_RATE)
                    
                    await websocket.send_json({
                        "type": "partial",
                        "transcript": result["transcript"],
                        "confidence": result["confidence"],
                        "buffer_duration_sec": round(buffer_duration, 2),
                        "timestamp_ms": int(time.time() * 1000),
                    })
                    
                    # Keep last 0.5s for overlap
                    overlap_bytes = int(0.5 * config.SAMPLE_RATE * 2)
                    audio_buffer = audio_buffer[-overlap_bytes:]
    
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}", exc_info=True)
        try:
            await websocket.send_json({
                "type": "error",
                "message": str(e)
            })
        except:
            pass


@app.post("/retell/transcribe")
async def retell_transcribe(
    file: UploadFile = File(...),
):
    """
    Retell-compatible transcription endpoint.
    
    Accepts telephony audio (8kHz PCM) and returns format 
    compatible with Retell's custom STT expectations.
    
    Response format:
    {
        "text": "transcribed text here",
        "confidence": 0.95,
        "words": []  // word-level timestamps (optional)
    }
    """
    if not model_loaded:
        if not load_model():
            raise HTTPException(status_code=503, detail="Model not available")
    
    try:
        content = await file.read()
        
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Empty audio")
        
        # Retell typically sends 8kHz PCM
        try:
            audio_data, sr = sf.read(io.BytesIO(content))
        except:
            # Assume raw PCM 16-bit 8kHz (telephony standard)
            audio_data = np.frombuffer(content, dtype=np.int16).astype(np.float32) / 32768.0
            sr = config.TELEPHONY_SAMPLE_RATE
        
        if len(audio_data.shape) > 1:
            audio_data = audio_data.mean(axis=1)
        
        result = transcribe_audio(audio_data, sr)
        
        # Return Retell-compatible format
        return JSONResponse(content={
            "text": result["transcript"],
            "confidence": result["confidence"],
            "words": [],  # TODO: word-level timestamps
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Retell transcription error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ─── Startup ─────────────────────────────────────────────

@app.on_event("startup")
async def startup():
    logger.info("=" * 50)
    logger.info("Taiwan Voice AI — ASR Server Starting")
    logger.info(f"Model: {config.MODEL_ID}")
    logger.info(f"Device: {config.DEVICE}")
    logger.info(f"Port: {config.PORT}")
    logger.info("=" * 50)
    
    # Pre-load model if env var set
    if os.getenv("ASR_PRELOAD", "false").lower() == "true":
        load_model()
    else:
        logger.info("Model will be loaded on first request (set ASR_PRELOAD=true to preload)")


# ─── Main ────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    import os
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=os.getenv("ASR_DEV", "false").lower() == "true",
        log_level=config.LOG_LEVEL.lower(),
    )
