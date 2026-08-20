"""
tests/test_utils.py — llm-wiki Unit Tests
==========================================
Run with: python -m pytest tests/test_utils.py -v
         python -m pytest tests/test_utils.py -v -k "test_parse_frontmatter"
"""
from __future__ import annotations

import json
import os
import sys
import importlib.util
from datetime import datetime, timezone, timedelta
from pathlib import Path
import pytest

# ── Setup: dynamically load llm_wiki from llm-wiki directory ──
# (Directory name 'llm-wiki' has a hyphen; use importlib instead of import)

SKILL_ROOT = Path(__file__).parent.parent  # = llm-wiki/
UTILS_PATH = SKILL_ROOT / "utils.py"
CONFIG_PATH = SKILL_ROOT / "config.py"
YT_PATH = SKILL_ROOT / "youtube_handler.py"

# Create a fake parent package 'llm_wiki' before loading sub-modules
# This is required so dataclass decorators resolve sys.modules correctly
_fake_pkg = type(sys)('llm_wiki')  # Module-like object
sys.modules['llm_wiki'] = _fake_pkg

# Load modules into the fake package namespace
_spec_config = importlib.util.spec_from_file_location("llm_wiki.config", CONFIG_PATH)
_spec_yt = importlib.util.spec_from_file_location("llm_wiki.youtube_handler", YT_PATH)
_spec_utils = importlib.util.spec_from_file_location("llm_wiki.utils", UTILS_PATH)

_config_mod = importlib.util.module_from_spec(_spec_config)
_yt_mod = importlib.util.module_from_spec(_spec_yt)
_utils = importlib.util.module_from_spec(_spec_utils)

# Register sub-modules (needed for intra-package imports like `from . import config`)
sys.modules['llm_wiki.config'] = _config_mod
sys.modules['llm_wiki.youtube_handler'] = _yt_mod
sys.modules['llm_wiki.utils'] = _utils
sys.modules['llm_wiki'] = _fake_pkg  # refresh with sub-module refs
_fake_pkg.config = _config_mod
_fake_pkg.youtube_handler = _yt_mod
_fake_pkg.utils = _utils

# Execute in dependency order
_spec_config.loader.exec_module(_config_mod)
_spec_yt.loader.exec_module(_yt_mod)
_spec_utils.loader.exec_module(_utils)

# Re-export from utils
parse_frontmatter = _utils.parse_frontmatter
compute_sha256 = _utils.compute_sha256
compute_string_hash = _utils.compute_string_hash
compute_content_hash = _utils.compute_content_hash
extract_title = _utils.extract_title
extract_tags = _utils.extract_tags
extract_sources = _utils.extract_sources
extract_youtube_info = _utils.extract_youtube_info
IngestLog = _utils.IngestLog
load_ingest_log = _utils.load_ingest_log
check_incremental_cache = _utils.check_incremental_cache
health_check = _utils.health_check
generate_report = _utils.generate_report
update_ingest_log = _utils.update_ingest_log
find_orphan_pages = _utils.find_orphan_pages
find_broken_links = _utils.find_broken_links
find_missing_sources = _utils.find_missing_sources

# From config
LlmWikiConfig = _config_mod.LlmWikiConfig

def _load_config():
    return _config_mod.load_config()

def reset_config():
    _config_mod.reset_config()  # Calls config.py's reset_config() which clears _config

# From youtube_handler
extract_video_id = _yt_mod.extract_video_id
extract_lcz_me_id = _yt_mod.extract_lcz_me_id
check_youtube_completeness = _yt_mod.check_youtube_completeness
YouTubeMetadata = _yt_mod.YouTubeMetadata
TranscriptResult = _yt_mod.TranscriptResult
build_youtube_note_content = _yt_mod.build_youtube_note_content


# ── Fixtures ───────────────────────────────────────────

