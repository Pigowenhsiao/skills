"""
youtube_handler.py — YouTube Source Processing
==============================================
Handles YouTube video metadata extraction, transcript fetching,
and source-completeness validation.

Requires: requests (pip install requests)
"""
from __future__ import annotations

import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional
import hashlib

try:
    import requests
    _REQUESTS_OK = True
except ImportError:
    _REQUESTS_OK = False


# ── Dataclasses ──────────────────────────────────────────

@dataclass
class YouTubeMetadata:
    video_id: str
    title: str
    channel: str
    channel_id: Optional[str] = None
    duration: Optional[str] = None  # ISO 8601 or HH:MM:SS
    thumbnail: Optional[str] = None
    view_count: Optional[int] = None
    published_at: Optional[str] = None
    description_snippet: Optional[str] = None
    lcz_me_url: Optional[str] = None
    url: str = ""
    
    def to_frontmatter_dict(self) -> dict:
        """Convert to frontmatter-compatible dict."""
        data = {
            "video_id": self.video_id,
            "source_url": self.url,
            "channel": self.channel,
            "source-completeness": "description-only",
            "transcribed": False,
        }
        if self.thumbnail:
            data["thumbnail"] = self.thumbnail
        if self.duration:
            data["duration"] = self.duration
        if self.lcz_me_url:
            data["lcz_me_url"] = self.lcz_me_url
        return data


@dataclass 
class TranscriptResult:
    source_type: str  # "lcz_me" | "whisper" | "youtube_caption" | "none"
    content: str
    language: Optional[str] = "zh"
    confidence: float = 1.0
    source_url: Optional[str] = None


# ── URL Parsing ──────────────────────────────────────────

YOUTUBE_PATTERNS = [
    re.compile(r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)([a-zA-Z0-9_-]{11})"),
    re.compile(r"youtube\.com/embed/([a-zA-Z0-9_-]{11})"),
]

LCZ_ME_PATTERN = re.compile(r"lcz\.me/topic/(\d+)")

# ── oEmbed (no API key needed) ───────────────────────────

_OEMBED_URL = "https://www.youtube.com/oembed?url={url}&format=json"
_USER_AGENT = "Mozilla/5.0 (compatible; llm-wiki-bot/1.0)"


def extract_video_id(url: str) -> Optional[str]:
    """Extract 11-char YouTube video ID from URL."""
    for pattern in YOUTUBE_PATTERNS:
        m = pattern.search(url)
        if m:
            return m.group(1)
    return None


def extract_lcz_me_id(url: str) -> Optional[str]:
    """Extract lcz.me topic ID from URL."""
    m = LCZ_ME_PATTERN.search(url)
    return m.group(1) if m else None


def fetch_youtube_metadata(url: str, timeout: int = 10) -> Optional[YouTubeMetadata]:
    """
    Fetch YouTube video metadata via oEmbed API.
    No API key required. Falls back gracefully on network errors.
    
    Args:
        url: YouTube video URL
        timeout: HTTP timeout in seconds
    
    Returns:
        YouTubeMetadata or None on failure
    """
    if not _REQUESTS_OK:
        return None
    
    video_id = extract_video_id(url)
    if not video_id:
        return None
    
    oembed_url = _OEMBED_URL.format(url=url)
    
    try:
        resp = requests.get(oembed_url, timeout=timeout,
                           headers={"User-Agent": _USER_AGENT})
        resp.raise_for_status()
        data = resp.json()
        
        # Try to build lcz.me URL from video_id
        lcz_url = None
        
        # Check if lcz URL is known (stored in local cache or derived)
        # lcz.me/topic/{numeric_id} — we can't derive this from video_id
        
        return YouTubeMetadata(
            video_id=video_id,
            title=data.get("title", "Unknown"),
            channel=data.get("author_name", "Unknown"),
            channel_id=data.get("author_url", ""),
            thumbnail=f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
            url=url,
            lcz_me_url=lcz_url,
        )
    except Exception:
        return None


