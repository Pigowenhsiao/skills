# Upstream Feature Map: `nashsu/llm_wiki` vs Pigo `llm-wiki`

## Source Compared

- Repo: `https://github.com/nashsu/llm_wiki`
- Snapshot reviewed: `v0.3.10`
- Commit: `a0dac9a3517008cb277f37bad75024a6b4a5d706`

## Purpose of This Note

This file records which upstream capabilities should be adopted into the Pigo
`llm-wiki` skill, which should be deferred, and why.

## Adopt Now: Workflow-Level Features

### 1. `purpose.md`

- Upstream use: persistent statement of goals, key questions, and thesis.
- Adopted here: yes.
- Reason: improves ingest and query quality without requiring a new app.

### 2. `overview.md`

- Upstream use: continuously refreshed summary of the whole wiki.
- Adopted here: yes.
- Reason: gives future sessions a faster orientation layer than `index.md` alone.

### 3. Two-step ingest

- Upstream use: analysis pass, then generation pass.
- Adopted here: yes.
- Reason: better quality control, lower duplicate risk, clearer checkpoints.

### 4. `sources: []` traceability

- Upstream use: generated pages retain source lineage.
- Adopted here: yes.
- Reason: required for trust, lint, merge decisions, and later cleanup.

### 5. Review queue

- Upstream use: async human-in-the-loop review items.
- Adopted here: yes, in markdown form.
- Reason: keeps unresolved judgment calls visible without needing UI state.

### 6. Deep research follow-up

- Upstream use: graph insights can trigger targeted research.
- Adopted here: yes, as a workflow rule.
- Reason: useful even without graph UI; unresolved gaps can still generate
  bounded research tasks.

### 7. Ingest cache

- Upstream use: source hash cache to skip unchanged content.
- Adopted here: yes, as a lightweight JSON manifest.
- Reason: reduces repeat work and token waste in repeated ingest flows.

## Defer: Application-Level Features

### 1. Tauri desktop application

- Status: defer.
- Reason: not a skill concern; requires separate runtime, packaging, and Rust toolchain.

### 2. Interactive graph visualization

- Status: defer.
- Reason: belongs to an app or plugin, not markdown workflow rules.

### 3. Louvain communities and graph insights UI

- Status: defer.
- Reason: the concept can inform lint and research, but the full feature needs
  graph infrastructure and UI.

### 4. Vector semantic search / LanceDB

- Status: defer.
- Reason: useful later, but adds infrastructure and operational complexity.

### 5. Browser extension / clipper runtime

- Status: defer.
- Reason: acquisition is already delegated to `web-access`; no need to duplicate.

### 6. Multi-conversation persistent chat UI

- Status: defer.
- Reason: product behavior, not skill behavior.

## Local Role Split

- `Agent\llm-wiki`: canonical authoring source for the skill.
- `Agent\Obsidian_skill_set\llm-wiki`: synced copy for Agent-side distribution.
- `Pigo_Obsidian\.codex\skills\llm-wiki`: vault runtime wrapper for actual use.
- `C:\Users\hsi67063\.codex\skills\llm-wiki`: global runtime wrapper referenced by other skills.
- `Pigo_Obsidian\llm-wiki`: lightweight vault-local wrapper and references package.

## Rule of Thumb

Adopt upstream features when they improve the agent workflow contract.
Defer upstream features when they require a desktop application runtime.
