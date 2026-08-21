---
name: vault-deep-clean
description: Use when the user wants a low-frequency but thorough vault cleanup focused on stale content, duplicate clusters, broken links, template drift, and accumulated maintenance debt after an audit or major reorganization.
---

# Vault Deep Clean

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

## Vault Classification Control Plane

When this skill classifies, moves, rewrites, imports, summarizes, or routes any Vault note, use the Vault navigation files as the classification authority before choosing a destination.

1. Read the Vault root `AGENTS.md` first.
2. Read the nearest relevant directory `README.md` for the current note or working folder.
3. Before choosing a destination category, read the candidate destination directory `README.md` files, including parent and child directories when needed.
4. Use each README's purpose, usage principles, child directory table, common choices, and sensitive data boundary as classification evidence.
5. Priority order: current Pigo instruction, Vault `AGENTS.md`, relevant directory `README.md`, then this skill's local workflow.
6. If the correct category is ambiguous, do not move the note. Present the candidate destinations, explain the evidence from README files, and ask Pigo to confirm.
7. Do not place sensitive or local-only work content into publishable Vault folders unless `AGENTS.md` and the relevant README explicitly allow it.

## Description


ault-deep-clean æ˜¯ Pigo vault çš„æ·±åº¦ç¶­è­·æ¨¡å¼ã€‚
å®ƒè™•ç†çš„æ˜¯ stale contentã€é‡è¤‡ç«¶çˆ­é ã€å¤±æ•ˆé€£çµã€æ¨¡æ¿æ¼‚ç§»èˆ‡ç´¯ç©æ€§ç¶­è­·å‚µï¼Œä¸è² è²¬ä¸»é¡Œåˆ†é¡žæ”¹ç‰ˆï¼Œä¹Ÿä¸æ‡‰å–ä»£å–®ç¯‡æ•´ç†æµç¨‹ã€‚

## When to Use

ä½¿ç”¨æ™‚æ©Ÿï¼š

- vault å·²ç´¯ç©ä¸€æ®µæ™‚é–“ï¼Œé–‹å§‹å‡ºç¾ stale notesã€é‡è¤‡é èˆ‡å¤±æ•ˆå…¥å£
-
ault-check å·²æ‰¾å‡ºå¤§é‡ hygiene å•é¡Œï¼Œéœ€è¦é€²ä¸€æ­¥æ¸…ç†
- å¤§æ‰¹æ¬ç§»æˆ–é‡åˆ†é¡žå¾Œï¼Œéœ€è¦è£œåšæ·±åº¦ä¿®å¾©
- ä½ æ‡·ç–‘æœ‰å¾ˆå¤šæ­·å²æ®˜ç•™é é¢ã€èˆŠæ©‹æŽ¥é ã€ç„¡æ•ˆ Sourceã€æ¨¡æ¿é£„ç§»

ä¸è¦ç”¨åœ¨ï¼š

- å–®ç¯‡ç­†è¨˜æ­£å¼åŒ–ï¼šæ”¹ç”¨
ote-update
- çµæ§‹æ”¹ç‰ˆèˆ‡åˆ†é¡žæ”¶æ–‚ï¼šæ”¹ç”¨
ault-reshape
- å°Žèˆªèˆ‡ hub æ²»ç†ï¼šæ”¹ç”¨
ault-GPS
- åªæƒ³å…ˆåšç›¤é»žï¼šå…ˆç”¨
ault-check

## Vault Index Usage


ault-deep-clean è¦å…ˆç”¨ vault index ç¸®å°å•é¡Œç¯„åœï¼Œå†å°é«˜é¢¨éšªå€™é¸åšé€æª”æª¢æŸ¥ã€‚

- Vault rootï¼š
  C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian
- Query toolï¼š
  C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian\.vault-index\query_vault.py
- Databaseï¼š
  C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian\.vault-index\notes.db

å„ªå…ˆæŸ¥é€™äº›ï¼š

- duplicate-candidates
-
ts
-
elated-notes
- links-to
- links-from

åŽŸå‰‡ï¼š

1. å…ˆç”¨ index æ‰¾ stale clusterã€duplicate clusterã€link hotspot
2. å†å°é«˜é¢¨éšªå€™é¸åšé€æª”æ·±æŸ¥
3. åªæœ‰åœ¨ index ç„¡æ³•è¦†è“‹ç´°ç¯€æ™‚æ‰ fallback åˆ°
g

