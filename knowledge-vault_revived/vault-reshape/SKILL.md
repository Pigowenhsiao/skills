---
name: vault-reshape
description: Use when the user wants to restructure the vault at the category, landing-page, or navigation level, especially after taxonomy drift, source-based folder sprawl, or repeated classification inconsistencies.
---

# Vault Reshape


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

`vault-reshape` Ã¦ËœÂ¯ Pigo vault Ã§Å¡â€žÃ§ÂµÂÃ¦Â§â€¹Ã©â€¡ÂÃ¦â€¢Â´Ã¦Â¨Â¡Ã¥Â¼ÂÃ£â‚¬â€š
Ã¥Â®Æ’Ã¨â„¢â€¢Ã§Ââ€ Ã§Å¡â€žÃ¦ËœÂ¯Ã¥Ë†â€ Ã©Â¡Å¾Ã¦â€Â¶Ã¦â€“â€šÃ£â‚¬ÂÃ¥Â°Å½Ã¨Ë†ÂªÃ¤Â¿Â®Ã¨Â£Å“Ã£â‚¬ÂÃ¤Â¾â€ Ã¦ÂºÂÃ¥Å¾â€¹Ã¨Â³â€¡Ã¦â€“â„¢Ã¥Â¤Â¾Ã©â‚¬â‚¬Ã¥Â Â´Ã£â‚¬ÂÃ¤Â¸Â»Ã©Â¡Å’Ã¥Å¾â€¹Ã¨ÂÂ½Ã©Â»Å¾Ã©â€¡ÂÃ¥Â»ÂºÃ¨Ë†â€¡Ã§ÂµÂÃ¦Â§â€¹Ã¥â‚¬â„¢Ã©ÂÂ¸Ã¨Â¦ÂÃ¥Å Æ’Ã¯Â¼Å’Ã¤Â¸ÂÃ¨Â²Â Ã¨Â²Â¬Ã¥â€“Â®Ã§Â¯â€¡Ã¥â€¦Â§Ã¥Â®Â¹Ã¦Â­Â£Ã¥Â¼ÂÃ¥Å’â€“Ã¯Â¼Å’Ã¤Â¹Å¸Ã¤Â¸ÂÃ¨Â²Â Ã¨Â²Â¬Ã¦Â·Â±Ã¥ÂºÂ¦Ã¦Â¸â€¦Ã§Ââ€ Ã£â‚¬â€š

## When to Use

Ã¤Â½Â¿Ã§â€Â¨Ã¦â„¢â€šÃ¦Â©Å¸Ã¯Â¼Å¡

- Ã¤Â¾â€ Ã¦ÂºÂÃ¥Å¾â€¹Ã¥Ë†â€ Ã©Â¡Å¾Ã¥Â·Â²Ã§Â¶â€œÃ¥Â¤Â±Ã¦Å½Â§Ã¯Â¼Å’Ã¤Â¾â€¹Ã¥Â¦â€š `youtube/`Ã£â‚¬Â`twitter/` Ã¤Â¹â€¹Ã©Â¡Å¾Ã§Å¡â€žÃ¦Â®ËœÃ§â€¢â„¢Ã¥Ââ‚¬Ã¥Â¡Å 
- Ã¥ÂÅ’Ã¤Â¸Â»Ã©Â¡Å’Ã¥â€¦Â§Ã¥Â®Â¹Ã¥Ë†â€ Ã¦â€¢Â£Ã¥Å“Â¨Ã¥Â¤Å¡Ã¥â‚¬â€¹Ã¨Â·Â¯Ã¥Â¾â€˜Ã¯Â¼Å’Ã¥Â°Å½Ã¨â€¡Â´Ã¥Â°Å½Ã¨Ë†ÂªÃ¨Ë†â€¡Ã§Â´Â¢Ã¥Â¼â€¢Ã¦Â·Â·Ã¤Âºâ€š
- Ã¦Å¸ÂÃ¤Âºâ€ºÃ¥Ë†â€ Ã©Â¡Å¾Ã¥Â·Â²Ã¤Â¸ÂÃ¥â€ ÂÃ¥ÂË†Ã§Ââ€ Ã¯Â¼Å’Ã©Å“â‚¬Ã¨Â¦ÂÃ¦â€Â¶Ã¦â€“â€šÃ£â‚¬ÂÃ¦ÂÂ¬Ã§Â§Â»Ã¦Ë†â€“Ã¦â€¹â€ Ã¥Ë†â€ 
- Ã¥Â¤Â§Ã©â€¡Â `index.md`Ã£â‚¬Âlanding pageÃ£â‚¬ÂÃ¤Â¸Â»Ã©Â¡Å’Ã©Â ÂÃ©Å“â‚¬Ã¨Â¦ÂÃ¤Â¸â‚¬Ã¨ÂµÂ·Ã¨ÂªÂ¿Ã¦â€¢Â´
- `vault-check` Ã¥Â·Â²Ã¦Å’â€¡Ã¥â€¡ÂºÃ§ÂµÂÃ¦Â§â€¹Ã¦â‚¬Â§Ã¥â€¢ÂÃ©Â¡Å’Ã¯Â¼Å’Ã©Å“â‚¬Ã¨Â¦ÂÃ¦Â­Â£Ã¥Â¼ÂÃ©â‚¬Â²Ã¨Â¡Å’ reshape

