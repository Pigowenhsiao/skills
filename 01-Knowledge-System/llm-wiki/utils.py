"""
llm-wiki Utilities
==================
Python utilities for maintaining PigoVault knowledge base.

Functions:
- check_session_start(): Validate required files exist
- check_incremental_cache(): SHA256 hash comparison
- update_indexes(): Auto-update index/log files
- health_check(): Detect orphans, broken links, missing sources
- generate_report(): Structured health report
"""

import os
import json
import hashlib
import re
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Set, Tuple

# ── Paths ─────────────────────────────────────────────────

VAULT_ROOT = Path("E:/obsidian/PigoVault")
LLM_WIKI_DIR = VAULT_ROOT / "10-LLM-Wiki"
INBOX_DIR = VAULT_ROOT / "00-Inbox"
LEARNING_DIR = VAULT_ROOT / "08-Learning"
MAINTENANCE_DIR = LEARNING_DIR / "99_Maintenance" / "status"

# ── Session Start Check ──────────────────────────────────

REQUIRED_FILES = [
    "00-Inbox/index.md",
    "08-Learning/index.md",
    "09-Article-Notes/index.md",
    "12-Meta/vault-structure.md",
    "08-Learning/99_Maintenance/status/LLM-Wiki-Index.md",
    "08-Learning/99_Maintenance/status/LLM-Wiki-Ingest-Log.md",
]

def check_session_start() -> Dict[str, any]:
    """Check required files exist before starting session.
    
    Returns:
        Dict with 'ok' (bool), 'missing' (list), 'found' (list)
    """
    missing = []
    found = []
    
    for rel_path in REQUIRED_FILES:
        full_path = VAULT_ROOT / rel_path
        if full_path.exists():
            found.append(str(full_path))
        else:
            missing.append(str(full_path))
    
    return {
        "ok": len(missing) == 0,
        "found_count": len(found),
        "missing_count": len(missing),
        "missing": missing,
        "found": found,
    }

# ── Incremental Cache ───────────────────────────────────

def compute_sha256(file_path: Path) -> str:
    """Compute SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def compute_string_hash(content: str) -> str:
    """Compute SHA256 hash of a string."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def load_ingest_log() -> Dict[str, str]:
    """Load previous ingest log as {source_path: hash}."""
    log_path = MAINTENANCE_DIR / "LLM-Wiki-Ingest-Log.md"
    
    if not log_path.exists():
        return {}
    
    # Parse frontmatter or simple key-value format
    hashes = {}
    content = log_path.read_text(encoding="utf-8")
    
    # Simple pattern: `- source: <path> | hash: <hash>`
    pattern = r`- \[?\.\.\/\.\.\/\]?\s*\|\s*hash:\s*([a-f0-9]{64})`
    
    # Alternative: parse structured log
    for line in content.split("\n"):
        if "hash:" in line.lower():
            parts = line.split("hash:")
            if len(parts) == 2:
                hash_val = parts[1].strip().split()[0]
                if len(hash_val) == 64:
                    # Try to extract source
                    src_match = re.search(r'sources?\s*:\s*\[?([^\]]+)', line)
                    if src_match:
                        src = src_match.group(1).strip("[]")
                        hashes[src] = hash_val
    
    return hashes

def check_incremental_cache(source: Path) -> Tuple[bool, str]:
    """Check if source needs reprocessing.
    
    Args:
        source: Path to source file or URL
    
    Returns:
        (needs_processing, previous_hash)
        - needs_processing=True: hash changed or new, should process
        - needs_processing=False: hash unchanged, can skip
    """
    if isinstance(source, str):
        source = Path(source)
    
    # Compute current hash
    if source.exists():
        current_hash = compute_sha256(source)
    else:
        # URL or non-file source - use string hash of the path
        current_hash = compute_string_hash(str(source))
    
    # Load previous log
    previous_hashes = load_ingest_log()
    previous_hash = previous_hashes.get(str(source), "")
    
    if not previous_hash:
        # New source - needs processing
        return True, ""
    
    if current_hash == previous_hash:
        # Unchanged - can skip
        return False, previous_hash
    
    # Hash changed - needs processing
    return True, previous_hash

