---
name: paper-summary-expand
description: Expand a paper into a structured chapter-level summary covering background, literature context, methods, results, limitations, and conclusions without drifting beyond the source. Use when the user wants a deep paper walkthrough rather than a short abstract summary.
---

# Paper Summary Expand

## Description

把論文從短摘要擴成章節級解讀。這顆 skill 的目標不是加長字數，而是忠實重建研究脈絡。

## Workflow

1. 先確認來源邊界，必要時先跑 `source-grill`。
2. 讀論文時按章節抽取：
   - 研究背景
   - 問題定義
   - 文獻探討
   - 方法
   - 實驗設計
   - 結果
   - 限制
   - 結論
3. 每一節都用兩層寫法：
   - 作者原意
   - 分析者的整理與解釋
4. 若論文缺少某個標準章節，就明講，不要硬補。
5. 收尾時整理三類結論：
   - 這篇論文做了什麼
   - 它的重要性在哪
   - 它的限制與下一步是什麼

## Guardrails

- 不要把自己的延伸評論寫成論文作者的主張。
- 不要只重寫 abstract；要覆蓋論文內文。
- 缺資訊時，明講缺口，不要猜。

## Output

輸出一份章節級研究摘要，可直接用於：
- 長版 llm-wiki
- 簡報講稿
- 深讀筆記
- 研究報告骨架