## Risk-Tier Contract

- Low-risk
  å¯ç›´æŽ¥ç”¢å‡ºå€™é¸æ¸…å–®ã€çµ±è¨ˆã€æ˜Žç¢ºå¯é€†çš„ cleanup å»ºè­°èˆ‡å±€éƒ¨ deterministic fixã€‚
- Medium-risk
  ä¸ç›´æŽ¥åŸ·è¡Œæ‰¹æ¬¡åˆä½µã€æ‰¹æ¬¡åˆªé™¤æˆ–å¤§ç¯„åœæ›¿æ›ã€‚å…ˆæ•´ç†æˆ Pending Approval Planã€‚
- High-risk
  ä¸åœ¨æœ¬ skill å…§ç›´æŽ¥åš taxonomy redesignã€çµæ§‹æ”¹ç‰ˆæˆ–å¤§è¦æ¨¡èªžæ„åˆä½µã€‚

## Deep Clean Workflow

### 1. Stale Content Scan

æª¢æŸ¥ï¼š

- é•·æœŸæœªæ›´æ–°ä½†ä»è¢«ç•¶æˆå…¥å£çš„é é¢
- å·²è¢«æ–°ç­†è¨˜å–ä»£çš„èˆŠæ‘˜è¦é 
- åªå‰©æ­·å²åƒ¹å€¼ä½†ä»ä½”æ“šä¸»è¦å°Žèˆªä½ç½®çš„é é¢

### 2. Duplicate And Competition Review

æª¢æŸ¥ï¼š

- åŒä¸»é¡Œç«¶çˆ­é 
- åŒä¾†æºç«¶çˆ­é 
- æ‡‰åˆä½µä½†å°šæœªåˆä½µçš„æ©‹æŽ¥é èˆ‡èˆŠç‰ˆæœ¬

### 3. Link And Source Repair

æª¢æŸ¥ï¼š

- broken wikilinks
- stale Source å€å¡Š
- æŒ‡å‘èˆŠåˆ†é¡žæˆ–èˆŠæ¨™é¡Œçš„å…¥å£
- åªå‰©å–®å‘éˆæŽ¥çš„åŠå­¤å…’é é¢

### 4. Template And Metadata Drift

æª¢æŸ¥ï¼š

- frontmatter æ¼‚ç§»
- classification_path èˆ‡å¯¦éš›è·¯å¾‘ä¸ä¸€è‡´
- processed / status éŽæ™‚
- èˆŠæ¨¡æ¿æ®˜ç•™æ¬„ä½

### 5. Cleanup Plan

è¼¸å‡ºï¼š

- å¯ç›´æŽ¥è™•ç†çš„ low-risk ä¿®è£œ
- éœ€è¦äººå·¥æ ¸å‡†çš„ Pending Approval Plan
- å»ºè­°äº¤çµ¦
ault-reshape æˆ–
ote-update çš„å¾ŒçºŒå·¥ä½œ

## Expected Output

è¼¸å‡ºè‡³å°‘è¦æœ‰ï¼š

- æ ¸å¿ƒçµè«–
- ä¸»è¦æ·±å±¤å•é¡Œ
- duplicate / stale / broken-link å€™é¸
- Pending Approval Plan
- å»ºè­°ä¸‹ä¸€æ­¥

## Common Mistakes

- æŠŠ
ault-deep-clean ç•¶æˆçµæ§‹é‡æ•´å·¥å…·
- æ²’åšå€™é¸é ç¯©å°±ç›´æŽ¥å…¨ vault æš´åŠ›æ¸…ç†
- æŠŠèªžæ„åˆä½µèˆ‡æ ¼å¼ä¿®è£œæ··åœ¨åŒä¸€æ‰¹æ¬¡äº‚åš
- æ¸…æŽ‰èˆŠé ï¼Œä½†ä¸è£œå…¥å£èˆ‡å›žæ»¾è·¯å¾‘

## Handoff


ault-deep-clean å®Œæˆå¾Œï¼Œä¸‹ä¸€æ­¥é€šå¸¸æ˜¯ï¼š

-
ault-check
-
ote-update
-
ault-reshape
- 	ag-check
"@

 = @"
---
name: tag-check
description: Use when the user wants a low-frequency audit of vault tags, including orphan tags, duplicate tags, taxonomy drift, inconsistent formats, or tag usage that no longer matches the current knowledge structure.
---

