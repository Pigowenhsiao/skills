---
name: vault-GPS
description: Use when the user wants to improve vault navigation, canonical entry points, landing pages, or topic hubs so people and agents can find the right knowledge area without relying on source-based folders or scattered links.
---

# Vault GPS


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

`vault-GPS` Ã¦ËœÂ¯ Pigo vault Ã§Å¡â€žÃ¥Â°Å½Ã¨Ë†ÂªÃ¦Â²Â»Ã§Ââ€  skillÃ£â‚¬â€š
Ã¥Â®Æ’Ã¨Â²Â Ã¨Â²Â¬Ã¥Â»ÂºÃ§Â«â€¹Ã§Â©Â©Ã¥Â®Å¡Ã§Å¡â€žÃ¥â€¦Â¥Ã¥ÂÂ£Ã£â‚¬ÂÃ¤Â¸Â»Ã©Â¡Å’ hubÃ£â‚¬Âlanding page Ã¨Ë†â€¡ root navigation Ã¦â€Â¶Ã¦â€“â€šÃ¨Â¦ÂÃ¥â€°â€¡Ã¯Â¼Å’Ã¨Â®â€œÃ¤ÂºÂºÃ¥â€™Å’ agent Ã©Æ’Â½Ã¨Æ’Â½Ã¦â€ºÂ´Ã¥Â¿Â«Ã¦â€°Â¾Ã¥Ë†Â°Ã¦Â­Â£Ã§Â¢ÂºÃ§Å¸Â¥Ã¨Â­ËœÃ¥Ââ‚¬Ã¯Â¼Å’Ã¨â‚¬Å’Ã¤Â¸ÂÃ¦ËœÂ¯Ã¤Â¾ÂÃ¨Â³Â´Ã¤Â¾â€ Ã¦ÂºÂÃ¥Å¾â€¹Ã¨Â³â€¡Ã¦â€“â„¢Ã¥Â¤Â¾Ã¦Ë†â€“Ã©â€ºÂ¶Ã¦â€¢Â£Ã©â‚¬Â£Ã§ÂµÂÃ£â‚¬â€š

## When to Use

Ã¤Â½Â¿Ã§â€Â¨Ã¦â„¢â€šÃ¦Â©Å¸Ã¯Â¼Å¡

- vault Ã¥Â·Â²Ã¦Å“â€°Ã¤Â¸ÂÃ¥Â°â€˜Ã¥â€¦Â§Ã¥Â®Â¹Ã¯Â¼Å’Ã¤Â½â€ Ã¥â€¦Â¥Ã¥ÂÂ£Ã¤Â¸ÂÃ¦Â¸â€¦Ã¦Â¥Å¡
- Ã¥ÂÅ’Ã¤Â¸â‚¬Ã¥â‚¬â€¹Ã¤Â¸Â»Ã©Â¡Å’Ã¦â€¢Â£Ã¨ÂÂ½Ã¥Â¤Å¡Ã¨â„¢â€¢Ã¯Â¼Å’Ã§Â¼Âº canonical hub
- `index.md`Ã£â‚¬ÂÃ¤Â¸Â»Ã©Â¡Å’Ã¥â€¦Â¥Ã¥ÂÂ£Ã©Â ÂÃ£â‚¬ÂÃ¥Ë†â€ Ã©Â¡Å¾ landing page Ã¤Â¹â€¹Ã©â€“â€œÃ¤Â¸ÂÃ¤Â¸â‚¬Ã¨â€¡Â´
- Ã¤Â½Â Ã¥â€°â€ºÃ¥ÂÅ¡Ã¥Â®Å’ `vault-reshape`Ã¯Â¼Å’Ã©Å“â‚¬Ã¨Â¦ÂÃ¨Â£Å“Ã¥Â°Å½Ã¨Ë†ÂªÃ¥Â±Â¤
- Ã¤Â½Â¿Ã§â€Â¨Ã¨â‚¬â€¦Ã¥Â¸Â¸Ã¥Â¸Â¸Ã§Å¸Â¥Ã©Ââ€œÃ¨Â¦ÂÃ¦â€°Â¾Ã¤Â»â‚¬Ã©ÂºÂ¼Ã¯Â¼Å’Ã¤Â½â€ Ã¤Â¸ÂÃ§Å¸Â¥Ã©Ââ€œÃ¨Â©Â²Ã¥Â¾Å¾Ã¥â€œÂªÃ¥â‚¬â€¹Ã¥Ë†â€ Ã©Â¡Å¾Ã©â‚¬Â²Ã¥Å½Â»

