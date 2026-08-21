---
name: vault-check
description: Use when the user wants a low-frequency full-vault health check for duplicates, broken links, orphan notes, frontmatter drift, or classification inconsistency before deeper cleanup or restructuring.
---

# Vault Check


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

`vault-check` Ã¦ËœÂ¯ Pigo vault Ã§Å¡â€žÃ¤Â½Å½Ã©Â Â»Ã¥â€¦Â¨Ã¥Â±â‚¬Ã¦ÂªÂ¢Ã¦Å¸Â¥Ã¦Â¨Â¡Ã¥Â¼ÂÃ£â‚¬â€š
Ã¥Â®Æ’Ã§Å¡â€žÃ¥Â·Â¥Ã¤Â½Å“Ã¤Â¸ÂÃ¦ËœÂ¯Ã¥Â¤Â§Ã©â€¡ÂÃ¦â€Â¹Ã¦Âªâ€Ã¯Â¼Å’Ã¨â‚¬Å’Ã¦ËœÂ¯Ã¥â€¦Ë†Ã§â€Â¨ `.vault-index` Ã¥ÂÅ¡Ã¥â‚¬â„¢Ã©ÂÂ¸Ã§â€ºÂ¤Ã©Â»Å¾Ã¯Â¼Å’Ã¥â€ ÂÃ¨Â¼Â¸Ã¥â€¡ÂºÃ¤Â¸â‚¬Ã¤Â»Â½Ã¥ÂÂ¯Ã¥Å¸Â·Ã¨Â¡Å’Ã§Å¡â€žÃ¥ÂÂ¥Ã¥ÂºÂ·Ã¦ÂªÂ¢Ã¦Å¸Â¥Ã§ÂµÂÃ¦Å¾Å“Ã£â‚¬ÂÃ©Â¢Â¨Ã©Å¡ÂªÃ¥Ë†â€ Ã§Â´Å¡Ã¨Ë†â€¡Ã¥Â¾Å’Ã§ÂºÅ’Ã¥Â»ÂºÃ¨Â­Â°Ã£â‚¬â€š

## When to Use

Ã¤Â½Â¿Ã§â€Â¨Ã¦â„¢â€šÃ¦Â©Å¸Ã¯Â¼Å¡

- Ã¤Â½Â Ã¨Â¦ÂÃ¥ÂÅ¡Ã¦â€¢Â´Ã¥â‚¬â€¹ vault Ã§Å¡â€žÃ¥ÂÂ¥Ã¥ÂºÂ·Ã¦ÂªÂ¢Ã¦Å¸Â¥
- Ã¤Â½Â Ã¦â€¡Â·Ã§â€“â€˜Ã¦Å“â€°Ã©â€¡ÂÃ¨Â¤â€¡Ã§Â­â€ Ã¨Â¨ËœÃ£â‚¬ÂÃ¥Â­Â¤Ã¥â€¦â€™Ã§Â­â€ Ã¨Â¨ËœÃ£â‚¬ÂÃ¥Ë†â€ Ã©Â¡Å¾Ã¦Â¼â€šÃ§Â§Â»Ã¦Ë†â€“ index Ã©ÂÂºÃ¦Â¼Â
- Ã¥Â¤Â§Ã©â€¡ÂÃ¦ÂÂ¬Ã§Â§Â»Ã£â‚¬ÂÃ¥ÂË†Ã¤Â½ÂµÃ¦Ë†â€“Ã©â€¡ÂÃ¥Ë†â€ Ã©Â¡Å¾Ã¤Â¹â€¹Ã¥â€°ÂÃ¯Â¼Å’Ã¨Â¦ÂÃ¥â€¦Ë†Ã§â€ºÂ¤Ã©Â»Å¾Ã©Â¢Â¨Ã©Å¡Âª
- `vault-reshape` Ã¦Ë†â€“ `vault-deep-clean` Ã¥Å¸Â·Ã¨Â¡Å’Ã¥â€°ÂÃ¥Â¾Å’Ã¯Â¼Å’Ã©Å“â‚¬Ã¨Â¦ÂÃ¤Â¸â‚¬Ã¤Â»Â½Ã¥Å¸ÂºÃ¦Âºâ€“Ã¥Â Â±Ã¥â€˜Å 

