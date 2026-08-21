---
date: 2026-04-13
type: test-report
topic: llm-wiki-regenerated-note-smoke-test
---

# llm-wiki Smoke Test Comparison

## 測試範圍

本次測試不是直接覆寫 vault 原筆記，而是依照更新後 `Agent\llm-wiki\SKILL.md` 的工作原則，對 3 份現有樣本做「重產稿」測試，輸出到目前專案的 `test-output/2026-04-13/`。

樣本來源：

- `Learning/youtube/Claude-Code-3-Skills-Save-2-Hours-rxXefCxpOok.md`
- `Learning/youtube/Nuwa-Skill-17大佬思维方式蒸馏-koRzYM3R-gg.md`
- `Learning/twitter/nftcps-agent-skills-115k-stars-2043174437810573522.md`

## 測試限制

- 目前沒有直接使用原始影片逐字稿或 tweet 原始抓取結果，主要以現有筆記內容與 `source_url` 作為 proxy input。
- 因此這是一個 `structure-and-linkage smoke test`，驗證的是：
  - 新 skill 的整理邏輯是否更一致
  - 關聯筆記與 wiki 入口是否更穩定
  - 風險與限制是否有被明講
- 這不是最終品質的 full re-ingest test。

## 样本一：Claude Code 3 Skills

原筆記特徵：

- 優點：資訊密度高，保留很多案例細節
- 缺點：章節偏影片式整理，對「我為什麼要保留這篇」的提煉沒有那麼集中

重產稿改善：

- 開頭先抽出工作流層級的核心結論
- 把三個 skill 案例統一收束到同一主軸：高頻摩擦的流程封裝
- 加入明確的 `風險與限制`
- `關聯筆記` 保留 index / repo / 同主題影片三種層級

判斷：

- 原稿比較像「詳細課堂筆記」
- 重產稿比較像「能進 wiki 長期保留的主題筆記」

## 样本二：Nuwa Skill

原筆記特徵：

- 優點：內容豐富，幾乎已經是一份長篇方法論整理
- 缺點：資訊很多，但層次稍微平鋪，重點與邊界有時混在一起

重產稿改善：

- 先用摘要把「不是 role-play，而是 cognitive system extraction」定錨
- 把五層結構與六路採集 / 三重驗證重新組成更清楚的論證順序
- 將「誠實邊界」升格成單獨的風險框架，而不是文末補充

判斷：

- 原稿適合深讀
- 重產稿適合當 wiki 的 canonical summary，再往下連原稿或 repo

## 样本三：Anthropic Agent Skills Tweet

原筆記特徵：

- 優點：快速、準確、可作為速報摘要
- 缺點：偏 tweet 摘要格式，對中長期知識用途來說，缺少結構化的「我會怎麼用」

重產稿改善：

- 把兩則消息拉進同一條 skill ecosystem 脈絡
- 明確區分「能力封裝層」與「學習入口層」
- 補入 `我會怎麼用這篇文章`，更符合 Pigo 長期知識庫的整理習慣

判斷：

- 原稿適合保存訊息
- 重產稿更適合做 topic hub 的子頁或概念索引入口

## 整體結論

更新後的 `llm-wiki` 邏輯，在這 3 個樣本上的主要改善方向是：

- 更像 wiki 的 canonical page，而不是一次性的素材摘要
- 更清楚區分 `核心結論 / 分析 / 風險 / 使用方式`
- 更穩定地把內容連回 index、repo、主題頁與 landing page
- 更符合「query / ingest 都應該讓知識庫變好」的思路

目前仍未驗證的部分：

- 真正用原始 transcript 或原始 tweet 內容做 full re-ingest
- 將更新後 skill 同步進 vault runtime `.codex/skills/llm-wiki/` 後的真實執行結果

## 建議下一步

1. 先決定是否要把更新同步到 vault runtime skill
2. 若要正式驗證，再挑 1 個 YouTube + 1 個 Twitter 樣本做 full re-ingest
3. full re-ingest 時直接抓原始來源，而不是只用既有筆記做 proxy input
