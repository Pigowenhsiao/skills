---
name: hermes-agent-self-evolution-executor
description: Run hermes-agent-self-evolution on skills from ~/Documents/Agent repo. Handles skill discovery, path patching, framework constraints, and result deployment.
trigger: "When the user asks to improve/optimize/evolve a skill using hermes-agent-self-evolution"
category: hermes-agent-self-evolution
---

# hermes-agent-self-evolution Executor

---

## Installation (one-time)

```bash
# Clone framework (uses ~/Downloads, not ~/.hermes)
git clone https://github.com/NousResearch/hermes-agent-self-evolution ~/Downloads/hermes-agent-self-evolution

# Install into hermes-agent venv (includes dspy + gepa dependencies)
~/.hermes/hermes-agent/venv/bin/pip install -e ~/Downloads/hermes-agent-self-evolution/"[dev]"

# Verify — dry-run needs no API key
~/.hermes/hermes-agent/venv/bin/python -m evolution.skills.evolve_skill --skill github-code-review --dry-run
```

**Python env**: Always invoke via `~/.hermes/hermes-agent/venv/bin/python`. Do NOT `source activate`.
**lxml conflict**: Some system packages conflict with crawl4ai's lxml~=5.3 requirement. Ignore — the venv has the correct version.
**Install location**: `~/Downloads/hermes-agent-self-evolution` (not `~/.hermes/hermes-agent-self-evolution`).

## Skill Health Scan（進化前必做）

使用 `terminal` + Python3 對技能做大健康檢查（`execute_code` 在 cron 模式被封鎖）：

```bash
python3 - << 'PYEOF'
import re
from pathlib import Path

skills_dir = Path.home() / ".hermes" / "skills"
results = []

for skill in sorted(skills_dir.iterdir()):
    if not skill.is_dir(): continue
    md = skill / "SKILL.md"
    if not md.exists(): continue

    content = md.read_text()
    size = len(content)

    steps = len(re.findall(r'^\d+\.\s', content, re.MULTILINE))

    has_trigger = bool(re.search(r'(?i)##?\s*trigger|觸發', content))
    has_pitfalls = bool(re.search(r'(?i)##?\s*pitfall|陷阱', content))
    has_verification = bool(re.search(r'(?i)##?\s*verif|驗證', content))
    has_examples = bool(re.search(r'(?i)##?\s*example|範例', content))

    score = 0
    if has_trigger: score += 2
    if has_pitfalls: score += 2
    if has_verification: score += 2
    if has_examples: score += 1
    if steps >= 3: score += 2
    if size > 5000: score += 1
    score = min(score, 10)

    results.append({
        'name': skill.name, 'size': size, 'size_kb': size / 1024,
        'score': score, 'is_oversized': size > 15000,
        'is_gstack': skill.name.startswith('gstack-'),
    })

results.sort(key=lambda x: x['score'])

candidates = [r for r in results if not r['is_oversized'] and not r['is_gstack'] and 4 <= r['score'] <= 6]
print(f"進化候選（分數 4-6）：")
for r in candidates:
    print(f"  {r['name']}: {r['size_kb']:.1f}KB, 分數={r['score']}")

print(f"\n跳過（已足夠好，分數 7+）：")
for r in [x for x in results if x['score'] >= 7 and not x['is_oversized']][:10]:
    print(f"  {r['name']}: {r['size_kb']:.1f}KB, 分數={r['score']}")

print(f"\n跳過（超標或 gstack）：")
for r in [x for x in results if x['is_oversized'] or x['is_gstack']][:10]:
    flag = "🚨" if r['is_oversized'] else "⚠️"
    print(f"  {flag} {r['name']}: {r['size_kb']:.1f}KB, 分數={r['score']}")
PYEOF
```

**判斷基準：**
- 🚨 超標（>15KB）：需先手動拆解或壓縮，否則進化失敗
- ✅ 可進化：大小 OK + 品質分 < 7 的技能優先進化
- 良好（≥7分）：可跳過浪費

## Pre-flight Checklist

1. **Three directory locations to keep straight**:
   - `~/.hermes/skills/<skill-name>/` — **runtime skills** that Hermes actually loads at runtime
   - `~/.hermes/hermes-agent/skills/<category>/<skill-name>/` — **framework's copy** the evolution tool reads from
   - `~/Documents/Agent/<skill-name>/` — **git-tracked source of truth** (may not exist for all skills)
