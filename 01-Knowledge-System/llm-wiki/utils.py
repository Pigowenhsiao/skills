"""
llm-wiki Utilities
==================
Core functions for PigoVault knowledge base maintenance.

Exports:
- check_session_start(): Validate required files
- check_incremental_cache(): SHA256 / URL-hash deduplication
- update_ingest_log(): Dual-format (JSON + Markdown) logging
- health_check(): Full vault health + YouTube transcription checks
- generate_report(): Markdown health report
- update_indexes(): Auto-update LLM-Wiki-Index, Ingest-Log, Inbox-Index
- find_youtube_orphans(): YouTube L3 notes needing transcription
"""
from __future__ import annotations

import hashlib
import json
import logging
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# ── Local imports (lazy — avoids circular dependency) ───
# Due to hyphenated directory name 'llm-wiki', use lazy import inside functions.

_YOUTUBE_OK = False
_yt_handler = None

def _lazy_import_config():
    """Lazily load config module."""
    import importlib.util
    import sys
    from pathlib import Path as _Path
    p = _Path(__file__).parent / "config.py"
    spec = importlib.util.spec_from_file_location("llm_wiki_config", str(p))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["llm_wiki_config"] = mod
    spec.loader.exec_module(mod)
    return mod

def _lazy_import_youtube():
    """Lazily load youtube_handler module."""
    global _yt_handler, _YOUTUBE_OK
    if _yt_handler is None:
        import importlib.util
        import sys
        from pathlib import Path as _Path
        p = _Path(__file__).parent / "youtube_handler.py"
        spec = importlib.util.spec_from_file_location("llm_wiki_yt", str(p))
        mod = importlib.util.module_from_spec(spec)
        sys.modules["llm_wiki_yt"] = mod
        spec.loader.exec_module(mod)
        _yt_handler = mod
        _YOUTUBE_OK = True
    return _yt_handler


# ── Logging ─────────────────────────────────────────────

_logger = logging.getLogger("llm-wiki")
if not _logger.handlers:
    _handler = logging.StreamHandler(sys.stderr)
    _handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    ))
    _logger.addHandler(_handler)
    _logger.setLevel(logging.INFO)


# ── Aliases (lazy — resolved on first use via config) ────

def _vault_root() -> Path:
    cfg = _lazy_import_config()
    return cfg.get_config().vault_root

def _inbox_dir() -> Path:
    cfg = _lazy_import_config()
    return cfg.get_config().inbox_dir

def _learning_dir() -> Path:
    cfg = _lazy_import_config()
    return cfg.get_config().learning_dir

def _maintenance_dir() -> Path:
    cfg = _lazy_import_config()
    return cfg.get_config().maintenance_dir

def _ingest_log_path() -> Path:
    cfg = _lazy_import_config()
    return cfg.get_config().ingest_log

def _inbox_index_path() -> Path:
    cfg = _lazy_import_config()
    return cfg.get_config().inbox_index

def _llm_wiki_index_path() -> Path:
    cfg = _lazy_import_config()
    return cfg.get_config().llm_wiki_index

def _llm_wiki_dir() -> Path:
    cfg = _lazy_import_config()
    return cfg.get_config().llm_wiki_dir


# ── Required Files ──────────────────────────────────────

REQUIRED_FILES: List[str] = [
    "00-Inbox/index.md",
    "08-Learning/index.md",
    "09-Article-Notes/index.md",
    "12-Meta/vault-structure.md",
    "08-Learning/99_Maintenance/status/LLM-Wiki-Index.md",
    "08-Learning/99_Maintenance/status/LLM-Wiki-Ingest-Log.md",
]


# ── Session Start ───────────────────────────────────────

def check_session_start() -> Dict[str, object]:
    """
    Validate required vault files exist.
    Returns dict with 'ok', 'found_count', 'missing_count', 'missing', 'found'.
    """
    vr = _vault_root()
    missing: List[str] = []
    found: List[str] = []
    
    for rel in REQUIRED_FILES:
        full = vr / rel
        if full.exists():
            found.append(str(full))
        else:
            missing.append(str(full))
    
    return {
        "ok": len(missing) == 0,
        "found_count": len(found),
        "missing_count": len(missing),
        "missing": missing,
        "found": found,
    }


# ── Hash Utilities ───────────────────────────────────────

