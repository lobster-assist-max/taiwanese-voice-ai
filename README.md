# 🇹🇼 Taiwanese Voice AI Integration

**專案代號：** TAIDE
**目標：** 將台語 ASR/TTS 整合到 Retell AI 平台
**時程：** 2026-03-14 ~ 2026-04-14（一個月）
**狀態：** 🟡 進行中 (25%)
**GitHub：** https://github.com/lobster-assist-max/taiwanese-voice-ai

---

## 📋 目標

讓 Retell AI 支援台語：
1. **ASR（語音辨識）：** 聽懂台語
2. **TTS（語音合成）：** 說台語

---

## 🛤️ 策略

### Phase 1：聯繫 Retell（Week 1-2）
- [x] 發送 email 詢問 custom ASR/TTS 整合 ✅ 3/14
- [x] 追蹤回覆 — email 無效，改走 Forum + Discord ✅ 3/18
- [x] 研究 Retell API 文件 — 確認 custom_stt_config 可用 ✅ 3/18
- [x] ✅ Retell Forum 帖子已發 https://community.retellai.com/t/custom-stt-integration-for-taiwanese-hokkien-using-self-hosted-whisper-model/1870
- [ ] ⚠️ **Alex 加入 Retell Discord 發問** https://discord.com/invite/wxtjkjj2zp
- [ ] 帖子內容在 `emails/02-retell-forum-post.md`，直接貼上

### Phase 2：技術準備（Week 2-3）
- [x] 找到台語 ASR 模型：NUTN-KWS/Whisper-Taiwanese-model-v0.5 ✅ 3/18
- [x] 建立 ASR Server（FastAPI + WebSocket + Retell endpoint）✅ 3/18
- [ ] 租 GPU server（RunPod A10G ~$0.44/hr）
- [ ] 部署 ASR server + 下載模型
- [ ] 找台語音訊樣本測試辨識效果
- [ ] 評估 TTS 方案（先用 ElevenLabs 中文 multilingual）

### Phase 3：整合（Week 3-4）
- [ ] 根據 Retell 的回應決定整合方式
- [ ] 連接 ASR server 到 Retell custom_stt_config
- [ ] 設定 LLM WebSocket
- [ ] 端到端測試（台語電話 → 辨識 → 回覆）

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

### 2026-03-29
- 17:18 定期檢查：Retell 仍無任何回覆（Email Day 15、Follow-up Day 9、Forum Day 11）
- 專案剩餘天數：16 天（截止 4/14）
- 進度報告已傳 Alex，請求決策：啟動 POC or 繼續等
- **自 3/23 以來無新進展，完全等待 Alex 決策中**

### 2026-03-23
- 09:00 自動檢查：Retell 仍無新回覆
  - Email: 原始信 Day 9，follow-up (Day 6) 發出已 3 天，無回覆
  - Forum: 帖子已 5 天無回覆
  - Forum Summary emails：只是社群摘要（hangup detection、dynamic variables），非我們帖子的回覆
  - Discord: Alex 尚未加入發問
- 專案剩餘天數：22 天（截止 4/14）
- **🚨 今天是決策日！已在 09:00 報告中通知 Alex，建議啟動 POC**
- 追蹤頻率：降為每日 1 次（09:00），不再一天 3 次
- 等待 Alex 回覆決定下一步

### 2026-03-22
- 09:48 自動檢查：Retell 仍無新回覆
  - Email: 原始信 Day 8，follow-up (Day 6) 發出已 2 天，無回覆
  - Forum: 帖子已 4 天無回覆
  - Discord: Alex 尚未加入發問
- 專案剩餘天數：23 天（截止 4/14）
- **🚨 明天 3/23 是決策點 — 若仍無回覆，直接開始 POC（租 GPU、部署 Whisper）**
- 今日為週日，持續等待中
- Follow-up email 已超過 2 天無回覆，但明天就是決策日，不再發第二封 follow-up
- 12:09 中午檢查：仍無回覆，進度報告已傳 Alex
- 18:24 傍晚檢查：仍無回覆，進度報告已傳 Alex
- **今日總結：週日等待日。Email Day 8、Forum Day 4，均無回覆。明天 3/23 是決策點。**
- **明日計畫：** 3/23 決策日。如無回覆 → 通知 Alex 並啟動 POC（租 RunPod A10G、部署 Whisper-Taiwanese-model-v0.5）

