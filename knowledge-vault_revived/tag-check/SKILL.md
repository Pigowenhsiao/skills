---
name: tag-check
description: Use when the user wants a low-frequency audit of vault tags, including orphan tags, duplicate tags, taxonomy drift, inconsistent formats, or tag usage that no longer matches the current knowledge structure.
---

# Tag Check


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

`tag-check` æ˜¯ Pigo vault çš„ tag å°ˆé …æª¢æŸ¥æ¨¡å¼ã€‚
å®ƒå°ˆæ³¨åœ¨ tag æ ¼å¼ä¸€è‡´æ€§ã€taxonomy æ¼‚ç§»ã€è¿‘ä¼¼ tag åˆä½µå€™é¸èˆ‡éŽåº¦/éŽå°‘ä½¿ç”¨çš„ tagï¼Œä¸å–ä»£çµæ§‹é‡æ•´ï¼Œä¹Ÿä¸å–ä»£å–®ç¯‡æ•´ç†ã€‚

## When to Use

ä½¿ç”¨æ™‚æ©Ÿï¼š

- ä½ æ‡·ç–‘ tag é–‹å§‹å¤±æŽ§
- æœ‰å¾ˆå¤šåŒç¾© tagã€å¤§å°å¯«å·®ç•°ã€æ ¼å¼ä¸ä¸€è‡´
- `vault-check` æŒ‡å‡º tag health æœ‰å•é¡Œ
- å¤§é‡æ¬ç§»æˆ–åŒ¯å…¥å¾Œï¼Œéœ€è¦é‡æ–°ç›¤é»ž tag

ä¸è¦ç”¨åœ¨ï¼š

- å–®ç¯‡ç­†è¨˜ç·¨ä¿®ï¼šæ”¹ç”¨ `note-update`
- å¤§ç¯„åœåˆ†é¡žæ¬ç§»ï¼šæ”¹ç”¨ `vault-reshape`
- æ·±åº¦å…§å®¹æ¸…ç†ï¼šæ”¹ç”¨ `vault-deep-clean`

## Vault Index Usage

ç›®å‰ `.vault-index` æ²’æœ‰å°ˆç”¨ tag queryï¼Œæ‰€ä»¥ `tag-check` æ‡‰å…ˆç”¨ index éŽ–å®šæ´»èºåˆ†é¡žèˆ‡é«˜é »ä¸»é¡Œå€ï¼Œå†å›žåˆ° frontmatter / å…§å®¹åšç²¾ç¢º tag æª¢æŸ¥ã€‚

- Vault rootï¼š
  `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian`
- Query toolï¼š
  `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian\.vault-index\query_vault.py`

å„ªå…ˆæŸ¥é€™äº›ï¼š

- `by-classification`
- `fts`
- `related-notes`

åŽŸå‰‡ï¼š

1. å…ˆæ‰¾ tag å•é¡Œæœ€å¯èƒ½é›†ä¸­çš„åˆ†é¡žå€
2. å†åšç²¾ç¢º tag æŽƒæèˆ‡æ¯”å°
3. tag èªžæ„åˆä½µä¸€å¾‹ä¿å®ˆè™•ç†

## Risk-Tier Contract

- `Low-risk`
  å¯ç›´æŽ¥æå‡º format-only normalization å»ºè­°ï¼Œä¾‹å¦‚å¤§å°å¯«ã€ç©ºç™½ã€é€£å­—è™Ÿçµ±ä¸€ã€‚
- `Medium-risk`
  åŒç¾© tag åˆä½µã€taxonomy æ›´æ–°ã€æ‰¹æ¬¡ retag ä¸€å¾‹é€² `Pending Approval Plan`ã€‚
- `High-risk`
  ä¸åœ¨æœ¬ skill è£¡é‡åšæ•´å¥— tag æ¨¡åž‹ï¼Œä¹Ÿä¸ä¸»å‹•ç™¼æ˜Žæ–°çš„å¤§åˆ†é¡ž tag familyã€‚

## Tag Workflow

### 1. Tag Inventory

ç›¤é»žï¼š

- ç¸½ tag æ•¸é‡
- é«˜é » tag
- åªå‡ºç¾ 1 åˆ° 2 æ¬¡çš„ tag
- åŒç¾©æˆ–è¿‘ä¼¼ tag å€™é¸

### 2. Format Review

æª¢æŸ¥ï¼š

- å¤§å°å¯«ä¸ä¸€è‡´
- å¤šè©ž tag æ ¼å¼ä¸ä¸€è‡´
- èˆŠå‘½åæ®˜ç•™
- æ˜Žé¡¯ typo

### 3. Taxonomy Drift Review

æª¢æŸ¥ï¼š

- tag æ˜¯å¦ä»ç¬¦åˆç•¶å‰åˆ†é¡žèˆ‡çŸ¥è­˜æ¨¡åž‹
- æ˜¯å¦æœ‰ä¾†æºåž‹ tag å…¶å¯¦æ‡‰é€€å ´
- æ˜¯å¦æœ‰ä¸»é¡Œå·²æˆç†Ÿä½† tag ä»åœåœ¨è‡¨æ™‚ç‹€æ…‹

### 4. Merge Candidates

è¼¸å‡ºï¼š

- å»ºè­°ä¿ç•™çš„ canonical tag
- å»ºè­°åˆä½µçš„è¿‘ä¼¼ tag
- å»ºè­°é€€ä¼‘çš„èˆŠ tag

## Expected Output

è¼¸å‡ºè‡³å°‘è¦æœ‰ï¼š

- `æ ¸å¿ƒçµè«–`
- `tag inventory`
- `format-only å•é¡Œ`
- `merge candidates`
- `Pending Approval Plan`

## Common Mistakes

- æ²’å…ˆçœ‹åˆ†é¡žä¸Šä¸‹æ–‡å°±ç›´æŽ¥åˆä½µ tag
- æŠŠèªžæ„ä¸åŒä½†å­—é¢ç›¸è¿‘çš„ tag å¼·è¡Œåˆä½µ
- åªæ”¹ tagï¼Œä¸æª¢æŸ¥è©²ä¸»é¡Œæ˜¯å¦å…¶å¯¦æ‡‰å‡ç´šç‚ºåˆ†é¡žæˆ– hub

## Handoff

`tag-check` å®Œæˆå¾Œï¼Œä¸‹ä¸€æ­¥é€šå¸¸æ˜¯ï¼š

- `vault-check`
- `vault-reshape`
- `note-update`

<!-- AGENT_SKILL_DEDUPE_NOTE -->
## Duplicate Consolidation

This is the canonical tag-check Skill after Agent dedupe on 2026-04-29.

Archived duplicate variants:
- Obsidian_skill_set/tag-check/SKILL.merged.md
- skills/tag-check/SKILL.merged.md
<!-- /AGENT_SKILL_DEDUPE_NOTE -->