# Tag Check

## Description

	ag-check æ˜¯ Pigo vault çš„ tag å°ˆé …æª¢æŸ¥æ¨¡å¼ã€‚
å®ƒå°ˆæ³¨åœ¨ tag æ ¼å¼ä¸€è‡´æ€§ã€taxonomy æ¼‚ç§»ã€è¿‘ä¼¼ tag åˆä½µå€™é¸èˆ‡éŽåº¦/éŽå°‘ä½¿ç”¨çš„ tagï¼Œä¸å–ä»£çµæ§‹é‡æ•´ï¼Œä¹Ÿä¸å–ä»£å–®ç¯‡æ•´ç†ã€‚

## When to Use

ä½¿ç”¨æ™‚æ©Ÿï¼š

- ä½ æ‡·ç–‘ tag é–‹å§‹å¤±æŽ§
- æœ‰å¾ˆå¤šåŒç¾© tagã€å¤§å°å¯«å·®ç•°ã€æ ¼å¼ä¸ä¸€è‡´
-
ault-check æŒ‡å‡º tag health æœ‰å•é¡Œ
- å¤§é‡æ¬ç§»æˆ–åŒ¯å…¥å¾Œï¼Œéœ€è¦é‡æ–°ç›¤é»ž tag

ä¸è¦ç”¨åœ¨ï¼š

- å–®ç¯‡ç­†è¨˜ç·¨ä¿®ï¼šæ”¹ç”¨
ote-update
- å¤§ç¯„åœåˆ†é¡žæ¬ç§»ï¼šæ”¹ç”¨
ault-reshape
- æ·±åº¦å…§å®¹æ¸…ç†ï¼šæ”¹ç”¨
ault-deep-clean

## Vault Index Usage

ç›®å‰ .vault-index æ²’æœ‰å°ˆç”¨ tag queryï¼Œæ‰€ä»¥ 	ag-check æ‡‰å…ˆç”¨ index éŽ–å®šæ´»èºåˆ†é¡žèˆ‡é«˜é »ä¸»é¡Œå€ï¼Œå†å›žåˆ° frontmatter / å…§å®¹åšç²¾ç¢º tag æª¢æŸ¥ã€‚

- Vault rootï¼š
  C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian
- Query toolï¼š
  C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian\.vault-index\query_vault.py

å„ªå…ˆæŸ¥é€™äº›ï¼š

- y-classification
-
ts
-
elated-notes

åŽŸå‰‡ï¼š

1. å…ˆæ‰¾ tag å•é¡Œæœ€å¯èƒ½é›†ä¸­çš„åˆ†é¡žå€
2. å†åšç²¾ç¢º tag æŽƒæèˆ‡æ¯”å°
3. tag èªžæ„åˆä½µä¸€å¾‹ä¿å®ˆè™•ç†

## Risk-Tier Contract

- Low-risk
  å¯ç›´æŽ¥æå‡º format-only normalization å»ºè­°ï¼Œä¾‹å¦‚å¤§å°å¯«ã€ç©ºç™½ã€é€£å­—è™Ÿçµ±ä¸€ã€‚
- Medium-risk
  åŒç¾© tag åˆä½µã€taxonomy æ›´æ–°ã€æ‰¹æ¬¡ retag ä¸€å¾‹é€² Pending Approval Planã€‚
- High-risk
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

- æ ¸å¿ƒçµè«–
- 	ag inventory
-
ormat-only å•é¡Œ
- merge candidates
- Pending Approval Plan

## Common Mistakes

- æ²’å…ˆçœ‹åˆ†é¡žä¸Šä¸‹æ–‡å°±ç›´æŽ¥åˆä½µ tag
- æŠŠèªžæ„ä¸åŒä½†å­—é¢ç›¸è¿‘çš„ tag å¼·è¡Œåˆä½µ
- åªæ”¹ tagï¼Œä¸æª¢æŸ¥è©²ä¸»é¡Œæ˜¯å¦å…¶å¯¦æ‡‰å‡ç´šç‚ºåˆ†é¡žæˆ– hub

## Handoff

	ag-check å®Œæˆå¾Œï¼Œä¸‹ä¸€æ­¥é€šå¸¸æ˜¯ï¼š

-
ault-check
-
ault-reshape
-
ote-update
"@

 = @"