def compute_sha256(file_path: Path) -> str:
    """Compute SHA256 hash of a file."""
    sha = hashlib.sha256()
    with open(file_path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            sha.update(chunk)
    return sha.hexdigest()


def compute_string_hash(text: str) -> str:
    """Compute SHA256 hash of a string (used for URLs)."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def compute_content_hash(content: str) -> str:
    """Alias for compute_string_hash (API consistency)."""
    return compute_string_hash(content)


# ── Ingest Log (Dual Format: JSON + Markdown) ───────────

class IngestLog:
    """
    Manages the ingest log in dual format:
    - {{maintenance_dir}}/LLM-Wiki-Ingest-Log.json  (canonical, machine-readable)
    - {{maintenance_dir}}/LLM-Wiki-Ingest-Log.md    (human-readable)
    
    JSON schema:
    {
      "version": "1.0",
      "entries": [
        {
          "timestamp": "2026-08-20T10:30:00+08:00",
          "source": "E:/obsidian/00-Inbox/x.md",
          "source_type": "file|url|youtube",
          "hash": "sha256...",
          "source_url": "https://..." (for URLs/youtube),
          "notes": ["note1.md", "note2.md"],
          "content_hash": "sha256...",
          "transcribed": true,        (YouTube)
          "source_completeness": "L1" (YouTube)
        }
      ]
    }
    """
    
    VERSION = "1.0"
    
    def __init__(self, log_path: Optional[Path] = None):
        self.log_path = log_path or _ingest_log_path()
        self.json_path = self.log_path.with_suffix(".json")
        # md_path must be distinct so save() doesn't overwrite JSON with Markdown
        self.md_path = self.log_path.with_suffix(".md")
        self.entries: List[Dict] = []
        self._loaded = False
    
    def _ensure_dir(self) -> None:
        self.json_path.parent.mkdir(parents=True, exist_ok=True)
    
    def load(self) -> "IngestLog":
        """Load entries from JSON file. Falls back to parsing Markdown."""
        self.entries = []
        if self.json_path.exists():
            try:
                data = json.loads(self.json_path.read_text(encoding="utf-8"))
                self.entries = data.get("entries", [])
                self._loaded = True
                return self
            except (json.JSONDecodeError, OSError) as e:
                _logger.warning("Failed to load JSON log (%s), falling back to Markdown", e)
        
        # Fallback: parse Markdown
        self.entries = self._parse_markdown_log()
        self._loaded = True
        return self
    
    def _parse_markdown_log(self) -> List[Dict]:
        """Parse legacy Markdown ingest log."""
        if not self.md_path.exists():
            return []
        
        entries = []
        content = self.md_path.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()
        
        for line in lines:
            if not line.startswith("- "):
                continue
            
            entry = {"_raw": line}
            
            # Parse: "- YYYY-MM-DD HH:MM | Source: ... | Hash: ... | Notes: ..."
            ts_m = re.search(r"^-\s*(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(?::\d{2})?[+-]\d{2}:?\d{2}?)", line)
            if ts_m:
                entry["timestamp"] = ts_m.group(1)
            
            src_m = re.search(r"[Ss]ource:\s*([^\|]+)", line)
            if src_m:
                entry["source"] = src_m.group(1).strip().strip('"`')
            
            hash_m = re.search(r"[Hh]ash:\s*([a-f0-9]{64})", line)
            if hash_m:
                entry["hash"] = hash_m.group(1)
            
            notes_m = re.search(r"[Nn]otes?:\s*(.+)", line)
            if notes_m:
                raw_notes = notes_m.group(1).strip()
                entry["notes"] = [
                    n.strip().strip("[]")
                    for n in re.findall(r"\[\[[^\]]+\]\]|[^,\|]+", raw_notes)
                ]
            
            entries.append(entry)
        
        return entries
    
    def add(
        self,
        source: str,
        source_type: str = "file",
        content_hash: str = "",
        source_url: str = "",
        notes: Optional[List[str]] = None,
        transcribed: bool = False,
        source_completeness: str = "",
        extra: Optional[Dict] = None,
    ) -> "IngestLog":
        """Add an entry and persist."""
        utc8 = timezone(timedelta(hours=8))
        entry: Dict = {
            "timestamp": datetime.now(utc8).isoformat(),
            "source": source,
            "source_type": source_type,
            "hash": content_hash or "",
            "notes": notes or [],
        }
        if source_url:
            entry["source_url"] = source_url
        if source_type == "youtube":
            entry["transcribed"] = transcribed
            entry["source_completeness"] = source_completeness
        if extra:
            entry.update(extra)
        
        self.entries.insert(0, entry)
        self.save()
        return self
    
    def save(self) -> bool:
        """Write both JSON and Markdown formats."""
        try:
            self._ensure_dir()
            
            # JSON (canonical)
            data = {"version": self.VERSION, "entries": self.entries}
            self.json_path.write_text(
                json.dumps(data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            
            # Markdown (human-readable) — writes to .md, not .json
            md_lines = ["# LLM-Wiki Ingest Log", "", f"_Version {self.VERSION} — auto-generated_", ""]
            
            # Group by date
            by_date: Dict[str, List[Dict]] = {}
            for e in self.entries:
                ts = e.get("timestamp", "")
                date = ts[:10] if ts else "Unknown"
                by_date.setdefault(date, []).append(e)
            
            for date, ents in sorted(by_date.items(), reverse=True):
                md_lines.append(f"## {date}")
                for e in ents:
                    ts = e.get("timestamp", "")
                    time_part = ts[11:16] if len(ts) > 16 else ""
                    src = e.get("source", "")
                    h = e.get("hash", "")
                    notes_list = e.get("notes", [])
                    notes_str = ", ".join(f"[[{n}]]" for n in notes_list) if notes_list else ""
                    
                    parts = [f"- {time_part}"]
                    if src:
                        parts.append(f"Source: {src}")
                    if h:
                        parts.append(f"Hash: {h}")
                    if notes_str:
                        parts.append(f"Notes: {notes_str}")
                    
                    # YouTube-specific
                    if e.get("source_type") == "youtube":
                        if e.get("transcribed"):
                            parts.append("Status: ✅ Transcribed")
                        elif e.get("source_completeness"):
                            parts.append(f"Completeness: {e['source_completeness']}")
                    
                    md_lines.append(" | ".join(parts))
                md_lines.append("")
            
            self.md_path.write_text("\n".join(md_lines), encoding="utf-8")
            return True
            
        except Exception as e:
            _logger.error("Failed to save ingest log: %s", e)
            return False
    
    def get_hash(self, source: str) -> Optional[str]:
        """Get most recent hash for a source."""
        self.load()
        for e in self.entries:
            if e.get("source") == source:
                return e.get("hash", "")
        return None
    
    def sources(self) -> Set[str]:
        """Return set of all sources in log."""
        self.load()
        return {e.get("source", "") for e in self.entries if e.get("source")}


# ── Incremental Cache ────────────────────────────────────

def load_ingest_log() -> Dict[str, str]:
    """
    Load ingest log as {source: hash} dict.
    Used for backward compatibility.
    """
    log = IngestLog().load()
    return {e.get("source", ""): e.get("hash", "") 
            for e in log.entries if e.get("source")}


def check_incremental_cache(
    source: str | Path,
    ingest_log: Optional["IngestLog"] = None,
) -> Tuple[bool, str]:
    """
    Check if source needs reprocessing.
    
    Args:
        source: File path or URL string.
        ingest_log: Optional IngestLog instance. If None, uses default vault log.
    
    Returns: (needs_processing: bool, previous_hash: str)
    """
    source_str = str(source)
    
    if source_str.startswith("http"):
        # URL — hash the URL string itself
        current_hash = compute_string_hash(source_str)
    elif Path(source_str).exists():
        # Local file
        current_hash = compute_sha256(Path(source_str))
    else:
        # Unknown — always process
        return True, ""
    
    log = ingest_log if ingest_log is not None else IngestLog()
    prev_hash = log.get_hash(source_str)
    
    if not prev_hash:
        return True, ""
    
    return current_hash != prev_hash, prev_hash


def update_ingest_log(
    source: str | Path,
    hash_value: str = "",
    notes: Optional[List[str]] = None,
    source_url: str = "",
    transcribed: bool = False,
    source_completeness: str = "",
) -> bool:
    """
    Add entry to ingest log.
    
    For YouTube notes, include transcribed/completeness so we can
    track transcription progress across the knowledge base.
    """
    source_str = str(source)
    
    # Determine source_type
    if "youtube" in source_str.lower() or ".youtube" in source_str.lower():
        src_type = "youtube"
    elif str(source).startswith("http"):
        src_type = "url"
    else:
        src_type = "file"
    
    log = IngestLog().add(
        source=source_str,
        source_type=src_type,
        content_hash=hash_value,
        source_url=source_url,
        notes=notes,
        transcribed=transcribed,
        source_completeness=source_completeness,
    )
    return True


# ── File Discovery ───────────────────────────────────────

def get_inbox_files(include_youtube: bool = True) -> List[Path]:
    """Get all markdown files in 00-Inbox."""
    inbox = _inbox_dir()
    if not inbox.exists():
        return []
    
    files = []
    for f in sorted(inbox.glob("*.md")):
        if f.name == "index.md":
            continue
        if not include_youtube and "youtube" in f.name.lower():
            continue
        files.append(f)
    return files


def get_youtube_inbox_files() -> List[Path]:
    """Get only YouTube notes from 00-Inbox."""
    inbox = _inbox_dir()
    if not inbox.exists():
        return []
    
    pattern = re.compile(r"_x-note_youtube[-_][^/]*\.md$", re.IGNORECASE)
    return [f for f in inbox.glob("*youtube*.md") if pattern.search(f.name)]


def get_learning_files() -> List[Path]:
    """Get all markdown files in 08-Learning."""
    learning = _learning_dir()
    if not learning.exists():
        return []
    return sorted(learning.rglob("*.md"))


# ── Frontmatter Parsing ──────────────────────────────────

def parse_frontmatter(text: str) -> Tuple[Dict[str, object], str]:
    """
    Parse YAML-like frontmatter from markdown text.
    
    Handles:
    - Simple key: value
    - List values (indented or inline)
    - Quoted values
    
    Returns: (frontmatter_dict, body_text)
    """
    if not text.strip().startswith("---"):
        return {}, text
    
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
    if not m:
        return {}, text
    
    fm_raw, body = m.group(1), m.group(2)
    fm: Dict[str, object] = {}
    current_key: Optional[str] = None
    
    for line in fm_raw.splitlines():
        stripped = line.strip()
        
        # ── 1. Continuation lines (indented list items) ──
        # Accept any line that starts with 2+ spaces/tabs followed by "- "
        if re.match(r'^[ \t]{2,}-\s', line):
            if current_key and isinstance(fm.get(current_key), list):
                fm[current_key].append(stripped.lstrip('- '))
            continue
        
        # ── 2. Top-level list item on the same line as the key ──
        # e.g. "tags:\n  - python"  or  "tags:\n    - python"
        if re.match(r'^\s*-\s', stripped):
            # List item without a key yet — set up a sentinel key
            if current_key is None:
                continue  # bare list item before any key, skip
            if isinstance(fm.get(current_key), list):
                fm[current_key].append(stripped.lstrip('- '))
            continue
        
        # ── 3. Normal key: value or empty ──
        if ":" not in stripped:
            continue
        
        key, _, val = stripped.partition(":")
        key = key.strip()
        val = val.strip()
        
        if val == "":
            # Empty value — expect list items on next lines
            fm[key] = []
            current_key = key
        else:
            fm[key] = val.strip('"')
            current_key = key
    
    return fm, body


def extract_title(filepath: Path) -> str:
    """Extract title from markdown frontmatter or H1."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return filepath.stem
    
    fm, body = parse_frontmatter(content)
    if fm.get("title"):
        return str(fm["title"])
    
    m = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    if m:
        return m.group(1).strip()
    
    return filepath.stem


def extract_tags(filepath: Path) -> List[str]:
    """Extract tags list from frontmatter."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []
    
    fm, _ = parse_frontmatter(content)
    tags = fm.get("tags", [])
    if isinstance(tags, list):
        return [str(t) for t in tags]
    return []


def extract_sources(filepath: Path) -> List[str]:
    """Extract sources list from frontmatter.
    
    Handles:
    - sources: ["url1", "url2"]       (proper YAML list)
    - sources: "url1"                 (malformed single string)
    - sources: []                     (empty list)
    """
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []
    
    fm, _ = parse_frontmatter(content)
    sources = fm.get("sources", [])
    if isinstance(sources, list):
        return [str(s) for s in sources if s]
    # Handle malformed single-string case
    if isinstance(sources, str) and sources.strip():
        return [sources.strip()]
    return []


def extract_youtube_info(filepath: Path) -> Dict[str, object]:
    """Extract YouTube-specific frontmatter fields."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {}
    
    fm, _ = parse_frontmatter(content)
    
    return {
        "type": fm.get("type", ""),
        "source_completeness": fm.get("source-completeness", "description-only"),
        "transcribed": str(fm.get("transcribed", "false")).lower() in {"true", "yes", "1"},
        "video_id": fm.get("video_id", ""),
        "channel": fm.get("channel", ""),
        "lcz_me_url": fm.get("lcz_me_url", ""),
        "thumbnail": fm.get("thumbnail", ""),
        "duration": fm.get("duration", ""),
    }


# ── Index Updates ────────────────────────────────────────

def update_inbox_index() -> int:
    """Update 00-Inbox/index.md."""
    index_path = _inbox_index_path()
    _inbox_dir().mkdir(parents=True, exist_ok=True)
    
    files = get_inbox_files()
    youtube_files = get_youtube_inbox_files()
    
    utc8 = timezone(timedelta(hours=8))
    now = datetime.now(utc8)
    date_str = now.strftime("%Y-%m-%d %H:%M")
    
    lines = [
        "# 00-Inbox",
        "",
        f"## Files ({len(files)}) — {date_str}",
        "",
    ]
    
    # Non-YouTube files
    if files:
        lines.append("### Regular Notes")
        for f in files:
            title = extract_title(f)
            tags = extract_tags(f)
            tag_str = " " + " ".join(f"#{t}" for t in tags) if tags else ""
            rel = f.relative_to(_vault_root())
            mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=utc8).strftime("%Y-%m-%d %H:%M")
            lines.append(f"- [[{rel}|{title}]]{tag_str}  ({mtime})")
        lines.append("")
    
    # YouTube files
    if youtube_files:
        lines.append("### YouTube Notes")
        for f in youtube_files:
            title = extract_title(f)
            yt_info = extract_youtube_info(f)
            completeness = yt_info.get("source_completeness", "description-only")
            transcribed = yt_info.get("transcribed", False)
            
            if transcribed:
                status = "✅ L1"
            elif completeness in {"full-transcript", "external-transcript"}:
                status = "📄 L2"
            else:
                stale = ""
                try:
                    fm, _ = parse_frontmatter(f.read_text(encoding="utf-8", errors="replace"))
                    created = fm.get("created", "")
                    if created:
                        dt = datetime.strptime(created[:10], "%Y-%m-%d")
                        days = (now.date() - dt.date()).days
                        if days > 7:
                            stale = f" ⚠️ {days}d"
                except Exception:
                    pass
                status = f"📝 L3{stale}"
            
            rel = f.relative_to(_vault_root())
            lines.append(f"- [[{rel}|{title}]] {status}")
        lines.append("")
    
    index_path.write_text("\n".join(lines), encoding="utf-8")
    return len(files)


