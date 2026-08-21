---
name: email-triage
description: Use when the user or older docs still refer to the legacy skill name email-triage; immediately follow mail-triage instead for the current Codex-compatible workflow.
---

# email-triage


## Folder Context Before Placement

Before creating, moving, reclassifying, or updating any durable note, study the local folder context first so the note lands in the correct place.

Required reading order:
1. Read the vault root `AGENTS.md`.
2. Read the `README.md` in the candidate destination folder when it exists.
3. Walk upward from the candidate destination folder to the vault root and read each available parent `README.md`.
4. When comparing multiple candidate folders, read each candidate folder's local `README.md` before choosing.

Placement rules:
- Treat `AGENTS.md` as the global control plane and folder `README.md` files as local placement contracts.
- Use folder `README.md` content to understand purpose, accepted note types, naming conventions, index expectations, and sensitive-content boundaries.
- If a folder has no `README.md`, do not invent rules for it. Infer conservatively from `AGENTS.md`, nearby `index.md`, existing notes, and the user's explicit instruction.
- If folder guidance conflicts, follow this priority: user instruction, vault root `AGENTS.md`, nearest folder `README.md`, parent folder `README.md`, then this skill.
- If the correct folder is still ambiguous after reading context, pause and ask Pigo instead of filing the note into a guessed location.

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