Ã¤Â¸ÂÃ¨Â¦ÂÃ§â€Â¨Ã¥Å“Â¨Ã¯Â¼Å¡

- Ã¥â€“Â®Ã§Â¯â€¡Ã¥â€¦Â§Ã¥Â®Â¹Ã©â€¡ÂÃ¥Â¯Â«Ã¯Â¼Å¡Ã¦â€Â¹Ã§â€Â¨ `note-update`
- Ã¥Â¤Â§Ã¨Â¦ÂÃ¦Â¨Â¡Ã¥Ë†â€ Ã©Â¡Å¾Ã¦ÂÂ¬Ã§Â§Â»Ã¯Â¼Å¡Ã¦â€Â¹Ã§â€Â¨ `vault-reshape`
- Ã¥â€¦Â¨Ã¥Â±â‚¬Ã¥ÂÂ¥Ã¥ÂºÂ·Ã§â€ºÂ¤Ã©Â»Å¾Ã¯Â¼Å¡Ã¥â€¦Ë†Ã§â€Â¨ `vault-check`
- Ã¦Â¸â€¦Ã§Ââ€ Ã¥Â¤Â±Ã¦â€¢Ë†Ã¥â€¦Â§Ã¥Â®Â¹Ã¨Ë†â€¡ broken external linksÃ¯Â¼Å¡Ã¦â€Â¹Ã§â€Â¨ `vault-deep-clean`

## Vault Index Usage

`vault-GPS` Ã¨Â¦ÂÃ¥â€¦Ë†Ã§â€Â¨ vault index Ã¦â€°Â¾Ã©Â«ËœÃ©Â Â»Ã¤Â¸Â»Ã©Â¡Å’Ã¨Ë†â€¡Ã©â‚¬Â£Ã§ÂµÂÃ§â€ Â±Ã¥Ââ‚¬Ã¯Â¼Å’Ã¥â€ ÂÃ¦Â±ÂºÃ¥Â®Å¡Ã¥â€œÂªÃ¤Âºâ€ºÃ¥â€¦Â¥Ã¥ÂÂ£Ã¥â‚¬Â¼Ã¥Â¾â€” canonicalizeÃ£â‚¬â€š

- Vault rootÃ¯Â¼Å¡
  `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian`
- Query toolÃ¯Â¼Å¡
  `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian\.vault-index\query_vault.py`
- DatabaseÃ¯Â¼Å¡
  `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian\.vault-index\notes.db`

Ã¥â€žÂªÃ¥â€¦Ë†Ã¦Å¸Â¥Ã©â‚¬â„¢Ã¤Âºâ€ºÃ¯Â¼Å¡

- `fts`
- `related-notes`
- `by-classification`
- `links-to`
- `links-from`

Ã¥Å½Å¸Ã¥â€°â€¡Ã¯Â¼Å¡

1. Ã¥â€¦Ë†Ã¦â€°Â¾Ã©Â«ËœÃ©Â Â»Ã¦Â¦â€šÃ¥Â¿ÂµÃ¨Ë†â€¡Ã©Â«ËœÃ¦ÂµÂÃ©â€¡ÂÃ¤Â¸Â»Ã©Â¡Å’Ã¥Ââ‚¬
2. Ã¥â€ ÂÃ¦Â±ÂºÃ¥Â®Å¡Ã¥â€œÂªÃ¤Âºâ€ºÃ¥â‚¬Â¼Ã¥Â¾â€”Ã¥Â»ÂºÃ§Â«â€¹ canonical hub Ã¦Ë†â€“ landing page
3. Ã¥ÂÂªÃ¦Å“â€°Ã¥Å“Â¨ index Ã¤Â¸ÂÃ¨Æ’Â½Ã¨Â§Â£Ã©â€¡â€¹Ã¥Â°Å½Ã¨Ë†ÂªÃ§Â¼ÂºÃ¥ÂÂ£Ã¦â„¢â€šÃ¦â€°Â fallback Ã¥Ë†Â° `rg`

## Risk-Tier Contract

- `Low-risk`
  Ã¥ÂÂ¯Ã§â€ºÂ´Ã¦Å½Â¥Ã¦â€“Â°Ã¥Â¢Å¾Ã¦Ë†â€“Ã¦â€ºÂ´Ã¦â€“Â° landing pageÃ£â‚¬ÂÃ¥Â°Å½Ã¨Ë†ÂªÃ©Â ÂÃ£â‚¬Âwrapper hubÃ£â‚¬ÂÃ§Â´Â¢Ã¥Â¼â€¢Ã¥â€¦Â¥Ã¥ÂÂ£Ã¨Ë†â€¡ status Ã¦Âªâ€Ã£â‚¬â€š
