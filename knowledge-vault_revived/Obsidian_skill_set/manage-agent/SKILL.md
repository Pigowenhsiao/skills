---
name: manage-agent
description: Use when the user or older docs still refer to the legacy skill name manage-agent; immediately follow agent-manage instead for the current Codex-compatible workflow.
---

# manage-agent

## Description

manage-agent 已經是 legacy compatibility wrapper。
目前請直接依照 agent-manage 的流程執行；這個 skill 的存在只是為了讓舊文件、舊習慣與舊指令名稱仍能正確導向新 canonical skill。

## Current Routing

- Legacy name: manage-agent
- Canonical skill: agent-manage
- Focus: inspection, rename, retirement, and maintenance of custom agents

## How to Use

1. 若使用者明確提到 manage-agent，不要沿用舊流程。
2. 立即改走 agent-manage。
3. 若舊流程與新 taxonomy 衝突，以 agent-manage 為準。

## Migration Note

這個 wrapper 不應再擴充新邏輯。
所有後續能力都應加在 agent-manage，而不是 manage-agent。

## Handoff

完成後若需要回報，請在結果中使用新 canonical 名稱 agent-manage。