def update_llm_wiki_index() -> int:
    """Update LLM-Wiki-Index.md with full statistics."""
    index_path = _llm_wiki_index_path()
    _maintenance_dir().mkdir(parents=True, exist_ok=True)
    
    inbox_files = get_inbox_files(include_youtube=False)
    yt_files = get_youtube_inbox_files()
    learning_files = get_learning_files()
    
    # Count by completeness
    yt_by_level = {"L1": 0, "L2": 0, "L3": 0}
    yt_stale = 0
    if _YOUTUBE_OK:
        for f in yt_files:
            try:
                result = check_youtube_completeness(f)
                lvl = result.get("level", "L3")
                if lvl in yt_by_level:
                    yt_by_level[lvl] += 1
                if result.get("stale_days", 0) and result["stale_days"] > 7:
                    yt_stale += 1
            except Exception:
                pass
    
    utc8 = timezone(timedelta(hours=8))
    now = datetime.now(utc8)
    date_str = now.strftime("%Y-%m-%d %H:%M")
    
    total = len(inbox_files) + len(learning_files)
    
    content = f"""# LLM-Wiki Index

## Statistics

| Area | Files |
|------|-------|
| 00-Inbox | {len(inbox_files)} |
| 08-Learning | {len(learning_files)} |
| **Total** | **{total}** |

### YouTube Transcription Status

| Level | Count | Meaning |
|-------|-------|---------|
| L1 (Transcribed) | {yt_by_level['L1']} | Whisper full transcript |
| L2 (External) | {yt_by_level['L2']} | lcz.me or external transcript |
| L3 (Description) | {yt_by_level['L3']} | YouTube description only |
| **Stale L3 (>7d)** | **{yt_stale}** | Needs upgrade |

## Last Updated

{date_str} (UTC+8)

## Recent Files

"""
    
    recent = sorted(
        inbox_files + yt_files,
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )[:15]
    
    for f in recent:
        title = extract_title(f)
        rel = f.relative_to(_vault_root())
        tags = extract_tags(f)
        tag_str = " " + " ".join(f"#{t}" for t in tags[:3]) if tags else ""
        content += f"- [[{rel}|{title}]]{tag_str}\n"
    
    content += "\n---\n*Auto-generated by llm-wiki*\n"
    index_path.write_text(content, encoding="utf-8")
    
    return total