- `Medium-risk`
  Ã¤Â¸ÂÃ§â€ºÂ´Ã¦Å½Â¥Ã¦â€Â¹Ã¥ÂÂÃ¥Â¤Â§Ã©â€¡ÂÃ¦â€”Â¢Ã¦Å“â€° hubÃ£â‚¬ÂÃ¤Â¹Å¸Ã¤Â¸ÂÃ§â€ºÂ´Ã¦Å½Â¥Ã©â€¡ÂÃ¥Â¯Â«Ã¥Â¤Å¡Ã¥â‚¬â€¹Ã¥Ë†â€ Ã©Â¡Å¾ indexÃ£â‚¬â€šÃ¥â€¦Ë†Ã¥ÂÅ¡ `Pending Approval Plan`Ã£â‚¬â€š
- `High-risk`
  Ã¤Â¸ÂÃ¥Å“Â¨Ã¦Å“Â¬ skill Ã¤Â¸Â»Ã¥â€¹â€¢Ã©â€¡ÂÃ¥ÂÅ¡Ã¦â€¢Â´Ã¥Â¥â€” taxonomy Ã¦Ë†â€“Ã¥Â¤Â§Ã¨Â¦ÂÃ¦Â¨Â¡Ã¥Â°Å½Ã¨Ë†ÂªÃ§Â³Â»Ã§ÂµÂ±Ã¦â€ºÂ¿Ã¦Ââ€ºÃ£â‚¬â€š

## Navigation Workflow

### 1. Baseline Scan

Ã§â€ºÂ¤Ã©Â»Å¾Ã¯Â¼Å¡

- root navigation Ã§ÂÂ¾Ã¦Â³Â
- Ã¥Ââ€žÃ¥Â¤Â§Ã¥Ë†â€ Ã©Â¡Å¾Ã¦ËœÂ¯Ã¥ÂÂ¦Ã¦Å“â€°Ã§Â©Â©Ã¥Â®Å¡Ã¥â€¦Â¥Ã¥ÂÂ£
- Ã¦ËœÂ¯Ã¥ÂÂ¦Ã¥Â­ËœÃ¥Å“Â¨Ã©Â«ËœÃ©Â Â»Ã¤Â¸Â»Ã©Â¡Å’Ã¤Â½â€ Ã¦Â²â€™Ã¦Å“â€° canonical page
- Ã¦ËœÂ¯Ã¥ÂÂ¦Ã¥Â­ËœÃ¥Å“Â¨Ã¥Â¤Å¡Ã¥â‚¬â€¹Ã§Â«Â¶Ã§Ë†Â­Ã¥â€¦Â¥Ã¥ÂÂ£Ã©â‚¬Â Ã¦Ë†ÂÃ¥Â°Å½Ã¨Ë†ÂªÃ¦Â·Â·Ã¤Âºâ€š

### 2. Coverage Model

Ã¥Â®Å¡Ã§Â¾Â©Ã¯Â¼Å¡

- Ã¥â€œÂªÃ¤Âºâ€ºÃ¨Â³â€¡Ã¦â€“â„¢Ã¥Â¤Â¾Ã¦â€¡â€°Ã¦Å“â€° landing page
- Ã¥â€œÂªÃ¤Âºâ€ºÃ¤Â¸Â»Ã©Â¡Å’Ã¦â€¡â€°Ã¦Å“â€° canonical hub
- Ã¥â€œÂªÃ¤Âºâ€ºÃ¥â€¦Â¥Ã¥ÂÂ£Ã¥ÂÂªÃ©Å“â‚¬Ã¨Â¦ÂÃ¥Å“Â¨ `index.md` Ã¦Å¡Â´Ã©Å“Â²Ã¯Â¼Å’Ã¤Â¸ÂÃ©Å“â‚¬Ã¨Â¦ÂÃ§ÂÂ¨Ã§Â«â€¹Ã¤Â¸Â»Ã©Â¡Å’Ã©Â Â

### 3. Landing Pages

Ã¨â€¹Â¥Ã¦Å¸ÂÃ¥â‚¬â€¹Ã©Â«ËœÃ¥Æ’Â¹Ã¥â‚¬Â¼Ã¥Ë†â€ Ã©Â¡Å¾Ã§Â¼ÂºÃ¥â€¦Â¥Ã¥ÂÂ£Ã¯Â¼Å’Ã¥Â»ÂºÃ§Â«â€¹Ã¦Ë†â€“Ã¦â€ºÂ´Ã¦â€“Â°Ã¦Å“â‚¬Ã¥Â°Â landing pageÃ¯Â¼Å’Ã¥â€¦Â§Ã¥Â®Â¹Ã¥ÂÂªÃ¤Â¿ÂÃ§â€¢â„¢Ã¯Â¼Å¡

