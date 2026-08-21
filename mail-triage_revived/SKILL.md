---
name: mail-triage
description: Use when the user wants to triage email into actionable buckets or vault notes, while recognizing that live email connectors may not yet be enabled in the current Codex runtime.
---

# Mail Triage

## Description

mail-triage 是 email workflow 的 Codex-compatible 入口。  
目前屬 deferred-mode：保留 skill 發現性與流程骨架，但不假裝已啟用完整 live email integration。

## Current Mode

- 可整理使用者提供的 email 文字
- 可規劃 triage 規則
- 若未啟用連接器，不直接聲稱可掃 live inbox
