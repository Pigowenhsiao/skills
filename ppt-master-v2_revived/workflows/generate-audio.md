---
description: Generate per-slide narration audio with AI-recommended voice selection, then optionally re-export PPTX with embedded audio
---

# Generate Audio Workflow

> Standalone post-export step. Run when the user asks for "產生旁白音檔" / "錄製旁白" / "簡報加旁白" / "有旁白的簡報" / "narrated PPT" / "video export with voice" / "匯出成有旁白的影片", or proactively offer it after a deck is exported. Produces one MP3 per slide via `edge-tts`, then optionally re-exports the PPTX with the audio embedded and per-slide auto-advance timings.

This workflow is **independent**: it reads `notes/*.md` and queries the TTS voice catalog — no upstream conversation context required. Safe to invoke in a fresh session.

## When to Run

- `notes/total.md` exists and has been split into per-page files at `notes/*.md` (post-processing Step 7.1 done).
- `edge-tts` is installed (`python3 -m pip install edge-tts`).
- The deck is in a single dominant language (mixed-language decks: pick the dominant one — the AI uses judgment, not a heuristic).

If `notes/*.md` are missing, run `total_md_split.py <project_path>` first.

---

## Step 1: Determine the deck's language

The AI already knows the deck's language from writing the notes. No detection script needed.

- Identify the primary language from the notes content: `zh` / `en` / `ja` / `ko` / etc.
- For mixed-language decks (e.g. Chinese with English technical terms), pick the language the audience will hear most of.
- For Chinese specifically: pick the locale based on context — `zh-TW` (Taiwan Mandarin, default for Taiwan-context projects), `zh-CN` (Mainland Mandarin), or `zh-HK` (Cantonese). Ask the user only if the project context does not make it clear.

---

## Step 2: Pull the voice catalog filtered by locale

```bash
python3 skills/ppt-master/scripts/notes_to_audio.py --list-voices --locale <locale>
```

The output is a flat list of all available voices for that locale. From this list, the AI picks **3–6 candidates** to recommend, applying these rules:

- **Cover both genders** when both exist for the locale.
- **Prefer `COMMON_VOICES`-listed voices** (curated set inside `notes_to_audio.py`) when the locale has them — they are battle-tested.
- **Match the deck's tone** — pick the strongest recommendation based on style:
  - Consultant / data-driven / 財報 → 穩重男聲（如 `zh-TW-YunJheNeural`）or 清晰女聲（如 `zh-TW-HsiaoChenNeural`）
  - General / 教學 / 產品介紹 → 清楚親切的女聲 / 年輕自然的男聲（優先從 `zh-TW-*` 清單挑選）
  - 發表會 / 播報 → 穩定、有正式感的聲線（優先從 `zh-TW-*` 清單挑選）
  - English consultant deck → `en-US-GuyNeural` (steady) or `en-US-JennyNeural` (clear)
  - Japanese / Korean → pick from `ja-JP-*` / `ko-KR-*` neural voices, mark gender + tone

For each candidate, write a **one-line Chinese description** covering: 性別 · 語氣風格 · 適用情境。

---

## Step 3: One-shot user interaction (mandatory)

Send a single message to the user that asks all three questions at once and provides a recommended value for each. Do NOT split into multiple rounds.

**Message template** (Chinese; translate to user's chat language if different):

> 偵測到 notes 主要語言為 **<語言>**（locale: `<locale>`）。依照這份簡報的語氣風格（<風格>），我建議使用以下設定：
>
> **聲音**：
> - **[1] <ShortName>** — <性別·語氣風格·適用情境> ⭐ **建議**
> - [2] <ShortName> — <性別·語氣風格·適用情境>
> - [3] <ShortName> — <性別·語氣風格·適用情境>
> - [4] <ShortName> — <性別·語氣風格·適用情境>
> - [5] <ShortName> — <性別·語氣風格·適用情境>
> - 也可直接輸入清單中的其他 ShortName。
>
> **語速**：⭐ 建議 `<rate>`（理由：<一句話，例如「每頁約 2–3 句，正常語速聽起來最穩」或「頁面資訊密度高，建議 -5% 稍慢一點」>）。
>
> **產生完成後，是否重新匯出已嵌入旁白音訊的 PPTX**：⭐ 建議 **是**（一次完成，並自動依照旁白長度設定每頁停留時間）。
>
> 直接回「好」就會採用全部建議值；也可以告訴我想調整的部分，例如「聲音 2，語速 -5%」。

**Recommended-value rules**:
- 聲音：從 Step 2 候選清單中，挑選最符合簡報語氣風格的選項。
- 語速：預設 `+0%`；notes 字數密集（平均每頁超過 4 句長句）建議 `-5%`；notes 簡短緊湊則建議 `+5%`；超出此範圍需說明理由。
- 嵌入：預設建議「是」；除非使用者已有客製 PPTX 且不希望覆蓋。

---

## Step 4: Execute (no further interaction)

Run sequentially — do NOT bundle:

```bash
# 1. Generate audio
python3 skills/ppt-master/scripts/notes_to_audio.py <project_path> \
  --voice <chosen-ShortName> --rate <chosen-rate>

# 2. (If user kept embedding) Re-export PPTX with audio embedded
python3 skills/ppt-master/scripts/svg_to_pptx.py <project_path> -s final \
  --recorded-narration audio
```

If `notes_to_audio.py` errors with a missing dependency, install `edge-tts` and re-run — do NOT swallow the error.

---

## Step 5: Completion report

Output one summary block listing:

- Number of MP3 files generated and their location (`<project_path>/audio/*.mp3`).
- The voice + rate actually used.
- (If embedded) the new narrated PPTX path under `<project_path>/exports/`.
- (If skipped embedding) one-line hint on how to embed later: `python3 skills/ppt-master/scripts/svg_to_pptx.py <project_path> -s final --recorded-narration audio`.
