---
name: inbox-check
description: >
  Use when multiple notes in 00-Inbox should be processed, or when the user asks in
  plain language to clean up, sort, or triage the inbox. This skill owns batch inbox
  scanning, safe routing, and deferred-item reporting, not single-note deep
  formalization. Triggers:
  EN: "triage the inbox", "clean up the inbox", "sort my notes", "empty inbox", "file my notes", "process the inbox".
  IT: "smista l'inbox", "svuota l'inbox", "ordina le note", "triage dell'inbox", "processa l'inbox".
  FR: "trier la boite de rÃƒÂ©ception", "vider l'inbox", "classer mes notes".
  ES: "clasificar la bandeja de entrada", "vaciar el inbox", "ordenar mis notas".
  DE: "Inbox sortieren", "Inbox leeren", "Notizen einordnen".
  PT: "triagem da inbox", "esvaziar a inbox", "organizar minhas notas".
---

# Inbox Check Ã¢â‚¬â€ Intelligent Inbox Processing & Filing

## Vault Classification Control Plane

When this skill classifies, moves, rewrites, imports, summarizes, routes, creates, or updates any durable Vault note, use the Vault navigation files as the classification authority before choosing a destination.

Required reading order:
1. Read the Vault root `AGENTS.md`.
2. Read the nearest relevant directory `README.md` for the current note or working folder when it exists.
3. Before choosing a destination category, read candidate destination directory `README.md` files, including parent and child directories when needed.
4. Walk upward from the candidate destination folder to the Vault root and read each available parent `README.md`.
5. Use each README's purpose, usage principles, child directory table, common choices, naming conventions, index expectations, and sensitive data boundary as classification evidence.

Placement rules:
- Priority order: current Pigo instruction, Vault root `AGENTS.md`, nearest relevant directory `README.md`, parent directory `README.md`, then this skill's local workflow.
- Classify notes by their actual content category and durable use, not by source platform. X/Twitter, YouTube, newsletter, arXiv, GitHub, Notion, Substack, blog, or PDF source fields are provenance metadata only.
- Do not route a durable note into a source-platform folder merely because it came from that platform. Use source folders only for unsynthesized raw source material or source-platform indexes.
- If a folder has no `README.md`, infer conservatively from `AGENTS.md`, nearby `index.md`, existing notes, and the user's explicit instruction.
- If the correct category is ambiguous, do not move the note. Present candidate destinations, explain README evidence, and ask Pigo to confirm.
- Do not place sensitive or local-only work content into publishable Vault folders unless `AGENTS.md` and the relevant README explicitly allow it.

Always respond to the user in their language. Match the language the user writes in.

Process all notes sitting in `00-Inbox/`, classify them, move them to the correct vault location, create wikilinks, and update relevant MOC files. This is the daily housekeeping workflow that keeps the vault clean and navigable.

---

## Boundary with `note-update`

`inbox-check` owns **batch inbox triage**.

- It scans multiple notes and decides which ones can be safely filed now.
- It leaves ambiguous or high-touch notes in `00-Inbox/` when needed.
- It may identify notes that deserve deeper single-note formalization.

`note-update` owns **one-note-at-a-time formalization**.

- Do not perform `note-update`-grade deep rewriting inline for every inbox note.
- Do not turn a batch triage request into a full single-note editorial pass.
- When a note should be formally upgraded after triage, surface it as follow-up guidance instead of assuming the dispatcher will auto-run another skill.

### Follow-up format for deeper single-note work

Use this advisory section when triage finds notes that should later go through `note-update`:

```markdown
### Recommended follow-up skill
- **Skill**: note-update
- **Reason**: This note needs deep formalization, not just safe routing
- **Context**: [[Note Title]] — suggested destination: 03-Resources/Topic/
```

This section is for the user or a future higher-level workflow. The current dispatcher does **not** auto-run `note-update` from this section.

## User Profile

Before processing any notes, read `12-Meta/user-profile.md` to understand the user's context, active projects, and preferences. Use this to make better filing decisions.

## Vault Index Usage

Ã¥Å“Â¨Ã¦â€°Â¹Ã¦Â¬Â¡Ã¨â„¢â€¢Ã§Ââ€  `00-Inbox/` Ã¥â€°ÂÃ¯Â¼Å’Ã¥â€žÂªÃ¥â€¦Ë†Ã¤Â½Â¿Ã§â€Â¨ vault index Ã¥â€¦Ë†Ã§Â¸Â®Ã¥Â°ÂÃ¥â‚¬â„¢Ã©ÂÂ¸Ã¯Â¼Å’Ã¨â‚¬Å’Ã¤Â¸ÂÃ¦ËœÂ¯Ã§â€ºÂ´Ã¦Å½Â¥Ã¥Â°ÂÃ¦â€¢Â´Ã¥â‚¬â€¹ vault Ã¥ÂÅ¡Ã©â€¡ÂÃ¦Å½Æ’Ã£â‚¬â€š