def update_ingest_log(source: Path, hash_value: str, notes: List[str] = None) -> bool:
    """Update ingest log with new source entry.
    
    Args:
        source: Path to source file
        hash_value: SHA256 hash
        notes: Optional list of note file paths created
    
    Returns:
        True if successful
    """
    log_path = MAINTENANCE_DIR / "LLM-Wiki-Ingest-Log.md"
    
    # Create maintenance dir if needed
    MAINTENANCE_DIR.mkdir(parents=True, exist_ok=True)
    
    UTC8 = timezone(timedelta(hours=8))
    now = datetime.now(UTC8)
    date_str = now.strftime("%Y-%m-%d %H:%M")
    
    # Build entry
    note_links = ""
    if notes:
        note_links = " | Notes: " + ", ".join([f"[[{Path(n).stem}]]" for n in notes])
    
    entry = f"- {date_str} | Source: {source} | Hash: {hash_value}{note_links}\n"
    
    # Append to log
    if log_path.exists():
        existing = log_path.read_text(encoding="utf-8")
        # Add entry at top
        content = entry + "\n" + existing
    else:
        content = f"# LLM-Wiki Ingest Log\n\n{entry}\n"
    
    log_path.write_text(content, encoding="utf-8")
    return True

# ── Index Updates ────────────────────────────────────────

def get_inbox_files() -> List[Path]:
    """Get all markdown files in 00-Inbox."""
    if not INBOX_DIR.exists():
        return []
    return sorted(INBOX_DIR.glob("*.md"))

def get_learning_files() -> List[Path]:
    """Get all markdown files in 08-Learning."""
    if not LEARNING_DIR.exists():
        return []
    return sorted(LEARNING_DIR.rglob("*.md"))

def extract_title(filepath: Path) -> str:
    """Extract title from markdown file."""
    content = filepath.read_text(encoding="utf-8")
    
    # Try frontmatter title first
    match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    
    # Fall back to first H1
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    
    return filepath.stem

def extract_tags(filepath: Path) -> List[str]:
    """Extract tags from markdown frontmatter."""
    content = filepath.read_text(encoding="utf-8")
    
    # Find tags section
    match = re.search(r'^tags:\s*\n((?:\s*-\s*.+\n)+)', content, re.MULTILINE)
    if match:
        tags_block = match.group(1)
        tags = re.findall(r'-\s*(.+)', tags_block)
        return [t.strip() for t in tags]
    
    return []

def extract_sources(filepath: Path) -> List[str]:
    """Extract sources from frontmatter."""
    content = filepath.read_text(encoding="utf-8")
    
    match = re.search(r'^sources:\s*\n((?:\s*-\s*.+\n)+)', content, re.MULTILINE)
    if match:
        sources_block = match.group(1)
        sources = re.findall(r'-\s*(.+)', sources_block)
        return [s.strip() for s in sources]
    
    return []

def update_inbox_index() -> int:
    """Update 00-Inbox/index.md with current files.
    
    Returns:
        Number of files listed
    """
    index_path = INBOX_DIR / "index.md"
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    
    files = get_inbox_files()
    
    lines = ["# 00-Inbox\n", f"## Files ({len(files)})\n", "\n"]
    
    for f in files:
        title = extract_title(f)
        tags = extract_tags(f)
        tag_str = " #" + " #".join(tags) if tags else ""
        
        # Relative path for wikilink
        rel_path = f.relative_to(VAULT_ROOT)
        lines.append(f"- [[{rel_path}]]{tag_str}  ({f.stat().st_mtime_ns})\n")
    
    content = "".join(lines)
    index_path.write_text(content, encoding="utf-8")
    
    return len(files)

def update_llm_wiki_index() -> int:
    """Update LLM-Wiki-Index.md with vault statistics.
    
    Returns:
        Number of total files indexed
    """
    index_path = MAINTENANCE_DIR / "LLM-Wiki-Index.md"
    MAINTENANCE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Count files
    inbox_count = len(get_inbox_files())
    learning_count = len(get_learning_files())
    
    UTC8 = timezone(timedelta(hours=8))
    now = datetime.now(UTC8)
    date_str = now.strftime("%Y-%m-%d %H:%M")
    
    content = f"""# LLM-Wiki Index

## Statistics

| Area | Files |
|------|-------|
| 00-Inbox | {inbox_count} |
| 08-Learning | {learning_count} |
| **Total** | **{inbox_count + learning_count}** |

## Last Updated

{date_str}

## Recent Files

"""
    
    # Add recent files from inbox
    recent = sorted(get_inbox_files(), key=lambda p: p.stat().st_mtime_ns, reverse=True)[:10]
    for f in recent:
        title = extract_title(f)
        rel = f.relative_to(VAULT_ROOT)
        content += f"- [[{rel}|{title}]]\n"
    
    index_path.write_text(content, encoding="utf-8")
    
    return inbox_count + learning_count