Ã¤Â¸ÂÃ¨Â¦ÂÃ§â€Â¨Ã¥Å“Â¨Ã¯Â¼Å¡

- Ã¥â€“Â®Ã§Â¯â€¡Ã¥â€¦Â§Ã¥Â®Â¹Ã¤Â¿Â®Ã¨Â£Å“Ã¯Â¼Å¡Ã¦â€Â¹Ã§â€Â¨ `note-update`
- `00-Inbox` Ã¦â€°Â¹Ã¦Â¬Â¡Ã¦Â¸â€¦Ã§Ââ€ Ã¯Â¼Å¡Ã¦â€Â¹Ã§â€Â¨ `inbox-check`
- Ã¥â€¦Â¨Ã¥Â±â‚¬Ã§â€ºÂ¤Ã©Â»Å¾Ã¤Â½â€ Ã¥Â°Å¡Ã¦Å“ÂªÃ¦Â±ÂºÃ¥Â®Å¡Ã¥Â¦â€šÃ¤Â½â€¢Ã©â€¡ÂÃ¦â€¢Â´Ã¯Â¼Å¡Ã¥â€¦Ë†Ã§â€Â¨ `vault-check`
- broken links / stale external links / Ã¦â€°Â¹Ã¦Â¬Â¡Ã¦Â¸â€¦Ã§Ââ€ Ã¯Â¼Å¡Ã¦â€Â¹Ã§â€Â¨ `vault-deep-clean`

## Vault Index Usage

`vault-reshape` Ã¥Â¿â€¦Ã©Â Ë†Ã¥â€¦Ë†Ã§â€Â¨ vault index Ã¦â€°Â¾ cluster Ã¨Ë†â€¡Ã§ÂµÂÃ¦Â§â€¹Ã¥â‚¬â„¢Ã©ÂÂ¸Ã¯Â¼Å’Ã¥â€ ÂÃ¥ÂÅ¡Ã§ÂµÂÃ¦Â§â€¹Ã¦Â±ÂºÃ§Â­â€“Ã£â‚¬â€š

- Vault rootÃ¯Â¼Å¡
  `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian`
- Query toolÃ¯Â¼Å¡
  `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian\.vault-index\query_vault.py`
- DatabaseÃ¯Â¼Å¡
  `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian\.vault-index\notes.db`

Ã¥â€žÂªÃ¥â€¦Ë†Ã¦Å¸Â¥Ã©â‚¬â„¢Ã¤Âºâ€ºÃ¯Â¼Å¡

- `by-classification`
- `fts`
- `related-notes`
- `links-to`
- `links-from`

Ã¥Å½Å¸Ã¥â€°â€¡Ã¯Â¼Å¡