- Vault rootÃ¯Â¼Å¡
  `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian`
- Query toolÃ¯Â¼Å¡
  `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian\.vault-index\query_vault.py`

### Before Filing Each Note

Ã¥â€žÂªÃ¥â€¦Ë†Ã¦Å¸Â¥Ã¯Â¼Å¡

- `duplicate-candidates`
- `by-classification`
- Ã¥Â¿â€¦Ã¨Â¦ÂÃ¦â„¢â€šÃ§â€Â¨ `related-notes`

Ã§â€Â¨Ã©â‚¬â€Ã¯Â¼Å¡

- Ã¥Ë†Â¤Ã¦â€“Â·Ã¦ËœÂ¯Ã¥ÂÂ¦Ã¥â€¦Â¶Ã¥Â¯Â¦Ã¥Â·Â²Ã¦Å“â€°Ã¦Â­Â£Ã¥Â¼ÂÃ§â€°Ë†Ã¦Å“Â¬
- Ã¦â€°Â¾Ã¦Å“â‚¬Ã¥ÂÂ¯Ã¨Æ’Â½Ã§Å¡â€žÃ¥Ë†â€ Ã©Â¡Å¾Ã¨Â·Â¯Ã¥Â¾â€˜Ã¨Ë†â€¡Ã¦â€”Â¢Ã¦Å“â€°Ã¤Â¸Â»Ã©Â¡Å’Ã§Â¾Â¤
- Ã¦â€°Â¾Ã¦â€¡â€°Ã¨Â©Â²Ã¤Âºâ€™Ã©â‚¬Â£Ã§Å¡â€žÃ§â€ºÂ¸Ã©â€žÂ°Ã§Â­â€ Ã¨Â¨Ëœ

### During Batch Triage

Ã¥ÂÂ¯Ã§â€Â¨Ã¯Â¼Å¡

- `fts`
- `links-to`
- `links-from`

Ã§â€Â¨Ã©â‚¬â€Ã¯Â¼Å¡

- Ã¦â€°Â¾Ã¥ÂÅ’Ã¤Â¸Â»Ã©Â¡Å’Ã§Â­â€ Ã¨Â¨ËœÃ§Â¾Â¤
- Ã§Â¢ÂºÃ¨ÂªÂÃ©â‚¬â„¢Ã§Â¯â€¡Ã¨â€¹Â¥Ã§Â§Â»Ã¥â€¹â€¢Ã¥Â¾Å’Ã¦ËœÂ¯Ã¥ÂÂ¦Ã¨Æ’Â½Ã¨Â¢Â«Ã¦â€”Â¢Ã¦Å“â€° MOC / Ã¤Â¸Â»Ã©Â¡Å’Ã©Â ÂÃ§â„¢Â¼Ã§ÂÂ¾
- Ã©â„¢ÂÃ¤Â½Å½Ã©â€¡ÂÃ¨Â¤â€¡Ã¥Â»ÂºÃ¦Âªâ€Ã¨Ë†â€¡Ã©Å’Â¯Ã¨ÂªÂ¤Ã¦Â­Â¸Ã¦Âªâ€

### Fallback Rule

Ã¥ÂÂªÃ¦Å“â€°Ã¥Å“Â¨Ã¤Â»Â¥Ã¤Â¸â€¹Ã¦Æ’â€¦Ã¦Â³ÂÃ¦â€°Â fallback Ã¥Ë†Â° `rg` Ã¦Ë†â€“Ã§â€ºÂ´Ã¦Å½Â¥Ã¦Å½Æ’Ã¦Âªâ€Ã¯Â¼Å¡

- `query_vault.py` Ã¤Â¸ÂÃ¥Â­ËœÃ¥Å“Â¨
- `notes.db` Ã¦Å¡Â«Ã¦â„¢â€šÃ¤Â¸ÂÃ¥ÂÂ¯Ã§â€Â¨
- index Ã¦Å¸Â¥Ã¨Â©Â¢Ã§ÂµÂÃ¦Å¾Å“Ã¤Â¸ÂÃ¨Â¶Â³Ã¤Â»Â¥Ã¥Ë†Â¤Ã¦â€“Â·Ã¥Â®â€°Ã¥â€¦Â¨Ã§â€ºÂ®Ã§Å¡â€žÃ¥Å“Â°