@pytest.fixture
def temp_vault(tmp_path: Path) -> Path:
    """Create a minimal temp vault structure."""
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "00-Inbox").mkdir()
    (vault / "08-Learning").mkdir()
    (vault / "08-Learning/99_Maintenance/status").mkdir(parents=True)
    (vault / "10-LLM-Wiki").mkdir()
    (vault / "12-Meta").mkdir()
    (vault / ".git").mkdir()  # Makes autodetect work
    return vault


@pytest.fixture
def sample_youtube_note(temp_vault: Path) -> Path:
    """Create a sample YouTube note."""
    content = """---
title: "Test YouTube Video"
sources:
  - "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  - "https://lcz.me/topic/123"
type: youtube-note
transcribed: false
source-completeness: description-only
created: "2026-08-20"
tags:
  - test
  - youtube
---
# Test YouTube Video

**影片標題**：Test
**頻道**：Test Channel
"""
    path = temp_vault / "00-Inbox/2026-08-20_x-note_youtube_test.md"
    path.write_text(content, encoding="utf-8")
    return path


@pytest.fixture
def sample_x_note(temp_vault: Path) -> Path:
    """Create a sample x-note."""
    content = """---
title: "Test Post"
sources:
  - "https://x.com/test/status/123"
source_url: "https://x.com/test/status/123"
tweet_id: "123"
handle: "@test"
author_display: "Test User"
created: "2026-08-20T10:00:00+08:00"
captured_at: "2026-08-20 10:00:00 +08:00"
capture_method: fxtwitter
content_hash: "abc123"
text_length: 500
score: 7.5
score_reason: "good post"
status: inbox
classification_path: "00-Inbox"
type: x-post-summary
tags:
  - test
  - x-note
---
# Test Post

## Core Summary
A good post about AI.
"""
    path = temp_vault / "00-Inbox/2026-08-20_x-note_test.md"
    path.write_text(content, encoding="utf-8")
    return path


# ── Tests: Frontmatter Parsing ──────────────────────────

class TestParseFrontmatter:
    
    def test_simple_key_value(self):
        text = "---\ntitle: Hello\nscore: 7.5\n---\nBody"
        fm, body = parse_frontmatter(text)
        assert fm["title"] == "Hello"
        assert fm["score"] == "7.5"
        assert body == "Body"
    
    def test_quoted_values(self):
        text = '---\ntitle: "Hello World"\n---\n'
        fm, _ = parse_frontmatter(text)
        assert fm["title"] == "Hello World"
    
    def test_list_values(self):
        text = """---
tags:
  - python
  - ai
sources:
  - https://example.com
---
"""
        fm, _ = parse_frontmatter(text)
        assert "python" in fm["tags"]
        assert "ai" in fm["tags"]
        assert "https://example.com" in fm["sources"]
    
    def test_no_frontmatter(self):
        text = "Just plain text"
        fm, body = parse_frontmatter(text)
        assert fm == {}
        assert body == text
    
    def test_indented_list_continuation(self):
        text = """---
tags:
    - python
    - ai
---
"""
        fm, _ = parse_frontmatter(text)
        assert "python" in fm["tags"]
        assert "ai" in fm["tags"]
    
    def test_mixed_frontmatter(self):
        text = """---
title: Test
sources:
  - https://x.com/1
  - https://x.com/2
transcribed: true
count: 42
---
# Body
"""
        fm, body = parse_frontmatter(text)
        assert fm["title"] == "Test"
        assert len(fm["sources"]) == 2
        assert fm["transcribed"] == "true"
        assert fm["count"] == "42"
        assert body.startswith("# Body")


# ── Tests: Extraction ───────────────────────────────────

