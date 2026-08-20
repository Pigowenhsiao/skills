"""
curator.py
==========
LLM-based curator for x-note notes.

Generates Traditional Chinese (zh-TW) prose for the analysis sections of each
x-note: Core Summary, Key Points, Why It Matters.

Also provides:
- score_and_classify(): MiniMax-M3 semantic scoring + Vault classification
- validate_note_with_llm(): MiniMax-M3 inline note validation

Endpoint: https://api.minimax.io/anthropic/v1/messages
Auth: x-api-key header (NOT Authorization: Bearer)
Reference: https://platform.minimax.io/docs/api-reference/text-chat-anthropic

API key resolution order (2026-08-09):
1. .path-config.json MINIMAX_API_KEY
2. ~/Documents/.env MINIMAX_API_KEY="..."
3. env var MINIMAX_API_KEY
4. ~/.pi/agent/auth.json (minimax or MiniMax.key)

When the API call fails or returns empty, callers MUST fail loud
(write_to_inbox.py does this) — no heuristic fallback is provided here.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

API_URL_DEFAULT = "https://api.minimax.io/anthropic/v1/messages"
CACHE_DIR = Path.home() / ".cache" / "x-note-curator"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
CURATOR_TIMEOUT = 60
MAX_HTTP_RETRIES = 2

# Placeholder / fallback text patterns. ANY match means curator did not run.
# Used by validate_note.py to reject placeholder notes.
PLACEHOLDER_PATTERNS = (
    "未在沒有翻譯證據時",
    "本筆記只整理來源可確認",
    "此筆記只代表單篇 X 貼文",
    "摘要僅依本次完整來源內容整理",
    "本次未在沒有翻譯證據時改寫原文",
    "完整來源文字保留於",
    "(auto-generated; check text below)",
    "(auto-generated",
    "待補",
    "todo",
)

# Vault classification mapping — MiniMax-M3 maps content to these keys
CLASSIFICATION_MAP = {
    "prompt-engineering": "08-Learning/03_Prompt-Context-Engineering",
    "prompt": "08-Learning/03_Prompt-Context-Engineering",
    "agent": "08-Learning/04_AI-Agents",
    "ai-agent": "08-Learning/04_AI-Agents",
    "code": "08-Learning/01_AI-Agent",
    "developer": "08-Learning/01_AI-Agent",
    "tool": "08-Learning/05_Tool-Use",
    "mcp": "08-Learning/06_Tool-Use/MCP",
    "business": "01-Daily/03_Business",
    "startup": "01-Daily/03_Business",
    "finance": "01-Daily/02_Finance",
    "macro": "01-Daily/02_Finance",
    "stock": "01-Daily/02_Finance",
    "crypto": "01-Daily/02_Finance",
    "science": "08-Learning/02_AI-Research",
    "research": "08-Learning/02_AI-Research",
    "biology": "08-Learning/02_AI-Research",
    "design": "08-Learning/07_Design-Media",
    "media": "08-Learning/07_Design-Media",
    "llm": "01-Daily/01_AI",
    "news": "01-Daily/01_AI",
    "opinion": "01-Daily/01_AI",
    "uncategorized": "08-Learning/99_Uncategorized",
}

DEFAULT_CLASSIFICATION = "01-Daily/01_AI"


# ─────────────────────────────────────────────────────────────────────────────
# Low-level API helpers
# ─────────────────────────────────────────────────────────────────────────────

def _strip_codeblock_wrappers(text_resp: str) -> str:
    text_resp = text_resp.strip()
    if text_resp.startswith("```markdown"):
        text_resp = text_resp[11:].strip()
    if text_resp.endswith("```"):
        text_resp = text_resp[:-3].strip()
    return text_resp


def strip_thinking_blocks(text: str) -> str:
    import re
    text = re.sub(r"<thinking>.*?</thinking>", "", text, flags=re.DOTALL)
    text = re.sub(r"\[TOKENS_THINKING\].*?\[/TOKENS_THINKING\]", "", text, flags=re.DOTALL)
    return text.strip()


# Known MiniMax-M3 Chinese-character corruption patterns.
# These appear when the API returns invalid UTF-8 byte sequences for common
# Traditional Chinese characters embedded in otherwise-correct text.
_CORRUPTION_MAP = {
    # Traditional Chinese character corruption (� = U+FFFD replacement char)
    "圍\ufffd著": "圍繞",       # 圍 + 壞字 → 圍繞
    "追\ufffd、": "追蹤、",    # 追 + 壞字 → 追蹤
    "圍\ufffd著它": "圍繞它",  # 圍 + 壞字 → 圍繞 (variant)
}

def _clean_corruption(text: str) -> str:
    """Fix known MiniMax-M3 Chinese-character corruption.

    MiniMax-M3 sometimes emits U+FFFD (replacement char) inside otherwise-
    correct Traditional Chinese text.  This replaces known pairs with the
    correct characters.
    """
    if "\ufffd" not in text:
        return text
    for broken, fixed in _CORRUPTION_MAP.items():
        text = text.replace(broken, fixed)
    return text


def _to_traditional(value: str) -> str:
    """Normalize generated prose to Taiwan Traditional Chinese."""
    try:
        from opencc import OpenCC
        return OpenCC("s2twp").convert(value or "")
    except Exception:
        return value or ""


def _api_call(payload: dict, api_key: str, api_url: str = API_URL_DEFAULT) -> str:
    """Make one MiniMax API call, return response text or empty string on failure."""
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
    }
    last_err = None
    for attempt in range(1, MAX_HTTP_RETRIES + 1):
        try:
            req = urllib.request.Request(
                api_url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=CURATOR_TIMEOUT) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            content = result.get("content", [])
            text_parts = []
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text_parts.append(block.get("text", ""))
            body = _strip_codeblock_wrappers(strip_thinking_blocks("\n".join(text_parts)))
            if body:
                return body
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            last_err = f"attempt {attempt}: {type(e).__name__}: {e}"
            time.sleep(1)
        except Exception as e:
            last_err = f"attempt {attempt}: {type(e).__name__}: {e}"
            break
    print(f"[ERROR] API call failed: {last_err}")
    return ""


def load_api_key(cfg: dict | None = None) -> str:
    """Resolve API key from .path-config.json → ~/Documents/.env → ~/.pi/agent/auth.json."""
    if cfg and cfg.get("MINIMAX_API_KEY"):
        return cfg["MINIMAX_API_KEY"]

    env_file = Path.home() / "Documents" / ".env"
    if env_file.exists():
        try:
            for line in env_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("MINIMAX_API_KEY"):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if key:
                        return key
        except Exception:
            pass

    env_key = os.environ.get("MINIMAX_API_KEY") or os.environ.get("minimax")
    if env_key:
        return env_key

    auth_path = Path.home() / ".pi" / "agent" / "auth.json"
    if auth_path.exists():
        try:
            auth = json.loads(auth_path.read_text(encoding="utf-8"))
            return (
                auth.get("minimax", {}).get("key")
                or auth.get("MiniMax", {}).get("key")
                or ""
            )
        except Exception:
            return ""
    return ""


# ─────────────────────────────────────────────────────────────────────────────
# Fix #1: MiniMax-M3 semantic scoring
# ─────────────────────────────────────────────────────────────────────────────

def score_post_with_llm(
    text: str,
    handle: str,
    author_display: str,
    likes: int = 0,
    reposts: int = 0,
    replies: int = 0,
    views: int = 0,
    api_key: str | None = None,
    cfg: dict | None = None,
) -> dict:
    """
    MiniMax-M3 semantic scoring + content type detection.

    Returns:
        {
            "score": float,           # 0-10
            "reasoning": str,          # why this score
            "content_type": str,       # prompt|workflow|case|study|news|opinion|tool|...
            "usefulness": str,         # high|medium|low
            "tags": list[str],
            "keep": bool,              # score >= threshold (6.5)
            "raw_response": str,       # original LLM text (for debugging)
        }
    """
    if api_key is None:
        api_key = load_api_key(cfg)

    if not api_key:
        return _fallback_rule_score(text, likes)

    # Cache by content_hash to avoid re-scoring identical posts
    cache_key = hashlib.sha256(
        f"score|{handle}|{likes}|{text}".encode("utf-8")
    ).hexdigest()[:32]
    cache_file = CACHE_DIR / f"score_{cache_key}.json"
    if cache_file.exists():
        try:
            cached = json.loads(cache_file.read_text(encoding="utf-8"))
            if cached:
                return cached
        except Exception:
            pass

    system_prompt = (
        "你是一個 X 推文品質評分員。\n"
        "根據推文的實用性、內容深度、資訊密度、可重複利用性，評分 0-10。\n"
        "評分標準：\n"
        "  10: 含完整 Prompt / Code / Workflow，可直接複製使用，且有深度\n"
        "  9:  有具體工具/方法論/案例，含具體數據或實作細節\n"
        "  8:  有價值的乾貨內容，分析或介紹有深度\n"
        "  7:  有用的資訊，總結或分析有價值\n"
        "  6:  內容有价值但较简短或较一般\n"
        "  5:  一般内容，缺乏深度\n"
        "  4:  较泛泛，缺乏具体内容\n"
        "  3:  纯情绪抒发或闲聊\n"
        "  2:  几乎无实质内容\n"
        "  1:  纯感言/表情/打招呼\n"
        "  0:  垃圾/广告/完全无价值\n"
        "你的回應必須是 JSON 格式，不要多餘文字：\n"
        '  {"score": 8.5, "reasoning": "...", "content_type": "workflow", '
        '"usefulness": "high", "tags": ["AI", "workflow"], "keep": true}'
    )

    user_prompt = f"""評分以下 X 推文。

