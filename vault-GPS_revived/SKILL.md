---
name: vault-GPS
description: Use when the user wants to improve vault navigation, canonical entry points, landing pages, or topic hubs so people and agents can find the right knowledge area without relying on source-based folders or scattered links.
---

# Vault GPS

## Description

`vault-GPS` æ˜¯ Pigo vault çš„å°Žèˆªæ²»ç† skillã€‚  
å®ƒè² è²¬å»ºç«‹ç©©å®šçš„å…¥å£ã€ä¸»é¡Œ hubã€landing page èˆ‡ root navigation æ”¶æ–‚è¦å‰‡ï¼Œè®“äººå’Œ agent éƒ½èƒ½æ›´å¿«æ‰¾åˆ°æ­£ç¢ºçŸ¥è­˜å€ï¼Œè€Œä¸æ˜¯ä¾è³´ä¾†æºåž‹è³‡æ–™å¤¾æˆ–é›¶æ•£é€£çµã€‚

## When to Use

ä½¿ç”¨æ™‚æ©Ÿï¼š

- vault å·²æœ‰ä¸å°‘å…§å®¹ï¼Œä½†å…¥å£ä¸æ¸…æ¥š
- åŒä¸€å€‹ä¸»é¡Œæ•£è½å¤šè™•ï¼Œç¼º canonical hub
- `index.md`ã€ä¸»é¡Œå…¥å£é ã€åˆ†é¡ž landing page ä¹‹é–“ä¸ä¸€è‡´
- ä½ å‰›åšå®Œ `vault-reshape`ï¼Œéœ€è¦è£œå°Žèˆªå±¤
- ä½¿ç”¨è€…å¸¸å¸¸çŸ¥é“è¦æ‰¾ä»€éº¼ï¼Œä½†ä¸çŸ¥é“è©²å¾žå“ªå€‹åˆ†é¡žé€²åŽ»

ä¸è¦ç”¨åœ¨ï¼š

- å–®ç¯‡å…§å®¹é‡å¯«ï¼šæ”¹ç”¨ `note-update`
- å¤§è¦æ¨¡åˆ†é¡žæ¬ç§»ï¼šæ”¹ç”¨ `vault-reshape`
- å…¨å±€å¥åº·ç›¤é»žï¼šå…ˆç”¨ `vault-check`
- æ¸…ç†å¤±æ•ˆå…§å®¹èˆ‡ broken external linksï¼šæ”¹ç”¨ `vault-deep-clean`

## Vault Index Usage

`vault-GPS` è¦å…ˆç”¨ vault index æ‰¾é«˜é »ä¸»é¡Œèˆ‡é€£çµç†±å€ï¼Œå†æ±ºå®šå“ªäº›å…¥å£å€¼å¾— canonicalizeã€‚

- Vault rootï¼š
  `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian`
- Query toolï¼š
  `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian\.vault-index\query_vault.py`
- Databaseï¼š
  `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian\.vault-index\notes.db`

å„ªå…ˆæŸ¥é€™äº›ï¼š

- `fts`
- `related-notes`
- `by-classification`
- `links-to`
- `links-from`

åŽŸå‰‡ï¼š

1. å…ˆæ‰¾é«˜é »æ¦‚å¿µèˆ‡é«˜æµé‡ä¸»é¡Œå€
2. å†æ±ºå®šå“ªäº›å€¼å¾—å»ºç«‹ canonical hub æˆ– landing page
3. åªæœ‰åœ¨ index ä¸èƒ½è§£é‡‹å°Žèˆªç¼ºå£æ™‚æ‰ fallback åˆ° `rg`

## Risk-Tier Contract

- `Low-risk`
  å¯ç›´æŽ¥æ–°å¢žæˆ–æ›´æ–° landing pageã€å°Žèˆªé ã€wrapper hubã€ç´¢å¼•å…¥å£èˆ‡ status æª”ã€‚
- `Medium-risk`
  ä¸ç›´æŽ¥æ”¹åå¤§é‡æ—¢æœ‰ hubã€ä¹Ÿä¸ç›´æŽ¥é‡å¯«å¤šå€‹åˆ†é¡ž indexã€‚å…ˆåš `Pending Approval Plan`ã€‚
- `High-risk`
  ä¸åœ¨æœ¬ skill ä¸»å‹•é‡åšæ•´å¥— taxonomy æˆ–å¤§è¦æ¨¡å°Žèˆªç³»çµ±æ›¿æ›ã€‚

## Navigation Workflow

