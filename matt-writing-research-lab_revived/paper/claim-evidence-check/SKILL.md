---
name: claim-evidence-check
description: Audit whether each conclusion in a paper summary or research note is supported by the cited source, and flag extrapolation, missing evidence, or blended author/analyst voice. Use when validating paper summaries, research notes, or chapter-level analyses.
---

# Claim Evidence Check

## Description

這顆 skill 專門檢查「你寫出來的每個重點，到底有沒有證據撐住」。它適合放在論文摘要完成後，做一次可信度稽核。

## Workflow

1. 先讀兩份東西：
   - 原始來源
   - 已寫出的摘要或分析稿
2. 把稿件中的關鍵主張逐條列出。
3. 逐條分類：
   - 有直接證據支持
   - 只能算合理推論
   - 證據不足
   - 與來源不一致
4. 特別檢查兩類高風險句子：
   - 過度擴大結果的商業或產業意義
   - 把分析者評論寫成作者原結論
5. 對每個問題主張提出修法：
   - 改寫
   - 降低語氣
   - 加上限定詞
   - 直接刪除

## Guardrails

- 不要因為句子流暢就放過證據缺口。
- 不要用常識替代論文證據。
- 對「看起來很合理」的延伸評論要特別嚴格。

## Output

輸出一份 claim audit：
- 主張
- 證據狀態
- 問題類型
- 建議修法