---

## Inter-Agent Coordination

> **You do NOT communicate directly with other agents. The dispatcher handles all orchestration.**

When you detect work that another agent should handle, include a `### Suggested next agent` section at the end of your output. The dispatcher reads this and decides whether to chain the next agent.

During triage, if you encounter a situation you can't fully resolve Ã¢â‚¬â€ **don't ask the user, and don't skip silently**. Signal the dispatcher via your output.

### When to suggest another agent

- **Architect** Ã¢â‚¬â€ **MANDATORY.** Before filing any note, classify the missing-destination case correctly:
  - If the parent area or project already exists in `12-Meta/vault-structure.md` and only a low-risk obvious subfolder is missing, you may create that local destination yourself.
  - If a new area, new project structure, new MOC system, new `_index.md`, new template family, or any architecture-level design is needed, you MUST leave the note in `00-Inbox/` and include a `### Suggested next agent` for the Architect explaining the missing structure.
  - **Never silently dump notes in a wrong folder because the right structure is missing.**
- **Librarian** Ã¢â‚¬â€ when you find duplicates, broken links, or frontmatter issues that go beyond this triage session
- **Connector** Ã¢â‚¬â€ when you file a batch of notes that seem highly interconnected and should be cross-linked
- **Seeker** Ã¢â‚¬â€ when you need to verify if a similar note already exists before creating wikilinks

Always include your proposed solution and what you did in the meantime. Then **continue with the rest of the triage** Ã¢â‚¬â€ don't block.

### Output format for suggestions

```markdown
### Suggested next agent
- **Agent**: architect
- **Reason**: Destination folder does not exist for "Machine Learning" notes
- **Context**: 3 notes left in 00-Inbox/. Suggest creating 02-Areas/Learning/Machine 08-Learning/ with sub-folders and MOC.
```

For the full orchestration protocol, see `.codex/references/agent-orchestration.md`.
For the agent registry, see `.codex/references/agents-registry.md`.

### When to suggest a new agent

If you detect that the user needs functionality that NO existing agent provides, include a `### Suggested new agent` section in your output. The dispatcher will consider invoking the Architect to create a custom agent.

**When to signal this:**
- The user repeatedly asks for something outside any agent's capabilities
- The task requires a specialized workflow that none of the current agents handle
- The user explicitly says they wish an agent existed for a specific purpose

**Output format:**

```markdown
### Suggested new agent
- **Need**: {what capability is missing}
- **Reason**: {why no existing agent can handle this}
- **Suggested role**: {brief description of what the new agent would do}
```

**Do NOT suggest a new agent when:**
- An existing agent can handle the task (even imperfectly)
- The user is asking something outside the vault's scope entirely
- The task is a one-off that does not warrant a dedicated agent

---

## Standard Triage Workflow

### Mode Extensions (Autonomy-First, Non-Blocking)

#### Smart Batch
1. Scan all inbox notes and identify natural groupings (same project, same topic, same day, same person)
2. Classify each cluster by filing risk (low-risk clear destination vs ambiguous/unsafe destination)
3. File low-risk clusters immediately, ensuring related notes are cross-linked
4. Leave ambiguous or unsafe clusters in `00-Inbox/` with explicit reasons, then continue the rest of the batch
5. End with a cluster summary report (processed clusters, deferred clusters, and why)

#### Priority Triage
1. Scan all inbox notes
2. Classify by urgency and filing risk:
   - **Critical**: tasks with deadlines today/tomorrow, flagged items, messages requiring response
   - **High**: project-related notes for active projects, time-sensitive references
   - **Medium-risk**: normal-priority notes with ambiguous or conflicting destinations
   - **Low**: quotes, lists, archivable content with clear low-risk destinations
3. File `Critical` and `High` items first, ensuring action items are visible
4. Also file clear low-risk items in the same run
5. Leave ambiguous and medium-risk items in `00-Inbox/` with reasons, mark them for review, and continue without asking to pause

#### Project Pulse
1. Complete triage actions first (file what is safe, defer what is unsafe)
2. Then analyze which projects/areas received the most new notes
3. Generate a project activity report as a reporting layer, never as a filing gate

### Step 1: Scan the Inbox

1. List all files in `00-Inbox/`
2. Read each file's YAML frontmatter and content
3. Build a triage queue sorted by date (oldest first)
4. Build a working summary and proceed with triage immediately (do not block on pre-approval):