---
name: transcript-to-note
description: Use when the user has transcript text, meeting notes, lecture transcripts, podcast transcripts, or transcript-like material that should be turned into a structured Obsidian note before later filing or formalization.
---

# Transcript To Note

## Description

	ranscript-to-note æ˜¯ transcript intake skillã€‚
å®ƒæŠŠé€å­—ç¨¿ã€æœƒè­°è½‰å¯«ã€èª²ç¨‹ transcriptã€podcast transcript æˆ– transcript-like text è½‰æˆçµæ§‹åŒ– Obsidian ç­†è¨˜åˆç¨¿ï¼Œä¹‹å¾Œå†äº¤çµ¦
ote-update æˆ– inbox-triage é€²ä¸€æ­¥æ­£å¼åŒ–èˆ‡æ­¸æª”ã€‚

## When to Use

ä½¿ç”¨æ™‚æ©Ÿï¼š

- ä½¿ç”¨è€…å·²ç¶“æœ‰ transcript text
- ä½ è¦æŠŠæœƒè­°ã€è¬›åº§ã€podcastã€è¨ªè«‡è½‰æˆå¯æ•´ç†ç­†è¨˜
- éœ€è¦å…ˆæŠ½å‡ºæ±ºç­–ã€è¡Œå‹•é …ã€é—œéµçŸ¥è­˜é»žï¼Œå†æ±ºå®šè¦ä¸è¦æ­£å¼æ­¸æª”

ä¸è¦ç”¨åœ¨ï¼š

- åªæœ‰ raw audio ä¸”æ²’æœ‰å¯è®€æ–‡å­—æ™‚ï¼Œé€™å€‹ skill ä¸åšåŽŸå§‹èªžéŸ³è¾¨è­˜
- å·²ç¶“æ˜¯æˆç†Ÿæ­£å¼ç­†è¨˜æ™‚ï¼Œæ”¹ç”¨
ote-update
- åªæ˜¯è¦åšæ•´é«”åˆ†é¡žæ¬ç§»æ™‚ï¼Œæ”¹ç”¨
ault-reshape

## Vault Index Usage

åœ¨è½‰å¯«å…§å®¹é€² note ä¹‹å‰ï¼Œå…ˆç”¨ vault index æŸ¥æ˜¯å¦å·²æœ‰åŒä¸»é¡Œæˆ–åŒä¾†æºæ­£å¼é ï¼Œé¿å…ç”Ÿæˆå®Œå…¨è„«ç¯€çš„æ–°è‰ç¨¿ã€‚

- Vault rootï¼š
  C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian
- Query toolï¼š
  C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian\.vault-index\query_vault.py

å„ªå…ˆæŸ¥é€™äº›ï¼š

-
ts
- 	itle-candidates
-
elated-notes
- y-classification

## Intake Workflow

### 1. Source Gate

å…ˆåˆ†è¾¨ï¼š

- æ˜¯å¦å·²æœ‰ transcript text
- æ˜¯å¦åªæ˜¯ raw audio
- æ˜¯å¦å·²æœ‰èªªæ˜Žä¸»é¡Œã€è¬›è€…ã€æ—¥æœŸã€ç”¨é€”

è‹¥åªæœ‰ raw audioï¼Œæ‡‰æ˜Žç¢ºå‘ŠçŸ¥éœ€è¦å…ˆå–å¾— transcript textã€‚

### 2. Transcript Structuring

å°‡ transcript è½‰æˆï¼š

- æ ¸å¿ƒæ‘˜è¦
- é—œéµæ®µè½ æˆ– ä¸»é¡Œå€å¡Š
- æ±ºç­– / è¡Œå‹•é …ï¼ˆå¦‚æžœæ˜¯æœƒè­°ï¼‰
- é—œéµçŸ¥è­˜é»žï¼ˆå¦‚æžœæ˜¯å…§å®¹åž‹ transcriptï¼‰
- å¾…ç¢ºèªå•é¡Œ

### 3. Destination Decision

æ ¹æ“šå…§å®¹æ±ºå®šï¼š

- å…ˆé€² 0-Inbox
- æˆ–ç›´æŽ¥äº¤ç”±
ote-update æ­£å¼åŒ–
- æˆ–æ¨™è¨˜ç‚ºæŸä¸€åˆ†é¡žçš„å€™é¸

## Expected Output

è¼¸å‡ºè‡³å°‘è¦æœ‰ï¼š

