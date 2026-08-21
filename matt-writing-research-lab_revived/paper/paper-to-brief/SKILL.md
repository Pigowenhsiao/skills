---
name: paper-to-brief
description: Turn a paper or research source into a concise writing brief that defines audience, depth, coverage, and output constraints before any long summary is drafted. Use when the user wants a paper summary, explainer, or slide-ready research note but the target form is not yet fixed.
---

# Paper To Brief

## Description

這顆 skill 先把「論文要怎麼被摘要」定義清楚。它不直接產出長摘要，而是先決定摘要的目的、讀者、深度與輸出形式。

## Workflow

1. 先確認來源：
   - 論文本體
   - 補充 repo
   - 補充文章或投影片
2. 問清楚這份摘要要給誰看：
   - 自己研究用
   - 給非專業讀者
   - 給團隊簡報
   - 給投資／商業判讀
3. 定義輸出深度：
   - 短摘要
   - 長摘要
   - 章節級深讀
   - 簡報骨架
4. 明確指定要覆蓋哪些部分：
   - 背景
   - 文獻位置
   - 方法
   - 結果
   - 限制
   - 意義
5. 產出一份 paper brief，交給 `paper-summary-expand` 或其他後續 skill。

## Guardrails

- 不要在 brief 階段偷做長篇解讀。
- 不要把所有論文都當成需要章節級深讀。
- 如果讀者不需要方法細節，就明確收斂輸出。

## Output

輸出：
- 目標讀者
- 摘要目的
- 輸出深度
- 必須覆蓋章節
- 不需要展開的範圍