def fetch_lcz_me_transcript(url: str, timeout: int = 15) -> Optional[str]:
    """
    Attempt to fetch transcript/text from lcz.me topic page.
    
    lcz.me is a community transcript aggregator for Chinese-language YouTube.
    This scrapes the visible text content from the topic page.
    
    Args:
        url: lcz.me topic URL (e.g. https://lcz.me/topic/1187)
        timeout: HTTP timeout in seconds
    
    Returns:
        Transcript text or None on failure
    """
    if not _REQUESTS_OK:
        return None
    
    topic_id = extract_lcz_me_id(url)
    if not topic_id:
        return None
    
    try:
        resp = requests.get(url, timeout=timeout,
                           headers={
                               "User-Agent": _USER_AGENT,
                               "Accept": "text/html,application/xhtml+xml",
                           })
        resp.raise_for_status()
        html = resp.text
        
        # Extract text content from lcz.me HTML
        # Strategy: find article/content div and extract paragraphs
        content_parts = []
        
        # Common lcz.me content selectors (best-effort)
        # The actual page structure may vary; this is a heuristic approach
        for pattern in [
            r'<div class="content">(.+?)</div>',
            r'<article[^>]*>(.+?)</article>',
            r'<div class="post-content">(.+?)</div>',
        ]:
            m = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
            if m:
                raw = m.group(1)
                # Strip tags, keep text
                text = re.sub(r'<[^>]+>', ' ', raw)
                text = re.sub(r'\s+', ' ', text).strip()
                if len(text) > 100:
                    content_parts.append(text)
        
        if content_parts:
            return content_parts[0][:50000]  # Cap at 50K chars
        
        # Fallback: extract all paragraph text
        paragraphs = re.findall(r'<p[^>]*>([^<]+)</p>', html)
        if paragraphs:
            text = " ".join(p.strip() for p in paragraphs if len(p.strip()) > 20)
            return text[:50000] if text else None
        
        return None
        
    except Exception:
        return None


def fetch_youtube_caption(url: str, timeout: int = 15) -> Optional[str]:
    """
    Attempt to fetch auto-generated captions from YouTube.
    Uses a third-party caption extraction service (youtubesubtitles.com API).
    This is a best-effort approach — may fail due to geo-blocking or captions.
    
    Args:
        url: YouTube video URL
        timeout: HTTP timeout in seconds
    
    Returns:
        Caption transcript or None
    """
    if not _REQUESTS_OK:
        return None
    
    video_id = extract_video_id(url)
    if not video_id:
        return None
    
    # Try youtubesubtitles.com API (free tier)
    try:
        api_url = f"https://youtubesubtitles.com/api/v1/captions?video_id={video_id}"
        resp = requests.get(api_url, timeout=timeout,
                           headers={"User-Agent": _USER_AGENT})
        if resp.status_code == 200:
            data = resp.json()
            if data.get("success") and data.get("data"):
                return data["data"].get("text", "")
    except Exception:
        pass
    
    return None


def fetch_transcript(url: str, prefer_lcz_me: bool = True) -> TranscriptResult:
    """
    Fetch transcript using the best available source.
    Priority: lcz.me → YouTube captions → whisper (manual)
    
    Args:
        url: YouTube URL or lcz.me URL
        prefer_lcz_me: Try lcz.me first for Chinese content
    
    Returns:
        TranscriptResult with source_type, content, language
    """
    # If already a lcz.me URL
    if "lcz.me" in url:
        content = fetch_lcz_me_transcript(url)
        if content:
            return TranscriptResult(
                source_type="lcz_me",
                content=content,
                language="zh",
                confidence=0.9,
                source_url=url,
            )
        return TranscriptResult(source_type="none", content="")
    
    # YouTube URL — try lcz.me first if Chinese content suspected
    video_id = extract_video_id(url)
    if not video_id:
        return TranscriptResult(source_type="none", content="")
    
    if prefer_lcz_me:
        # Try to find lcz.me link (would need page scrape or cached lookup)
        # For now, try direct caption fetch
        caption = fetch_youtube_caption(url)
        if caption:
            return TranscriptResult(
                source_type="youtube_caption",
                content=caption,
                language="auto",
                confidence=0.7,
            )
    
    return TranscriptResult(source_type="none", content="")


# ── Completeness Checking ────────────────────────────────

COMPLETENESS_LEVELS = {
    "L1": {"transcribed": True, "source_completeness": None},
    "L2a": {"transcribed": False, "source_completeness": "full-transcript"},
    "L2b": {"transcribed": False, "source_completeness": "external-transcript"},
    "L3": {"transcribed": False, "source_completeness": "description-only"},
}

FRONTMATTER_TRANSCRIBED_TRUE = {"true", "yes", "1"}
FRONTMATTER_COMPLETENESS_FULL = {"full-transcript", "full_transcript", "transcript", "full"}
FRONTMATTER_COMPLETENESS_EXTERNAL = {"external-transcript", "external_transcript", "external"}


def parse_youtube_frontmatter(frontmatter_text: str) -> dict:
    """Parse YouTube-specific frontmatter fields."""
    fm = {}
    current_key = None
    multiline_buffer = []
    
    for raw_line in frontmatter_text.splitlines():
        stripped = raw_line.strip()
        
        # List item continuation
        if raw_line.startswith("    ") or raw_line.startswith("\t"):
            if current_key and isinstance(fm.get(current_key), list):
                fm[current_key].append(stripped.lstrip("- \t"))
            continue
        
        if ":" not in stripped:
            continue
        
        key, _, val = stripped.partition(":")
        key = key.strip()
        val = val.strip()
        
        if val == "" or val.startswith("- "):
            # Empty or list start
            fm[key] = []
            current_key = key
        else:
            fm[key] = val.strip('"')
            current_key = key
    
    return fm