- Ã©â‚¬â„¢Ã¥â‚¬â€¹Ã¥Ë†â€ Ã©Â¡Å¾Ã¦ËœÂ¯Ã¥ÂÅ¡Ã¤Â»â‚¬Ã©ÂºÂ¼Ã§Å¡â€ž
- Ã¤Â¸Â»Ã¨Â¦ÂÃ¥Â­ÂÃ©Â¡Å’Ã¦Å“â€°Ã¥â€œÂªÃ¤Âºâ€º
- Ã¥Â»ÂºÃ¨Â­Â°Ã¥Â¾Å¾Ã¥â€œÂªÃ¥Â¹Â¾Ã§Â¯â€¡Ã©â€“â€¹Ã¥Â§â€¹
- Ã§â€ºÂ¸Ã©â€”Å“Ã¥â€¦Â¥Ã¥ÂÂ£Ã©Â Â

### 4. Canonical Hubs

Ã§â€¢Â¶Ã¥ÂÅ’Ã¤Â¸â‚¬Ã¦Â¦â€šÃ¥Â¿ÂµÃ¨Â¢Â«Ã¥Â¤Å¡Ã¤ÂºÂºÃ¦Ë†â€“Ã¥Â¤Å¡Ã¥â‚¬â€¹ workflow Ã¥ÂÂÃ¨Â¦â€ Ã¥Â¼â€¢Ã§â€Â¨Ã¯Â¼Å’Ã¤Â½â€ Ã¦Â²â€™Ã¦Å“â€°Ã§Â©Â©Ã¥Â®Å¡Ã¥â€¦Â¥Ã¥ÂÂ£Ã¦â„¢â€šÃ¯Â¼Å¡

- Ã¥Â»ÂºÃ§Â«â€¹ canonical hub Ã¦Ë†â€“ wrapper page
- Ã¦Å’â€¡Ã¥Ââ€˜Ã§Å“Å¸Ã¦Â­Â£Ã§Å¡â€žÃ¥â€¦Â§Ã¥Â®Â¹Ã¨ÂÅ¡Ã©â€ºâ€ Ã¥Ââ‚¬
- Ã¨Â£Å“Ã¤Â¸Å Ã¦Å“â‚¬Ã¥Â°ÂÃ¥Â¿â€¦Ã¨Â¦ÂÃ§Å¡â€žÃ§â€ºÂ¸Ã©â€”Å“Ã¤Â¸Â»Ã©Â¡Å’Ã©â‚¬Â£Ã§ÂµÂ

### 5. Navigation Convergence

Ã¦â€Â¶Ã¦â€“â€šÃ¯Â¼Å¡

- root `index.md`
- Ã¥Ââ€žÃ¥Ë†â€ Ã©Â¡Å¾ `index.md`
- Ã¤Â¸Â»Ã©Â¡Å’ hub
- landing pages

Ã¨Â¦ÂÃ¦Â±â€šÃ¯Â¼Å¡

- Ã§â€ºÂ¸Ã¥ÂÅ’Ã¦Â¦â€šÃ¥Â¿ÂµÃ¤Â¸ÂÃ¨Â¦ÂÃ¦Å“â€°Ã¥Â¤Å¡Ã¥â‚¬â€¹Ã§Â«Â¶Ã§Ë†Â­Ã¥â€¦Â¥Ã¥ÂÂ£
- Ã§â€ºÂ¸Ã¥ÂÅ’Ã¥Ë†â€ Ã©Â¡Å¾Ã¦Â¨Â¡Ã¥Å¾â€¹Ã¤Â¸ÂÃ¨Â¦ÂÃ¥Å“Â¨Ã¥Â¤Å¡Ã¥â‚¬â€¹Ã¥Â°Å½Ã¨Ë†ÂªÃ©Â ÂÃ¨ÂªÂªÃ¤Â¸ÂÃ¥ÂÅ’Ã§Å¡â€žÃ¦â€¢â€¦Ã¤Âºâ€¹

### 6. Verification

Ã©Â©â€”Ã¨Â­â€°Ã¯Â¼Å¡

