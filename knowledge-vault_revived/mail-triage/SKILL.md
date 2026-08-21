---
name: mail-triage
description: Use when the user wants to triage email into actionable buckets or vault notes, while recognizing that live email connectors may not yet be enabled in the current Codex runtime.
---

# Mail Triage

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

Triage email-related work safely without pretending that live inbox access exists when it does not.

## When to Use

Use this skill when the user wants to:

- sort email into action buckets
- summarize provided email text
- convert email content into vault notes
- define a mail-triage workflow before live connectors are available

Do not use this skill when:

- the user expects direct mailbox access that has not been enabled
- no email text or email-derived note has been provided
- the request is actually about calendar scheduling rather than email handling

## Runtime Constraint

Current mode is connector-limited.

That means this skill may:

- process pasted email text
- process exported email notes
- propose a triage framework

That also means this skill may not:

- claim to read the live inbox
- claim unread counts
- claim message state from an external system unless it was actually queried

## Workflow

### 1. Identify the Input Type

Classify the source as one of:

- pasted email text
- summarized email notes
- user description of inbox categories
- workflow design request

### 2. Separate Signal from Noise

For each email or email cluster, label:

- action required
- waiting on someone else
- reference only
- archive candidate
- missing context

### 3. Extract Durable Outputs

When useful, convert into:

- action list
- follow-up list
- vault note summary
- decision log

### 4. Add a Checkpoint for Missing Live Access

If the user asked for live inbox behavior, state clearly what is and is not possible in the current runtime.

### 5. Keep the Output Operational

The result should help the user decide what to do next, not just summarize messages.

## Output Format

Use this structure:

1. input scope
2. triage buckets
3. urgent follow-ups
4. notes worth saving to the vault
5. runtime limitations

## Common Mistakes

- pretending live inbox access exists
- turning a triage request into a long narrative summary
- losing the distinction between action, waiting, and reference
- omitting the follow-up actions the user actually needs

## Handoff

- use `deadline-summary` if email content reveals due-date risk
- use `meeting-brief` if the email thread is really preparation for one meeting
- keep migration-gated connector limits explicit until they are actually available

<!-- AGENT_SKILL_DEDUPE_NOTE -->
## Duplicate Consolidation

This is the canonical mail-triage Skill after Agent dedupe on 2026-04-29.

Archived duplicate variants:
- Obsidian_skill_set/mail-triage/SKILL.merged.md
- skills/mail-triage/SKILL.merged.md
<!-- /AGENT_SKILL_DEDUPE_NOTE -->