作者：{author_display} (@{handle})
互動：{likes} likes / {reposts} reposts / {replies} replies / {views} views
字數：{len(text)}

推文內容：
\"\"\"
{text}
\"\"\"

回應嚴格 JSON，無其他文字：
"""

    payload = {
        "model": "MiniMax-M3",
        "max_tokens": 1024,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_prompt}],
    }

    raw = _api_call(payload, api_key)

    # Parse JSON response
    result = _parse_json_response(raw)
    if result:
        result["keep"] = result.get("score", 0) >= 6.5
        result["raw_response"] = raw
        # Cache
        try:
            cache_file.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass
        return result

    # Fallback on parse failure
    print(f"[WARN] score_post_with_llm: failed to parse response, using rule fallback")
    return _fallback_rule_score(text, likes)


def _fallback_rule_score(text: str, likes: int = 0) -> dict:
    """Rule-based fallback when LLM call fails."""
    import re
    L = len(text)
    score = 5.0
    reasons = []

    CHAT_PATTERNS = [r"^(rt|via @)", r"^(good morning|happy|thanks|thx|ty|great)[\.\!]*$",
                     r"^(lol|lmao|haha|😂|👍|🎉)+$"]
    SPAM_PATTERNS = [r"\b(airdrop|giveaway|free \$|claim now)\b",
                      r"\b(dm me|join my|sign up)\b"]

    t = text.strip()
    if any(re.match(p, t, re.I) for p in CHAT_PATTERNS):
        return {"score": 0.5, "reasoning": "chat-only/emoji/thanks", "content_type": "chat",
                "usefulness": "low", "tags": [], "keep": False, "raw_response": ""}
    if any(re.search(p, t, re.I) for p in SPAM_PATTERNS):
        return {"score": 0.0, "reasoning": "spam/promotional", "content_type": "spam",
                "usefulness": "low", "tags": [], "keep": False, "raw_response": ""}

    if L < 30:
        return {"score": 1.0, "reasoning": f"too short ({L} chars)", "content_type": "short",
                "usefulness": "low", "tags": [], "keep": False, "raw_response": ""}
    elif L < 80:
        reasons.append(f"short ({L} chars)")
    elif L < 200:
        score += 1.0
        reasons.append("medium length")
    elif L < 500:
        score += 2.0
        reasons.append("long-form")
    else:
        score += 2.5
        reasons.append(f"long-form ({L} chars)")

    code_blocks = len(re.findall(r"```", text)) // 2
    if code_blocks > 0:
        score += 2.0
        reasons.append(f"has code blocks ({code_blocks})")

    if re.search(r"(You are|Act as|prompt|gpt|llm)", text, re.I):
        score += 2.0
        reasons.append("prompt-related")
    if re.search(r"(step\s*\d|how to|workflow|stack:)", text, re.I):
        score += 1.5
        reasons.append("workflow/how-to")
    if re.search(r"(case study|built|shipped|results|metrics)", text, re.I):
        score += 1.5
        reasons.append("case/example")

    if likes > 1000:
        score += 1.0
        reasons.append(f"high likes ({likes})")
    elif likes > 100:
        score += 0.5
        reasons.append(f"good likes ({likes})")

    score = max(0.0, min(10.0, score))
    return {
        "score": round(score, 1),
        "reasoning": " | ".join(reasons) if reasons else f"rule-based ({L} chars)",
        "content_type": "unknown",
        "usefulness": "medium" if score >= 6 else "low",
        "tags": [],
        "keep": score >= 6.5,
        "raw_response": "",
    }


# ─────────────────────────────────────────────────────────────────────────────
# Fix #2: MiniMax-M3 classification
# ─────────────────────────────────────────────────────────────────────────────

def classify_with_llm(
    text: str,
    handle: str,
    author_display: str,
    api_key: str | None = None,
    cfg: dict | None = None,
) -> dict:
    """
    MiniMax-M3 semantic classification into Vault folder path.

    Returns:
        {
            "classification": str,     # e.g. "08-Learning/03_Prompt-Context-Engineering"
            "confidence": float,       # 0-1
            "reasoning": str,           # why this classification
            "tags": list[str],          # suggested tags
            "raw_response": str,
        }
    """
    if api_key is None:
        api_key = load_api_key(cfg)

    if not api_key:
        return _fallback_rule_classify(text, handle)

    cache_key = hashlib.sha256(
        f"classify|{handle}|{text[:200]}".encode("utf-8")
    ).hexdigest()[:32]
    cache_file = CACHE_DIR / f"classify_{cache_key}.json"
    if cache_file.exists():
        try:
            cached = json.loads(cache_file.read_text(encoding="utf-8"))
            if cached:
                return cached
        except Exception:
            pass

    system_prompt = (
        "你是一個 Vault 知識庫分類專家。\n"
        "根據推文內容，將其分類到最合適的 Vault 資料夾。\n"
        "可用分類：\n"
        "  08-Learning/01_AI-Agent         — AI 程式開發、程式碼、工具介紹\n"
        "  08-Learning/02_AI-Research      — 研究論文、科學發現、技術原理\n"
        "  08-Learning/03_Prompt-Context-Engineering — Prompt 工程、LLM 技巧\n"
        "  08-Learning/04_AI-Agents        — AI Agent、自動化流程\n"
        "  08-Learning/05_Tool-Use         — 工具使用技巧\n"
        "  08-Learning/06_Tool-Use/MCP    — MCP 相關\n"
        "  08-Learning/07_Design-Media     — 設計、媒體創作\n"
        "  08-Learning/99_Uncategorized    — 未能分類\n"
        "  01-Daily/01_AI                 — 一般 AI 新聞、趨勢、觀察\n"
        "  01-Daily/02_Finance             — 金融、投資、宏觀經濟\n"
        "  01-Daily/03_Business            — 商業、創業、變現\n"
        "回應嚴格 JSON：\n"
        '  {"classification": "08-Learning/03_Prompt-Context-Engineering", '
        '"confidence": 0.92, "reasoning": "...", "tags": ["prompt", "llm"]}'
    )

    user_prompt = f"""為以下推文選擇最合適的 Vault 分類。

