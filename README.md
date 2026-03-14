# 🇹🇼 Taiwanese Voice AI Integration

**專案代號：** TAIDE
**目標：** 將台語 ASR/TTS 整合到 Retell AI 平台
**時程：** 2026-03-14 ~ 2026-04-14（一個月）
**狀態：** 🟡 進行中
**GitHub：** https://github.com/lobster-assist-max/taiwanese-voice-ai

---

## 📋 目標

讓 Retell AI 支援台語：
1. **ASR（語音辨識）：** 聽懂台語
2. **TTS（語音合成）：** 說台語

---

## 🛤️ 策略

### Phase 1：聯繫 Retell（Week 1-2）
- [ ] 發送 email 詢問 custom ASR/TTS 整合
- [ ] 追蹤回覆
- [ ] 評估他們的回應

### Phase 2：技術準備（Week 2-3）
- [ ] 部署台語 ASR 服務（Whisper fine-tune）
- [ ] 部署台語 TTS 服務（Tacotron2）
- [ ] 測試 API endpoint

### Phase 3：整合（Week 3-4）
- [ ] 根據 Retell 的回應決定整合方式
- [ ] 實作整合
- [ ] 測試

---

## 📧 Communications Log

| 日期 | 對象 | 內容 | 狀態 |
|-----|------|------|------|
| 2026-03-14 | Retell AI | 初次詢問 custom ASR/TTS | 📤 已發送 |

---

## 🔗 資源

### 台語 ASR
- [ChineseTaiwaneseWhisper](https://github.com/sandy1990418/ChineseTaiwaneseWhisper)
- [中研院 Speech Research](https://github.com/sinica-speech)

### 台語 TTS
- [Taiwanese-Speech-Synthesis](https://github.com/ga642381/Taiwanese-Speech-Synthesis)

### Retell AI
- [Docs](https://docs.retellai.com/)
- [Custom LLM WebSocket](https://docs.retellai.com/api-references/llm-websocket)
- [Create Agent API](https://docs.retellai.com/api-references/create-agent)
- [Discord](https://discord.com/invite/retellai) ⬅️ 可以在這裡發問
- [LinkedIn](https://www.linkedin.com/company/retellai)
- 創辦人：Yan Wang

---

## 📝 Daily Log

### 2026-03-14
- 專案啟動
- 研究 Retell AI 架構
- 發現 `custom_stt_config` 已支援 Azure，可能可以擴展
- 發送初次詢問 email 至 support@retellai.com
- 建立 GitHub repo
- 設定 3 個追蹤 cron jobs（09:00, 12:00, 18:00）
- 找到 Retell Discord 和 LinkedIn
- 研究台語 ASR 開源專案（ChineseTaiwaneseWhisper）
  - 支援 Whisper fine-tune + LoRA
  - 有 streaming 模式
  - T4 GPU 可跑，1:24 效能

---

## 💰 預算需求

| 項目 | 估計費用 | 狀態 |
|-----|---------|------|
| GPU Server（ASR/TTS hosting）| ~$50-100/月 | 待確認 |
| Retell AI 費用 | 依用量 | Alex 已有 |

---

*Last updated: 2026-03-14*
