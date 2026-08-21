---
name: vault-reshape
description: Use when the user wants to restructure the vault at the category, landing-page, or navigation level, especially after taxonomy drift, source-based folder sprawl, or repeated classification inconsistencies.
---

# Vault Reshape

## Description

`vault-reshape` æ˜¯ Pigo vault çš„çµæ§‹é‡æ•´æ¨¡å¼ã€‚  
å®ƒè™•ç†çš„æ˜¯åˆ†é¡žæ”¶æ–‚ã€å°Žèˆªä¿®è£œã€ä¾†æºåž‹è³‡æ–™å¤¾é€€å ´ã€ä¸»é¡Œåž‹è½é»žé‡å»ºèˆ‡çµæ§‹å€™é¸è¦åŠƒï¼Œä¸è² è²¬å–®ç¯‡å…§å®¹æ­£å¼åŒ–ï¼Œä¹Ÿä¸è² è²¬æ·±åº¦æ¸…ç†ã€‚

## When to Use

ä½¿ç”¨æ™‚æ©Ÿï¼š

- ä¾†æºåž‹åˆ†é¡žå·²ç¶“å¤±æŽ§ï¼Œä¾‹å¦‚ `youtube/`ã€`twitter/` ä¹‹é¡žçš„æ®˜ç•™å€å¡Š
- åŒä¸»é¡Œå…§å®¹åˆ†æ•£åœ¨å¤šå€‹è·¯å¾‘ï¼Œå°Žè‡´å°Žèˆªèˆ‡ç´¢å¼•æ··äº‚
- æŸäº›åˆ†é¡žå·²ä¸å†åˆç†ï¼Œéœ€è¦æ”¶æ–‚ã€æ¬ç§»æˆ–æ‹†åˆ†
- å¤§é‡ `index.md`ã€landing pageã€ä¸»é¡Œé éœ€è¦ä¸€èµ·èª¿æ•´
- `vault-check` å·²æŒ‡å‡ºçµæ§‹æ€§å•é¡Œï¼Œéœ€è¦æ­£å¼é€²è¡Œ reshape

ä¸è¦ç”¨åœ¨ï¼š

- å–®ç¯‡å…§å®¹ä¿®è£œï¼šæ”¹ç”¨ `note-update`
- `00-Inbox` æ‰¹æ¬¡æ¸…ç†ï¼šæ”¹ç”¨ `inbox-check`
- å…¨å±€ç›¤é»žä½†å°šæœªæ±ºå®šå¦‚ä½•é‡æ•´ï¼šå…ˆç”¨ `vault-check`
- broken links / stale external links / æ‰¹æ¬¡æ¸…ç†ï¼šæ”¹ç”¨ `vault-deep-clean`

## Vault Index Usage

`vault-reshape` å¿…é ˆå…ˆç”¨ vault index æ‰¾ cluster èˆ‡çµæ§‹å€™é¸ï¼Œå†åšçµæ§‹æ±ºç­–ã€‚

- Vault rootï¼š
  `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian`
- Query toolï¼š
  `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian\.vault-index\query_vault.py`
- Databaseï¼š
  `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian\.vault-index\notes.db`

å„ªå…ˆæŸ¥é€™äº›ï¼š

- `by-classification`
- `fts`
- `related-notes`
- `links-to`
- `links-from`

åŽŸå‰‡ï¼š

1. å…ˆæ‰¾ä¸»é¡Œ cluster èˆ‡åˆ†é¡žæ¼‚ç§»ç†±å€
2. å†æ±ºå®šæ‡‰æ”¶æ–‚ã€åˆ†æµã€æ¬ç§»æˆ–å»ºç«‹ landing page çš„å€å¡Š
3. åªæœ‰åœ¨ index ç„¡æ³•è¦†è“‹ç´°ç¯€æ™‚æ‰ fallback åˆ° `rg`

## Risk-Tier Contract

- `Low-risk`
  å¯ç›´æŽ¥æ•´ç†çµæ§‹å ±å‘Šã€æ¬ç§»å€™é¸æ¸…å–®ã€index ç¼ºå£æ¸…å–®èˆ‡ landing page å»ºè­°ã€‚
