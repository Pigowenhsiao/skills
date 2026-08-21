"""
Load cookies for X/Twitter CDP injection.

Auto-detects and parses Chrome cookies from JSON and Netscape formats.
Filters to x.com/twitter.com domains only.
Outputs in CDP Network.setCookies format: name, value, domain, path, secure.

Standard library only.
"""

import json
import os
from pathlib import Path
from typing import Optional


# Chrome cookie database paths (Windows)
CHROME_JSON_PATHS = [
    # Primary JSON cookies location (Windows)
    Path(os.environ.get("LOCALAPPDATA", "")) / "Google/Chrome/User Data/Default/Network/Cookies",
    # Fallback to Default profile
    Path.home() / "AppData/Local/Google/Chrome/User Data/Default/Network/Cookies",
    # Profile-specific paths
    Path.home() / "AppData/Local/Google/Chrome/User Data/Profile 1/Network/Cookies",
    Path.home() / "AppData/Local/Google/Chrome/User Data/Profile 2/Network/Cookies",
]

# Netscape format cookie files (common for browser extensions, curl, etc.)
NETSCAPE_PATHS = [
    # Standard locations
    Path.home() / "Downloads/x_cookies_logged_in.json",
    Path.home() / "Downloads/cookies_netscape.txt",
    Path.home() / "Downloads/cookies.txt",
    Path.home() / ".cookies",
    # Current working directory fallback
    Path.cwd() / "x_cookies_logged_in.json",
    Path.cwd() / "cookies_netscape.txt",
]

import re

# Regex patterns for proper domain boundary matching
TARGET_DOMAIN_PATTERNS = [
    re.compile(r'^(x\.com|twitter\.com)$', re.IGNORECASE),
    re.compile(r'\.(x\.com|twitter\.com)$', re.IGNORECASE),
]


def is_target_domain(domain: str) -> bool:
    """Check if domain matches x.com or twitter.com (with boundary check)."""
    if not domain:
        return False
    domain_lower = domain.lower()
    for pattern in TARGET_DOMAIN_PATTERNS:
        if pattern.search(domain_lower):
            return True
    return False


def parse_chrome_json(content: str) -> list[dict]:
    """
    Parse Chrome cookies from JSON format.
    
    Chrome JSON cookies typically have fields like:
    - name, value, domain, path, expires_sec, is_secure, etc.
    
    Returns list of cookie dicts in CDP format.
    """
    cookies = []
    try:
        data = json.loads(content)
        
        # Handle array of cookies directly
        if isinstance(data, list):
            cookie_items = data
        # Handle object with cookies array
        elif isinstance(data, dict):
            cookie_items = data.get("cookies", data.get("Cookie", data))
        else:
            return cookies
        
        for item in cookie_items:
            if not isinstance(item, dict):
                continue
            
            # Extract domain - Chrome JSON may use 'domain' or 'host'
            domain = item.get("domain", item.get("host", ""))
            
            # Filter to target domains
            if not is_target_domain(domain):
                continue
            
            cookie = {
                "name": item.get("name", item.get("key", "")),
                "value": item.get("value", item.get("content", "")),
                "domain": domain.lstrip(".") if domain else "",
                "path": item.get("path", "/"),
                "secure": bool(item.get("is_secure", item.get("secure", True))),
            }
            
            # Add optional fields if present
            if "expires" in item:
                cookie["expires"] = item["expires"]
            elif "expires_sec" in item:
                cookie["expires"] = item["expires_sec"]
            
            if cookie["name"] and cookie["domain"]:
                cookies.append(cookie)
                
    except json.JSONDecodeError as e:
        print(f"Failed to parse Chrome JSON cookies: {e}")
    
    return cookies


def parse_netscape(content: str) -> list[dict]:
    """
    Parse cookies from Netscape/Mozilla format.
    
    Netscape format has header line: # Netscape HTTP Cookie File
    Then tab-separated fields: domain, flag, path, secure, expires, name, value
    
    Returns list of cookie dicts in CDP format.
    """
    cookies = []
    lines = content.strip().split("\n")
    
    for line in lines:
        line = line.strip()
        
        # Skip comments and empty lines
        if not line or line.startswith("#"):
            continue
        
        parts = line.split("\t")
        if len(parts) < 7:
            continue
        
        domain, flag, path, secure_str, expires, name, value = parts[:7]
        
        # Filter to target domains
        if not is_target_domain(domain):
            continue
        
        cookie = {
            "name": name,
            "value": value,
            "domain": domain.lstrip(".") if domain else "",
            "path": path,
            "secure": secure_str.lower() in ("true", "1", "yes"),
        }
        
        # Add expiration if present and valid
        if expires and expires.isdigit():
            cookie["expires"] = int(expires)
        
        if cookie["name"] and cookie["domain"]:
            cookies.append(cookie)
    
    return cookies