Ã¤Â¸ÂÃ¨Â¦ÂÃ§â€Â¨Ã¥Å“Â¨Ã¯Â¼Å¡

- Ã¥â€“Â®Ã§Â¯â€¡Ã§Â­â€ Ã¨Â¨ËœÃ¦Â­Â£Ã¥Â¼ÂÃ¥Å’â€“Ã¯Â¼Å¡Ã¦â€Â¹Ã§â€Â¨ `note-update`
- `00-Inbox` Ã¥Â°ÂÃ¦â€°Â¹Ã¦Â¬Â¡Ã¦â€¢Â´Ã§Ââ€ Ã¯Â¼Å¡Ã¦â€Â¹Ã§â€Â¨ `inbox-check`
- Ã¥Â¤Â§Ã¨Â¦ÂÃ¦Â¨Â¡Ã§ÂµÂÃ¦Â§â€¹Ã©â€¡ÂÃ¦â€¢Â´Ã¯Â¼Å¡Ã¦â€Â¹Ã§â€Â¨ `vault-reshape`
- Ã¦Â·Â±Ã¥ÂºÂ¦Ã¤Â¿Â®Ã¥Â¾Â©Ã¨Ë†â€¡Ã¦â€°Â¹Ã¦Â¬Â¡Ã¦Â¸â€¦Ã§Ââ€ Ã¯Â¼Å¡Ã¦â€Â¹Ã§â€Â¨ `vault-deep-clean`

## Vault Index Usage

Ã¦Å Å  vault index Ã¨Â¦â€“Ã§â€šÂº primary lookupÃ¯Â¼Å’Ã¤Â¸ÂÃ¨Â¦ÂÃ¤Â¸â‚¬Ã©â€“â€¹Ã¥Â§â€¹Ã¥Â°Â±Ã¦Å¡Â´Ã¥Å â€ºÃ¦Å½Æ’Ã¦â€¢Â´Ã¥â‚¬â€¹ vaultÃ£â‚¬â€š

- Vault rootÃ¯Â¼Å¡
  `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian`
- Query toolÃ¯Â¼Å¡
  `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian\.vault-index\query_vault.py`
- DatabaseÃ¯Â¼Å¡
  `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian\.vault-index\notes.db`

Ã¥â€žÂªÃ¥â€¦Ë†Ã¦Å¸Â¥Ã©â‚¬â„¢Ã¤Âºâ€ºÃ¯Â¼Å¡

- `duplicate-candidates`
- `fts`
- `by-classification`
- `links-to`
- `links-from`

Ã¥Å½Å¸Ã¥â€°â€¡Ã¯Â¼Å¡

1. Ã¥â€¦Ë†Ã§â€Â¨ index Ã¦â€°Â¾Ã¥â‚¬â„¢Ã©ÂÂ¸Ã©â€ºâ€ Ã¥ÂË†
2. Ã¥â€ ÂÃ¥Â°ÂÃ©Â«ËœÃ©Â¢Â¨Ã©Å¡ÂªÃ¦Ë†â€“Ã©Â«ËœÃ¥Æ’Â¹Ã¥â‚¬Â¼Ã¥â‚¬â„¢Ã©ÂÂ¸Ã¥ÂÅ¡Ã©â‚¬ÂÃ¦Âªâ€Ã¦ÂªÂ¢Ã¦Å¸Â¥
3. Ã¥ÂÂªÃ¦Å“â€°Ã¥Å“Â¨ index Ã¤Â¸ÂÃ¥ÂÂ¯Ã§â€Â¨Ã£â‚¬ÂÃ¦Ë†â€“Ã¨Â¦ÂÃ©Â©â€”Ã¨Â­â€°Ã§Â´Â°Ã§Â¯â‚¬Ã¦â„¢â€šÃ¦â€°Â fallback Ã¥Ë†Â° `rg`

## Risk-Tier Contract

