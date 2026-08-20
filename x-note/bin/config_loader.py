"""
config_loader.py
================
Centralized config loader for x-note.
Reads .path-config.json from VAULT_ROOT, applies defaults, validates.
"""
import json
import os
import sys
from pathlib import Path
from typing import Any, Optional


DEFAULTS = {
    "CDP_PORT": 19825,
    "CDP_START_WAIT": 5,
    "CHROME_PROFILE_NAME": "Hsiaopigo",
    "CHROME_EXE": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "CHROME_USER_DATA_DIR": r"%LOCALAPPDATA%\Google\Chrome\User Data",
    "X2_MIN_SCORE": 6.5,
    "X2_LIMIT_HANDLES": 5,
    "X2_DRY_RUN": False,
    "X2_HEADLESS": True,
    "X2_FXTWITTER_HOST": "https://api.fxtwitter.com",
    "X2_USE_FXTWITTER": True,
    "X2_FET_TIMEOUT": 30,
    "X2_RATE_LIMIT_SLEEP": 1.0,
}


def resolve_path(raw: str) -> str:
    """Resolve %VAR% syntax in Windows paths."""
    if not raw:
        return raw
    out = raw
    for _ in range(3):
        expanded = os.path.expandvars(out)
        if expanded == out:
            break
        out = expanded
    return out


def find_vault_root() -> Path:
    """
    Find Vault root by searching for .path-config.json.
    Order: CWD parents (3 levels) → env X2_VAULT_ROOT → common paths.
    """
    # 1. CWD parents
    for p in [Path.cwd()] + list(Path.cwd().parents)[:3]:
        if (p / ".path-config.json").exists():
            return p.resolve()

    # 2. Env var
    env = os.environ.get("X2_VAULT_ROOT")
    if env and (Path(env) / ".path-config.json").exists():
        return Path(env).resolve()

    # 3. Common Windows paths
    candidates = [
        Path.home() / "obsidian",
        Path.home() / "Documents" / "obsidian",
        Path("E:/obsidian"),
        Path("E:/obsidian/PigoVault"),
        Path("C:/obsidian"),
    ]
    for c in candidates:
        if (c / ".path-config.json").exists():
            return c.resolve()

    raise FileNotFoundError(
        ".path-config.json not found. "
        "Set X2_VAULT_ROOT env var or run setup-vault-host.sh first."
    )


def load_config() -> dict:
    """Load config from .path-config.json + defaults."""
    config_path = find_vault_root() / ".path-config.json"
    raw = json.loads(config_path.read_text(encoding="utf-8"))

    # Strip metadata keys
    cfg = {k: v for k, v in raw.items() if not k.startswith("_")}

    # Apply defaults
    for k, v in DEFAULTS.items():
        cfg.setdefault(k, v)

    # Resolve paths
    for key in [
        "VAULT_ROOT", "AGENT_ROOT", "DOWNLOADS", "DOCUMENTS",
        "CODEX_SKILLS", "AGENTS_SKILLS",
        "CHROME_EXE", "CHROME_USER_DATA_DIR",
        "TWITTER_HANDLE_FILE", "X_COOKIES_FILE",
    ]:
        if key in cfg:
            cfg[key] = resolve_path(cfg[key])

    # Validate required
    for key in ["VAULT_ROOT", "AGENT_ROOT"]:
        if not cfg.get(key):
            raise ValueError(f"Missing required config: {key}")

    return cfg


def get(cfg: dict, key: str, default: Any = None) -> Any:
    """Typed get with default."""
    return cfg.get(key, default)


def paths(cfg: dict) -> dict:
    """Return frequently-used paths object."""
    return {
        "vault_root": Path(cfg["VAULT_ROOT"]),
        "agent_root": Path(cfg["AGENT_ROOT"]),
        "downloads": Path(cfg.get("DOWNLOADS", Path.home() / "Downloads")),
        "inbox": Path(cfg["VAULT_ROOT"]) / "00-Inbox",
        "cookies_file": Path(cfg.get("X_COOKIES_FILE", "")),
        "handle_file": Path(cfg.get("TWITTER_HANDLE_FILE", "")),
        "chrome_exe": Path(cfg["CHROME_EXE"]),
        "chrome_user_data": Path(resolve_path(cfg["CHROME_USER_DATA_DIR"])),
    }


if __name__ == "__main__":
    cfg = load_config()
    print(json.dumps(cfg, indent=2, ensure_ascii=False))