class TestExtract:
    
    def test_extract_title_from_frontmatter(self, temp_vault: Path):
        content = "---\ntitle: My Title\n---\n# Should not be used"
        path = temp_vault / "00-Inbox/test.md"
        path.write_text(content, encoding="utf-8")
        assert extract_title(path) == "My Title"
    
    def test_extract_title_from_h1(self, temp_vault: Path):
        content = "---\nscore: 7\n---\n# Actual Title\n"
        path = temp_vault / "00-Inbox/test2.md"
        path.write_text(content, encoding="utf-8")
        assert extract_title(path) == "Actual Title"
    
    def test_extract_title_fallback_to_stem(self, temp_vault: Path):
        content = "No frontmatter or H1"
        path = temp_vault / "00-Inbox/test5.md"
        path.write_text(content, encoding="utf-8")
        assert extract_title(path) == "test5"
    
    def test_extract_tags(self, temp_vault: Path):
        content = "---\ntags:\n  - python\n  - ai\n  - llm\n---\n"
        path = temp_vault / "00-Inbox/test3.md"
        path.write_text(content, encoding="utf-8")
        tags = extract_tags(path)
        assert "python" in tags
        assert "ai" in tags
        assert "llm" in tags
    
    def test_extract_sources(self, temp_vault: Path):
        content = "---\nsources:\n  - https://x.com/1\n  - https://x.com/2\n---\n"
        path = temp_vault / "00-Inbox/test4.md"
        path.write_text(content, encoding="utf-8")
        sources = extract_sources(path)
        assert "https://x.com/1" in sources
        assert "https://x.com/2" in sources
    
    def test_extract_youtube_info(self, sample_youtube_note: Path):
        info = extract_youtube_info(sample_youtube_note)
        assert info["type"] == "youtube-note"
        assert info["source_completeness"] == "description-only"
        assert info["transcribed"] is False


# ── Tests: Hash Functions ────────────────────────────────

class TestHash:
    
    def test_compute_sha256_file(self, tmp_path: Path):
        f = tmp_path / "test.txt"
        f.write_text("hello world", encoding="utf-8")
        h = compute_sha256(f)
        assert len(h) == 64
        assert h.isalnum()
    
    def test_compute_sha256_consistency(self, tmp_path: Path):
        f = tmp_path / "test.txt"
        f.write_text("hello world", encoding="utf-8")
        h1 = compute_sha256(f)
        h2 = compute_sha256(f)
        assert h1 == h2
    
    def test_compute_string_hash(self):
        h = compute_string_hash("https://example.com")
        assert len(h) == 64
        assert h == compute_content_hash("https://example.com")
    
    def test_different_inputs_different_hashes(self):
        h1 = compute_string_hash("a")
        h2 = compute_string_hash("b")
        assert h1 != h2


# ── Tests: Ingest Log ──────────────────────────────────

class TestIngestLog:
    
    def test_add_and_retrieve_hash(self, tmp_path: Path):
        log = IngestLog(tmp_path / "log.json")
        log.add(
            source="E:/test/note.md",
            content_hash="abc123def456",
            source_type="file",
        )
        retrieved = log.get_hash("E:/test/note.md")
        assert retrieved == "abc123def456"
    
    def test_load_from_json(self, tmp_path: Path):
        log = IngestLog(tmp_path / "log.json")
        log.add(source="E:/test.md", content_hash="hash1")
        log.add(source="E:/test2.md", content_hash="hash2")
        log2 = IngestLog(tmp_path / "log.json")
        log2.load()
        assert log2.get_hash("E:/test.md") == "hash1"
        assert log2.get_hash("E:/test2.md") == "hash2"
    
    def test_save_creates_both_formats(self, tmp_path: Path):
        log = IngestLog(tmp_path / "log.json")
        log.add(source="E:/test.md", content_hash="abc")
        assert log.json_path.exists()
        assert log.md_path.exists()
        data = json.loads(log.json_path.read_text(encoding="utf-8"))
        assert data["version"] == "1.0"
        assert len(data["entries"]) == 1
    
    def test_youtube_entry_with_transcription(self, tmp_path: Path):
        log = IngestLog(tmp_path / "log.json")
        log.add(
            source="E:/00-Inbox/2026-08-20_x-note_youtube_test.md",
            source_type="youtube",
            content_hash="yt_hash",
            source_url="https://youtube.com/watch?v=abc",
            transcribed=True,
            source_completeness="L1",
        )
        retrieved_hash = log.get_hash("E:/00-Inbox/2026-08-20_x-note_youtube_test.md")
        assert retrieved_hash == "yt_hash"
        data = json.loads(log.json_path.read_text(encoding="utf-8"))
        entry = data["entries"][0]
        assert entry["transcribed"] is True
        assert entry["source_completeness"] == "L1"
        assert entry["source_url"] == "https://youtube.com/watch?v=abc"