### 1. Baseline Scan

ç›¤é»žï¼š

- root navigation ç¾æ³
- å„å¤§åˆ†é¡žæ˜¯å¦æœ‰ç©©å®šå…¥å£
- æ˜¯å¦å­˜åœ¨é«˜é »ä¸»é¡Œä½†æ²’æœ‰ canonical page
- æ˜¯å¦å­˜åœ¨å¤šå€‹ç«¶çˆ­å…¥å£é€ æˆå°Žèˆªæ··äº‚

### 2. Coverage Model

å®šç¾©ï¼š

- å“ªäº›è³‡æ–™å¤¾æ‡‰æœ‰ landing page
- å“ªäº›ä¸»é¡Œæ‡‰æœ‰ canonical hub
- å“ªäº›å…¥å£åªéœ€è¦åœ¨ `index.md` æš´éœ²ï¼Œä¸éœ€è¦ç¨ç«‹ä¸»é¡Œé 

### 3. Landing Pages

è‹¥æŸå€‹é«˜åƒ¹å€¼åˆ†é¡žç¼ºå…¥å£ï¼Œå»ºç«‹æˆ–æ›´æ–°æœ€å° landing pageï¼Œå…§å®¹åªä¿ç•™ï¼š

- é€™å€‹åˆ†é¡žæ˜¯åšä»€éº¼çš„
- ä¸»è¦å­é¡Œæœ‰å“ªäº›
- å»ºè­°å¾žå“ªå¹¾ç¯‡é–‹å§‹
- ç›¸é—œå…¥å£é 

### 4. Canonical Hubs

ç•¶åŒä¸€æ¦‚å¿µè¢«å¤šäººæˆ–å¤šå€‹ workflow åè¦†å¼•ç”¨ï¼Œä½†æ²’æœ‰ç©©å®šå…¥å£æ™‚ï¼š

- å»ºç«‹ canonical hub æˆ– wrapper page
- æŒ‡å‘çœŸæ­£çš„å…§å®¹èšé›†å€
- è£œä¸Šæœ€å°å¿…è¦çš„ç›¸é—œä¸»é¡Œé€£çµ

### 5. Navigation Convergence

æ”¶æ–‚ï¼š

- root `index.md`
- å„åˆ†é¡ž `index.md`
- ä¸»é¡Œ hub
- landing pages

è¦æ±‚ï¼š

- ç›¸åŒæ¦‚å¿µä¸è¦æœ‰å¤šå€‹ç«¶çˆ­å…¥å£
- ç›¸åŒåˆ†é¡žæ¨¡åž‹ä¸è¦åœ¨å¤šå€‹å°Žèˆªé èªªä¸åŒçš„æ•…äº‹

### 6. Verification

é©—è­‰ï¼š

- æ–°å…¥å£æ˜¯å¦å¯è¢«ç™¼ç¾
- ä¸»è¦å°Žèˆªé æ˜¯å¦ä»æœ‰ broken wikilinks
- ä¸»é¡Œ hub æ˜¯å¦çœŸçš„ç¸®çŸ­æŸ¥æ‰¾è·¯å¾‘

## Expected Output

è¼¸å‡ºè‡³å°‘è¦æœ‰ï¼š

- `æ ¸å¿ƒçµè«–`
- `å°Žèˆªç¼ºå£`
- `å»ºè­°æ–°å¢žæˆ–æ›´æ–°çš„å…¥å£`
- `canonical hub å€™é¸`
- `Pending Approval Plan`
- `ä¸‹ä¸€æ­¥å»ºè­°`

## Common Mistakes

- æŠŠ `vault-GPS` ç•¶æˆåˆ†é¡žæ¬å®¶å·¥å…·
- ç‚ºæ¯å€‹æ¦‚å¿µéƒ½å»ºç«‹ hubï¼Œé€ æˆ hub éŽé‡
- å»º hub ä½†ä¸æŒ‡å‘å¯¦éš›å…§å®¹å€
- root navigationã€åˆ†é¡ž indexã€ä¸»é¡Œé å½¼æ­¤èªªä¸åŒçš„çµæ§‹æ•…äº‹
- åªè£œå…¥å£ï¼Œä¸é©—è­‰å¯ç™¼ç¾æ€§

## Handoff

`vault-GPS` å®Œæˆå¾Œï¼Œä¸‹ä¸€æ­¥é€šå¸¸æ˜¯ï¼š

- `vault-check`
- `vault-reshape`
- `note-update`
- `tag-check`