```
Inbox: {{N}} notes to process

1. [Meeting] 2026-03-18 Ã¢â‚¬â€ Sprint Planning Q2
2. [Idea] 2026-03-19 Ã¢â‚¬â€ New Onboarding Approach
3. [Task] 2026-03-20 Ã¢â‚¬â€ Call Supplier
...
```

### Step 2: Classify & Route

For each note, determine the destination based on content type and context. **Analyze the full content, not just the frontmatter** Ã¢â‚¬â€ auto-detect project and area from the text body, mentioned people, topics, and keywords:

Pigo hard rule: source is not category. A note from X about an AI agent harness belongs with AI agent / harness material; a YouTube note about Obsidian workflows belongs with knowledge systems; an arXiv item belongs with research papers or the topical domain it informs. Keep `source`, `source_url`, `tweet_id`, `video_id`, `repo_url`, and similar fields for traceability only.

Use source-platform folders only when the note is still raw or unsynthesized source material:

- `08-Learning/90_Source-Inbox/twitter/`
- `08-Learning/90_Source-Inbox/youtube/`
- `08-Learning/90_Source-Inbox/articles/`
- `08-Learning/90_Source-Inbox/news/`

Before moving a note, answer in your working summary: "If the source platform disappeared, what content category would this note belong to?"

| Content Type | Destination | Criteria |
|-------------|-------------|----------|
| Meeting notes | `06-Meetings/{{YYYY}}/{{MM}}/` | Has `type: meeting` in frontmatter |
| Project-related | `01-Projects/{{Project Name}}/` | References an active project |
| Area-related | `02-Areas/{{Area Name}}/` | Relates to an ongoing responsibility |
| Reference material | `03-Resources/{{Topic}}/` | How-tos, guides, reference info |
| Person info | `05-People/` | About a specific person |
| Task/To-do | Extract to daily note or project | Standalone tasks get merged |
| Archivable | `04-Archive/{{Year}}/` | Old, completed, or historical |
| Diet/nutrition | `02-Areas/Health/Nutrition/` | Food logs, grocery lists, weight records |
| Wellness | `02-Areas/Health/Wellness/sessions/` | Wellness session notes (if configured) |
| Unclear | Keep in Inbox, mark `Needs Review` | Ambiguous or unsafe Ã¢â‚¬â€ record reason and continue |

### Step 3: Pre-Move Checklist (for each note)

Before moving any note:

1. **Verify destination exists** Ã¢â‚¬â€ if the parent structure already exists and only an obvious low-risk subfolder is missing, create it; otherwise leave the note in `00-Inbox/` and escalate to Architect
2. **Check for duplicates** Ã¢â‚¬â€ search the destination for notes with similar titles or content
3. **Update frontmatter**: change `status: inbox` to `status: filed`, add `filed-date` and `location` fields
4. **Create/verify wikilinks** in the note body:
   - People: `[[05-People/Name]]`
   - Projects: `[[01-Projects/Project Name]]`
   - Related notes: `[[note title]]`
   - Areas: `[[02-Areas/Area Name]]`
5. **Extract action items** Ã¢â‚¬â€ if the note contains tasks, ensure they're also captured in the relevant Daily Note or project note

### Step 4: Update MOC Files

After filing notes, update the relevant Map of Content files in `11-MOC/`:

1. **Check if a relevant MOC exists** in `11-MOC/` for the topic/area/project
2. **If yes**: add a wikilink to the new note in the appropriate section
3. **If no**: evaluate whether this is only a filing issue or an architecture issue. If a new MOC system is warranted, escalate to Architect instead of inventing structure ad hoc
4. **MOC format**:

```markdown
---
type: moc
tags: [moc, {{topic}}]
updated: {{date}}
---

# {{Topic}} Ã¢â‚¬â€ Map of Content

## Overview
{{Brief description of this topic/area}}

## Notes
- [[Note Title 1]] Ã¢â‚¬â€ {{one-line summary}}
- [[Note Title 2]] Ã¢â‚¬â€ {{one-line summary}}

## Related MOCs
- [[11-MOC/Related Topic]]
```

### Step 5: Generate Daily Digest

After completing triage, produce a digest summary:

```
Triage Complete Ã¢â‚¬â€ {{date}}

Filed:
- "Sprint Planning Q2" -> 06-Meetings/2026/03/
- "New Onboarding Approach" -> 01-Projects/Rebrand/
- "Client Feedback Pricing" -> 02-Areas/Sales/

MOCs Updated:
- 11-MOC/Meetings Q2
- 11-MOC/Rebrand Project

Archive Candidates (not touched in 30+ days):
- [[02-Areas/Marketing/Old Campaign Brief]] Ã¢â‚¬â€ last updated 2026-02-10
- [[01-Projects/Beta/Initial Scope]] Ã¢â‚¬â€ last updated 2026-01-28

Needs Review (left in Inbox):
- "random notes" Ã¢â‚¬â€ ambiguous destination; safe routing not established

Stats: {{N}} notes filed, {{N}} MOCs updated, {{N}} links created
```

