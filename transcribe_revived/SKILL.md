---
name: transcribe
description: Use when the user or older docs still refer to the legacy skill name transcribe; immediately follow transcript-to-note instead for the current Codex-compatible workflow.
---

# transcribe

## Description

transcribe 已經是 legacy compatibility wrapper。  
目前請直接依照 transcript-to-note 的流程執行；這個 skill 的存在只是為了讓舊文件、舊習慣與舊指令名稱仍能正確導向新 canonical skill。

## Current Routing

- Legacy name: transcribe
- Canonical skill: transcript-to-note
- Focus: transcript intake, transcript structuring, and note draft generation

## How to Use

1. 若使用者明確提到 transcribe，不要沿用舊流程。
2. 立即改走 transcript-to-note。
3. 若舊流程與新 taxonomy 衝突，以 transcript-to-note 為準。

## Migration Note

這個 wrapper 不應再擴充新邏輯。  
所有後續能力都應加在 transcript-to-note，而不是 transcribe。

## Handoff

完成後若需要回報，請在結果中使用新 canonical 名稱 transcript-to-note。