def update_indexes(notes_created: Optional[List[Path]] = None) -> Dict[str, object]:
    """
    Update all llm-wiki indexes.
    
    Args:
        notes_created: Optional list of new note paths to log
    
    Returns:
        Dict with update results
    """
    results: Dict[str, object] = {}
    
    try:
        results["inbox_index"] = update_inbox_index()
    except Exception as e:
        results["inbox_index_error"] = str(e)
        _logger.error("Failed to update inbox index: %s", e)
    
    try:
        results["llm_wiki_index"] = update_llm_wiki_index()
    except Exception as e:
        results["llm_wiki_index_error"] = str(e)
        _logger.error("Failed to update LLM-Wiki index: %s", e)
    
    # Log each created note
    if notes_created:
        for note in notes_created:
            try:
                if note.exists():
                    content_hash = compute_sha256(note)
                else:
                    content_hash = ""
                
                fm, _ = parse_frontmatter(note.read_text(encoding="utf-8", errors="replace"))
                
                # Determine YouTube info
                is_youtube = fm.get("type") == "youtube-note"
                transcribed = str(fm.get("transcribed", "")).lower() in {"true", "yes"}
                completeness = fm.get("source-completeness", "")
                source_url = fm.get("source_url", "")
                if not source_url:
                    sources = fm.get("sources", [])
                    if isinstance(sources, list) and sources:
                        source_url = str(sources[0])
                
                update_ingest_log(
                    source=str(note),
                    hash_value=content_hash,
                    notes=[str(n) for n in notes_created],
                    source_url=source_url,
                    transcribed=transcribed if is_youtube else False,
                    source_completeness=completeness if is_youtube else "",
                )
            except Exception as e:
                _logger.error("Failed to log note %s: %s", note.name, e)
                results[f"ingest_log_error_{note.name}"] = str(e)
    
    return results