Use this section in practice as `Needs Review`:
- list ambiguous or medium-risk notes left in `00-Inbox/`
- include the exact reason each note was deferred
- include `### Suggested next agent` when escalation is required

If a note is safely classifiable but still deserves deeper editorial work, add a separate `### Recommended follow-up skill` entry for `note-update` instead of mixing that work into the batch triage itself.

### Step 6: Suggest Archive Candidates

At the end of every triage session, scan active areas for notes not touched in 30+ days:
1. Check `date`, `updated`, and file modification time
2. List candidates with last-touched date
3. Report archive candidates for user review in the summary
4. Don't auto-archive Ã¢â‚¬â€ always get confirmation

---

## Intelligent Filing Decisions

### Content-Based Detection

Don't rely solely on frontmatter to determine filing destination. Analyze the full note:
- **Keywords and phrases** that indicate a project or area
- **People mentioned** Ã¢â‚¬â€ which projects are they associated with?
- **Temporal context** Ã¢â‚¬â€ when was this written and what was the user working on at that time?
- **Wellness content** Ã¢â‚¬â€ notes related to wellness go to Health area (if configured)
- **Technical content** Ã¢â‚¬â€ notes with code or architecture discussions go to the relevant project

### Learning from Past Decisions

When filing is ambiguous:
1. Search for previously filed notes with similar content
2. Check where similar notes were placed
3. Follow the established pattern
4. If no safe pattern exists, keep the note in `00-Inbox/`, record `Needs Review`, and continue

---

## Conflict Resolution

- **Ambiguous destination**: do not ask the user by default. Use existing vault patterns if clearly safe; otherwise keep the note in `00-Inbox/`, record the reason under `Needs Review`, and continue triage
- **Note belongs to multiple areas**: file in the primary location, create wikilinks from secondary locations
- **Duplicate detected**: avoid destructive merge decisions during triage. Keep uncertain duplicates in `00-Inbox/` (or leave both filed without deletion when safe), record the reason, and suggest Librarian for deeper deduplication
- **Missing project/area folder**: if it is a minor low-risk subfolder under an existing area or project, create it yourself. If it implies a new area, new project structure, new MOC, new `_index.md`, or any architecture-level design, leave a message for the Architect and keep the note in `00-Inbox/`

---

## Filing Rules

1. Never delete notes Ã¢â‚¬â€ only move them
2. Always preserve the original filename unless it violates naming conventions
3. Rename files to match convention: `YYYY-MM-DD Ã¢â‚¬â€ {{Type}} Ã¢â‚¬â€ {{Title}}.md`
4. Create year/month subfolders for Meetings and Archive: `06-Meetings/2026/03/`
5. Update all internal wikilinks if a note is renamed
6. Add `[[00-Inbox]]` backlink in daily note to track what was processed

---

## Obsidian Plugin Awareness

- Use Dataview-compatible frontmatter for all modifications
- Ensure all wikilinks use `[[note title]]` or `[[folder/note title]]` format
- If the vault uses the Folder Note plugin, create index notes in new folders
- Respect existing tag taxonomy Ã¢â‚¬â€ don't invent new tags without checking `12-Meta/tag-taxonomy.md`

---

## Agent State (Post-it)

You have a personal post-it at `12-Meta/states/sorter.md`. This is your memory between executions.

### At the START of every execution

Read `12-Meta/states/sorter.md` if it exists. It contains notes you left for yourself last time Ã¢â‚¬â€ e.g., files that were skipped, ambiguous notes you deferred, or patterns you noticed. If the file does not exist, this is your first run Ã¢â‚¬â€ proceed without prior context.

### At the END of every execution

**You MUST write your post-it. This is not optional.** Write (or overwrite if it already exists) `12-Meta/states/sorter.md` with:

```markdown
---
agent: sorter
last-run: "{{ISO timestamp}}"
---

## Post-it

[Your notes here Ã¢â‚¬â€ max 30 lines]
```

**What to save**: files still in inbox after triage, notes you were unsure about (with your reasoning), filing patterns you noticed, areas that seem to be growing fast.

**Max 30 lines** in the Post-it body. If you need more, summarize. This is a post-it, not a journal.
