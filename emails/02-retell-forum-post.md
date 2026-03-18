# Retell Community Forum Post

**Post to:** https://community.retellai.com/
**Category:** Feature Request / Support Help

---

## Title: Custom STT Integration for Taiwanese Hokkien (台語) — Using Self-hosted Whisper Model

## Body:

Hi Retell team and community! 👋

We're **Pain Point AI Tech**, an AI company based in **Taipei, Taiwan**. We're building a voice AI agent that needs to understand **Taiwanese Hokkien (台語)** — a language spoken by millions in Taiwan but not currently supported by Retell's native STT providers.

### What We Want to Do

We have a **fine-tuned Whisper model** specifically trained for Taiwanese Hokkien ASR (from NUTN-KWS on HuggingFace). We want to integrate it as a **custom STT provider** in Retell.

### Our Questions

1. **Does `custom_stt_config` support fully custom STT endpoints?** We see it supports Azure and Whisper, but can we point it to our own self-hosted Whisper server (e.g., a FastAPI endpoint that accepts audio chunks and returns transcripts)?

2. **What is the expected API contract for a custom STT endpoint?** Specifically:
   - What audio format does Retell send? (PCM, WAV, raw bytes?)
   - What sample rate? (8kHz for telephony? 16kHz?)
   - Does it expect streaming (WebSocket) or batch (HTTP POST) responses?
   - What should the response format look like? (JSON with transcript field?)

3. **Is there documentation for building a custom STT adapter?** We couldn't find detailed docs on this — only references to Azure and OpenAI Whisper as supported options.

4. **For TTS:** We plan to use ElevenLabs or MiniMax multilingual voice in Chinese as an interim solution. Are there any tips for getting the best Chinese pronunciation quality?

### Our Setup

- **ASR Model:** Fine-tuned `openai/whisper-large-v3-turbo` for Taiwanese Hokkien
- **Hosting:** Planning to deploy on RunPod/Lambda Labs (A10G GPU)
- **Integration:** Will expose as FastAPI + WebSocket endpoint
- **LLM:** Custom LLM via Retell's WebSocket API

### Why This Matters

Taiwanese Hokkien is spoken by **~15 million people** in Taiwan. There's growing demand for voice AI that understands local languages, especially for:
- Customer service hotlines
- Healthcare (elderly patients often prefer speaking Taiwanese)
- Tourism and hospitality

We'd love to work with Retell to make this happen, and we're happy to share our findings with the community.

Thanks!

— **Pain Point AI Tech** 🦞
Taipei, Taiwan
https://painpoint-ai.com