# ── Tests: YouTube Handler ──────────────────────────────

class TestYouTubeHandler:
    
    @pytest.mark.parametrize("url,expected", [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/shorts/abc123DEF12", "abc123DEF12"),  # 11 chars
        ("https://youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("not a youtube url", None),
        ("https://youtube.com", None),
    ])
    def test_extract_video_id(self, url: str, expected: str):
        assert extract_video_id(url) == expected
    
    def test_extract_lcz_me_id(self):
        assert extract_lcz_me_id("https://lcz.me/topic/1187") == "1187"
        assert extract_lcz_me_id("https://lcz.me/topic/42/") == "42"
        assert extract_lcz_me_id("https://youtube.com/watch") is None
    
    def test_check_youtube_completeness_l1(self, temp_vault: Path):
        content = """---
title: Test
sources:
  - https://youtube.com/watch?v=abc
type: youtube-note
transcribed: true
source-completeness: full-transcript
created: "2026-08-20"
---
"""
        path = temp_vault / "00-Inbox/test_yt_l1.md"
        path.write_text(content, encoding="utf-8")
        result = check_youtube_completeness(path)
        assert result["level"] == "L1"
        assert result["status"] == "complete"
        assert result["transcribed"] is True
    
    def test_check_youtube_completeness_l2_external(self, temp_vault: Path):
        content = """---
title: Test
sources:
  - https://youtube.com/watch?v=abc
  - https://lcz.me/topic/123
type: youtube-note
transcribed: false
source-completeness: external-transcript
created: "2026-08-20"
---
"""
        path = temp_vault / "00-Inbox/test_yt_l2.md"
        path.write_text(content, encoding="utf-8")
        result = check_youtube_completeness(path)
        assert result["level"] == "L2"
        assert result["status"] == "complete"
    
    def test_check_youtube_completeness_l3(self, temp_vault: Path):
        content = """---
title: Test
sources:
  - https://youtube.com/watch?v=abc
type: youtube-note
transcribed: false
source-completeness: description-only
created: "2026-08-20"
---
"""
        path = temp_vault / "00-Inbox/test_yt_l3.md"
        path.write_text(content, encoding="utf-8")
        result = check_youtube_completeness(path)
        assert result["level"] == "L3"
        assert result["status"] == "incomplete"
    
    def test_check_youtube_completeness_stale(self, temp_vault: Path):
        old_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
        content = f"""---
title: Test
sources:
  - https://youtube.com/watch?v=abc
type: youtube-note
transcribed: false
source-completeness: description-only
created: "{old_date}"
---
"""
        path = temp_vault / "00-Inbox/test_yt_stale.md"
        path.write_text(content, encoding="utf-8")
        result = check_youtube_completeness(path)
        assert result["level"] == "L3"
        assert result["stale_days"] is not None
        assert result["stale_days"] >= 10
    
    def test_youTubeMetadata_to_frontmatter_dict(self):
        meta = YouTubeMetadata(
            video_id="abc123",
            title="Test Video",
            channel="Test Channel",
            url="https://youtube.com/watch?v=abc123",
            lcz_me_url="https://lcz.me/topic/123",
        )
        d = meta.to_frontmatter_dict()
        assert d["video_id"] == "abc123"
        assert d["channel"] == "Test Channel"
        assert d["source-completeness"] == "description-only"
        assert d["transcribed"] is False
    
    def test_build_youtube_note_content(self):
        meta = YouTubeMetadata(
            video_id="abc123",
            title="Test Video",
            channel="Test Channel",
            url="https://youtube.com/watch?v=abc123",
        )
        body = build_youtube_note_content(
            metadata=meta,
            transcript="This is a test transcript.",
            summary_sections="## Summary\n- Point 1\n- Point 2",
        )
        assert "Test Video" in body
        assert "Test Channel" in body
        assert "## Summary" in body
        assert "This is a test transcript." in body


# ── Tests: Config ──────────────────────────────────────

class TestConfig:
    
    def test_load_config_resolves_vault(self, temp_vault: Path, monkeypatch):
        # Set env var BEFORE importing config module to ensure it takes effect
        monkeypatch.setenv("LLM_WIKI_VAULT_ROOT", str(temp_vault))
        # Force re-import by clearing the cached module
        import sys
        _cfg_mod_name = "llm_wiki_config"
        if _cfg_mod_name in sys.modules:
            del sys.modules[_cfg_mod_name]
        reset_config()
        cfg = _load_config()
        assert cfg.vault_root == temp_vault
        assert cfg.inbox_dir == temp_vault / "00-Inbox"
        assert cfg.maintenance_dir == temp_vault / "08-Learning/99_Maintenance/status"
    
    def test_config_method_is_env(self, temp_vault: Path, monkeypatch):
        monkeypatch.setenv("LLM_WIKI_VAULT_ROOT", str(temp_vault))
        import sys
        _cfg_mod_name = "llm_wiki_config"
        if _cfg_mod_name in sys.modules:
            del sys.modules[_cfg_mod_name]
        reset_config()
        cfg = _load_config()
        assert cfg.resolution_method == "env"


# ── Tests: Edge Cases ─────────────────────────────────

class TestEdgeCases:
    
    def test_empty_frontmatter(self, temp_vault: Path):
        content = "---\n---\n# Just a heading"
        path = temp_vault / "00-Inbox/empty.md"
        path.write_text(content, encoding="utf-8")
        title = extract_title(path)
        assert title == "Just a heading"
    
    def test_malformed_yaml(self, temp_vault: Path):
        content = "---\ntitle: Test\n  - bad list\n---\n"
        path = temp_vault / "00-Inbox/bad.md"
        path.write_text(content, encoding="utf-8")
        fm, _ = parse_frontmatter(content)
        assert "title" in fm
    
    def test_nonexistent_file(self, temp_vault: Path):
        path = temp_vault / "00-Inbox/does_not_exist.md"
        assert extract_title(path) == "does_not_exist"
        assert extract_tags(path) == []
        assert extract_sources(path) == []


# ── Tests: Incremental Cache ───────────────────────────

class TestIncrementalCache:
    
    def test_new_file_needs_processing(self, tmp_path: Path):
        f = tmp_path / "new.md"
        f.write_text("hello", encoding="utf-8")
        needs, prev = check_incremental_cache(str(f))
        assert needs is True
        assert prev == ""
    
    def test_unchanged_file_skipped(self, tmp_path: Path):
        f = tmp_path / "same.md"
        f.write_text("same content", encoding="utf-8")
        
        # Use a temp IngestLog so tests don't pollute the real vault log
        log = IngestLog(tmp_path / "log.json")
        
        # First: it needs processing (no prior hash in log)
        needs1, _ = check_incremental_cache(str(f), ingest_log=log)
        assert needs1 is True, "New file should need processing"
        
        # Log it via the same IngestLog
        h = compute_sha256(f)
        log.add(source=str(f), content_hash=h)
        
        # Second check: same hash via same IngestLog → no reprocessing
        needs2, prev2 = check_incremental_cache(str(f), ingest_log=log)
        assert needs2 is False, "Same hash should not need reprocessing"
        assert prev2 == h
    
    def test_url_needs_processing(self):
        url = "https://www.youtube.com/watch?v=new"
        needs, prev = check_incremental_cache(url)
        assert needs is True


# ── Tests: Report Generation ───────────────────────────

class TestReportGeneration:
    
    def test_generate_report_has_required_sections(self, temp_vault: Path, monkeypatch):
        monkeypatch.setenv("LLM_WIKI_VAULT_ROOT", str(temp_vault))
        reset_config()
        report = generate_report()
        assert "# llm-wiki Health Report" in report
        assert "## Statistics" in report
        assert "## Alerts" in report


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