1. Ã¥â€¦Ë†Ã¦â€°Â¾Ã¤Â¸Â»Ã©Â¡Å’ cluster Ã¨Ë†â€¡Ã¥Ë†â€ Ã©Â¡Å¾Ã¦Â¼â€šÃ§Â§Â»Ã§â€ Â±Ã¥Ââ‚¬
2. Ã¥â€ ÂÃ¦Â±ÂºÃ¥Â®Å¡Ã¦â€¡â€°Ã¦â€Â¶Ã¦â€“â€šÃ£â‚¬ÂÃ¥Ë†â€ Ã¦ÂµÂÃ£â‚¬ÂÃ¦ÂÂ¬Ã§Â§Â»Ã¦Ë†â€“Ã¥Â»ÂºÃ§Â«â€¹ landing page Ã§Å¡â€žÃ¥Ââ‚¬Ã¥Â¡Å 
3. Ã¥ÂÂªÃ¦Å“â€°Ã¥Å“Â¨ index Ã§â€žÂ¡Ã¦Â³â€¢Ã¨Â¦â€ Ã¨â€œâ€¹Ã§Â´Â°Ã§Â¯â‚¬Ã¦â„¢â€šÃ¦â€°Â fallback Ã¥Ë†Â° `rg`

## Risk-Tier Contract

- `Low-risk`
  Ã¥ÂÂ¯Ã§â€ºÂ´Ã¦Å½Â¥Ã¦â€¢Â´Ã§Ââ€ Ã§ÂµÂÃ¦Â§â€¹Ã¥Â Â±Ã¥â€˜Å Ã£â‚¬ÂÃ¦ÂÂ¬Ã§Â§Â»Ã¥â‚¬â„¢Ã©ÂÂ¸Ã¦Â¸â€¦Ã¥â€“Â®Ã£â‚¬Âindex Ã§Â¼ÂºÃ¥ÂÂ£Ã¦Â¸â€¦Ã¥â€“Â®Ã¨Ë†â€¡ landing page Ã¥Â»ÂºÃ¨Â­Â°Ã£â‚¬â€š
- `Medium-risk`
  Ã¤Â¸ÂÃ§â€ºÂ´Ã¦Å½Â¥Ã¥Å¸Â·Ã¨Â¡Å’Ã¦â€°Â¹Ã¦Â¬Â¡Ã¦ÂÂ¬Ã§Â§Â»Ã¦Ë†â€“Ã¥Â¤Â§Ã§Â¯â€žÃ¥Å“Â index Ã©â€¡ÂÃ¥Â¯Â«Ã£â‚¬â€šÃ¥â€¦Ë†Ã¥ÂÅ¡ `Pending Approval Plan`Ã£â‚¬â€š
- `High-risk`
  Ã¤Â¸ÂÃ¥Å“Â¨Ã¦Å“Â¬ skill Ã¨â€¡ÂªÃ¤Â¸Â»Ã¥Â®Å’Ã¦Ë†ÂÃ¦â€¢Â´Ã¥â‚¬â€¹ vault Ã¦â€Â¹Ã§â€°Ë†Ã£â‚¬â€šÃ¨â€¹Â¥Ã§â€°Â½Ã¦Â¶â€°Ã¥Â¤Â§Ã§Â¯â€žÃ¥Å“Â taxonomy redesignÃ¯Â¼Å’Ã¦â€¡â€°Ã¦â€¹â€ Ã¦Ë†ÂÃ¥Â¤Å¡Ã¦â€°Â¹Ã¦Â¬Â¡Ã¥Å¸Â·Ã¨Â¡Å’Ã£â‚¬â€š

## Reshape Workflow

### 1. Structure Scan

Ã§â€ºÂ¤Ã©Â»Å¾Ã¯Â¼Å¡

- Ã¥â€œÂªÃ¤Âºâ€ºÃ¨Â³â€¡Ã¦â€“â„¢Ã¥Â¤Â¾Ã¦ËœÂ¯Ã¤Â¾â€ Ã¦ÂºÂÃ¥Å¾â€¹Ã¥Ë†â€ Ã©Â¡Å¾
- Ã¥â€œÂªÃ¤Âºâ€ºÃ¤Â¸Â»Ã©Â¡Å’Ã¥Ë†â€ Ã©Â¡Å¾Ã¥Â·Â²Ã¦Ë†ÂÃ§â€šÂºÃ¥Â¯Â¦Ã©Å¡â€ºÃ§Å¸Â¥Ã¨Â­ËœÃ¤Â¸Â­Ã¥Â¿Æ’
- Ã¥â€œÂªÃ¤Âºâ€ºÃ¨Â·Â¯Ã¥Â¾â€˜Ã¥Â­ËœÃ¥Å“Â¨Ã©â€¡ÂÃ§â€“Å Ã¦Ë†â€“Ã§Â«Â¶Ã§Ë†Â­Ã©â€”Å“Ã¤Â¿â€š