- `Low-risk`
  Ã¥ÂÂ¯Ã§â€ºÂ´Ã¦Å½Â¥Ã§â€Â¢Ã¥â€¡ÂºÃ¥Â Â±Ã¥â€˜Å Ã£â‚¬ÂÃ§ÂµÂ±Ã¨Â¨Ë†Ã£â‚¬ÂÃ¥â‚¬â„¢Ã©ÂÂ¸Ã¥ÂÂÃ¥â€“Â®Ã¨Ë†â€¡Ã¦ËœÅ½Ã§Â¢ÂºÃ¥ÂÂ¯Ã©â‚¬â€ Ã§Å¡â€žÃ¥Â°ÂÃ¥Å¾â€¹ hygiene Ã¥Â»ÂºÃ¨Â­Â°Ã£â‚¬â€š
- `Medium-risk`
  Ã¤Â¸ÂÃ§â€ºÂ´Ã¦Å½Â¥Ã¥Å¸Â·Ã¨Â¡Å’Ã£â‚¬â€šÃ¦â€¢Â´Ã§Ââ€ Ã¦Ë†Â `Pending Approval Plan`Ã¯Â¼Å’Ã¥Ë†â€”Ã¥â€¡ÂºÃ§Â²Â¾Ã§Â¢ÂºÃ¨Â·Â¯Ã¥Â¾â€˜Ã£â‚¬ÂÃ¥Â»ÂºÃ¨Â­Â°Ã¥â€¹â€¢Ã¤Â½Å“Ã£â‚¬ÂÃ¥â€ºÅ¾Ã¦Â»Â¾Ã¦â€“Â¹Ã¥Â¼ÂÃ£â‚¬â€š
- `High-risk`
  Ã¤Â¸ÂÃ¥Å“Â¨ `vault-check` Ã¥â€¦Â§Ã¥Å¸Â·Ã¨Â¡Å’Ã£â‚¬â€šÃ¦â€¡â€°Ã¨Â½â€°Ã§ÂµÂ¦ `vault-reshape` Ã¦Ë†â€“ `vault-deep-clean`Ã£â‚¬â€š

## Audit Workflow

### 1. Coverage Scan

Ã§â€ºÂ¤Ã©Â»Å¾Ã¦â€¢Â´Ã©Â«â€Ã¨Â¦ÂÃ¦Â¨Â¡Ã¨Ë†â€¡Ã¤Â¸Â»Ã¨Â¦ÂÃ¥Ââ‚¬Ã¥Â¡Å Ã¯Â¼Å¡

- note Ã¦â€¢Â¸Ã©â€¡Â
- Ã¤Â¸Â»Ã¥Ë†â€ Ã©Â¡Å¾Ã¨Â¦â€ Ã¨â€œâ€¹
- Ã¦Å“â‚¬Ã¨Â¿â€˜Ã¦â€ºÂ´Ã¦â€“Â°Ã§â€ Â±Ã¥Ââ‚¬
- `youtube/twitter` Ã©â‚¬â„¢Ã©Â¡Å¾Ã¤Â¾â€ Ã¦ÂºÂÃ¥Å¾â€¹Ã¦Â®ËœÃ§â€¢â„¢Ã¥Ââ‚¬Ã¥Â¡Å 

### 2. Duplicate Review

Ã¦ÂªÂ¢Ã¦Å¸Â¥Ã¯Â¼Å¡

- Ã¥ÂÅ’Ã¦Â¨â„¢Ã©Â¡Å’Ã§Â«Â¶Ã§Ë†Â­Ã©Â Â
- Ã¥ÂÅ’ `source_url` Ã§Â«Â¶Ã§Ë†Â­Ã©Â Â
- Ã©Â«ËœÃ¥ÂºÂ¦Ã§â€ºÂ¸Ã¨Â¿â€˜Ã§Å¡â€žÃ¦Â­Â£Ã¥Â¼ÂÃ§Â­â€ Ã¨Â¨Ëœ

Ã¨Â¼Â¸Ã¥â€¡ÂºÃ¯Â¼Å¡

