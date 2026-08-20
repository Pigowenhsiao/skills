"""
resolve_profile.py
==================
Find the best Chrome profile to use.
Order of fallback:
1. CHROME_PROFILE_NAME from config (.path-config.json)
2. Any existing profile in CHROME_USER_DATA_DIR
3. None (default / non-logged-in state)

Usage:
    python resolve_profile.py                  # print discovered result
    python resolve_profile.py --launch         # launch Chrome headless
    python resolve_profile.py --launch-headed  # launch Chrome with UI
"""
import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config_loader import load_config, paths, get


def list_profiles(user_data_dir: Path) -> list:
    """List all available Chrome profiles (Default + Profile N + named)."""
    if not user_data_dir.exists():
        return []
    profiles = []
    for entry in user_data_dir.iterdir():
        if entry.is_dir() and (entry / "Preferences").exists():
            profiles.append(entry.name)
    return sorted(profiles)


def cdp_alive(port: int, timeout: float = 2.0) -> bool:
    """Check if a CDP server is alive on the given port."""
    try:
        with urllib.request.urlopen(
            f"http://localhost:{port}/json/version", timeout=timeout
        ) as r:
            data = json.loads(r.read())
        return bool(data.get("webSocketDebuggerUrl"))
    except Exception:
        return False


def launch_chrome(
    chrome_exe: Path,
    user_data_dir: Path,
    profile_name: str | None,
    port: int,
    headless: bool,
    wait_seconds: int = 5,
    fallback_to_tmp: bool = True,
) -> bool:
    """Launch Chrome with CDP enabled. Falls back to tmp profile if locked."""
    if cdp_alive(port):
        print(f"[INFO] CDP already running on port {port}")
        return True

    if not chrome_exe.exists():
        print(f"[ERROR] Chrome not found: {chrome_exe}")
        return False

    user_data_dir = Path(user_data_dir)
    user_data_dir.mkdir(parents=True, exist_ok=True)
    args = [
        str(chrome_exe),
        f"--remote-debugging-port={port}",
        f"--user-data-dir={user_data_dir}",
        "--remote-allow-origins=*",
    ]
    if profile_name:
        args.append(f"--profile-directory={profile_name}")
    if headless:
        args.append("--headless=new")
    args.extend([
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-background-timer-throttling",
        "--disable-features=IsolateOrigins,site-per-process",
    ])

    print(f"[INFO] Launching Chrome (profile={profile_name})...")
    p = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    pid = p.pid

    # Wait for CDP to come alive
    for i in range(wait_seconds * 2):
        if cdp_alive(port):
            print(f"[OK] CDP ready on port {port}")
            return True
        time.sleep(0.5)

    # CDP didn't come alive - try fallback to tmp profile
    if fallback_to_tmp:
        print(f"[WARN] Chrome with profile {profile_name} failed; retrying with tmp profile...")
        try:
            p.kill()
        except Exception:
            pass
        import tempfile
        tmp_dir = tempfile.mkdtemp(prefix='chrome_x2_')
        args2 = [
            str(chrome_exe),
            f"--remote-debugging-port={port}",
            f"--user-data-dir={tmp_dir}",
            "--remote-allow-origins=*",
            "--headless=new",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-gpu",
            "--no-sandbox",
        ]
        subprocess.Popen(args2, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for i in range(wait_seconds * 2):
            if cdp_alive(port):
                print(f"[OK] CDP ready on port {port} (tmp profile)")
                return True
            time.sleep(0.5)
    print(f"[ERROR] Chrome did not start within {wait_seconds}s")
    return False


def resolve(cfg: dict) -> dict:
    """Resolve the best profile path."""
    p = paths(cfg)
    requested = cfg.get("CHROME_PROFILE_NAME")
    user_data_dir = p["chrome_user_data"]
    profiles = list_profiles(user_data_dir)

    chosen = None
    fallback_reason = None

    # 1. Try requested profile
    if requested and (user_data_dir / requested).exists():
        chosen = requested
    else:
        # 2. Fallback: any existing profile
        # Prefer "Default" first, then "Profile 1", etc.
        if "Default" in profiles:
            chosen = "Default"
            fallback_reason = f"Requested '{requested}' not found; using Default"
        elif profiles:
            chosen = profiles[0]
            fallback_reason = f"Requested '{requested}' not found; using {profiles[0]}"

    # 3. None found → empty (caller decides)
    return {
        "user_data_dir": str(user_data_dir),
        "profile_name": chosen,
        "requested_profile": requested,
        "available_profiles": profiles,
        "fallback_reason": fallback_reason,
        "logged_in_likely": bool(chosen),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--launch", action="store_true", help="Launch Chrome with CDP")
    parser.add_argument("--launch-headed", action="store_true", help="Launch Chrome with UI")
    parser.add_argument("--port", type=int, default=None, help="CDP port override")
    parser.add_argument("--status", action="store_true", help="Just print status")
    args = parser.parse_args()

    cfg = load_config()
    port = args.port or cfg["CDP_PORT"]
    headless = not args.launch_headed

    info = resolve(cfg)
    print(json.dumps(info, indent=2, ensure_ascii=False))

    if args.status:
        print(f"CDP port {port}: {'ALIVE' if cdp_alive(port) else 'DOWN'}")
        return

    if args.launch or args.launch_headed:
        p = paths(cfg)
        ok = launch_chrome(
            chrome_exe=p["chrome_exe"],
            user_data_dir=Path(info["user_data_dir"]),
            profile_name=info["profile_name"],
            port=port,
            headless=headless,
            wait_seconds=cfg.get("CDP_START_WAIT", 5),
        )
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