def check_youtube_completeness(filepath: Path) -> dict:
    """
    Check YouTube note's transcription completeness level.
    
    Returns:
        {
            "level": "L1"|"L2"|"L3",
            "status": "complete"|"incomplete",
            "transcribed": bool,
            "source_completeness": str,
            "stale_days": Optional[int],
            "lcz_me_valid": Optional[bool],
            "notes": list[str],
        }
    """
    try:
        raw = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {"level": "L3", "status": "incomplete", "error": str(Exception)}
    
    # Extract frontmatter
    fm_text_match = re.search(r"^---\s*\n(.*?)\n---", raw, re.DOTALL)
    if not fm_text_match:
        return {"level": "L3", "status": "incomplete", "notes": ["No frontmatter found"]}
    
    fm_text = fm_text_match.group(1)
    fm = parse_youtube_frontmatter(fm_text)
    
    # Normalize
    transcribed_raw = fm.get("transcribed", "false")
    transcribed = transcribed_raw.lower().strip('"') in FRONTMATTER_TRANSCRIBED_TRUE
    
    completeness_raw = fm.get("source-completeness", "description-only")
    completeness = completeness_raw.lower().strip('"')
    
    # Determine level
    if transcribed:
        level = "L1"
        status = "complete"
    elif completeness in FRONTMATTER_COMPLETENESS_FULL:
        level = "L2"
        status = "complete"
    elif completeness in FRONTMATTER_COMPLETENESS_EXTERNAL:
        level = "L2"
        status = "complete"
    else:
        level = "L3"
        status = "incomplete"
    
    # Check staleness
    stale_days: Optional[int] = None
    created_raw = fm.get("created", "")
    if created_raw:
        try:
            utc8 = timezone(timedelta(hours=8))
            if "T" in created_raw:
                created_dt = datetime.fromisoformat(created_raw.replace("Z", "+00:00"))
            else:
                created_dt = datetime.strptime(
                    created_raw, "%Y-%m-%d"
                ).replace(tzinfo=utc8)
            now = datetime.now(utc8)
            stale_days = (now - created_dt).days
        except Exception:
            stale_days = None
    
    # Validate lcz.me link if present
    lcz_me_valid = None
    lcz_url = fm.get("lcz_me_url") or fm.get("lcz_url", "")
    if lcz_url and "lcz.me" in str(lcz_url):
        result = fetch_lcz_me_transcript(lcz_url, timeout=5)
        lcz_me_valid = result is not None and len(result) > 100
    
    notes = []
    if level == "L3" and stale_days and stale_days > 7:
        notes.append(f"L3 note is {stale_days} days old — consider upgrading to L1/L2")
    if level == "L2" and lcz_me_valid is False:
        notes.append("lcz.me link present but content is inaccessible")
    
    return {
        "level": level,
        "status": status,
        "transcribed": transcribed,
        "source_completeness": completeness,
        "stale_days": stale_days,
        "lcz_me_valid": lcz_me_valid,
        "notes": notes,
        "created": created_raw,
    }


def compute_content_hash(text: str) -> str:
    """Compute SHA256 hash of content."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_youtube_note_content(
    metadata: YouTubeMetadata,
    transcript: Optional[str] = None,
    summary_sections: Optional[str] = None,
) -> str:
    """
    Build the body of a YouTube note.
    
    Args:
        metadata: YouTubeMetadata object
        transcript: Optional transcript text
        summary_sections: Optional AI-generated summary sections
    
    Returns:
        Markdown body string
    """
    lines = [
        f"**影片標題**：{metadata.title}",
        f"**頻道**：{metadata.channel}",
        f"**影片連結**：{metadata.url}",
    ]
    
    if metadata.thumbnail:
        lines.append(f"**縮圖**：{metadata.thumbnail}")
    if metadata.lcz_me_url:
        lines.append(f"**文稿與圖片**：{metadata.lcz_me_url}")
    
    lines.append("\n---\n")
    
    if summary_sections:
        lines.append(summary_sections)
    else:
        lines.append("## 重點摘要\n\n_待填寫_\n")
    
    if transcript:
        lines.append("\n---\n\n## 完整文稿\n\n")
        lines.append(f"```text\n{transcript[:49000]}\n```\n")
    
    return "\n".join(lines)