# ── Health Check ────────────────────────────────────────

def find_orphan_pages(limit: int = 20) -> List[Dict[str, str]]:
    """Find pages with no inbound wikilinks."""
    vr = _vault_root()
    all_files = set(vr.rglob("*.md"))
    linked_files: Set[Path] = set()
    
    for md_file in all_files:
        try:
            content = md_file.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        
        for link in re.findall(r"\[\[([^\]|#]+)(?:\|[^\]]+)?\]\]", content):
            link = link.strip()
            
            for resolver in [
                md_file.parent / link,
                vr / link,
                md_file.parent / (link + ".md"),
                vr / (link + ".md"),
            ]:
                if resolver.exists():
                    linked_files.add(resolver.resolve())
                    break
    
    orphans: List[Dict[str, str]] = []
    for md_file in all_files:
        if md_file.name in ("index.md", "SKILL.md"):
            continue
        if md_file.name.startswith("."):
            continue
        if md_file.name.endswith("_Ingest-Log.md"):
            continue
        if md_file.resolve() in linked_files:
            continue
        
        orphans.append({
            "path": str(md_file.relative_to(vr)),
            "reason": "No inbound wikilinks",
        })
        if len(orphans) >= limit:
            break
    
    return orphans


def find_broken_links(limit: int = 20) -> List[Dict[str, str]]:
    """Find wikilinks pointing to non-existent files."""
    vr = _vault_root()
    broken: List[Dict[str, str]] = []
    
    for md_file in vr.rglob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        
        for link in re.findall(r"\[\[([^\]|#]+)(?:\|[^\]]+)?\]\]", content):
            link = link.strip()
            
            found = any(p.exists() for p in [
                md_file.parent / link,
                vr / link,
                md_file.parent / (link + ".md"),
                vr / (link + ".md"),
            ])
            
            if not found:
                broken.append({
                    "source": str(md_file.relative_to(vr)),
                    "target": link,
                    "resolved": str(vr / link),
                })
                if len(broken) >= limit:
                    return broken
    
    return broken