2. **Evolution reads from framework dir**: copy skill to `~/.hermes/hermes-agent/skills/<category>/<skill-name>/` before running
3. **Deployment targets runtime dir**: evolved content deploys to `~/.hermes/skills/<skill-name>/SKILL.md`, NOT back to framework dir
4. **Check vault/path variables**: skills with hardcoded paths (e.g., `E:/obsidian/PigoVault`) need updating to Linux paths BEFORE running evolution
5. **Add 繁體中文 requirement**: insert `**重要：所有輸出內容必須使用繁體中文。**` after the title block in SKILL.md
6. **Check if skill already has evolved content in framework dir**: Use `diff` or byte compare against the backup before running. If the framework file is already larger/different from the backup, a previous subagent may have already written results — check runtime skill size too (runtime can be AHEAD of framework if a prior evolution deployed to runtime but never synced back to framework).

## CRITICAL: delegate_task Timeout Behavior

When running evolutions via `delegate_task` with parallel subagents:
- **Parent timeout does NOT mean subagents failed.** A 600s parent timeout means the orchestrator gave up waiting, but individual subagents that were still running often COMPLETE SUCCESSFULLY and write their evolved content to the framework directory.
- **Always check the framework directory after a timeout.** Compare bytes of `~/.hermes/hermes-agent/skills/<category>/<skill-name>/SKILL.md` against the `.bak` backup — if bytes changed, the evolution succeeded despite the timeout.
- **Also check the runtime skill.** If a previous session deployed to runtime (`~/.hermes/skills/<skill-name>/SKILL.md`) but didn't sync back to framework, runtime will be LARGER than framework. This is recoverable — sync runtime → framework → Agent repo.

**Parallel batch size: max 2 at a time.** Three parallel subagents each running MIPROv2 (~5min) can exceed the 600s delegate_task timeout. Use batches of 2.

## Step-by-Step

### Step 1: Locate and Copy Skill to Framework Dir

```bash
# Check if skill exists in framework dir
ls ~/.hermes/hermes-agent/skills/<category>/<skill-name>/

# If skill is only in ~/Documents/Agent, copy it:
mkdir -p ~/.hermes/hermes-agent/skills/<category>/<skill-name>/
cp ~/Documents/Agent/<skill-name>/SKILL.md ~/.hermes/hermes-agent/skills/<category>/<skill-name>/SKILL.md
```

### Step 2: Update Hardcoded Paths (e.g., vault paths)

Common replacements:
- `E:/obsidian/PigoVault` → `/home/pigo/Documents/Pigo_Obsidian`
- `E:\obsidian\PigoVault` → `/home/pigo/Documents/Pigo_Obsidian`
- Any Windows path → appropriate Linux path

Always ask user for the correct Linux path BEFORE running evolution.

### Step 3: Add 繁體中文 Requirement

In SKILL.md, after the title line (e.g., `# Note Update — ...`), add:

```
**重要：所有輸出內容必須使用繁體中文。**
```

### Step 4: Backup Original

```bash
cp ~/.hermes/hermes-agent/skills/<category>/<skill-name>/SKILL.md \
   ~/.hermes/hermes-agent/skills/<category>/<skill-name>/SKILL.md.bak
```

### Step 5: Run Evolution

**⚠️ `--run-tests` does NOT take a value** — pass the flag alone without `=true` or `=false`.

Use Qwen3 (cheap ~$0.21, reliable) or MiniMax via OpenRouter:

```bash
cd ~/Downloads/hermes-agent-self-evolution && \
~/.hermes/hermes-agent/venv/bin/python -m evolution.skills.evolve_skill \
  --skill <skill-name> \
  --iterations 3 \
  --eval-source synthetic \
  --eval-model "openrouter/qwen/qwen3-next-80b-a3b-instruct" \
  --optimizer-model "openrouter/qwen/qwen3-next-80b-a3b-instruct" \
  --run-tests          # ← NO value, flag alone
```

Background with watch:
```bash
python -m evolution.skills.evolve_skill ... 2>&1
```
(Use background=true terminal mode with notify_on_complete=true and watch_patterns=["Best score", "FAILED", "✗ Evolved skill"])

### Step 6: Evaluate Evolution Result

**⚠️ Framework Bug (NOT fixed as of 2026-05-10)**: The validation stage reads the **original** file from `~/.hermes/hermes-agent/skills/<category>/<skill-name>/SKILL.md` instead of the evolved output. This causes ALL evolutions to output `evolved_FAILED.md` even when the evolved content is valid and complete. The `.bak` suffix and FAILED label are misleading — the actual evolved content in `evolved_FAILED.md` is often a genuine improvement.

