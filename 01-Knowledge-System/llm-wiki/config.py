"""
config.py — llm-wiki Path Configuration
========================================
Resolves VAULT_ROOT and skill paths with strict priority order.
All other modules import from here — no hardcoded paths.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field


# ── Defaults ──────────────────────────────────────────────

_VAULT_CANDIDATES = [
    "E:/obsidian",
    "E:/obsidian/PigoVault",
    "D:/obsidian",
]

# ── Dataclass ────────────────────────────────────────────

@dataclass
class LlmWikiConfig:
    """Resolved llm-wiki configuration."""
    
    vault_root: Path
    inbox_dir: Path
    learning_dir: Path
    llm_wiki_dir: Path
    maintenance_dir: Path
    inbox_index: Path
    llm_wiki_index: Path
    ingest_log: Path
    youtube_inbox_pattern: str = r"_x-note_youtube[-_][^/]*\.md$"
    
    # YouTube
    lcz_me_base: str = "https://lcz.me/topic/"
    ytdlp_format: str = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
    
    # System
    config_file: Optional[Path] = None
    resolution_method: str = ""  # "env" | "json" | "autodetect" | "fallback"


# ── Resolution Pipeline ──────────────────────────────────

def _load_json_config(vault_root: Path) -> dict:
    """Load .path-config.json from vault root."""
    cfg_file = vault_root / ".path-config.json"
    if cfg_file.exists():
        try:
            return json.loads(cfg_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _autodetect_vault_root() -> Optional[Path]:
    """Walk up from CWD looking for .git + 00-Inbox."""
    cwd = Path.cwd()
    for root in [cwd] + list(cwd.parents):
        if (root / ".git").exists() and (root / "00-Inbox").exists():
            return root
    return None


def _detect_maintenance_dir(vault_root: Path) -> Path:
    """Find maintenance directory (may be in 08-Learning/99_Maintenance or 12-Meta)."""
    candidates = [
        vault_root / "08-Learning/99_Maintenance/status",
        vault_root / "08-Learning/99_Maintenance",
        vault_root / "12-Meta/health-reports",
    ]
    for d in candidates:
        if d.exists():
            return d
    
    # Create default
    default = vault_root / "08-Learning/99_Maintenance/status"
    default.mkdir(parents=True, exist_ok=True)
    return default


def load_config() -> LlmWikiConfig:
    """
    Resolve llm-wiki configuration with priority:
    1. LLM_WIKI_VAULT_ROOT env var
    2. {{VAULT_ROOT}}/.path-config.json
    3. Autodetect (.git + 00-Inbox)
    4. Fallback: E:/obsidian
    """
    # 1. Env var
    env_path = os.environ.get("LLM_WIKI_VAULT_ROOT")
    if env_path:
        vault_root = Path(env_path).resolve()
        resolution = "env"
    else:
        # 2. .path-config.json
        for candidate in _VAULT_CANDIDATES:
            cfg = _load_json_config(Path(candidate))
            if "vault_root" in cfg:
                vault_root = Path(cfg["vault_root"]).resolve()
                resolution = "json"
                break
        else:
            # 3. Autodetect
            detected = _autodetect_vault_root()
            if detected:
                vault_root = detected
                resolution = "autodetect"
            else:
                # 4. Fallback
                vault_root = Path("E:/obsidian").resolve()
                resolution = "fallback"

    # Derive all paths
    inbox_dir = vault_root / "00-Inbox"
    learning_dir = vault_root / "08-Learning"
    llm_wiki_dir = vault_root / "10-LLM-Wiki"
    maintenance_dir = _detect_maintenance_dir(vault_root)
    
    inbox_index = inbox_dir / "index.md"
    llm_wiki_index = maintenance_dir / "LLM-Wiki-Index.md"
    ingest_log = maintenance_dir / "LLM-Wiki-Ingest-Log.md"

    # Load YouTube settings
    json_cfg = _load_json_config(vault_root)
    yt_cfg = json_cfg.get("youtube", {})

    return LlmWikiConfig(
        vault_root=vault_root,
        inbox_dir=inbox_dir,
        learning_dir=learning_dir,
        llm_wiki_dir=llm_wiki_dir,
        maintenance_dir=maintenance_dir,
        inbox_index=inbox_index,
        llm_wiki_index=llm_wiki_index,
        ingest_log=ingest_log,
        lcz_me_base=yt_cfg.get("lcz_me_base", "https://lcz.me/topic/"),
        ytdlp_format=yt_cfg.get("ytdlp_format", 
            "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"),
        config_file=Path(json_cfg.get("__config_file__", "")) if json_cfg.get("__config_file__") else None,
        resolution_method=resolution,
    )


# ── Module-level singleton ────────────────────────────────

_config: Optional[LlmWikiConfig] = None

def get_config() -> LlmWikiConfig:
    """Get or create the global config singleton."""
    global _config
    if _config is None:
        _config = load_config()
    return _config


def reset_config() -> None:
    """Reset config singleton (useful for testing)."""
    global _config
    _config = None


# ── Convenience aliases ───────────────────────────────────

def vault_root() -> Path:
    return get_config().vault_root

def inbox_dir() -> Path:
    return get_config().inbox_dir

def maintenance_dir() -> Path:
    return get_config().maintenance_dir

def ingest_log_path() -> Path:
    return get_config().ingest_log