- Ã¥ÂÂ¯Ã§â€ºÂ´Ã¦Å½Â¥Ã¦Å½â€™Ã©â„¢Â¤Ã§Å¡â€žÃ¥Ââ€¡Ã©â„¢Â½Ã¦â‚¬Â§
- Ã©Å“â‚¬Ã¨Â¦ÂÃ¤ÂºÂºÃ¥Â·Â¥Ã¥Ë†Â¤Ã¦â€“Â·Ã§Å¡â€ž merge candidates

### 3. Link Health

Ã¦ÂªÂ¢Ã¦Å¸Â¥Ã¯Â¼Å¡

- broken wikilinks
- orphan notes
- Ã¥ÂÂªÃ¥â€¡ÂºÃ§ÂÂ¾Ã¥Å“Â¨Ã¥â€“Â®Ã¤Â¸â‚¬Ã¥Â­Â¤Ã§Â«â€¹Ã¥Ââ‚¬Ã¥Â¡Å Ã§Å¡â€žÃ§Â­â€ Ã¨Â¨Ëœ
- Ã¦â€¡â€°Ã¨Â¢Â« `index.md` Ã¦Ë†â€“Ã¤Â¸Â»Ã©Â¡Å’Ã©Â ÂÃ¦â€Â¶Ã©Å’â€žÃ¤Â½â€ Ã¥Â°Å¡Ã¦Å“ÂªÃ¦â€Â¶Ã©Å’â€žÃ§Å¡â€žÃ¥â€¦Â§Ã¥Â®Â¹

### 4. Metadata Health

Ã¦ÂªÂ¢Ã¦Å¸Â¥Ã¯Â¼Å¡

- frontmatter Ã§Â¼ÂºÃ¦Â¬â€ž
- `classification_path` Ã¨Ë†â€¡Ã¥Â¯Â¦Ã©Å¡â€ºÃ¨Â·Â¯Ã¥Â¾â€˜Ã¤Â¸ÂÃ¤Â¸â‚¬Ã¨â€¡Â´
- `processed` / `status` Ã¤Â¸ÂÃ¥ÂË†Ã§Ââ€ 
- `Source` Ã¨Ë†â€¡ `source_url` Ã§Â´â‚¬Ã©Å’â€žÃ¤Â¸ÂÃ¤Â¸â‚¬Ã¨â€¡Â´

### 5. Navigation Health

Ã¦ÂªÂ¢Ã¦Å¸Â¥Ã¯Â¼Å¡

- `index.md` Ã¦ËœÂ¯Ã¥ÂÂ¦Ã§Â¼ÂºÃ¥â€¦Â¥Ã¥ÂÂ£
- Ã¦ËœÂ¯Ã¥ÂÂ¦Ã¥Â­ËœÃ¥Å“Â¨Ã¥â‚¬Â¼Ã¥Â¾â€”Ã§ÂÂ¨Ã§Â«â€¹Ã¦Ë†ÂÃ¤Â¸Â»Ã©Â¡Å’Ã©Â ÂÃ§Å¡â€ž cluster
- Ã¦ËœÂ¯Ã¥ÂÂ¦Ã¦Å“â€°Ã¤Â¾â€ Ã¦ÂºÂÃ¥Å¾â€¹Ã¥Ë†â€ Ã©Â¡Å¾Ã¦Â®ËœÃ§â€¢â„¢Ã¯Â¼Å’Ã¦â€¡â€°Ã¦â€Â¶Ã¦â€“â€šÃ¦Ë†ÂÃ¤Â¸Â»Ã©Â¡Å’Ã¥Å¾â€¹Ã¥Ë†â€ Ã©Â¡Å¾

## Expected Output

Ã¨Â¼Â¸Ã¥â€¡ÂºÃ¦â€¡â€°Ã¨â€¡Â³Ã¥Â°â€˜Ã¥Å’â€¦Ã¥ÂÂ«Ã¯Â¼Å¡