### 2. Cluster Mapping

Ã§â€Â¨ index Ã¦â€°Â¾Ã¥â€¡ÂºÃ¯Â¼Å¡

- Ã¥â€¦Â§Ã¥Â®Â¹Ã©Â«ËœÃ¥ÂºÂ¦Ã§â€ºÂ¸Ã©â€”Å“Ã¤Â½â€ Ã¥Ë†â€ Ã¦â€¢Â£Ã¥Å“Â¨Ã¤Â¸ÂÃ¥ÂÅ’Ã¥Ë†â€ Ã©Â¡Å¾Ã§Å¡â€ž cluster
- Ã¦â€¡â€°Ã¥Ââ€¡Ã§Â´Å¡Ã¦Ë†ÂÃ§ÂÂ¨Ã§Â«â€¹Ã¤Â¸Â»Ã©Â¡Å’Ã©Â ÂÃ¦Ë†â€“ landing page Ã§Å¡â€žÃ§Â¾Â¤Ã§Âµâ€ž
- Ã¦â€¡â€°Ã¤Â½ÂµÃ¥â€¦Â¥Ã¦â€”Â¢Ã¦Å“â€° canonical category Ã§Å¡â€žÃ§Â¾Â¤Ã§Âµâ€ž

### 3. Target Taxonomy Proposal

Ã§â€šÂºÃ¦Â¯ÂÃ¥â‚¬â€¹Ã¥â‚¬â„¢Ã©ÂÂ¸Ã§Â¾Â¤Ã§Âµâ€žÃ¥Â®Å¡Ã§Â¾Â©Ã¯Â¼Å¡

- Ã§â€ºÂ®Ã¦Â¨â„¢Ã¥Ë†â€ Ã©Â¡Å¾
- Ã¦ËœÂ¯Ã¥ÂÂ¦Ã¦â€¡â€°Ã¦ÂÂ¬Ã§Â§Â»
- Ã¦ËœÂ¯Ã¥ÂÂ¦Ã¦â€¡â€°Ã¥ÂË†Ã¤Â½Âµ
- Ã¦ËœÂ¯Ã¥ÂÂ¦Ã¨Â¦ÂÃ¨Â£Å“ `index.md`
- Ã¦ËœÂ¯Ã¥ÂÂ¦Ã¨Â¦ÂÃ¥Â»ÂºÃ§Â«â€¹Ã¤Â¸Â»Ã©Â¡Å’Ã¥â€¦Â¥Ã¥ÂÂ£Ã©Â Â

### 4. Navigation Repair Plan

Ã¨Â¦ÂÃ¥Å Æ’Ã¯Â¼Å¡

- Ã¥â€œÂªÃ¤Âºâ€º `index.md` Ã¨Â¦ÂÃ¨Â£Å“Ã¥â€¦Â¥Ã¥ÂÂ£
- Ã¥â€œÂªÃ¤Âºâ€ºÃ¦â€”Â¢Ã¦Å“â€°Ã©Â ÂÃ©ÂÂ¢Ã¨Â¦ÂÃ¥ÂÅ¡Ã¦Å“â‚¬Ã¥Â°ÂÃ¥ÂÂÃ¥Ââ€˜Ã¤Â¿Â®Ã¨Â£Å“
- Ã¥â€œÂªÃ¤Âºâ€ºÃ¤Â¾â€ Ã¦ÂºÂÃ¥Å¾â€¹Ã¨Â³â€¡Ã¦â€“â„¢Ã¥Â¤Â¾Ã¥Â®Å’Ã¦Ë†ÂÃ©ÂÂ·Ã§Â§Â»Ã¥Â¾Å’Ã¥ÂÂ¯Ã©â‚¬â‚¬Ã¤Â¼â€˜

### 5. Execution Boundary

Ã§Å“Å¸Ã¦Â­Â£Ã¥Å¸Â·Ã¨Â¡Å’Ã¥â€°ÂÃ¨Â¦ÂÃ¦ËœÅ½Ã§Â¢ÂºÃ¥Ë†â€”Ã¥â€¡ÂºÃ¯Â¼Å¡

