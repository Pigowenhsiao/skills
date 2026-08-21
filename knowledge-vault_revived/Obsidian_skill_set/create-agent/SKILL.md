---
name: create-agent
description: Use when the user or older docs still refer to the legacy skill name create-agent; immediately follow agent-create instead for the current Codex-compatible workflow.
---

# create-agent

## Description

create-agent 已經是 legacy compatibility wrapper。
目前請直接依照 agent-create 的流程執行；這個 skill 的存在只是為了讓舊文件、舊習慣與舊指令名稱仍能正確導向新 canonical skill。

## Current Routing

- Legacy name: create-agent
- Canonical skill: agent-create
- Focus: new custom workflow or vault agent definition

## How to Use

1. 若使用者明確提到 create-agent，不要沿用舊流程。
2. 立即改走 agent-create。
3. 若舊流程與新 taxonomy 衝突，以 agent-create 為準。

## Migration Note

這個 wrapper 不應再擴充新邏輯。
所有後續能力都應加在 agent-create，而不是 create-agent。

## Handoff

完成後若需要回報，請在結果中使用新 canonical 名稱 agent-create。
