---
name: knowledge-framework
description: Compare the user's content against relevant knowledge frameworks, choose the most suitable one or ones without forcing weak matches, explain the definitions and reasons for selection, and rewrite the content through those frameworks. Use when the user asks for 知識框架, 套框架, SWOT, TOWS, 用框架改寫, 架構化分析, or when existing content should be reorganized through a formal analytical lens.
---

# 知識框架

## Objective

根據使用者輸入的文字，比對可用的知識框架，找出最相關的框架，並在最適用的段落套用。
可以不只一個框架，但必須合理、有意義，不要過度牽強。

## Startup Rule

If canvas is available and not yet started, start canvas and use it for drafting and editing.

## Required Workflow

1. Read the user's content carefully.
2. Compare the content against the knowledge frameworks available in references.
3. Choose the most relevant framework or frameworks.
4. First list the frameworks you will apply.
5. For each chosen framework, explain:
   - the framework definition
   - why it fits this task
   - which part of the content it will be applied to
6. Rewrite the content using the framework.
7. If no meaningful framework applies, reply exactly: `無可套用之框架`.

## Mandatory Rule

If you choose `SWOT`, you must also include `TOWS`.

## Selection Rule

- Prefer a small number of meaningful frameworks.
- Do not apply frameworks mechanically.
- Use only frameworks that improve clarity, structure, or actionability.
- If different sections clearly need different frameworks, state that explicitly.

## Output Order

1. Selected framework list
2. Definition and reason for each selected framework
3. Rewritten content with the framework applied

## Output Style

- Write in Traditional Chinese unless the user prefers otherwise.
- Keep definitions concise but concrete.
- Make the rewritten output feel native, not like framework labels pasted on top.

## References

- For framework selection and pairing guidance, read [references/framework-catalog.md](references/framework-catalog.md).

## Example Requests

- `請根據知識框架重寫這份市場進入分析`
- `幫我判斷這段商業描述適合套哪個框架，然後直接改寫`
- `用 SWOT 跟 TOWS 重整這份新產品策略草稿`