作者：{author_display} (@{handle})

推文內容：
\"\"\"
{text[:1000]}
\"\"\"

回應嚴格 JSON，無其他文字：
"""

    payload = {
        "model": "MiniMax-M3",
        "max_tokens": 256,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_prompt}],
    }

    raw = _api_call(payload, api_key)
    result = _parse_json_response(raw)

    if result:
        result["raw_response"] = raw
        try:
            cache_file.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass
        return result

    print(f"[WARN] classify_with_llm: failed to parse response, using rule fallback")
    return _fallback_rule_classify(text, handle)


def _fallback_rule_classify(text: str, handle: str) -> dict:
    """Keyword-based fallback classification."""
    t = text.lower()
    if any(k in t for k in ("prompt", "gpt", "llm", "claude")):
        return {"classification": "08-Learning/03_Prompt-Context-Engineering",
                "confidence": 0.6, "reasoning": "keyword fallback: prompt/LLM", "tags": [], "raw_response": ""}
    if any(k in t for k in ("code", "developer", "github", "api")):
        return {"classification": "08-Learning/01_AI-Agent",
                "confidence": 0.6, "reasoning": "keyword fallback: code/dev", "tags": [], "raw_response": ""}
    if any(k in t for k in ("business", "startup", "market", "revenue")):
        return {"classification": "01-Daily/03_Business",
                "confidence": 0.6, "reasoning": "keyword fallback: business", "tags": [], "raw_response": ""}
    if any(k in t for k in ("macro", "stock", "crypto", "btc", "finance")):
        return {"classification": "01-Daily/02_Finance",
                "confidence": 0.6, "reasoning": "keyword fallback: finance", "tags": [], "raw_response": ""}
    if any(k in t for k in ("agent", "autonomous", "automation")):
        return {"classification": "08-Learning/04_AI-Agents",
                "confidence": 0.6, "reasoning": "keyword fallback: agent", "tags": [], "raw_response": ""}
    return {"classification": DEFAULT_CLASSIFICATION,
            "confidence": 0.4, "reasoning": "keyword fallback: default", "tags": [], "raw_response": ""}


# ─────────────────────────────────────────────────────────────────────────────
# Fix #3: MiniMax-M3 inline note validation
# ─────────────────────────────────────────────────────────────────────────────

def validate_note_with_llm(
    note_text: str,
    original_post: dict,
    cfg: dict | None = None,
) -> dict:
    """
    MiniMax-M3 inline validation — replaces Subagent reviewer.

    Checks:
    - Frontmatter complete
    - Core Summary non-empty, substantive (>50 chars)
    - Key Points >= 3, each substantive (>10 chars)
    - Why It Matters non-empty
    - Reference (Complete X Post Text) present
    - No placeholder text

    Returns:
        {
            "valid": bool,
            "score": float,        # 0-100 evaluation score
            "issues": list[str],
            "passed_checks": list[str],
            "reasoning": str,
        }
    """
    api_key = load_api_key(cfg)

    if not api_key:
        # Fallback to rule-based validation
        return _fallback_validate_note(note_text, original_post)

    # Cache by content_hash of note_text
    content_hash = hashlib.sha256(note_text.encode("utf-8")).hexdigest()[:32]
    cache_file = CACHE_DIR / f"validate_{content_hash[:16]}.json"
    if cache_file.exists():
        try:
            cached = json.loads(cache_file.read_text(encoding="utf-8"))
            if cached:
                return cached
        except Exception:
            pass

    text = original_post.get("text", "")
    handle = original_post.get("handle", "?")
    author = original_post.get("author_display", "?")
    score = original_post.get("score", 0)

    system_prompt = (
        "你是一個 x-note 學習筆記品質審查員。\n"
        "審查筆記是否符合規範，適度寬容地評分。\n"
        "評分標準（0-100）：\n"
        "  95-100: 完全合格，所有必填項目滿足，內容有深度\n"
        "  85-94:  合格，幾乎所有必填項目滿足，有小幅改善空間\n"
        "  70-84:  有問題，某些必填項目未滿足或內容空洞\n"
        "  <70:   不合格，需要大幅修正\n"
        "MINOR 問題不扣分（> 80 分即可通過）：\n"
        "  - frontmatter 含非規範擴展欄位（如 _content_type, _usefulness）\n"
        "  - sources 含本地相對路徑（如 00-Inbox/...json）\n"
        "  - Core Summary 略為口語化但有實質內容\n"
        "  - Why It Matters 略短但有意義\n"
        "  - text_length 與原文略有不符（API 回傳截斷，非筆記問題）\n"
        "  - title 略為截斷但有意義\n"
        "  - Reference 原文來自 fxtwitter API，若有截斷屬外部因素\n"
        "CRITICAL 問題才扣分（這些問題才會把分數壓到 < 90）：\n"
        "  - Core Summary 空洞（< 50 字或有 placeholder：待補、todo、未在沒有翻譯證據時...）\n"
        "  - Key Points < 3 項或某項 < 10 字\n"
        "  - 完全無 Core Summary 或 Reference\n"
        "  - Key Points 某項 < 8 字\n"
        "  - score_reason 為空\n"
        "必填檢查項目：\n"
        "  [1] frontmatter 必填欄位：title, source_url, tweet_id, handle, author_display,\n"
        "       score, classification_path, tags\n"
        "  [2] ## Source Snapshot 存在\n"
        "  [3] ## Core Summary 非空，長度 > 50 字，無 placeholder 文字\n"
        "  [4] ## Key Points 至少 3 項，每項 > 8 字\n"
        "  [5] ## Why It Matters 非空，長度 > 30 字\n"
        "  [6] ## Reference 含 ### Complete X Post Text\n"
        "  [7] 無明顯 placeholder 文字\n"
        "  [8] text_length 與原文一致（誤差 < 10）\n"
        "回應嚴格 JSON（無其他文字）：\n"
        '  {"valid": true, "score": 97.0, "issues": [], "passed_checks": ["[1]","[2]","..."], '
        '"reasoning": "..."}'
    )

    user_prompt = f"""嚴格審查以下 x-note 筆記。

