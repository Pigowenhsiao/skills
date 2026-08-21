---
name: vault-audit
description: Use when the user or older docs still refer to the legacy skill name vault-audit; immediately follow vault-check instead for the current Codex-compatible workflow.
---

# vault-audit

## Description

vault-audit 已經是 legacy compatibility wrapper。
目前請直接依照 vault-check 的流程執行；這個 skill 的存在只是為了讓舊文件、舊習慣與舊指令名稱仍能正確導向新 canonical skill。

## Current Routing

- Legacy name: vault-audit
- Canonical skill: vault-check
- Focus: low-frequency full-vault health check and audit-first maintenance

## How to Use

1. 若使用者明確提到 vault-audit，不要沿用舊流程。
2. 立即改走 vault-check。
3. 若舊流程與新 taxonomy 衝突，以 vault-check 為準。

## Migration Note

這個 wrapper 不應再擴充新邏輯。
所有後續能力都應加在 vault-check，而不是 vault-audit。

## Handoff

完成後若需要回報，請在結果中使用新 canonical 名稱 vault-check。