- `Medium-risk`
  ä¸ç›´æŽ¥åŸ·è¡Œæ‰¹æ¬¡æ¬ç§»æˆ–å¤§ç¯„åœ index é‡å¯«ã€‚å…ˆåš `Pending Approval Plan`ã€‚
- `High-risk`
  ä¸åœ¨æœ¬ skill è‡ªä¸»å®Œæˆæ•´å€‹ vault æ”¹ç‰ˆã€‚è‹¥ç‰½æ¶‰å¤§ç¯„åœ taxonomy redesignï¼Œæ‡‰æ‹†æˆå¤šæ‰¹æ¬¡åŸ·è¡Œã€‚

## Reshape Workflow

### 1. Structure Scan

ç›¤é»žï¼š

- å“ªäº›è³‡æ–™å¤¾æ˜¯ä¾†æºåž‹åˆ†é¡ž
- å“ªäº›ä¸»é¡Œåˆ†é¡žå·²æˆç‚ºå¯¦éš›çŸ¥è­˜ä¸­å¿ƒ
- å“ªäº›è·¯å¾‘å­˜åœ¨é‡ç–Šæˆ–ç«¶çˆ­é—œä¿‚

### 2. Cluster Mapping

ç”¨ index æ‰¾å‡ºï¼š

- å…§å®¹é«˜åº¦ç›¸é—œä½†åˆ†æ•£åœ¨ä¸åŒåˆ†é¡žçš„ cluster
- æ‡‰å‡ç´šæˆç¨ç«‹ä¸»é¡Œé æˆ– landing page çš„ç¾¤çµ„
- æ‡‰ä½µå…¥æ—¢æœ‰ canonical category çš„ç¾¤çµ„

### 3. Target Taxonomy Proposal

ç‚ºæ¯å€‹å€™é¸ç¾¤çµ„å®šç¾©ï¼š

- ç›®æ¨™åˆ†é¡ž
- æ˜¯å¦æ‡‰æ¬ç§»
- æ˜¯å¦æ‡‰åˆä½µ
- æ˜¯å¦è¦è£œ `index.md`
- æ˜¯å¦è¦å»ºç«‹ä¸»é¡Œå…¥å£é 

### 4. Navigation Repair Plan

è¦åŠƒï¼š

- å“ªäº› `index.md` è¦è£œå…¥å£
- å“ªäº›æ—¢æœ‰é é¢è¦åšæœ€å°åå‘ä¿®è£œ
- å“ªäº›ä¾†æºåž‹è³‡æ–™å¤¾å®Œæˆé·ç§»å¾Œå¯é€€ä¼‘

### 5. Execution Boundary

çœŸæ­£åŸ·è¡Œå‰è¦æ˜Žç¢ºåˆ—å‡ºï¼š

- ç²¾ç¢ºè·¯å¾‘
- æ¬ç§»/åˆä½µæ–¹å¼
- å—å½±éŸ¿ index
- å›žæ»¾è·¯å¾‘

## Expected Output

è¼¸å‡ºè‡³å°‘è¦æœ‰ï¼š

- `æ ¸å¿ƒçµè«–`
- `ç›®å‰çµæ§‹å•é¡Œ`
- `å»ºè­°ç›®æ¨™åˆ†é¡ž`
- `Pending Approval Plan`
- `å°Žèˆªä¿®è£œæ¸…å–®`
- `å®Œæˆå¾Œå¯é€€ä¼‘çš„èˆŠåˆ†é¡ž`

## Common Mistakes

- æŠŠ `vault-reshape` ç•¶æˆå–®ç¯‡æ•´ç†å·¥å…·
- æ²’å…ˆåš cluster mapping å°±ç›´æŽ¥æ¬è³‡æ–™å¤¾
- åªæ¬æª”ï¼Œä¸è£œ `index.md` èˆ‡é—œè¯å…¥å£
- æŠŠå…§å®¹åŽ»é‡å’Œçµæ§‹é‡æ•´æ··æˆåŒä¸€è¼ª
- ä¸€æ¬¡è©¦åœ–é‡åšæ•´å€‹ vault taxonomy

## Handoff

`vault-reshape` å®Œæˆå¾Œï¼Œä¸‹ä¸€æ­¥é€šå¸¸æ˜¯ï¼š

- `note-update`
- `vault-check`
- `vault-deep-clean`
- `vault-GPS`

