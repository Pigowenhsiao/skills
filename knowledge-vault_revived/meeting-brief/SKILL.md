---
name: meeting-brief
description: Use when the user wants preparation material for an upcoming meeting, combining known context, prior notes, and supplied references into a concise brief.
---

# Meeting Brief

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

Prepare a concise meeting brief from known context without claiming live enrichment from systems that were not actually queried.

## When to Use

Use this skill when the user wants:

- a prep brief for an upcoming meeting
- talking points
- known context gathered into one page
- risks, decisions, or open questions before the meeting

Do not use this skill when:

- the user wants live calendar lookup that is not available in the current run
- there is no identifiable meeting target
- the user is asking for post-meeting notes rather than prep

## Required Inputs

Try to identify:

- meeting title or purpose
- participants, if known
- date or time, if known
- relevant notes, projects, or documents

If the meeting target is unclear, ask for the minimum clarification needed.

## Workflow

### 1. Define the Meeting Frame

State what is known and what is missing:

- purpose
- participants
- timing
- related project or topic

### 2. Gather Only Real Context

Use only:

- user-provided notes
- prior vault material already available
- referenced documents actually supplied in the conversation

Do not imply live email or calendar enrichment unless it was truly performed.

### 3. Extract the Prep Signals

Capture:

- objective of the meeting
- relevant background
- decisions already made
- unresolved issues
- likely questions
- risks or blockers

### 4. Add a Checkpoint for Missing Context

If the brief is materially weakened by missing participants, agenda, or source notes, say so explicitly.

### 5. Produce a Short Actionable Brief

Keep the output tight enough to be read right before the meeting.

## Output Format

Use this structure:

1. meeting frame
2. objective
3. context to know
4. open questions
5. recommended talking points
6. preparation gaps

## Common Mistakes

- inventing agenda details
- mixing prep notes with post-meeting minutes
- hiding unknowns instead of labeling them
- writing a generic summary that does not help the user enter the meeting

## Handoff

- use `transcript-to-note` after the meeting if raw notes or transcript text arrives
- use `deadline-summary` if the actual need is deadline risk review
- keep external connector limitations explicit when they apply

<!-- AGENT_SKILL_DEDUPE_NOTE -->
## Duplicate Consolidation

This is the canonical meeting-brief Skill after Agent dedupe on 2026-04-29.

Archived duplicate variants:
- Obsidian_skill_set/meeting-brief/SKILL.merged.md
- skills/meeting-brief/SKILL.merged.md
<!-- /AGENT_SKILL_DEDUPE_NOTE -->