原始推文作者：{author} (@{handle})，評分：{score}/10
原文長度：{len(text)}

完整筆記內容：
\"\"\"
{note_text[:6000]}
\"\"\"

回應嚴格 JSON，無其他文字：
"""

    payload = {
        "model": "MiniMax-M3",
        "max_tokens": 1024,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_prompt}],
    }

    raw = _api_call(payload, api_key)
    result = _parse_json_response(raw)

    if result:
        result["raw_response"] = raw
        try:
            cache_file.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass
        return result

    print(f"[WARN] validate_note_with_llm: LLM failed, using rule fallback")
    return _fallback_validate_note(note_text, original_post)


def _fallback_validate_note(note_text: str, original_post: dict) -> dict:
    """Rule-based validation fallback."""
    import re
    issues = []
    passed = []

    # Check required sections
    required_sections = [
        "## Source Snapshot", "## Core Summary", "## Key Points",
        "## Why It Matters", "## Reference",
    ]
    for section in required_sections:
        if section in note_text:
            passed.append(f"[OK] {section}")
        else:
            issues.append(f"[FAIL] Missing section: {section}")

    # Check frontmatter
    if note_text.startswith("---"):
        fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", note_text, re.DOTALL)
        if fm_match:
            fm_text = fm_match.group(1)
            required_fm = ["title:", "source_url:", "tweet_id:", "handle:",
                           "author_display:", "score:", "classification_path:"]
            for field in required_fm:
                if field in fm_text:
                    passed.append(f"[OK] frontmatter {field}")
                else:
                    issues.append(f"[FAIL] missing frontmatter: {field}")
        else:
            issues.append("[FAIL] frontmatter not parseable")
    else:
        issues.append("[FAIL] no frontmatter found")

    # Check placeholder text
    for pat in PLACEHOLDER_PATTERNS:
        if pat in note_text:
            issues.append(f"[FAIL] placeholder text: '{pat}'")
            break

    # Check Core Summary length
    m = re.search(r"## Core Summary\s*\n\s*\n?(.+?)(?=\n##\s|\Z)", note_text, re.DOTALL)
    if m and len(m.group(1).strip()) > 50:
        passed.append("[OK] Core Summary length > 50")
    elif m:
        issues.append(f"[FAIL] Core Summary too short: {len(m.group(1).strip())} chars")
    else:
        issues.append("[FAIL] no Core Summary")

    # Check Key Points >= 3
    kp_match = re.search(r"## Key Points\s*\n(.*?)(?=\n##\s|\Z)", note_text, re.DOTALL)
    if kp_match:
        points = [l for l in kp_match.group(1).splitlines()
                  if l.strip().startswith("-")]
        if len(points) >= 3:
            passed.append(f"[OK] Key Points {len(points)} >= 3")
            short = [p for p in points if len(p.strip().lstrip("-").strip()) < 10]
            if short:
                issues.append(f"[FAIL] {len(short)} Key Points too short (<10 chars)")
        else:
            issues.append(f"[FAIL] only {len(points)} Key Points (need >= 3)")
    else:
        issues.append("[FAIL] no Key Points section")

    valid = len(issues) == 0
    score = 100.0 if valid else max(0, 100 - len(issues) * 10)

    return {
        "valid": valid,
        "score": score,
        "issues": issues,
        "passed_checks": passed,
        "reasoning": "Rule-based fallback validation",
        "raw_response": "",
    }


# ─────────────────────────────────────────────────────────────────────────────
# JSON parsing helper
# ─────────────────────────────────────────────────────────────────────────────

def _parse_json_response(raw: str) -> dict | None:
    """Extract JSON dict from LLM response text."""
    if not raw:
        return None
    import re
    # Try direct JSON parse
    try:
        return json.loads(raw)
    except Exception:
        pass
    # Try to find JSON in markdown code block
    m = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", raw, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1).strip())
        except Exception:
            pass
    # Try to find first { ... } block
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            pass
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Original curator functions (kept for backward compatibility)
# ─────────────────────────────────────────────────────────────────────────────

def call_curator(
    text: str,
    handle: str,
    author_display: str,
    score: float,
    api_key: str,
    api_url: str = API_URL_DEFAULT,
    model: str = "MiniMax-M3",
) -> str:
    """Call MiniMax curator API. Returns empty string on failure."""
    if not api_key:
        return ""

    system_prompt = (
        "你是專業的 X 貼文內容整理助手，負責把英文、簡中或日文推文改寫成"
        "高品質的繁體中文學習筆記。\n"
        "Score scale: 0-10。\n"
        "必須根據原始推文實際內容產出；禁止寫「未在沒有翻譯證據時」「本"
        "筆記只整理來源可確認的範圍」等 placeholder 文字。\n"
        "所有輸出必須是流暢繁體中文（zh-TW）。"
    )

    user_prompt = f"""請將以下 X 推文整理成 x-note 學習筆記主體。