**Decision tree**:
1. Check exit code of the evolution run (always 0 in practice)
2. Read `evolved_FAILED.md` — evaluate content quality directly
3. If content improved meaningfully → deploy from `evolved_FAILED.md` regardless of FAILED suffix
4. If no meaningful improvement → report and ask: "維持原樣？"

### Step 7: Evaluate and Deploy Evolution Result

The evolution output lands in **two different places depending on execution method**:

**A. Direct execution** (you run `python -m evolution.skills.evolve_skill` yourself):
```bash
# Output goes to a timestamped subdirectory (not evolved_FAILED.md at top level)
ls ~/Downloads/hermes-agent-self-evolution/output/<skill-name>/
# Deploy from there
cp ~/Downloads/hermes-agent-self-evolution/output/<skill-name>/<timestamp>/evolved_SKILL.md \
   ~/.hermes/hermes-agent/skills/<category>/<skill-name>/SKILL.md
```

**B. Via delegate_task subagents** (the reliable pattern):
The subagent writes the evolved SKILL.md **directly to the framework directory** at
`~/.hermes/hermes-agent/skills/<category>/<skill-name>/SKILL.md`. The `evolved_FAILED.md` file is never involved.

**Always verify before deploying** — compare bytes:
```bash
echo "Original: $(wc -c < ~/.hermes/hermes-agent/skills/<category>/<skill-name>/SKILL.md.bak)"
echo "Evolved:  $(wc -c < ~/.hermes/hermes-agent/skills/<category>/<skill-name>/SKILL.md)"
# If identical bytes → no improvement, skip deployment
```

### Step 8: Sync Back to Documents/Agent

```bash
cp ~/.hermes/hermes-agent/skills/<category>/<skill-name>/SKILL.md \
   ~/Documents/Agent/<skill-name>/SKILL.md
git add ~/Documents/Agent/<skill-name>/SKILL.md
git -C ~/Documents/Agent commit -m "skill: <skill-name> evolved"
git -C ~/Documents/Agent push origin main
```

## Model Recommendations

| Model | Cost | Reliability | Notes |
|-------|------|-------------|-------|
| `openrouter/qwen/qwen3-next-80b-a3b-instruct` | ~$0.21/run | ✅ Best | Primary choice |
| `openrouter/minimax/minimax-m2.7` | varies | ⚠️ Parsing errors | Lower scores, JSON output issues |
| Free models (Gemma, etc.) | Free | ❌ Rate limited | MIPROv2 needs 80+ calls, rate limits cause gibberish |

## Known Framework Bugs (2026-05-10, updated 2026-06-21)

1. **Constraint validation reads original file, not evolved output**: `evolution/skills/evolve_skill.py` validation stage reads from the framework's source file (`~/.hermes/hermes-agent/skills/<category>/<skill-name>/SKILL.md`) instead of the evolved content. This causes all runs to produce `evolved_FAILED.md` even with valid content. Workaround: evaluate `evolved_FAILED.md` content directly and deploy if improved.
2. **max_skill_size limit**: Default 15,000 chars too small for large skills. Patch in `evolution/core/config.py`: `max_skill_size = 25,000` (already patched on this system)
3. **GEPA falls back to MIPROv2**: `GEPA.__init__()` gets unexpected `max_steps` kwarg and fails silently, falling back to MIPROv2. Not a problem — MIPROv2 works fine, just slower (~5min vs ~3min).
4. **ImportError: cannot import name 'SyntheticDatasetBuilder'** (2026-05-24): `evolution/core/dataset_builder.py` was 0 bytes (empty file) after a `git pull`. This breaks the entire GEPA/MIPROv2 pipeline. Diagnose: `wc -c ~/Downloads/hermes-agent-self-evolution/evolution/core/dataset_builder.py`. If 0 bytes, fix with:
   ```bash
   cd ~/Downloads/hermes-agent-self-evolution && git checkout HEAD -- evolution/core/dataset_builder.py
   ~/.hermes/hermes-agent/venv/bin/pip install -e ~/Downloads/hermes-agent-self-evolution/"[dev]"
   ```
