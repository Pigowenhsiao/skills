---
name: deadline-summary
description: Use when the user wants a deadline-oriented summary from known tasks, notes, and supplied context, while recognizing that external deadline aggregation may still be limited in the current runtime.
---

# Deadline Summary

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

Summarize known deadlines from available vault context without pretending that live calendar or inbox integrations exist when they do not.

## When to Use

Use this skill when the user wants:

- upcoming deadlines
- a due-soon summary
- risk flags for missed dates
- a compact view of what must happen first

Do not use this skill when:

- the user expects live email or calendar aggregation
- no task, note, or supplied context exists to summarize
- the user wants a full weekly plan rather than a deadline-first lens

## Source Policy

Allowed sources:

- user-supplied task lists
- current note text
- known vault notes
- previously captured project deadlines

Not allowed:

- claiming access to live calendar events that were not actually provided
- inventing due dates
- silently treating ambiguous dates as confirmed deadlines

## Workflow

### 1. Gather Available Inputs

Collect deadlines from:

- the user message
- attached or referenced notes
- relevant vault pages already available in the session

If no usable source exists, say that directly instead of fabricating a summary.

### 2. Normalize Each Date

For each candidate deadline, classify it as:

- confirmed date
- approximate date
- inferred but unconfirmed

Always separate confirmed dates from assumptions.

### 3. Build the Deadline View

Group items into:

- overdue
- due this week
- due soon but not immediate
- missing owner or missing date

### 4. Add Risk Checkpoints

Call out any item that has:

- no owner
- no next step
- unclear date source
- dependency on missing information

### 5. Confirm Gaps Explicitly

If external aggregation would materially change the answer, state that limitation plainly.

## Output Format

Use this structure:

1. deadline snapshot
2. overdue items
3. due soon
4. missing-information risks
5. suggested next actions

## Common Mistakes

- mixing confirmed and inferred dates without labels
- claiming live-system coverage that does not exist
- giving a weekly agenda instead of a deadline-first summary
- hiding missing owners or missing dates

## Handoff

- use `week-planner` when the user wants a full week plan
- use `meeting-brief` when the real need is preparation for one meeting
- keep migration-gated limits explicit if external sources are unavailable

<!-- AGENT_SKILL_DEDUPE_NOTE -->
## Duplicate Consolidation

This is the canonical deadline-summary Skill after Agent dedupe on 2026-04-29.

Archived duplicate variants:
- Obsidian_skill_set/deadline-summary/SKILL.merged.md
- skills/deadline-summary/SKILL.merged.md
<!-- /AGENT_SKILL_DEDUPE_NOTE -->