def update_indexes(notes_created: List[Path] = None) -> Dict[str, any]:
    """Update all llm-wiki indexes.
    
    Args:
        notes_created: Optional list of new note paths
    
    Returns:
        Dict with update results
    """
    results = {}
    
    try:
        results["inbox_index"] = update_inbox_index()
    except Exception as e:
        results["inbox_index_error"] = str(e)
    
    try:
        results["llm_wiki_index"] = update_llm_wiki_index()
    except Exception as e:
        results["llm_wiki_index_error"] = str(e)
    
    # Update ingest log if notes were created
    if notes_created:
        for note in notes_created:
            try:
                hash_val = compute_sha256(note) if note.exists() else ""
                update_ingest_log(note, hash_val, notes_created)
            except Exception as e:
                results[f"ingest_log_error_{note.name}"] = str(e)
    
    return results

# ── Health Check ─────────────────────────────────────────

def find_orphan_pages() -> List[Dict]:
    """Find pages with no inbound wikilinks.
    
    Returns:
        List of {path, reason} dicts
    """
    orphans = []
    
    # Build set of all markdown files
    all_files = set(VAULT_ROOT.rglob("*.md"))
    
    # Build set of files that are linked to
    linked_files = set()
    
    for md_file in all_files:
        try:
            content = md_file.read_text(encoding="utf-8")
            
            # Find wikilinks: [[path]] or [[path|display]]
            wikilinks = re.findall(r'\[\[([^\]|#]+)(?:\|[^\]]+)?\]\]', content)
            
            for link in wikilinks:
                # Resolve relative link
                link_clean = link.strip()
                
                # Try as relative to current file
                potential = md_file.parent / link_clean
                if potential.exists():
                    linked_files.add(potential.resolve())
                
                # Try as relative to vault root
                potential = VAULT_ROOT / link_clean
                if potential.exists():
                    linked_files.add(potential.resolve())
                
                # Try with .md extension
                if not link_clean.endswith(".md"):
                    potential = VAULT_ROOT / (link_clean + ".md")
                    if potential.exists():
                        linked_files.add(potential.resolve())
        
        except Exception:
            continue
    
    # Find orphans
    for md_file in all_files:
        # Skip index files
        if md_file.name == "index.md":
            continue
        
        # Skip if linked
        if md_file.resolve() in linked_files:
            continue
        
        # Skip SKILL.md files
        if md_file.name == "SKILL.md":
            continue
        
        orphans.append({
            "path": str(md_file.relative_to(VAULT_ROOT)),
            "reason": "No inbound wikilinks"
        })
    
    return orphans

def find_broken_links() -> List[Dict]:
    """Find wikilinks pointing to non-existent files.
    
    Returns:
        List of {source, target, target_resolved} dicts
    """
    broken = []
    
    for md_file in VAULT_ROOT.rglob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            
            # Find wikilinks
            wikilinks = re.findall(r'\[\[([^\]|#]+)(?:\|[^\]]+)?\]\]', content)
            
            for link in wikilinks:
                link_clean = link.strip()
                
                # Try various resolutions
                found = False
                
                # 1. Exact path relative to vault
                if (VAULT_ROOT / link_clean).exists():
                    found = True
                # 2. With .md extension
                elif (VAULT_ROOT / (link_clean + ".md")).exists():
                    found = True
                # 3. Relative to current file
                elif (md_file.parent / link_clean).exists():
                    found = True
                # 4. With .md relative to current file
                elif (md_file.parent / (link_clean + ".md")).exists():
                    found = True
                
                if not found:
                    broken.append({
                        "source": str(md_file.relative_to(VAULT_ROOT)),
                        "target": link_clean,
                        "resolved": str(VAULT_ROOT / link_clean)
                    })
        
        except Exception:
            continue
    
    return broken

def find_missing_sources() -> List[Dict]:
    """Find pages with sources pointing to non-existent files.
    
    Returns:
        List of {page, source, reason} dicts
    """
    missing = []
    
    for md_file in VAULT_ROOT.rglob("*.md"):
        try:
            sources = extract_sources(md_file)
            
            for source in sources:
                source_path = Path(source)
                
                # Skip URLs
                if source.startswith("http"):
                    continue
                
                # Try to resolve
                if not source_path.exists():
                    # Try relative to vault
                    resolved = VAULT_ROOT / source
                    if not resolved.exists():
                        missing.append({
                            "page": str(md_file.relative_to(VAULT_ROOT)),
                            "source": source,
                            "reason": "File not found"
                        })
        
        except Exception:
            continue
    
    return missing

