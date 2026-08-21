<!-- BEGIN AGENT_DIRECTORY_README -->
# Directory: skills\x-twitter-watch

## Purpose
Skill collection area. Directories here usually group SKILL.md workflows, references, scripts, and assets that AI agents can load selectively.

## Provenance
- provided_by_agent: Codex
- provided_by_computer: Pigo Windows workstation
- processing_skill: directory-readme-generation
- processed_at: 2026-05-19T21:19:16+09:00

## AI Reading Guide
- Start with the files or child folders listed in Primary read targets.
- Prefer nearby AGENTS.md, SKILL.md, README.md, and Readme.md files when present.
- Treat archived or vendored content as reference material unless a task explicitly targets it.

## Primary Read Targets
- `Readme.md`
- `README.md`
- `SKILL.md`
- `Skill.md`
- `Invoke-XWatchlist.ps1`

## Immediate Child Directories
- None detected.

## Immediate Files
- `Invoke-XWatchlist.ps1`
- `SKILL.md`

## Parent
- $parent
<!-- END AGENT_DIRECTORY_README -->

---

# X Watch Automation

此資料夾放 Vault 內的 X/Twitter watchlist 腳本。

## xiaoxiaodong01

手動執行：

```powershell
& "14-Skills\x-twitter-watch\Invoke-XWatchlist.ps1" -Account "xiaoxiaodong01" -UpdateState -WriteReport
```

如果你已經看到一則新貼文 URL，可以直接把 status ID 丟進去：

```powershell
& "14-Skills\x-twitter-watch\Invoke-XWatchlist.ps1" -Account "xiaoxiaodong01" -CandidateStatusIds "2056412276593410537" -UpdateState -WriteReport
```

輸出位置：

- Raw run JSON: `08-Learning/90_Source-Inbox/twitter/raw/`
- Watch report/state/config: `08-Learning/90_Source-Inbox/twitter/watchlists/`

限制：公開搜尋與鏡像可能漏掉最新貼文；這個腳本負責候選偵測，不替代正式 `llm-wiki summary` 整理流程。


