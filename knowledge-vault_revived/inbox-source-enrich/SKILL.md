---
name: inbox-source-enrich
description: >
  Use when Pigo asks to scan 00-Inbox notes and enrich incomplete notes from
  their original source path, source URL, attachment, or PDF. This skill
  complements llm-wiki, inbox-check, note-update, and pdf: it focuses on
  source-grounded completion of existing Inbox notes, including research-paper
  notes that need the original PDF extracted before generating the final note.
---

# Inbox Source Enrich

Use this skill to complete existing `00-Inbox` notes from their traceable
source material, while preserving Pigo's `llm-wiki` format and provenance
rules.

All durable output for Pigo must be written in Traditional Chinese.

## Boundaries

- This skill enriches existing notes. It does not own final filing or moving.
- Use `inbox-check` for batch triage, classification, and moving notes.
- Use `note-update` when Pigo asks for a deep editorial pass on one specific note.
- Use `llm-wiki` rules for note format, source traceability, indexes, and ingest logs.
- Use the PDF skill or local PDF tools when the source is a research paper PDF.
- Do not classify by source platform. X, YouTube, arXiv, GitHub, blogs, and PDFs are provenance only.

## Required Context

Before modifying notes, read these files when they exist:

1. Vault root `AGENTS.md`
2. `00-Inbox/index.md`
3. `08-Learning/index.md`
4. `08-Learning/README.md`
5. `08-Learning/purpose.md`
6. `08-Learning/99_Maintenance/status/LLM-Wiki-Index.md`
7. Recent entries in `08-Learning/99_Maintenance/status/LLM-Wiki-Ingest-Log.md`

If a required file is missing, continue conservatively and record the missing
context in the final report.

## Workflow

### 1. Build the Inbox Queue

Scan the active vault's `00-Inbox/` for Markdown notes. Ignore:

- `index.md`
- hidden files
- backup files
- files already marked as complete, processed, or archived unless Pigo explicitly asks to reprocess them

For each candidate, read frontmatter and body. Extract possible source pointers:

- `source`, `source_url`, `url`, `link`, `original_url`
- `source_path`, `original_path`, `path`, `file`, `attachment`
- `pdf`, `pdf_url`, `paper_url`, `doi`, `arxiv`, `pmid`
- Markdown links, Obsidian wikilinks, and local absolute paths in the body

Create a short processing queue with:

- note path
- detected source pointers
- inferred source type
- whether the source is available
- whether human confirmation is needed

### 2. Resolve the Source

Prefer sources in this order:

1. Local original file path
2. Local attachment or PDF path
3. Canonical source URL from frontmatter
4. URL found in the body
5. DOI/arXiv/PubMed identifier that can resolve to a paper page or PDF

Do not invent missing sources. If no source can be resolved, leave a `待確認`
section in the note and include the note in the deferred report.

For web sources, fetch or convert only the needed content and preserve the URL.
For local files, read the file directly. For PDFs, follow the paper workflow.

### 3. Paper / PDF Workflow

Treat a note as paper-like when any of these are true:

- frontmatter type includes `paper`, `research`, `arxiv`, `pdf`, or `literature`
- source URL contains `arxiv.org`, `doi.org`, `pubmed`, `biorxiv`, `medrxiv`, or journal domains
- note body references abstract, paper, experiment, method, benchmark, citation, or DOI
- original source is a PDF

For paper-like notes:

1. Locate the original PDF from local paths first.
2. If only a paper page or identifier exists, resolve the PDF URL when possible.
3. Download only when needed and when network access is allowed by the current environment.
4. Extract text with available PDF tools, preferring structured extraction when possible.
5. Use the abstract, introduction, methods, results, conclusion, limitations, and references as evidence.
6. If the PDF cannot be fetched or extracted, enrich only from available metadata and mark the gap clearly.

Paper note sections should include:

- `## 論文資訊`
- `## 研究問題`
- `## 方法`
- `## 實驗與資料`
- `## 主要發現`
- `## 限制與注意事項`
- `## 對 Pigo 的可用價值`
- `## 可引用觀點`
- `## 來源與追溯`

### 4. Enrich the Note

Preserve existing user-written content unless it is clearly a placeholder,
login-wall failure note, empty stub, or duplicate raw dump.

Use `llm-wiki` frontmatter expectations. At minimum include:

```yaml
---
title: ""
source: ""
source_url: ""
source_path: ""
created: ""
type: ""
tags: []
sources: []
status: enriched
---
```

Only include fields that are known or useful. Keep `sources` as the full
traceability list. Never drop the original path or URL.

General enriched note sections should include:

- `## 來源與脈絡`
- `## 核心摘要`
- `## 關鍵知識點`
- `## 詳細筆記`
- `## 與既有知識庫的關聯`
- `## 待確認`
- `## 來源與追溯`

When adding wikilinks, link only to concepts or notes that are likely to exist
or are useful future anchors. Avoid noisy over-linking.

### 5. Safety Rules

- Before editing, present a concise plan if Pigo has not already approved the modification.
- Back up or preserve the original content when the edit is large.
- Do not move the note out of `00-Inbox` unless Pigo explicitly asks.
- Do not overwrite a note if the source cannot be verified.
- Do not fabricate bibliographic metadata, quotes, page numbers, claims, or results.
- Mark uncertain items in `待確認` instead of smoothing over gaps.
- Respect source provenance: classification is based on content, not platform.

### 6. Index and Status Updates

After applying changes:

- Update `00-Inbox/index.md` if the vault uses it as an active Inbox index.
- Add an ingest/update entry to `08-Learning/99_Maintenance/status/LLM-Wiki-Ingest-Log.md` when appropriate.
- Write or update the task's `STATUS_*.md` with:
  - what changed
  - validation result
  - failures or blockers
  - recommended next step

## Verification

Before reporting completion:

1. Re-read each modified note.
2. Confirm frontmatter is still a valid YAML block.
3. Confirm all source paths or URLs used in the note are preserved.
4. Confirm paper notes cite PDF-derived evidence only when PDF extraction succeeded.
5. Confirm no unrelated notes were modified or moved.
6. Report deferred notes separately with exact reasons.

## Output Report

End with:

- processed notes
- enriched notes
- deferred notes and why
- source/PDF failures
- files modified
- validation performed
- next recommended action
