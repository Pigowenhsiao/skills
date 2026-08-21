---
name: draft-diagnose
description: Diagnose weaknesses in a draft by checking structure, evidence, clarity, tone, redundancy, and AI-writing artifacts. Use when a draft exists and needs targeted revision instead of blind rewriting.
---

# Draft Diagnose

## Description

這顆 skill 用來檢查草稿到底壞在哪裡，避免「整篇重寫」這種高成本但低精度的處理方式。

## Workflow

1. 先確認文稿類型：
   - 一般文章
   - 論文摘要
   - 長篇小說章節
2. 用六個面向檢查：
   - 結構是否清楚
   - 證據是否夠
   - 語句是否清楚
   - 語氣是否一致
   - 是否冗贅或重複
   - 是否有明顯 AI 味
3. 對每個問題標記：
   - 嚴重程度
   - 具體位置
   - 建議修法
4. 若問題不在句子，而在大綱，回退到 `to-outline`。
5. 若問題是來源失真，回退到 `source-grill`。

## Guardrails

- 不要只說「不自然」；一定要指出哪裡不自然。
- 不要一次給太多抽象建議，要能直接修改。
- 不要因為表面順就忽略證據缺口。

## Output

輸出一份診斷報告，包含：
- 問題列表
- 優先順序
- 建議修法
- 是否需要回退到前一個 workflow