def find_missing_sources(limit: int = 20) -> List[Dict[str, str]]:
    """Find notes with sources pointing to non-existent local files."""
    vr = _vault_root()
    missing: List[Dict[str, str]] = []
    
    for md_file in vr.rglob("*.md"):
        try:
            sources = extract_sources(md_file)
        except Exception:
            continue
        
        for source in sources:
            if source.startswith("http"):
                continue  # URLs are always "valid" at this level
            
            sp = Path(source)
            if sp.exists():
                continue
            
            resolved = vr / source
            if not resolved.exists():
                missing.append({
                    "page": str(md_file.relative_to(vr)),
                    "source": source,
                    "reason": "Local file not found",
                })
                if len(missing) >= limit:
                    return missing
    
    return missing


def find_youtube_orphans(max_age_days: int = 7, limit: int = 20) -> List[Dict[str, object]]:
    """
    Find YouTube notes at L3 level that are stale or lack transcription.
    These are candidates for Whisper/lcz.me upgrade.
    """
    orphans: List[Dict[str, object]] = []
    
    for f in get_youtube_inbox_files():
        try:
            result = check_youtube_completeness(f)
            
            # Include: L3 notes, or L2/L1 with stale_days > threshold
            include = False
            reason = ""
            
            if result["level"] == "L3":
                include = True
                reason = "L3 — description only"
            elif result.get("stale_days", 0) > max_age_days and result["level"] in {"L1", "L2"}:
                include = True
                reason = f"L{result['level'][1]} but stale ({result['stale_days']}d)"
            
            if not include:
                continue
            
            orphans.append({
                "file": str(f.relative_to(_vault_root())),
                "title": extract_title(f),
                "level": result["level"],
                "status": result["status"],
                "stale_days": result.get("stale_days"),
                "notes": result.get("notes", []),
                "reason": reason,
            })
            
            if len(orphans) >= limit:
                break
                
        except Exception as e:
            _logger.warning("Failed to check %s: %s", f.name, e)
    
    return orphans