def get_preferred_cookie_file() -> Optional[tuple[Path, str]]:
    """
    Find the first available cookie file and detect its format.
    
    Returns:
        Tuple of (Path, format_type) where format_type is 'json' or 'netscape'
        Returns None if no cookie file found.
    """
    # Check Chrome JSON paths
    for path in CHROME_JSON_PATHS:
        if path.exists() and path.is_file():
            return (path, "json")
    
    # Check Netscape format paths
    for path in NETSCAPE_PATHS:
        if path.exists() and path.is_file():
            # Detect format by content
            try:
                content = path.read_text(encoding="utf-8").strip()
                if not content:
                    continue
                    
                # Check if it's JSON (starts with { or [)
                if content.startswith(("{", "[")):
                    return (path, "json")
                # Otherwise treat as netscape format
                return (path, "netscape")
            except (UnicodeDecodeError, OSError):
                continue
    
    return None


def load_cookies(
    cookie_file: Optional[Path] = None,
    domain_filter: bool = True,
) -> list[dict]:
    """
    Load cookies for CDP injection.
    
    Args:
        cookie_file: Optional specific cookie file path.
                    If None, auto-detects from standard locations.
        domain_filter: If True, filter to x.com/twitter.com domains only.
    
    Returns:
        List of cookie dicts in CDP Network.setCookies format:
        {name, value, domain, path, secure, expires?}
    """
    cookies = []
    source_file = cookie_file
    file_format = None
    
    if source_file:
        # Unpack tuple if passed from get_preferred_cookie_file()
        if isinstance(source_file, tuple):
            source_file, file_format = source_file
        # Convert string to Path
        if isinstance(source_file, str):
            source_file = Path(source_file)
        # Use specified file
        if source_file.exists() and source_file.is_file():
            try:
                content = source_file.read_text(encoding="utf-8")
                if content.strip().startswith(("{")):
                    file_format = "json"
                else:
                    file_format = "netscape"
            except (UnicodeDecodeError, OSError) as e:
                print(f"Failed to read cookie file {source_file}: {e}")
                return cookies
        else:
            print(f"Cookie file not found: {source_file}")
            return cookies
    else:
        # Auto-detect
        result = get_preferred_cookie_file()
        if result:
            source_file, file_format = result
            try:
                content = source_file.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError) as e:
                print(f"Failed to read cookie file {source_file}: {e}")
                return cookies
        else:
            print("No cookie file found in standard locations:")
            print("  Chrome JSON:", [str(p) for p in CHROME_JSON_PATHS[:2]])
            print("  Netscape:", [str(p) for p in NETSCAPE_PATHS[:3]])
            return cookies
    
    print(f"Loading cookies from: {source_file} (format: {file_format})")
    
    # Parse based on detected format
    if file_format == "json":
        cookies = parse_chrome_json(content)
    else:
        cookies = parse_netscape(content)
    
    # Apply domain filter if requested
    if domain_filter:
        original_count = len(cookies)
        cookies = [c for c in cookies if is_target_domain(c.get("domain", ""))]
        print(f"Filtered {original_count} -> {len(cookies)} cookies for x.com/twitter.com")
    else:
        print(f"Loaded {len(cookies)} cookies (no domain filter)")
    
    return cookies


def get_cdp_cookies(cookie_file: Optional[Path] = None) -> list[dict]:
    """
    Convenience function to get cookies formatted for CDP Network.setCookies.
    
    This is the main entry point for CDP injection.
    """
    return load_cookies(cookie_file=cookie_file, domain_filter=True)


if __name__ == "__main__":
    # Demo: show what would be loaded
    print("=" * 60)
    print("X/Twitter Cookie Loader for CDP")
    print("=" * 60)
    
    cookies = load_cookies()
    
    if cookies:
        print(f"\nTotal cookies: {len(cookies)}")
        print("\nSample cookies (first 3):")
        for c in cookies[:3]:
            print(f"  {c['domain']}: {c['name']}={c['value'][:20]}...")
        
        print("\nCDP format ready:")
        print(f"  Network.setCookies([")
        for c in cookies:
            print(f"    {c},")
        print(f"  ])")
    else:
        print("\nNo cookies found. Please ensure:")
        print("  1. Chrome is logged into x.com")
        print("  2. Export cookies to Downloads/x_cookies_logged_in.json")
