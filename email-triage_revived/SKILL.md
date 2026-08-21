---
name: email-triage
description: Use when the user or older docs still refer to the legacy skill name email-triage; immediately follow mail-triage instead for the current Codex-compatible workflow.
---

# email-triage

## Description

email-triage 已經是 legacy compatibility wrapper。  
目前請直接依照 mail-triage 的流程執行；這個 skill 的存在只是為了讓舊文件、舊習慣與舊指令名稱仍能正確導向新 canonical skill。

## Current Routing

- Legacy name: email-triage
- Canonical skill: mail-triage
- Focus: email triage in a Codex-compatible deferred mode

## How to Use

1. 若使用者明確提到 email-triage，不要沿用舊流程。
2. 立即改走 mail-triage。
3. 若舊流程與新 taxonomy 衝突，以 mail-triage 為準。

## Migration Note

這個 wrapper 不應再擴充新邏輯。  
所有後續能力都應加在 mail-triage，而不是 email-triage。

## Handoff

完成後若需要回報，請在結果中使用新 canonical 名稱 mail-triage。