def health_check(include_youtube: bool = True) -> Dict[str, object]:
    """
    Run complete vault health check.
    
    Args:
        include_youtube: Whether to include YouTube-specific checks
    
    Returns:
        Structured health report dict
    """
    utc8 = timezone(timedelta(hours=8))
    now = datetime.now(utc8)
    
    inbox_files = get_inbox_files(include_youtube=False)
    yt_files = get_youtube_inbox_files() if include_youtube else []
    
    orphans = find_orphan_pages()
    broken = find_broken_links()
    missing_srcs = find_missing_sources()
    
    # YouTube-specific
    yt_orphans: List[Dict] = []
    yt_stale_count = 0
    yt_by_level = {"L1": 0, "L2": 0, "L3": 0}
    
    if include_youtube and _YOUTUBE_OK:
        for f in yt_files:
            try:
                result = check_youtube_completeness(f)
                lvl = result.get("level", "L3")
                if lvl in yt_by_level:
                    yt_by_level[lvl] += 1
                
                if result.get("stale_days", 0) > 7:
                    yt_stale_count += 1
                
                if result["level"] == "L3":
                    yt_orphans.append({
                        "file": str(f.relative_to(_vault_root())),
                        "title": extract_title(f),
                        "level": lvl,
                        "stale_days": result.get("stale_days"),
                    })
            except Exception as e:
                _logger.warning("YouTube check failed for %s: %s", f.name, e)
    
    # Index freshness
    index_path = _llm_wiki_index_path()
    index_stale = False
    if index_path.exists():
        try:
            content = index_path.read_text(encoding="utf-8", errors="replace")
            m = re.search(r"Last Updated\n(.+?) \(UTC", content)
            if m:
                last_updated = datetime.strptime(m.group(1).strip(), "%Y-%m-%d %H:%M")
                last_updated = last_updated.replace(tzinfo=utc8)
                if (now - last_updated).days > 7:
                    index_stale = True
        except Exception:
            index_stale = True
    else:
        index_stale = True
    
    return {
        "timestamp": now.isoformat(),
        "vault_root": str(_vault_root()),
        "statistics": {
            "inbox_count": len(inbox_files),
            "youtube_count": len(yt_files),
            "youtube_by_level": yt_by_level,
            "youtube_stale_l3": yt_stale_count,
            "learning_count": len(get_learning_files()),
            "total_files": len(inbox_files) + len(yt_files) + len(get_learning_files()),
            "orphans_count": len(orphans),
            "broken_links_count": len(broken),
            "missing_sources_count": len(missing_srcs),
        },
        "issues": {
            "orphans": orphans[:20],
            "broken_links": broken[:20],
            "missing_sources": missing_srcs[:20],
            "youtube_l3_orphans": yt_orphans[:10],
        },
        "alerts": {
            "inbox_high": len(inbox_files) > 50,
            "youtube_stale": yt_stale_count > 0,
            "index_stale": index_stale,
            "orphans_exist": len(orphans) > 0,
            "broken_links_exist": len(broken) > 0,
            "missing_sources_exist": len(missing_srcs) > 0,
        },
    }


# ── Report Generation ───────────────────────────────────

