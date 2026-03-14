# 技術評估報告

**更新日期：** 2026-03-14

---

## 🎙️ 台語 ASR（語音辨識）

### 選項：ChineseTaiwaneseWhisper
- **GitHub:** https://github.com/sandy1990418/ChineseTaiwaneseWhisper
- **狀態：** ✅ 活躍維護、文檔完整

#### 技術規格
| 項目 | 規格 |
|-----|------|
| 基礎模型 | OpenAI Whisper |
| 微調方式 | Full fine-tune 或 LoRA (PEFT) |
| 支援語言 | 中文（繁體）+ 台語 |
| 推理模式 | Batch / Streaming |
| 效能 | 1:24（T4 GPU，1 分鐘處理 24 分鐘音訊）|

#### 依賴
```
torch>=1.10.0
torchaudio>=0.10.0
transformers>=4.45.2
peft>=0.3.0
faster-whisper>=0.5.0
gradio>=3.20.0
```

#### 部署需求
- **GPU:** T4 或以上（建議 A10G / A100）
- **RAM:** 16GB+
- **Storage:** 10GB+（含模型）

#### 與 Retell 整合可行性
- ✅ 有 FastAPI server（api_main.py）
- ✅ 支援 streaming（電話需要）
- ⚠️ 需要自建 WebSocket 橋接到 Retell

---

## 🔊 台語 TTS（語音合成）

### 選項 1：Taiwanese-Speech-Synthesis
- **GitHub:** https://github.com/ga642381/Taiwanese-Speech-Synthesis
- **狀態：** ⚠️ 待評估

### 選項 2：中研院 TTS
- **來源:** https://github.com/sinica-speech
- **狀態：** ⚠️ 待評估

### 待研究
- [ ] 確認有無 pretrained model
- [ ] 測試語音品質
- [ ] 評估 latency（電話需要 <500ms）

---

## 🔗 整合架構（Draft）

```
┌─────────────────────────────────────────────────────────┐
│                    Retell AI Platform                    │
├─────────────────────────────────────────────────────────┤
│  Phone Call  →  [Custom STT Endpoint]  →  LLM WebSocket │
│                         ↓                               │
│              Our Taiwanese ASR Server                   │
│              (ChineseTaiwaneseWhisper)                  │
│                         ↓                               │
│              Transcript (台語 → 文字)                    │
│                         ↓                               │
│              LLM Response                               │
│                         ↓                               │
│              [Custom TTS Endpoint]                      │
│                         ↓                               │
│              Our Taiwanese TTS Server                   │
│                         ↓                               │
│              Audio Response → Phone Call                │
└─────────────────────────────────────────────────────────┘
```

---

## 💰 預估成本

### GPU Server（ASR + TTS）
| Provider | Instance | 價格 |
|----------|----------|------|
| RunPod | A10G | ~$0.44/hr |
| Lambda Labs | A10 | ~$0.60/hr |
| AWS | g5.xlarge | ~$1.00/hr |

### 月費估算（24/7 運行）
- 低：$320/月（RunPod A10G）
- 中：$450/月（Lambda）
- 高：$730/月（AWS）

### 按需計費（如果流量低）
- 可考慮 serverless（Modal、Replicate）
- 需測試 cold start latency

---

## 📋 待辦

- [ ] 本地測試 ASR（需要 GPU）
- [ ] 找台語音訊樣本測試
- [ ] 研究 TTS 選項
- [ ] 設計 Retell WebSocket 橋接方案
- [ ] 等待 Retell 回覆確認整合方式

---

*Last updated: 2026-03-14*