- Ã¦â€“Â°Ã¥â€¦Â¥Ã¥ÂÂ£Ã¦ËœÂ¯Ã¥ÂÂ¦Ã¥ÂÂ¯Ã¨Â¢Â«Ã§â„¢Â¼Ã§ÂÂ¾
- Ã¤Â¸Â»Ã¨Â¦ÂÃ¥Â°Å½Ã¨Ë†ÂªÃ©Â ÂÃ¦ËœÂ¯Ã¥ÂÂ¦Ã¤Â»ÂÃ¦Å“â€° broken wikilinks
- Ã¤Â¸Â»Ã©Â¡Å’ hub Ã¦ËœÂ¯Ã¥ÂÂ¦Ã§Å“Å¸Ã§Å¡â€žÃ§Â¸Â®Ã§Å¸Â­Ã¦Å¸Â¥Ã¦â€°Â¾Ã¨Â·Â¯Ã¥Â¾â€˜

## Expected Output

Ã¨Â¼Â¸Ã¥â€¡ÂºÃ¨â€¡Â³Ã¥Â°â€˜Ã¨Â¦ÂÃ¦Å“â€°Ã¯Â¼Å¡

- `Ã¦Â Â¸Ã¥Â¿Æ’Ã§ÂµÂÃ¨Â«â€“`
- `Ã¥Â°Å½Ã¨Ë†ÂªÃ§Â¼ÂºÃ¥ÂÂ£`
- `Ã¥Â»ÂºÃ¨Â­Â°Ã¦â€“Â°Ã¥Â¢Å¾Ã¦Ë†â€“Ã¦â€ºÂ´Ã¦â€“Â°Ã§Å¡â€žÃ¥â€¦Â¥Ã¥ÂÂ£`
- `canonical hub Ã¥â‚¬â„¢Ã©ÂÂ¸`
- `Pending Approval Plan`
- `Ã¤Â¸â€¹Ã¤Â¸â‚¬Ã¦Â­Â¥Ã¥Â»ÂºÃ¨Â­Â°`

## Common Mistakes

- Ã¦Å Å  `vault-GPS` Ã§â€¢Â¶Ã¦Ë†ÂÃ¥Ë†â€ Ã©Â¡Å¾Ã¦ÂÂ¬Ã¥Â®Â¶Ã¥Â·Â¥Ã¥â€¦Â·
- Ã§â€šÂºÃ¦Â¯ÂÃ¥â‚¬â€¹Ã¦Â¦â€šÃ¥Â¿ÂµÃ©Æ’Â½Ã¥Â»ÂºÃ§Â«â€¹ hubÃ¯Â¼Å’Ã©â‚¬Â Ã¦Ë†Â hub Ã©ÂÅ½Ã©â€¡Â
- Ã¥Â»Âº hub Ã¤Â½â€ Ã¤Â¸ÂÃ¦Å’â€¡Ã¥Ââ€˜Ã¥Â¯Â¦Ã©Å¡â€ºÃ¥â€¦Â§Ã¥Â®Â¹Ã¥Ââ‚¬
- root navigationÃ£â‚¬ÂÃ¥Ë†â€ Ã©Â¡Å¾ indexÃ£â‚¬ÂÃ¤Â¸Â»Ã©Â¡Å’Ã©Â ÂÃ¥Â½Â¼Ã¦Â­Â¤Ã¨ÂªÂªÃ¤Â¸ÂÃ¥ÂÅ’Ã§Å¡â€žÃ§ÂµÂÃ¦Â§â€¹Ã¦â€¢â€¦Ã¤Âºâ€¹
- Ã¥ÂÂªÃ¨Â£Å“Ã¥â€¦Â¥Ã¥ÂÂ£Ã¯Â¼Å’Ã¤Â¸ÂÃ©Â©â€”Ã¨Â­â€°Ã¥ÂÂ¯Ã§â„¢Â¼Ã§ÂÂ¾Ã¦â‚¬Â§

## Handoff

`vault-GPS` Ã¥Â®Å’Ã¦Ë†ÂÃ¥Â¾Å’Ã¯Â¼Å’Ã¤Â¸â€¹Ã¤Â¸â‚¬Ã¦Â­Â¥Ã©â‚¬Å¡Ã¥Â¸Â¸Ã¦ËœÂ¯Ã¯Â¼Å¡

- `vault-check`
- `vault-reshape`
- `note-update`
- `tag-check`

<!-- AGENT_SKILL_DEDUPE_NOTE -->
## Duplicate Consolidation

This is the canonical vault-GPS Skill after Agent dedupe on 2026-04-29.

Archived duplicate variants:
- Obsidian_skill_set/vault-GPS/SKILL.merged.md
- skills/vault-GPS/SKILL.merged.md
<!-- /AGENT_SKILL_DEDUPE_NOTE -->
