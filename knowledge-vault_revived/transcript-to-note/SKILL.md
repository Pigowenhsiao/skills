---
name: transcript-to-note
description: Use when the user has transcript text, meeting notes, lecture transcripts, podcast transcripts, or transcript-like material that should be turned into a structured Obsidian note before later filing or formalization.
---

# Transcript To Note

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

Turn transcript-like text into a structured Obsidian note before later filing, indexing, or deeper formalization.

## When to Use

Use this skill when the user provides:

- transcript text
- meeting notes
- lecture transcript
- podcast transcript
- interview transcript
- transcript-like raw notes that need structure first

Do not use this skill when:

- the user only has raw audio with no transcript text
- the note is already formalized and only needs light refinement
- the request is really about filing the whole inbox

## Source Gate

Before doing anything else, confirm the input is text, not audio.

If the user only has audio:

- say that transcript text is needed first
- do not pretend to perform transcription

## Vault Awareness

Use the local vault index when needed to avoid creating an isolated note that duplicates a known topic.

Relevant local paths:

- vault root: `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian`
- query tool: `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian\.vault-index\query_vault.py`

Prefer lightweight lookups such as:

- `fts`
- `title-candidates`
- `related-notes`
- `by-classification`

## Workflow

### 1. Identify the Source Type

Classify the input as:

- meeting
- lecture
- podcast
- interview
- generic transcript-like notes

### 2. Extract the Core Structure

Turn the text into a note with:

- source summary
- key points
- decisions or claims
- action items, if any
- open questions
- follow-up topics

### 3. Add a Checkpoint for Ambiguity

If the transcript is too noisy, fragmented, or context-poor, state that limitation instead of inventing certainty.

### 4. Choose the Immediate Destination

Decide whether the output should:

- stay as a structured draft
- be passed later to `note-update`
- be left for later batch filing through `inbox-check`

Do not silently escalate into a full vault restructuring step.

### 5. Keep the Output Reusable

The note should be easy to revisit later without rereading the whole transcript.

## Output Format

Use this structure:

1. source frame
2. concise summary
3. structured key points
4. action items and decisions
5. related-note suggestions
6. recommended next step

## Common Mistakes

- pretending audio transcription happened
- copying the transcript verbatim without structure
- inventing decisions that are not actually present
- performing full filing or vault cleanup instead of note structuring

## Handoff

- use `note-update` for deeper single-note formalization
- use `inbox-check` for batch inbox filing
- use `vault-GPS` later only if the resulting topic needs better navigation

<!-- AGENT_SKILL_DEDUPE_NOTE -->
## Duplicate Consolidation

This is the canonical transcript-to-note Skill after Agent dedupe on 2026-04-29.

Archived duplicate variants:
- Obsidian_skill_set/transcript-to-note/SKILL.merged.md
- skills/transcript-to-note/SKILL.merged.md
<!-- /AGENT_SKILL_DEDUPE_NOTE -->
