---
name: week-planner
description: Use when the user wants a weekly plan or agenda synthesized from known tasks, supplied context, and vault notes, while external calendar or email aggregation may still be limited.
---

# Week Planner

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

Build a practical weekly plan from known commitments and tasks without overstating access to live systems.

## When to Use

Use this skill when the user wants:

- a weekly plan
- a weekly agenda
- a prioritized week view
- a realistic next-seven-days layout

Do not use this skill when:

- the user only wants deadline risk review
- the user needs a meeting prep brief
- the answer would require live calendar or inbox data that is not available

## Planning Rules

The plan must distinguish between:

- confirmed commitments
- likely tasks
- inferred priorities
- open gaps that still need user input

Never present inferred availability as a confirmed calendar schedule.

## Workflow

### 1. Collect Weekly Inputs

Gather:

- tasks
- deadlines
- known meetings
- user constraints
- relevant vault notes

### 2. Normalize Priority

Sort work into:

- must happen this week
- should happen this week
- optional or stretch

### 3. Check Capacity

Before building the schedule, estimate whether the week is:

- realistic
- overloaded
- missing timing information

If overloaded, say so instead of forcing a fake neat plan.

### 4. Build the Week

Prefer a structure like:

- Monday to Friday blocks, if enough date context exists
- otherwise, a themed week plan by priority buckets

### 5. Add Explicit Checkpoints

Highlight:

- unresolved timing
- missing owner
- dependency risk
- places where a live calendar could change the plan

## Output Format

Use this structure:

1. week snapshot
2. must-do items
3. suggested day-by-day or block-by-block plan
4. overload or dependency risks
5. recommended next actions

## Common Mistakes

- pretending all tasks already have time blocks
- hiding overload
- mixing deadline summary with full weekly planning
- implying inbox or calendar coverage that was not actually queried

## Handoff

- use `deadline-summary` for deadline-first review
- use `meeting-brief` for one specific meeting
- use migration-gated connectors only when they are actually available

<!-- AGENT_SKILL_DEDUPE_NOTE -->
## Duplicate Consolidation

This is the canonical week-planner Skill after Agent dedupe on 2026-04-29.

Archived duplicate variants:
- Obsidian_skill_set/week-planner/SKILL.merged.md
- skills/week-planner/SKILL.merged.md
<!-- /AGENT_SKILL_DEDUPE_NOTE -->