- ä¾†æºèªªæ˜Ž
- æ ¸å¿ƒæ‘˜è¦
- çµæ§‹åŒ–å…§å®¹
- å¯èƒ½çš„ç›®æ¨™åˆ†é¡ž
- ä¸‹ä¸€æ­¥å»ºè­°

## Common Mistakes

- æŠŠ raw audio ç•¶æˆ transcript text ç›´æŽ¥è™•ç†
- transcript å¤ªé•·å»ä¸åˆ†æ®µ
- æ²’æœ‰æŠ½å‡ºæ±ºç­–èˆ‡è¡Œå‹•é …
- ç”Ÿæˆè‰ç¨¿å¾Œå®Œå…¨ä¸è€ƒæ…®æ—¢æœ‰æ­£å¼ç­†è¨˜

## Handoff

	ranscript-to-note å®Œæˆå¾Œï¼Œä¸‹ä¸€æ­¥é€šå¸¸æ˜¯ï¼š

-
ote-update
- inbox-triage
-
ault-GPS
"@

 = @"
---
name: vault-bootstrap
description: Use when initializing a brand-new vault or workspace that needs first-time structure, conventions, templates, and navigation rather than maintenance on an already mature vault.
---

# Vault Bootstrap

## Description


ault-bootstrap æ˜¯æ–° vault / æ–° workspace çš„èµ·å§‹å»ºç½® skillã€‚
å®ƒä¸é©åˆç›´æŽ¥æ‹¿ä¾†é‡åšæˆç†Ÿä¸­çš„ Pigo ä¸» vaultï¼›åœ¨ç›®å‰ Codex runtime ä¸­ï¼Œæ‡‰æŠŠå®ƒè¦–ç‚ºè¦åŠƒèˆ‡åˆå§‹åŒ–å…¥å£ï¼Œè€Œä¸æ˜¯æ—¥å¸¸ç¶­è­·å·¥å…·ã€‚

## Current Mode

ç›®å‰ç‚º deferred-mode å®‰è£ç‰ˆæœ¬ï¼š

- å¯ç”¨ä¾†è¦åŠƒæ–° vault çš„åˆå§‹åŒ–çµæ§‹
- å¯ç”¨ä¾†å®šç¾©åŸºæœ¬åˆ†é¡žã€æ¨¡æ¿èˆ‡å°Žèˆªå±¤
- ä¸æ‡‰ç›´æŽ¥é‡åšæ—¢æœ‰æˆç†Ÿ vault çš„éª¨æž¶

## Handoff

æˆç†Ÿ vault çš„æ—¥å¸¸ç¶­è­·è«‹æ”¹ç”¨ï¼š

-
ault-check
-
ault-reshape
-
ault-GPS
"@

 = @"
---
name: agent-create
description: Use when the user wants to define a brand-new custom vault or workflow agent with a dedicated role, trigger conditions, boundaries, and output contract.
---

# Agent Create

## Description

gent-create æ˜¯å»ºç«‹æ–° agent çš„å…¥å£ skillã€‚
ç›®å‰å…ˆä»¥ planning-first æ¨¡å¼å®‰è£ï¼Œé©åˆå®šç¾©æ–° agent çš„ç”¨é€”ã€é‚Šç•Œèˆ‡è¼¸å‡ºå¥‘ç´„ï¼Œä¸å»ºè­°åœ¨æ²’æœ‰æ˜Žç¢ºéœ€æ±‚æ™‚å¤§é‡ç”Ÿæˆ agentã€‚

## Current Mode

- å…ˆåš role å®šç¾©
- å…ˆåš trigger èˆ‡é‚Šç•Œè¨­è¨ˆ
- çœŸæ­£è½åœ°å‰ï¼Œå…ˆç¢ºèªæ˜¯å¦ç¾æœ‰ skill å·²è¶³å¤

<!-- AGENT_SKILL_DEDUPE_NOTE -->
## Duplicate Consolidation

This is the canonical `vault-deep-clean` Skill after Agent dedupe on 2026-04-29.

Archived duplicate variants:
- `Obsidian_skill_set/vault-deep-clean/SKILL.merged.md`
- `shared-skills/vault-deep-clean/SKILL.merged.md`
- `skills/vault-deep-clean/SKILL.merged.md`
<!-- /AGENT_SKILL_DEDUPE_NOTE -->