- `Ã¦Â Â¸Ã¥Â¿Æ’Ã§ÂµÂÃ¨Â«â€“`
- `Ã¤Â¸Â»Ã¨Â¦ÂÃ©Â¢Â¨Ã©Å¡Âª`
- `Ã¥ÂÂ¯Ã§â€ºÂ´Ã¦Å½Â¥Ã¨â„¢â€¢Ã§Ââ€ Ã§Å¡â€ž low-risk Ã©Â â€¦Ã§â€ºÂ®`
- `Pending Approval Plan`
- `Ã¥Â»ÂºÃ¨Â­Â°Ã¤Â¸â€¹Ã¤Â¸â‚¬Ã¦Â­Â¥`

Ã¨â€¹Â¥Ã¦Å“â€°Ã¥Â¯Â¦Ã©Å¡â€ºÃ§â€Â¢Ã¥â€¡ÂºÃ¦Âªâ€Ã¦Â¡Ë†Ã¯Â¼Å’Ã¥â€žÂªÃ¥â€¦Ë†Ã¦â€Â¾Ã¥Å“Â¨Ã¯Â¼Å¡

- `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian\.vault-index\`
  Ã¦Ë†â€“
- Ã§â€¢Â¶Ã¥â€°ÂÃ¥Â°Ë†Ã¦Â¡Ë†Ã¦â€“â€¡Ã¤Â»Â¶Ã¥Ââ‚¬

## Common Mistakes

- Ã¦Å Å  `vault-check` Ã§â€¢Â¶Ã¦Ë†ÂÃ¥â€¦Â¨Ã©ÂÂ¢Ã¦â€Â¹Ã¦Âªâ€Ã¥Â·Â¥Ã¥â€¦Â·
- Ã¤Â¸ÂÃ§Â¶â€œÃ©ÂÅ½ index Ã¥Â°Â±Ã§â€ºÂ´Ã¦Å½Â¥Ã¥â€¦Â¨ vault Ã¦Å½Æ’Ã¦ÂÂ
- Ã¦Å Å Ã§ÂµÂÃ¦Â§â€¹Ã©â€¡ÂÃ¦â€¢Â´Ã¦Â·Â·Ã©â‚¬Â² audit
- Ã¥ÂÂªÃ¥Ë†â€”Ã¥â€¢ÂÃ©Â¡Å’Ã¯Â¼Å’Ã¤Â¸ÂÃ¥Ë†â€”Ã§Â²Â¾Ã§Â¢ÂºÃ¨Â·Â¯Ã¥Â¾â€˜Ã¨Ë†â€¡Ã¥Â»ÂºÃ¨Â­Â°Ã¥â€¹â€¢Ã¤Â½Å“
- Ã¦Å Å Ã¥â€“Â®Ã§Â¯â€¡Ã¤Â¿Â®Ã¨Â£Å“Ã¥Â·Â¥Ã¤Â½Å“Ã¥Â¡Å¾Ã©â‚¬Â²Ã¥â€¦Â¨Ã¥Â±â‚¬ audit

## Handoff

`vault-check` Ã¥Â®Å’Ã¦Ë†ÂÃ¥Â¾Å’Ã¯Â¼Å’Ã¤Â¸â€¹Ã¤Â¸â‚¬Ã¦Â­Â¥Ã©â‚¬Å¡Ã¥Â¸Â¸Ã¦ËœÂ¯Ã¯Â¼Å¡

- `vault-reshape`
- `vault-deep-clean`
- `tag-check`
- Ã¦Ë†â€“Ã¥â€ºÅ¾Ã¥Ë†Â° `note-update` / `inbox-check` Ã¥ÂÅ¡Ã¥Â®Å¡Ã©Â»Å¾Ã¤Â¿Â®Ã¨Â£Å“

<!-- AGENT_SKILL_DEDUPE_NOTE -->
## Duplicate Consolidation

This is the canonical vault-check Skill after Agent dedupe on 2026-04-29.

Archived duplicate variants:
- Obsidian_skill_set/vault-check/SKILL.merged.md
- skills/vault-check/SKILL.merged.md
<!-- /AGENT_SKILL_DEDUPE_NOTE -->