def health_check() -> Dict:
    """Run complete health check on vault.
    
    Returns:
        Structured health report
    """
    UTC8 = timezone(timedelta(hours=8))
    now = datetime.now(UTC8)
    
    orphans = find_orphan_pages()
    broken = find_broken_links()
    missing_sources = find_missing_sources()
    
    inbox_count = len(get_inbox_files())
    
    # Check for stale indexes
    index_path = MAINTENANCE_DIR / "LLM-Wiki-Index.md"
    index_stale = False
    if index_path.exists():
        try:
            content = index_path.read_text(encoding="utf-8")
            date_match = re.search(r'Last Updated\n(\d{4}-\d{2}-\d{2})', content)
            if date_match:
                last_date = datetime.strptime(date_match.group(1), "%Y-%m-%d")
                if (now.date() - last_date.date()).days > 7:
                    index_stale = True
        except:
            index_stale = True
    else:
        index_stale = True
    
    return {
        "timestamp": now.isoformat(),
        "vault_root": str(VAULT_ROOT),
        "statistics": {
            "inbox_count": inbox_count,
            "total_files": inbox_count + len(get_learning_files()),
            "orphans_count": len(orphans),
            "broken_links_count": len(broken),
            "missing_sources_count": len(missing_sources),
        },
        "issues": {
            "orphans": orphans[:20],  # Limit to 20
            "broken_links": broken[:20],
            "missing_sources": missing_sources[:20],
        },
        "alerts": {
            "inbox_high": inbox_count > 50,
            "index_stale": index_stale,
            "orphans_exist": len(orphans) > 0,
            "broken_links_exist": len(broken) > 0,
        }
    }

# ── Generate Report ──────────────────────────────────────

def generate_report(health: Dict = None) -> str:
    """Generate human-readable health report.
    
    Args:
        health: Optional pre-computed health dict
    
    Returns:
        Markdown formatted report
    """
    if health is None:
        health = health_check()
    
    UTC8 = timezone(timedelta(hours=8))
    now = datetime.now(UTC8)
    
    report = f"""# llm-wiki Health Report

Generated: {now.strftime('%Y-%m-%d %H:%M')}

## Statistics

| Metric | Value |
|--------|-------|
| 00-Inbox | {health['statistics']['inbox_count']} files |
| Total Files | {health['statistics']['total_files']} |
| Orphan Pages | {health['statistics']['orphans_count']} |
| Broken Links | {health['statistics']['broken_links_count']} |
| Missing Sources | {health['statistics']['missing_sources_count']} |

## Alerts

"""
    
    alerts = health.get("alerts", {})
    if alerts.get("inbox_high"):
        report += "> ⚠️ **00-Inbox 超過 50 個檔案，建議整理**\n"
    if alerts.get("index_stale"):
        report += "> ⚠️ **Index 已超過 7 天未更新**\n"
    if alerts.get("orphans_exist"):
        report += f"> ⚠️ **{health['statistics']['orphans_count']} 個孤島頁面**\n"
    if alerts.get("broken_links_exist"):
        report += f"> ⚠️ **{health['statistics']['broken_links_count']} 個壞連結**\n"
    
    if not any(alerts.values()):
        report += "> ✅ **Vault 健康，無重大問題**\n"
    
    # Orphan pages
    orphans = health.get("issues", {}).get("orphans", [])
    if orphans:
        report += "\n## Orphan Pages (需要 inbound links)\n\n"
        for o in orphans[:10]:
            report += f"- [[{o['path']}]]\n"
        if len(orphans) > 10:
            report += f"\n_...還有 {len(orphans) - 10} 個_\n"
    
    # Broken links
    broken = health.get("issues", {}).get("broken_links", [])
    if broken:
        report += "\n## Broken Links\n\n"
        for b in broken[:10]:
            report += f"- [[{b['source']}]] → `{b['target']}`\n"
        if len(broken) > 10:
            report += f"\n_...還有 {len(broken) - 10} 個_\n"
    
    report += "\n---\n*Generated by llm-wiki-utils.py*\n"
    
    return report

# ── Main ─────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    
    print("=== llm-wiki Health Check ===\n")
    
    # Session start check
    print("1. Session Start Check:")
    session = check_session_start()
    if session["ok"]:
        print(f"   ✅ All {session['found_count']} required files found")
    else:
        print(f"   ⚠️  Missing {session['missing_count']} files:")
        for m in session["missing"]:
            print(f"      - {m}")
    
    print()
    
    # Health check
    print("2. Health Check:")
    health = health_check()
    print(f"   - Inbox: {health['statistics']['inbox_count']} files")
    print(f"   - Orphans: {health['statistics']['orphans_count']}")
    print(f"   - Broken links: {health['statistics']['broken_links_count']}")
    
    print()
    
    # Alerts
    alerts = health.get("alerts", {})
    if alerts.get("inbox_high"):
        print("   ⚠️  Inbox 超過 50 個檔案")
    if alerts.get("index_stale"):
        print("   ⚠️  Index 已超過 7 天未更新")
    
    print()
    
    # Generate report
    print("3. Full Report:")
    print(generate_report(health))