### 2026-03-21
- 09:00 自動檢查：Retell 仍無新回覆
  - Email: 原始信 Day 7，follow-up (Day 6) 發出已 1 天，無回覆
  - Forum: 帖子已 3 天無回覆
  - Discord: Alex 尚未加入發問
- 專案剩餘天數：24 天（截止 4/14）
- **決策點倒數：3/23（後天）前無回覆 → 直接開始 POC**
- 今日為週六，持續等待中
- 12:00 中午檢查：仍無回覆，進度報告已傳 Alex
- 18:00 傍晚檢查：仍無回覆，進度報告已傳 Alex
- **今日總結：週六等待日。Email Day 7、Forum Day 3，均無回覆。3/23 決策點不變。**
- **明日計畫：** 繼續等待；3/23 若無回覆直接開始 POC（租 GPU、部署 Whisper）

### 2026-03-20
- 09:00 自動檢查：Retell 仍無新回覆
  - Email: 自動回覆導向 Forum（3/14），無人工回覆
  - Forum: 帖子 6 天無回覆
  - Forum Summary emails 只是一般社群摘要，非針對我們的回覆
- ✅ **已發 follow-up email**（Day 6）至 support@retellai.com
  - 強調已有 ASR server + Whisper model，只需確認整合路徑
- 專案剩餘天數：25 天（截止 4/14）
- 下一步：若 3 天內仍無回覆，考慮直接開始技術 POC 不等 Retell 確認
- 12:00 中午檢查：仍無回覆，進度報告已傳 Alex
- 18:00 傍晚檢查：follow-up email 也無回覆，進度報告已傳 Alex
- **今日總結：Email 第 6 天無回覆，已發 follow-up。決策點：3/23 前無回覆就直接開始 POC。**

### 2026-03-19
- 09:00 自動檢查：Email 5 天無回覆（管道無效），Forum 帖 ~1 天無回覆
- 12:00 中午檢查：仍無回覆，進度報告已傳 Alex
- 18:00 傍晚檢查：仍無回覆（Forum 帖已 ~2 天）
- **今日總結：等待日，無技術進展。Email 管道已確認無效，Forum 帖仍在等待。**
- **明日計畫：**
  1. 如果 Forum 仍無回覆（超過 48 小時），在帖子上 bump
  2. 建議不再等，直接開始台語 ASR POC（租 GPU、部署 Whisper 模型）
  3. 追蹤 Alex 是否到 Retell Discord 發問

### 2026-03-18
- 09:00 自動檢查：Retell 無新回覆（僅收到自動回覆導向 Forum/Discord）
- 已過 4 天，email 管道確認無效
- **12:30 全面研究 Retell API 文件 + 台語 ASR 生態系**
- **關鍵發現：**
  1. Retell 有 `custom_stt_config` 可以接自訂 STT provider（設 `stt_mode: "custom"`）
  2. Retell 原生支援語言不含台語（只有 zh-CN）
  3. HuggingFace 有現成模型：`NUTN-KWS/Whisper-Taiwanese-model-v0.5`（台南大學，基於 whisper-large-v3-turbo）
  4. TAIDE 計畫有台語 ASR 相關資源
  5. Retell Community Forum: https://community.retellai.com/
  6. Retell Discord: https://discord.com/invite/wxtjkjj2zp
- **✅ Retell Community Forum 帖子已發布！**
  - URL: https://community.retellai.com/t/custom-stt-integration-for-taiwanese-hokkien-using-self-hosted-whisper-model/1870
  - 帳號: lobster-assist (lobster-assist@goldenraintree.tw)
- **準備 Retell Discord 訊息**
- **研究結果 push 到 GitHub** (04b1a32)
- **更新技術評估 + 整合架構**
- ⚠️ 需要 Alex 手動發帖到 Retell Forum + Discord（bot 無法加入外部 server）
- 15:07 收到 Retell 帳號驗證碼 email（非詢問回覆，是註冊驗證）
- 18:00 傍晚進度報告

### 2026-03-17
- Retell AI 仍未回覆（已過 72+ 小時）
- 12:00 中午進度報告已傳送給 Alex
- 計畫轉戰 Retell Discord 發問（明日執行）
- 建議：同步開始台語 ASR 技術 POC，不再等回覆

### 2026-03-16
- 等待 Retell AI 回覆中（已過 48 小時）
- 週日休息日
- 明日若仍無回覆，轉戰 Discord

### 2026-03-15
- 等待 Retell AI 回覆中（已過 24 小時）
- 無新進度，持續追蹤

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

*Last updated: 2026-03-22*
epo
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

*Last updated: 2026-03-18*