- Ã§Â²Â¾Ã§Â¢ÂºÃ¨Â·Â¯Ã¥Â¾â€˜
- Ã¦ÂÂ¬Ã§Â§Â»/Ã¥ÂË†Ã¤Â½ÂµÃ¦â€“Â¹Ã¥Â¼Â
- Ã¥Ââ€”Ã¥Â½Â±Ã©Å¸Â¿ index
- Ã¥â€ºÅ¾Ã¦Â»Â¾Ã¨Â·Â¯Ã¥Â¾â€˜

## Expected Output

Ã¨Â¼Â¸Ã¥â€¡ÂºÃ¨â€¡Â³Ã¥Â°â€˜Ã¨Â¦ÂÃ¦Å“â€°Ã¯Â¼Å¡

- `Ã¦Â Â¸Ã¥Â¿Æ’Ã§ÂµÂÃ¨Â«â€“`
- `Ã§â€ºÂ®Ã¥â€°ÂÃ§ÂµÂÃ¦Â§â€¹Ã¥â€¢ÂÃ©Â¡Å’`
- `Ã¥Â»ÂºÃ¨Â­Â°Ã§â€ºÂ®Ã¦Â¨â„¢Ã¥Ë†â€ Ã©Â¡Å¾`
- `Pending Approval Plan`
- `Ã¥Â°Å½Ã¨Ë†ÂªÃ¤Â¿Â®Ã¨Â£Å“Ã¦Â¸â€¦Ã¥â€“Â®`
- `Ã¥Â®Å’Ã¦Ë†ÂÃ¥Â¾Å’Ã¥ÂÂ¯Ã©â‚¬â‚¬Ã¤Â¼â€˜Ã§Å¡â€žÃ¨Ë†Å Ã¥Ë†â€ Ã©Â¡Å¾`

## Common Mistakes

- Ã¦Å Å  `vault-reshape` Ã§â€¢Â¶Ã¦Ë†ÂÃ¥â€“Â®Ã§Â¯â€¡Ã¦â€¢Â´Ã§Ââ€ Ã¥Â·Â¥Ã¥â€¦Â·
- Ã¦Â²â€™Ã¥â€¦Ë†Ã¥ÂÅ¡ cluster mapping Ã¥Â°Â±Ã§â€ºÂ´Ã¦Å½Â¥Ã¦ÂÂ¬Ã¨Â³â€¡Ã¦â€“â„¢Ã¥Â¤Â¾
- Ã¥ÂÂªÃ¦ÂÂ¬Ã¦Âªâ€Ã¯Â¼Å’Ã¤Â¸ÂÃ¨Â£Å“ `index.md` Ã¨Ë†â€¡Ã©â€”Å“Ã¨ÂÂ¯Ã¥â€¦Â¥Ã¥ÂÂ£
- Ã¦Å Å Ã¥â€¦Â§Ã¥Â®Â¹Ã¥Å½Â»Ã©â€¡ÂÃ¥â€™Å’Ã§ÂµÂÃ¦Â§â€¹Ã©â€¡ÂÃ¦â€¢Â´Ã¦Â·Â·Ã¦Ë†ÂÃ¥ÂÅ’Ã¤Â¸â‚¬Ã¨Â¼Âª
- Ã¤Â¸â‚¬Ã¦Â¬Â¡Ã¨Â©Â¦Ã¥Å“â€“Ã©â€¡ÂÃ¥ÂÅ¡Ã¦â€¢Â´Ã¥â‚¬â€¹ vault taxonomy

## Handoff

`vault-reshape` Ã¥Â®Å’Ã¦Ë†ÂÃ¥Â¾Å’Ã¯Â¼Å’Ã¤Â¸â€¹Ã¤Â¸â‚¬Ã¦Â­Â¥Ã©â‚¬Å¡Ã¥Â¸Â¸Ã¦ËœÂ¯Ã¯Â¼Å¡

- `note-update`
- `vault-check`
- `vault-deep-clean`
- `vault-GPS`

<!-- AGENT_SKILL_DEDUPE_NOTE -->
## Duplicate Consolidation

This is the canonical vault-reshape Skill after Agent dedupe on 2026-04-29.

Archived duplicate variants:
- Obsidian_skill_set/vault-reshape/SKILL.merged.md
- skills/vault-reshape/SKILL.merged.md
<!-- /AGENT_SKILL_DEDUPE_NOTE -->