def generate_report(health: Optional[Dict[str, object]] = None) -> str:
    """
    Generate human-readable Markdown health report.
    
    Args:
        health: Optional pre-computed health dict (computes if None)
    
    Returns:
        Markdown formatted report string
    """
    if health is None:
        health = health_check()
    
    utc8 = timezone(timedelta(hours=8))
    now = datetime.now(utc8)
    
    stats = health["statistics"]
    alerts = health.get("alerts", {})
    issues = health.get("issues", {})
    
    # YouTube summary
    yt_levels = stats.get("youtube_by_level", {})
    yt_total = sum(yt_levels.values())
    
    lines = [
        f"# llm-wiki Health Report",
        "",
        f"Generated: {now.strftime('%Y-%m-%d %H:%M')} (UTC+8)",
        f"Vault: `{health['vault_root']}`",
        "",
        "## Statistics",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| 00-Inbox (notes) | {stats['inbox_count']} |",
        f"| 00-Inbox (YouTube) | {stats.get('youtube_count', 0)} |",
        f"| 08-Learning | {stats.get('learning_count', 0)} |",
        f"| **Total** | **{stats.get('total_files', 0)}** |",
        "",
        "### YouTube Transcription",
        "",
        "| Level | Count |",
        "|-------|-------|",
        f"| L1 (Whisper transcribed) | {yt_levels.get('L1', 0)} |",
        f"| L2 (External transcript) | {yt_levels.get('L2', 0)} |",
        f"| L3 (Description only) | {yt_levels.get('L3', 0)} |",
        "",
        "## Alerts",
        "",
    ]
    
    alert_map = {
        "inbox_high": f"⚠️ **00-Inbox 超过 50 个文件** ({stats['inbox_count']})",
        "youtube_stale": f"⚠️ **{stats.get('youtube_stale_l3', 0)} 个 YouTube L3 笔记超过 7 天未转录**",
        "index_stale": "⚠️ **Index 已超过 7 天未更新**",
        "orphans_exist": f"⚠️ **{stats['orphans_count']} 个孤岛页面**",
        "broken_links_exist": f"⚠️ **{stats['broken_links_count']} 个坏链接**",
        "missing_sources_exist": f"⚠️ **{stats['missing_sources_count']} 个缺失来源**",
    }
    
    has_alert = False
    for key, msg in alert_map.items():
        if alerts.get(key):
            lines.append(f"- {msg}")
            has_alert = True
    
    if not has_alert:
        lines.append("- ✅ **Vault 健康，無重大問題**")
    
    # YouTube L3 orphans
    yt_l3 = issues.get("youtube_l3_orphans", [])
    if yt_l3:
        lines += ["", "## YouTube L3 Notes (需要升级)", ""]
        for item in yt_l3:
            days = item.get("stale_days")
            stale_str = f" ({days}d old)" if days else ""
            lines.append(f"- [[{item['file']}]] —{stale_str}")
    
    # General orphans
    orphans = issues.get("orphans", [])
    if orphans:
        lines += ["", "## Orphan Pages", ""]
        for o in orphans[:10]:
            lines.append(f"- [[{o['path']}]]")
        if len(orphans) > 10:
            lines.append(f"\n_...还有 {len(orphans) - 10} 个_")
    
    # Broken links
    broken = issues.get("broken_links", [])
    if broken:
        lines += ["", "## Broken Links", ""]
        for b in broken[:10]:
            lines.append(f"- [[{b['source']}]] → `{b['target']}`")
        if len(broken) > 10:
            lines.append(f"\n_...还有 {len(broken) - 10} 个_")
    
    lines += ["", "---", "*Generated by llm-wiki*"]
    
    return "\n".join(lines)


# ── CLI Entry Point ─────────────────────────────────────

def main(argv: Optional[List[str]] = None) -> int:
    """CLI for health check."""
    import argparse
    
    parser = argparse.ArgumentParser(description="llm-wiki Health Check")
    parser.add_argument("--report", action="store_true", help="Full Markdown report")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--skip-youtube", action="store_true", help="Skip YouTube checks")
    parser.add_argument("--output", type=str, help="Write report to file")
    args = parser.parse_args(argv)
    
    health = health_check(include_youtube=not args.skip_youtube)
    
    if args.json:
        print(json.dumps(health, ensure_ascii=False, indent=2))
    elif args.report:
        print(generate_report(health))
    else:
        # Compact output
        stats = health["statistics"]
        alerts = health.get("alerts", {})
        print("=== llm-wiki Health ===")
        print(f"  Vault: {health['vault_root']}")
        print(f"  Inbox: {stats['inbox_count']} | YouTube: {stats.get('youtube_count', 0)} | Learning: {stats.get('learning_count', 0)}")
        
        yt_levels = stats.get("youtube_by_level", {})
        if yt_levels:
            print(f"  YouTube: L1={yt_levels.get('L1',0)} L2={yt_levels.get('L2',0)} L3={yt_levels.get('L3',0)}")
        
        alert_parts = [k for k, v in alerts.items() if v and k != "missing_sources_exist"]
        if alert_parts:
            print(f"  ⚠️  Alerts: {', '.join(alert_parts)}")
        else:
            print("  ✅ All good")
        
        if stats.get("orphans_count", 0) or stats.get("broken_links_count", 0):
            print(f"  Orphans: {stats['orphans_count']} | Broken links: {stats['broken_links_count']}")
    
    if args.output:
        try:
            Path(args.output).write_text(generate_report(health), encoding="utf-8")
            print(f"\nReport written to: {args.output}")
        except Exception as e:
            print(f"Failed to write report: {e}", file=sys.stderr)
            return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
