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

## 🆕 新發現（2026-03-18）

### Retell Custom STT 整合方式
Retell API 支援 `custom_stt_config`，可設定自訂 STT provider：
- 設定 `stt_mode: "custom"` 
- 提供自訂 STT endpoint URL
- 支援 Azure、OpenAI Whisper 等
- **關鍵：可以接我們自架的台語 Whisper server**

### 現成台語 Whisper 模型
**NUTN-KWS/Whisper-Taiwanese-model-v0.5**（台南大學）
- 基於 `openai/whisper-large-v3-turbo` fine-tune
- 專門針對台語 ASR
- 國科會產學合作計畫（2024/09 ~ 2025/06）
- HuggingFace: https://huggingface.co/NUTN-KWS/Whisper-Taiwanese-model-v0.5

### TAIDE 計畫相關
- 台灣國科會主導的可信賴 AI 對話引擎
- 已有台語、客語 ASR 相關研究
- 最新模型 Gemma-3-TAIDE-12b-Chat-2602（2026/02 發布）
- 國網中心正在建置台灣族群語言 AI 語料庫

### Retell 語言支援限制
原生支援的語言不含台語：
- 有 zh-CN（中文-中國）
- **沒有台語 (Hokkien/Minnan)**
- 需要透過 custom STT 整合自建台語服務

### 修正後的整合架構
```
┌─────────────────────────────────────────────────────────┐
│                    Retell AI Platform                    │
├─────────────────────────────────────────────────────────┤
│  Phone Call                                             │
│      ↓                                                  │
│  stt_mode: "custom"                                     │
│  custom_stt_config → Our Taiwanese ASR Server           │
│      (NUTN Whisper-Taiwanese-model-v0.5)               │
│      ↓                                                  │
│  Transcript (台語 → 文字)                                │
│      ↓                                                  │
│  LLM Response (Custom LLM WebSocket)                   │
│      ↓                                                  │
│  TTS → ElevenLabs/MiniMax multilingual                  │
│      (中文發音，近似台語腔調)                              │
│      ↓                                                  │
│  Audio Response → Phone Call                            │
└─────────────────────────────────────────────────────────┘
```

**TTS 策略調整：** 先用 ElevenLabs/MiniMax 的中文 multilingual voice，
不完美但可用。長期再研究台語 TTS 專用模型。

## 📋 待辦

- [x] 研究 Retell API custom STT 文件 ✅
- [x] 找到現成台語 Whisper 模型 (NUTN) ✅
- [ ] 在 Retell Community Forum 發帖詢問 custom STT
- [ ] 在 Retell Discord 發問
- [ ] 下載 NUTN Whisper 模型測試
- [ ] 建立 FastAPI server 包裝 Whisper 模型
- [ ] 找台語音訊樣本測試
- [ ] 設計 Retell WebSocket 橋接方案
- [ ] 評估 GPU hosting 方案

---

*Last updated: 2026-03-14*