5. **Same-size evolution (0 improvement)**: Well-structured skills can evolve to `evolved_FAILED.md` with **identical byte count** to original (e.g., 7531→7531). This is a genuine failure mode — the optimizer made no meaningful changes. Decision: compare byte-for-byte; if size unchanged AND content unchanged, report "維持原樣" and skip deployment. If size increased meaningfully, evaluate content quality.
6. **Many evolutions produce identical output**: Well-structured skills (score ≥5) often return unchanged content. Always compare `evolved_FAILED.md` byte-for-byte with original before deploying.
7. **Subagent direct-write pattern (2026-06-14)**: When using `delegate_task` to run evolutions in parallel, subagents may write evolved content **directly to the framework directory** (`~/.hermes/hermes-agent/skills/<category>/<skill-name>/SKILL.md`) rather than to the expected output path. Always compare bytes of the framework file against the `.bak` backup to detect whether a meaningful change occurred — do not rely on checking `~/Downloads/hermes-agent-self-evolution/output/` for subagent-driven evolutions.
8. **Article-writer timeout but partial success (2026-06-21)**: Article-writer subagent timed out at 600s but the evolution had already written valid evolved content to the framework directory before the timeout. The framework file was updated (9061 bytes, unchanged from pre-evolution because subagent wrote to runtime, not framework). However, runtime skill WAS improved (12.8KB). Recovery: compare runtime vs framework, sync as needed.

## Evolution Effectiveness Patterns (empirical, updated 2026-06-28)

| Skill Type | Score | Evolution Effect | Recommendation |
|---|---|---|---|
| Barely-structured/simple | 1-3 | ✅ Meaningful additions (traps, pitfalls, examples) | Try evolution |
| Low-medium structured | 4 | ❌ Consistently unchanged (0/5 in 2026-06-28) | Manual improvement preferred |
| Medium structured | 3-5 | ⚠️ Mixed — some add traps, some unchanged | Try, compare output |
| Well-structured complex | 5-6 | ❌ Often unchanged | Manual improvement preferred |
| gstack-* | Any | 🚨 All exceed 15KB limit | Skip entirely |

**Empirical results from 2026-05-20 + 2026-05-24 sessions**:
- `ai-influence-digest` (score=1, 2026-05-20): +2.4KB additions, significant improvement ✅
- `ai-influence-digest` (score=1, 2026-05-24): 0 bytes change, optimizer failed to improve ❌
- `aihot` (score=3): +8.2KB, significant improvement ✅
- `brave-search` (score=3): 0 bytes change, no improvement ❌
- `dogfood`, `learning-from-experts`, `yuanbao`, `agent-create`: all unchanged

**2026-06-28 session (5 score=4 skills, all byte-for-byte identical)**:
- `cron-handover` (0.9KB, score=4): 1682→1682 bytes ❌
- `coherence-reviewer` (1.4KB, score=4): 2707→2707 bytes ❌
- `setup` (1.5KB, score=4): 2439→2439 bytes ❌
- `meeting-brief` (2.0KB, score=4): 3992→3992 bytes ❌
- `deadline-summary` (2.0KB, score=4): 3752→3752 bytes ❌

**Key finding**: Score=4 skills with proper YAML frontmatter are still reported as "missing frontmatter" by the constraint validator — the validation bug appears to read a different intermediate artifact, not the actual original or evolved file. All 5 produced `evolved_FAILED.md` with identical bytes to original, confirming genuine 0-change outcomes for this score tier.

**Parallel execution**: Run up to 2 evolutions in parallel via `delegate_task` subagents (each ~5min). Sequential is safer for error recovery. Do NOT background-block with `background=true` — use `delegate_task` with `tasks=[...]` and `timeout=300` per subagent. **Capped at 2** — three parallel MIPROv2 runs (~5min each) exceed the 600s delegate_task timeout.

## Verification

After deployment, confirm skill file is valid markdown and frontmatter is intact.

## References

- `references/2026-05-10-run-log.md` — run log of 2026-05-10 evolution session (5 skills evolved, validation bug documented)
- `references/2026-05-20-run-log.md` — run log of 2026-05-20 evolution session (same-size evolution pattern first observed)
- `references/2026-05-24-run-log.md` — run log of 2026-05-24: SyntheticDatasetBuilder import error confirmed + fix (git checkout)
- `references/2026-06-14-run-log.md` — run log of 2026-06-14: 5 skills evolved (Article-writer, Slidedeck, agent-create, agent-manage, asset-first-build); subagent direct-write pattern confirmed; Git push failed due to network timeout
- `references/2026-06-28-run-log.md` — run log of 2026-06-28: 5 score=4 skills (cron-handover, coherence-reviewer, setup, meeting-brief, deadline-summary) all produced 0-change outcomes; validation bug confirmed; score=4 tier added to effectiveness table