必須包含以下三個區塊（繁體中文）：

## Core Summary
[用 1-2 段，具體說明這篇貼文的主要結論或最值得保留的重點]

## Key Points
- <要點 1>
- <要點 2>
- <要點 3>
（至少 3 個，要從原文具體內容提煉）

## Why It Matters
[這篇內容對讀者來說為什麼重要，或實際如何應用]

作者：{author_display} (@{handle})
評分：{score}/10

原始推文：
\"\"\"
{text}
\"\"\"

注意：
1. 只輸出 markdown 主體，不要輸出 frontmatter。
2. 不要包在 ```markdown 裡。
3. 必須根據原始推文事實撰寫，禁止 placeholder 文字。
4. 原文若非繁中，必須用流暢繁中重寫。
5. Key Points 至少 3 個，每個都是具體內容。
"""
    payload = {
        "model": model,
        "max_tokens": 4000,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_prompt}],
    }
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
    }

    last_err = None
    for attempt in range(1, MAX_HTTP_RETRIES + 1):
        try:
            req = urllib.request.Request(
                api_url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=CURATOR_TIMEOUT) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            content = result.get("content", [])
            text_parts = []
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text_parts.append(block.get("text", ""))
            body = _strip_codeblock_wrappers(strip_thinking_blocks("\n".join(text_parts)))
            if body:
                return body
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            last_err = f"attempt {attempt}: {type(e).__name__}: {e}"
            time.sleep(1)
        except Exception as e:
            last_err = f"attempt {attempt}: {type(e).__name__}: {e}"
            break

    print(f"[ERROR] curator call failed: {last_err}")
    return ""


def curator_cached(
    text: str,
    handle: str,
    author_display: str,
    score: float,
    api_key: str,
    api_url: str = API_URL_DEFAULT,
) -> str:
    """Cached wrapper around call_curator."""
    key_material = f"{handle}|{score}|{text}".encode("utf-8")
    cache_key = hashlib.sha256(key_material).hexdigest()[:32]
    cache_file = CACHE_DIR / f"{cache_key}.md"
    if cache_file.exists():
        try:
            cached = cache_file.read_text(encoding="utf-8")
            if cached:
                return cached
        except Exception:
            pass

    body = call_curator(text, handle, author_display, score, api_key, api_url)
    if body:
        try:
            cache_file.write_text(body, encoding="utf-8")
        except Exception as e:
            print(f"[WARN] cache write failed: {e}")
    return body


def is_placeholder_text(value: str) -> bool:
    """True when a generated section still contains the fallback placeholder text."""
    if not value or len(value.strip()) < 20:
        return True
    return any(pat in value for pat in PLACEHOLDER_PATTERNS)


def curate_sections(
    text: str,
    handle: str,
    author_display: str,
    score: float,
    cfg: dict | None = None,
) -> dict[str, str]:
    """
    Returns dict with keys: summary, key_points, why_it_matters.
    ALL THREE must contain real content (no placeholder).
    Caller must check is_placeholder_text() and fail loud if detected.
    """
    api_key = load_api_key(cfg)
    body = ""
    if api_key:
        body = curator_cached(text, handle, author_display, score, api_key)
    # Fix MiniMax-M3 Chinese-character corruption (U+FFFD) before s2twp
    body = _clean_corruption(body)
    body = _to_traditional(body)

    import re
    sections = {"summary": "", "key_points": "", "why_it_matters": ""}
    if not body:
        return sections

    def extract(heading: str, ends: tuple) -> str:
        pattern = re.escape(heading) + r"\s*\n(.*?)(?=\n##?\s|\Z)"
        m = re.search(pattern, body, flags=re.DOTALL)
        if not m:
            return ""
        chunk = m.group(1).strip()
        for end in ends:
            chunk = re.split(re.escape(end), chunk, maxsplit=1)[0]
        return chunk.strip()

    sections["summary"] = extract(
        "## Core Summary", ("## Key Points", "## Why It Matters")
    )
    sections["key_points"] = extract(
        "## Key Points", ("## Why It Matters",)
    )
    sections["why_it_matters"] = extract(
        "## Why It Matters", ()
    )

    # Fix MiniMax-M3 Chinese char corruption (U+FFFD) before s2twp conversion
    sections = {k: _to_traditional(v) for k, v in sections.items()}
    return sections
