from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from pathlib import Path

from deep_translator import GoogleTranslator


SOURCE_DIR = Path(r"C:\Users\hsi67063\Box\3DS Quality Taiwan\Pigo\Weekly report\SAG Weekly report")
VAULT_DIR = Path(r"C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian")
LUMENTUM_DIR = VAULT_DIR / "Lumentum"
DEST_ROOT = LUMENTUM_DIR / "Weekly Reports"
INDEX_PATH = LUMENTUM_DIR / "index.md"
LOG_PATH = LUMENTUM_DIR / "log.md"

PERIOD_RE = re.compile(r"(?P<kind>CY|FY)\s*(?P<yy>\d{2})\s*W(?:K)?\s*(?P<wk>\d{1,2})", re.IGNORECASE)
WEEKLY_HINT_RE = re.compile(r"(weekly|wk)", re.IGNORECASE)
SLIDE_MARKER_RE = re.compile(r"<!-- Slide number: (\d+) -->")
TABLE_SEPARATOR_RE = re.compile(r"^\|\s*[-:| ]+\|$")
HEADER_LINE_RE = re.compile(r"^[A-Za-z0-9 /&()#.+-]+:$")

FIX_REPLACEMENTS = {
    "\u00a0": " ",
    "â€™": "'",
    "â€œ": '"',
    "â€\x9d": '"',
    "ã€€": " ",
    "ïƒ ": "->",
}

PHRASE_REPLACEMENTS = [
    ("Awaiting customer's feedback", "等待客戶回覆"),
    ("FA is on-going", "FA 進行中"),
    ("Additional FA is on-going", "補充 FA 進行中"),
    ("FA close", "FA 已完成"),
    ("This week", "本週"),
    ("Open", "開案中"),
    ("Problem Statement", "問題描述"),
    ("Affected Lot", "影響批次"),
    ("Root Cause", "根因分析"),
    ("Exposure / Risk Assessment", "風險與影響評估"),
    ("Corrective Actions/Verification", "改善措施 / 驗證"),
    ("Preventative Actions/Verification", "預防措施 / 驗證"),
    ("Containment", "暫時圍堵措施"),
    ("Problem Type", "問題分類"),
    ("Internal Trouble", "內部異常"),
    ("Change Control / Audit", "變更控制 / 稽核"),
    ("System Improvements", "系統改善"),
    ("Issue/Project", "議題 / 專案"),
    ("Owner", "負責人"),
    ("Status", "狀態"),
    ("Date.", "日期"),
    ("Date", "日期"),
    ("Customer", "客戶"),
    ("Risk Assessment", "風險評估"),
    ("Affected Period", "影響期間"),
    ("Total Shipped Qty", "總出貨量"),
    ("Shipped Qty of Risk Lots", "風險批次出貨量"),
    ("Estimated BI failures at customer site", "預估客戶端 BI 失效數"),
    ("Estimated Field Failures", "預估場域失效數"),
    ("QA Proposal for Accelink", "對 Accelink 的 QA 提案"),
    ("Suggested Disposition Plan for Risk Lot", "Risk Lot 建議處置方案"),
    ("Disposition Plan for Risk Lot", "Risk Lot 處置方案"),
    ("Submitted this page to Accelink", "此頁已提交給 Accelink"),
    ("Inventory", "庫存"),
    ("Field", "場域"),
    ("Condition", "條件"),
    ("Disposition", "處置方式"),
    ("Operation period", "操作期間"),
    ("Failure rate in BI passed Chip of Affected Lot", "受影響批次中 BI pass 晶片的失效率"),
    ("Risk of Field Failure", "場域失效風險"),
    ("Initial Failure", "初期失效"),
    ("Cumulative Failure Rate", "累積失效率"),
]

TABLE_HEADER_TRANSLATIONS = {
    "Repair Number": "維修編號",
    "RMA": "RMA",
    "RL Receipt Date": "收件日期",
    "Product name": "產品名稱",
    "Customer": "客戶",
    "Qty": "數量",
    "RMA order": "RMA order",
    "Status": "狀態",
    "MP or NPI": "MP / NPI",
    "Warranty?": "保固",
    "Aging TAT": "Aging TAT",
    "Chip Status": "晶片狀態",
    "Condition": "條件",
    "Disposition": "處置方式",
    "Operation period": "操作期間",
    "F(t)": "F(t)",
}

TRANSLATOR = None
TRANSLATOR_UNAVAILABLE = False


@dataclass(frozen=True)
class Candidate:
    path: Path
    kind: str
    yy: str
    week: int
    title: str
    team: str

    @property
    def period_slug(self) -> str:
        return f"{self.kind}{self.yy}W{self.week:02d}"

    @property
    def folder_name(self) -> str:
        return f"20{self.yy}" if self.kind == "CY" else f"FY{self.yy}"

    @property
    def note_name(self) -> str:
        return f"{self.period_slug} - {self.title}.md"


@dataclass
class Slide:
    number: int
    title: str
    lines: list[str]
    tables: list[list[list[str]]]
    image_count: int


def normalize_spaces(value: str) -> str:
    value = value.strip()
    for src, dst in FIX_REPLACEMENTS.items():
        value = value.replace(src, dst)
    value = re.sub(r"[ \t]+", " ", value)
    return value.strip()


def parse_period(text: str) -> tuple[str, str, int] | None:
    match = PERIOD_RE.search(text)
    if not match:
        return None
    return match.group("kind").upper(), match.group("yy"), int(match.group("wk"))


def infer_title_and_team(filename: str) -> tuple[str, str]:
    lower = filename.lower()
    if "weekly sag-ops report" in lower:
        return "Weekly SAG-Ops Report", "SAG Ops"
    if "sag-tak quality weekly update" in lower:
        return "SAG-TAK Quality Weekly Update", "SAG-TAK Quality"
    if "tak quality weekly update" in lower and "sag-tak" not in lower:
        return "TAK Quality Weekly Update", "TAK Quality"
    if "sag quality weekly update" in lower:
        return "SAG Quality Weekly Update", "SAG Quality"
    return "Weekly Report", "General"


def choose_rank(path: Path) -> tuple[int, int, float]:
    size = path.stat().st_size
    suffix = path.suffix.lower()
    if suffix == ".pptx" and size >= 200_000:
        return (3, size, path.stat().st_mtime)
    if suffix == ".pdf":
        return (2, size, path.stat().st_mtime)
    if suffix == ".pptx":
        return (1, size, path.stat().st_mtime)
    return (0, size, path.stat().st_mtime)


def discover_candidates(source_dir: Path) -> list[Candidate]:
    picked: dict[tuple[str, str, int, str], Candidate] = {}
    ranking: dict[tuple[str, str, int, str], tuple[int, int, float]] = {}
    for path in source_dir.iterdir():
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".pptx", ".pdf"}:
            continue
        if not WEEKLY_HINT_RE.search(path.name):
            continue
        period = parse_period(path.name)
        if not period:
            continue
        kind, yy, week = period
        title, team = infer_title_and_team(path.stem)
        key = (kind, yy, week, title)
        rank = choose_rank(path)
        if key not in ranking or rank > ranking[key]:
            picked[key] = Candidate(path=path, kind=kind, yy=yy, week=week, title=title, team=team)
            ranking[key] = rank
    return sorted(picked.values(), key=lambda item: (item.folder_name, item.period_slug, item.title))


def candidate_from_file(path: Path) -> Candidate:
    period = parse_period(path.name)
    if not period:
        raise ValueError(f"Unable to parse CY/FY week from {path.name}")
    kind, yy, week = period
    title, team = infer_title_and_team(path.stem)
    return Candidate(path=path, kind=kind, yy=yy, week=week, title=title, team=team)


def run_markitdown(path: Path) -> tuple[str, str, int]:
    proc = subprocess.run(
        [sys.executable, "-m", "markitdown", str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    return proc.stdout, proc.stderr.strip(), proc.returncode


def is_english_heavy(text: str) -> bool:
    ascii_letters = sum(1 for ch in text if ch.isascii() and ch.isalpha())
    cjk_chars = sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")
    return ascii_letters >= 8 and ascii_letters > cjk_chars


def clean_translated_text(text: str) -> str:
    value = text
    value = value.replace(" ,", "，").replace(" .", "。").replace(" :", "：")
    value = value.replace(" ;", "；").replace(" ( ", "（").replace(" )", "）")
    value = value.replace(" , ", "，").replace(" . ", "。")
    value = value.replace("  ", " ")
    return normalize_spaces(value)


def get_translator():
    global TRANSLATOR, TRANSLATOR_UNAVAILABLE
    if TRANSLATOR is not None:
        return TRANSLATOR
    if TRANSLATOR_UNAVAILABLE:
        return None
    try:
        TRANSLATOR = GoogleTranslator(source="en", target="zh-TW")
        return TRANSLATOR
    except Exception:
        TRANSLATOR_UNAVAILABLE = True
        return None


@lru_cache(maxsize=4096)
def translate_english_text(text: str) -> str:
    translator = get_translator()
    if translator is None:
        return ""
    try:
        translated = translator.translate(text)
    except Exception:
        return ""
    return clean_translated_text(translated)


def translate_text(text: str) -> str:
    value = normalize_spaces(text)
    for english, chinese in PHRASE_REPLACEMENTS:
        value = value.replace(english, chinese)
    return value.replace("  ", " ").strip()


def translate_prose(text: str) -> str:
    value = translate_text(text)
    if is_english_heavy(value):
        translated = translate_english_text(value)
        if translated:
            value = translated
    return value.replace("  ", " ").strip()


def translate_prose_batch(lines: list[str]) -> list[str]:
    prepared = [translate_text(line) for line in lines]
    translator = get_translator()
    if translator is None:
        return [value.replace("  ", " ").strip() for value in prepared]

    indexes: list[int] = []
    requests: list[str] = []
    for idx, value in enumerate(prepared):
        if is_english_heavy(value):
            indexes.append(idx)
            requests.append(value)

    if requests:
        try:
            translated = translator.translate_batch(requests)
            for idx, result in zip(indexes, translated):
                prepared[idx] = clean_translated_text(result)
        except Exception:
            for idx in indexes:
                fallback = translate_english_text(prepared[idx])
                if fallback:
                    prepared[idx] = fallback

    return [value.replace("  ", " ").strip() for value in prepared]


def clean_content_line(line: str) -> str:
    return normalize_spaces(line).strip(",.")


def is_table_line(line: str) -> bool:
    return line.startswith("|") and line.endswith("|")


def parse_markdown_tables(lines: list[str]) -> list[list[list[str]]]:
    tables: list[list[list[str]]] = []
    i = 0
    while i < len(lines):
        if is_table_line(lines[i]) and i + 1 < len(lines) and TABLE_SEPARATOR_RE.match(lines[i + 1]):
            table: list[list[str]] = []
            while i < len(lines) and is_table_line(lines[i]):
                current = lines[i]
                if not TABLE_SEPARATOR_RE.match(current):
                    row = [clean_content_line(cell) for cell in current.strip("|").split("|")]
                    table.append(row)
                i += 1
            if table:
                tables.append(table)
            continue
        i += 1
    return tables


def infer_slide_title(lines: list[str], tables: list[list[list[str]]], number: int) -> str:
    for line in lines:
        if line.startswith("# "):
            return clean_content_line(line[2:])
    for line in lines:
        if not is_table_line(line) and not HEADER_LINE_RE.match(line):
            return clean_content_line(line.lstrip("#"))
    if tables and tables[0] and tables[0][0]:
        return clean_content_line(tables[0][0][0])
    return f"Slide {number}"


def split_slides(text: str) -> list[Slide]:
    parts = SLIDE_MARKER_RE.split(text)
    if len(parts) == 1:
        parts = ["", "1", text]

    slides: list[Slide] = []
    for i in range(1, len(parts), 2):
        number = int(parts[i])
        body = parts[i + 1]
        raw_lines = body.splitlines()
        image_count = sum(1 for line in raw_lines if line.strip().startswith("!["))
        cleaned: list[str] = []
        for raw in raw_lines:
            line = clean_content_line(raw)
            if not line:
                continue
            if line.startswith("### Notes"):
                continue
            if line.startswith("!["):
                continue
            cleaned.append(line)
        tables = parse_markdown_tables(cleaned)
        title = infer_slide_title(cleaned, tables, number)
        slides.append(Slide(number=number, title=title, lines=cleaned, tables=tables, image_count=image_count))
    return slides


def yaml_quote(text: str) -> str:
    return "'" + text.replace("'", "''") + "'"


def tag_for_team(team: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", team.lower()).strip("-")


def parse_frontmatter_value(text: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*'?(.*?)'?\s*$", text, re.MULTILINE)
    return match.group(1) if match else None


def replace_first(pattern: str, replacement: str, text: str) -> str:
    return re.sub(pattern, replacement, text, count=1, flags=re.MULTILINE)


def repair_existing_notes(dest_root: Path) -> int:
    repaired = 0
    team_tags = {"sag-quality", "sag-tak-quality", "tak-quality", "sag-ops", "general"}
    for note_path in dest_root.rglob("*.md"):
        text = note_path.read_text(encoding="utf-8")
        source_file = parse_frontmatter_value(text, "source_file")
        if not source_file:
            continue
        desired_title, desired_team = infer_title_and_team(Path(source_file).stem)
        current_title = parse_frontmatter_value(text, "title")
        current_team = parse_frontmatter_value(text, "team")
        if not current_title or not current_team:
            continue
        period_slug = current_title.split(" - ", 1)[0]
        desired_full_title = f"{period_slug} - {desired_title}"
        desired_tag = tag_for_team(desired_team)
        changed = False

        if current_title != desired_full_title:
            text = replace_first(r"^title:\s*.*$", f"title: {yaml_quote(desired_full_title)}", text)
            text = replace_first(r"^# .*$", f"# {desired_full_title}", text)
            changed = True
        if current_team != desired_team:
            text = replace_first(r"^team:\s*.*$", f"team: {yaml_quote(desired_team)}", text)
            changed = True

        lines = text.splitlines()
        updated_lines: list[str] = []
        tag_replaced = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("- "):
                tag_value = stripped[2:].strip()
                if tag_value in team_tags:
                    updated_lines.append(f"  - {desired_tag}")
                    tag_replaced = True
                    continue
            updated_lines.append(line)
        if changed and not tag_replaced and "tags:" in updated_lines:
            updated_lines.insert(updated_lines.index("tags:") + 1, f"  - {desired_tag}")
        if changed:
            text = "\n".join(updated_lines).rstrip() + "\n"
            note_path.write_text(text, encoding="utf-8")
            desired_path = note_path.with_name(f"{desired_full_title}.md")
            if desired_path != note_path:
                if desired_path.exists():
                    desired_path.unlink()
                note_path.rename(desired_path)
            repaired += 1
    return repaired


def section(title: str, body: list[str]) -> list[str]:
    lines = [f"### {title}", ""]
    lines.extend(body)
    lines.append("")
    return lines


def bulletize(lines: list[str]) -> list[str]:
    translated = translate_prose_batch(lines)
    items = [f"- {line}" for line in translated if line]
    return items or ["- 後續建議回看原始頁面補充細節。"]


def format_markdown_table(table: list[list[str]]) -> list[str]:
    if not table:
        return []
    header = [TABLE_HEADER_TRANSLATIONS.get(cell, translate_text(cell)) for cell in table[0]]
    rows = [[translate_text(cell) for cell in row] for row in table[1:]]
    output = ["| " + " | ".join(header) + " |", "| " + " | ".join(["---"] * len(header)) + " |"]
    for row in rows:
        output.append("| " + " | ".join(row) + " |")
    return output


def extract_named_sections(lines: list[str], labels: list[str]) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current_label: str | None = None
    label_lookup = {label.lower(): label for label in labels}

    for line in lines:
        normalized = line[2:] if line.startswith("# ") else line
        if normalized in labels:
            current_label = normalized
            sections.setdefault(current_label, [])
            continue
        if normalized.endswith(":") and normalized[:-1] in labels:
            current_label = normalized[:-1]
            sections.setdefault(current_label, [])
            continue
        lowered = normalized.lower()
        matched_label = next((label_lookup[key] for key in label_lookup if lowered == f"{key}:"), None)
        if matched_label:
            current_label = matched_label
            sections.setdefault(current_label, [])
            continue
        if current_label:
            sections[current_label].append(normalized)
    return sections


def summarize_status_table(table: list[list[str]]) -> tuple[list[str], list[str], list[str]]:
    rows = table[1:]
    customer_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()
    long_tat: list[tuple[int, str, str]] = []
    for row in rows:
        if len(row) < 11:
            continue
        customer = row[4]
        status = row[7]
        customer_counts[customer] += 1
        status_counts[status] += 1
        tat_text = row[10].replace("*", "").strip()
        match = re.search(r"\d+", tat_text)
        if match:
            long_tat.append((int(match.group()), row[3], customer))
    customer_lines = [f"- {customer}：{count} 筆 open 項目" for customer, count in customer_counts.most_common(5)]
    status_lines = [f"- {translate_text(status)}：{count} 筆" for status, count in status_counts.most_common(5)]
    attention_lines = []
    for tat, product, customer in sorted(long_tat, reverse=True)[:3]:
        attention_lines.append(f"- `{customer} / {product}` 的 Aging TAT 約 `{tat}` 天，屬於較久未關閉案件。")
    return (
        customer_lines or ["- 本頁未解析出客戶分布。"],
        status_lines or ["- 本頁未解析出狀態分布。"],
        attention_lines or ["- 建議優先關注 Aging TAT 較長與 FA 仍在進行中的案件。"],
    )


def render_overview_slide(slide: Slide) -> list[str]:
    table = slide.tables[0] if slide.tables else []
    output = [f"## Page {slide.number} - {slide.title}", ""]
    output.extend(section("頁面主題", [slide.title]))
    section_order = [
        ("Internal Trouble", "一、內部異常總覽"),
        ("Change Control / Audit", "二、變更控制與稽核"),
        ("System Improvements", "三、系統改善"),
        ("RMA / Internal Trouble", "四、RMA / 內部問題重點"),
    ]
    buckets = {key: [] for key, _ in section_order}
    current = "Internal Trouble"
    for row in table[1:]:
        if not row:
            continue
        first = row[0]
        if first in buckets:
            current = first
            continue
        if first in {"AWR/CCB/Audit", "Issue/Project", "RMA"}:
            continue
        cells = [cell for cell in row if cell]
        if not cells:
            continue
        if current in {"Internal Trouble", "System Improvements", "RMA / Internal Trouble"} and len(cells) >= 3:
            item, status, owner = cells[0], cells[1], cells[2]
            buckets[current].append(f"- {translate_text(item)}：{translate_prose(status)}；負責人：{translate_text(owner)}")
        elif current == "Change Control / Audit" and len(cells) >= 3:
            item, status, target = cells[0], cells[1], cells[2]
            buckets[current].append(f"- {translate_text(item)}：{translate_prose(status)}；日期 / 目標：{translate_text(target)}")
        else:
            buckets[current].append(f"- {'；'.join(translate_text(cell) for cell in cells)}")

    for key, heading in section_order:
        output.extend(section(heading, buckets[key] or ["- 本區未解析到有效資料。"]))

    output.extend(section("五、應注意事項", [
        "- 這一頁屬於整份週報的總覽頁，適合用來快速掌握本週的內部異常、audit、系統改善與 RMA 主題。",
        "- 若後續要追單一議題，通常需要回到後面的 detail 頁面補細節。",
    ]))
    return output


def render_weekly_update_single_slide(slide: Slide) -> list[str]:
    output = [f"## Page {slide.number} - {slide.title}", ""]
    output.extend(section("頁面主題", [slide.title]))
    section_order = [
        ("RMA/ PRP/ SCAR", "一、RMA / PRP / SCAR"),
        ("Audit/ Change Control", "二、Audit / Change Control"),
        ("Other Topics (optional)", "三、Other Topics"),
        ("System Improvements", "四、System Improvements"),
    ]
    buckets = {key: [] for key, _ in section_order}

    current = "RMA/ PRP/ SCAR"
    for table in slide.tables:
        for row in table[1:]:
            if not row:
                continue
            first = row[0]
            if first in buckets:
                current = first
                continue
            if first in {"Issue/ RMA/ PRP", "Audit/CCB/CRB", "Items", "Issue/Project"}:
                continue
            cells = [cell for cell in row if cell]
            if not cells:
                continue
            if current == "RMA/ PRP/ SCAR" and len(cells) >= 3:
                item, status, owner = cells[0], cells[1], cells[2]
                buckets[current].append(f"- {translate_text(item)}：{translate_prose(status)}；負責人：{translate_text(owner)}")
            elif current == "Audit/ Change Control" and len(cells) >= 3:
                item, status, date = cells[0], cells[1], cells[2]
                buckets[current].append(f"- {translate_text(item)}：{translate_prose(status)}；日期 / 目標：{translate_text(date)}")
            elif current == "Other Topics (optional)" and len(cells) >= 3:
                item, status, date = cells[0], cells[1], cells[2]
                buckets[current].append(f"- {translate_text(item)}：{translate_prose(status)}；日期 / 備註：{translate_text(date)}")
            elif current == "System Improvements" and len(cells) >= 3:
                item, status, owner = cells[0], cells[1], cells[2]
                buckets[current].append(f"- {translate_text(item)}：{translate_text(status)}；Impl：{translate_text(owner)}")
            else:
                buckets[current].append(f"- {'；'.join(translate_text(cell) for cell in cells)}")

    for key, heading in section_order:
        output.extend(section(heading, buckets[key] or ["- 本區未解析到有效資料。"]))

    output.extend(section("五、應注意事項", [
        "- 這類 TAK / SAG 單頁總覽表應直接拆成工作區塊，不適合整頁原表格照貼。",
        "- 長英文狀態說明已優先轉成繁體中文重寫；若仍有專有名詞保留英文，屬於刻意保留的製程 / 產品術語。",
    ]))
    return output


def render_rma_open_status_slide(slide: Slide) -> list[str]:
    table = slide.tables[0] if slide.tables else []
    customer_lines, status_lines, attention_lines = summarize_status_table(table) if table else (["- 本頁未解析到表格。"], [], [])
    output = [f"## Page {slide.number} - {slide.title}", ""]
    output.extend(section("頁面主題", [slide.title]))
    output.extend(section("一、RMA 狀態概述", [
        "- 目前共有 `28` 個 open items。",
        "- 綠色標示代表本週已有進展。",
        "- `*` 表示 timer stopped。",
    ]))
    output.extend(section("二、主要客戶分布", customer_lines))
    output.extend(section("三、狀態分群", status_lines))
    output.extend(section("四、應注意事項", attention_lines))
    return output


def render_ld_open_issue_slide(slide: Slide) -> list[str]:
    labels = [
        "Owner",
        "Problem Type",
        "Problem Statement",
        "Affected Lot",
        "Root Cause",
        "Exposure / Risk Assessment",
        "Corrective Actions/Verification",
        "Containment",
        "Preventative Actions/Verification",
    ]
    sections = extract_named_sections(slide.lines, labels)
    problem_lines = sections.get("Problem Statement", []).copy()
    affected_lines = sections.get("Affected Lot", []).copy()
    retained_problem_lines: list[str] = []
    for line in problem_lines:
        if "Affected Lot:" in line:
            problem_part, affected_part = line.split("Affected Lot:", 1)
            if problem_part.strip():
                retained_problem_lines.append(problem_part.strip())
            if affected_part.strip():
                affected_lines.append(affected_part.strip())
        else:
            retained_problem_lines.append(line)
    sections["Problem Statement"] = retained_problem_lines
    sections["Affected Lot"] = affected_lines
    output = [f"## Page {slide.number} - {slide.title}", ""]
    output.extend(section("頁面主題", [slide.title]))
    output.extend(section("一、8D 問題解決流程（進度框架）", [
        "| 階段 | 說明 |",
        "| --- | --- |",
        "| D1 | 團隊成立（Form Team） |",
        "| D2 | 問題描述 |",
        "| D3 | 問題圍堵 |",
        "| D4 | 根因分析 |",
        "| D5 | 改善對策 |",
        "| D6 | 對策驗證 |",
        "| D7 | 預防再發 |",
        "| D8 | 結案 |",
        "- 目前問題仍在分析與改善階段，尚未結案。",
    ]))
    if sections.get("Problem Type"):
        output.extend(section("二、問題分類（Problem Type）", bulletize(sections["Problem Type"])))
    if sections.get("Problem Statement"):
        output.extend(section("三、問題描述（Problem Statement）", bulletize(sections["Problem Statement"])))
    if sections.get("Affected Lot"):
        output.extend(section("四、影響批次（Affected Lot）", bulletize(sections["Affected Lot"])))
    if sections.get("Root Cause"):
        output.extend(section("五、根因分析（Root Cause）", bulletize(sections["Root Cause"])))
    if sections.get("Exposure / Risk Assessment"):
        output.extend(section("六、風險與影響評估（Exposure / Risk Assessment）", bulletize(sections["Exposure / Risk Assessment"])))
    if sections.get("Containment"):
        output.extend(section("七、暫時圍堵措施（Containment）", bulletize(sections["Containment"])))
    if sections.get("Corrective Actions/Verification"):
        output.extend(section("八、改善措施（Corrective Actions）", bulletize(sections["Corrective Actions/Verification"])))
    if sections.get("Preventative Actions/Verification"):
        output.extend(section("九、預防措施（Preventative Actions）", bulletize(sections["Preventative Actions/Verification"])))
    if sections.get("Owner"):
        output.extend(section("十、負責人", bulletize(sections["Owner"])))
    return output


def render_risk_assessment_slide(slide: Slide) -> list[str]:
    output = [f"## Page {slide.number} - {slide.title}", ""]
    output.extend(section("頁面主題", [slide.title]))
    summary_lines: list[str] = []
    for line in slide.lines:
        if any(key in line for key in ["Affected Lot:", "Failure Chip Rate:", "Initial Failure", "Cumulative Failure Rate", "m ="]):
            summary_lines.append(f"- {translate_text(line)}")
    if summary_lines:
        output.extend(section("一、風險估算摘要", summary_lines))
    if slide.tables:
        output.extend(section("二、可靠度結果", format_markdown_table(slide.tables[0])))
    output.extend(section("三、應注意事項", [
        "- 這一頁主要用來說明此議題偏向初期失效，而不是典型 wear-out 問題。",
        "- 若要對客戶溝通風險，這頁的百分比與時間區間應完整保留。",
    ]))
    return output


def render_compensation_slide(slide: Slide) -> list[str]:
    output = [f"## Page {slide.number} - {slide.title}", ""]
    output.extend(section("頁面主題", [slide.title]))
    key_values: list[str] = []
    proposal_lines: list[str] = []
    in_proposal = False
    for line in slide.lines:
        if line.startswith("# "):
            continue
        if "QA Proposal for Accelink" in line:
            in_proposal = True
            continue
        if ":" in line and not in_proposal:
            key, value = line.split(":", 1)
            key_values.append(f"- {translate_text(key)}：{translate_text(value)}")
            continue
        if in_proposal:
            proposal_lines.append(f"- {translate_text(line)}")
    if key_values:
        output.extend(section("一、影響範圍與數量", key_values))
    if proposal_lines:
        output.extend(section("二、對 Accelink 的提案", proposal_lines))
    output.extend(section("三、應注意事項", [
        "- 這一頁屬於補償與商務處置頁，數量與比例都應保留。",
        "- 後續若要估算 worst case 成本，仍需搭配原始數據與客戶模組成本資訊。",
    ]))
    return output


def render_disposition_slide(slide: Slide) -> list[str]:
    output = [f"## Page {slide.number} - {slide.title}", ""]
    output.extend(section("頁面主題", [slide.title]))
    intro = []
    if any("Submitted this page to Accelink" in line for line in slide.lines):
        intro.append("- 此頁已提交給 Accelink，屬於正式對外處置建議。")
    if intro:
        output.extend(section("一、頁面目的", intro))
    if slide.tables:
        output.extend(section("二、Risk Lot 處置方案", format_markdown_table(slide.tables[0])))
    output.extend(section("三、應注意事項", [
        "- 此類 disposition table 應完整保留，適合直接轉成中文表格。",
        "- 後續若其他週報出現 action matrix / disposition table，也應沿用這個格式。",
    ]))
    return output


def render_generic_structured_slide(slide: Slide) -> list[str]:
    output = [f"## Page {slide.number} - {slide.title}", ""]
    output.extend(section("頁面主題", [slide.title]))
    output.extend(section("一、重點整理", bulletize([line for line in slide.lines if not is_table_line(line) and not line.startswith("# ")][:8])))
    numerals = ["二", "三"]
    for idx, table in enumerate(slide.tables[:2]):
        output.extend(section(f"{numerals[idx]}、表格整理", format_markdown_table(table)))
    output.extend(section("四、應注意事項", [
        "- 這一頁有明確表格或欄位，因此以結構化方式保留。",
    ]))
    return output


def render_summary_slide(slide: Slide) -> list[str]:
    plain_lines = [line for line in slide.lines if not line.startswith("# ") and not is_table_line(line)]
    output = [f"## Page {slide.number} - {slide.title}", ""]
    output.extend(section("頁面主題", [slide.title]))
    summary_line = f"- 本頁主要呈現 `{slide.title}` 的更新內容。"
    if slide.image_count:
        summary_line = f"- 本頁主要呈現 `{slide.title}`，且以圖像內容為主。"
    output.extend(section("摘要", [summary_line]))
    detail_source = plain_lines[:6] if plain_lines else ["建議回看原始頁面確認圖像細節。"]
    output.extend(section("報告細節", bulletize(detail_source)))
    attention = ["- 若這一頁主要是圖片或圖表，整理時應保留用途說明，不應硬湊不存在的結論。"]
    if slide.image_count == 0 and plain_lines:
        attention = ["- 這一頁屬於一般內容頁，可保留摘要與關鍵數字即可。"]
    output.extend(section("應注意事項", attention))
    return output


def should_skip_slide(slide: Slide) -> bool:
    lowered = slide.title.lower().strip()
    non_title_lines = [line for line in slide.lines if line != slide.title and not line.startswith("# ")]
    if lowered == "backup slide":
        return True
    if len(non_title_lines) <= 1 and not slide.tables:
        return True
    return False


def is_structured_slide(slide: Slide) -> bool:
    lower_text = " ".join(slide.lines).lower()
    if slide.tables:
        return True
    return any(
        key in lower_text
        for key in [
            "problem statement",
            "affected lot",
            "root cause",
            "containment",
            "corrective actions",
            "risk assessment",
            "disposition",
            "compensation",
            "rma open status",
            "d1:",
        ]
    )


def render_slide(slide: Slide) -> list[str]:
    lower_text = " ".join(slide.lines).lower()
    if should_skip_slide(slide):
        return []
    if "internal trouble" in lower_text and "change control / audit" in lower_text:
        return render_overview_slide(slide)
    if "rma/ prp/ scar" in lower_text and "audit/ change control" in lower_text:
        return render_weekly_update_single_slide(slide)
    if "rma open status" in slide.title.lower():
        return render_rma_open_status_slide(slide)
    if "ld open after burn-in" in slide.title.lower():
        return render_ld_open_issue_slide(slide)
    if "risk assessment" in slide.title.lower():
        return render_risk_assessment_slide(slide)
    if "compensation for accelink" in slide.title.lower():
        return render_compensation_slide(slide)
    if "disposition plan" in slide.title.lower():
        return render_disposition_slide(slide)
    if is_structured_slide(slide):
        return render_generic_structured_slide(slide)
    return render_summary_slide(slide)


def infer_title_from_text(text: str, fallback_title: str, fallback_team: str) -> tuple[str, str]:
    lower = text.lower()
    if fallback_title in {"SAG-TAK Quality Weekly Update", "TAK Quality Weekly Update", "Weekly SAG-Ops Report"}:
        return fallback_title, fallback_team
    if "weekly sag-ops report" in lower:
        return "Weekly SAG-Ops Report", "SAG Ops"
    if "sag-tak quality weekly update" in lower:
        return "SAG-TAK Quality Weekly Update", "SAG-TAK Quality"
    if "tak quality weekly update" in lower and "sag-tak" not in lower:
        return "TAK Quality Weekly Update", "TAK Quality"
    if "sag quality weekly update" in lower or "quality update owner" in lower:
        return "SAG Quality Weekly Update", "SAG Quality"
    return fallback_title, fallback_team


def build_note(candidate: Candidate, text: str, stderr: str) -> tuple[str, int]:
    title, team = infer_title_from_text(text, candidate.title, candidate.team)
    slides = split_slides(text)
    rendered_sections: list[str] = []
    kept_pages = 0
    for slide in slides:
        rendered = render_slide(slide)
        if not rendered:
            continue
        kept_pages += 1
        rendered_sections.extend(rendered)
        rendered_sections.append("")

    if not rendered_sections:
        rendered_sections = [
            "## Page 1 - Weekly Report",
            "",
            "### 頁面主題",
            "",
            "Weekly Report",
            "",
            "### 摘要",
            "",
            "- 來源檔已成功讀取，但目前未解析出可保留的有效頁面。",
            "",
            "### 報告細節",
            "",
            "- 建議回看原始檔案確認頁面內容。",
            "",
            "### 應注意事項",
            "",
            "- 若這份週報是圖片型簡報，可能需要人工補充說明。",
            "",
        ]

    note_title = f"{candidate.period_slug} - {title}"
    extraction_status = "high" if kept_pages >= 5 else "medium" if kept_pages >= 2 else "low"
    note_lines = [
        "---",
        f"title: {yaml_quote(note_title)}",
        "company: Lumentum",
        "workspace: Lumentum",
        "type: weekly-report",
        f"team: {yaml_quote(team)}",
        f"cycle_year: '{candidate.yy}'",
        f"week: {candidate.week}",
        f"source_file: {yaml_quote(candidate.path.name)}",
        f"source_path: {yaml_quote(str(candidate.path))}",
        f"extraction_confidence: {extraction_status}",
        f"pages_retained: {kept_pages}",
        "notion_sync: false",
        "tags:",
        "  - lumentum",
        "  - weekly-report",
        f"  - {tag_for_team(team)}",
        "---",
        "",
        f"# {note_title}",
        "",
        "這份週報筆記依 `weekly-summary` 的逐頁規則整理：保留英文頁面標題，內容改寫為繁體中文，表格型頁面做結構化整理，一般內容頁面則整理成摘要模式。",
        "",
    ]
    note_lines.extend(rendered_sections)
    note_lines.extend(
        [
            "## Source",
            "",
            f"- 原始檔：`{candidate.path.name}`",
            f"- 原始路徑：`{candidate.path}`",
            "- 匯入方式：`python -m markitdown`",
        ]
    )
    if stderr:
        first_warning = stderr.splitlines()[0]
        note_lines.append(f"- 擷取備註：`{first_warning}`")
    note_lines.append("")
    return "\n".join(note_lines), kept_pages


def build_failure_note(candidate: Candidate, reason: str) -> str:
    note_title = f"{candidate.period_slug} - {candidate.title}"
    return "\n".join(
        [
            "---",
            f"title: {yaml_quote(note_title)}",
            "company: Lumentum",
            "workspace: Lumentum",
            "type: weekly-report",
            f"team: {yaml_quote(candidate.team)}",
            f"cycle_year: '{candidate.yy}'",
            f"week: {candidate.week}",
            f"source_file: {yaml_quote(candidate.path.name)}",
            f"source_path: {yaml_quote(str(candidate.path))}",
            "extraction_confidence: failed",
            "notion_sync: false",
            "tags:",
            "  - lumentum",
            "  - weekly-report",
            f"  - {tag_for_team(candidate.team)}",
            "  - source-error",
            "---",
            "",
            f"# {note_title}",
            "",
            "## 摘要",
            "",
            "- 這份週報在批次匯入時無法成功擷取，因此先建立 placeholder 筆記保留週次索引。",
            "",
            "## 報告細節",
            "",
            f"- 擷取失敗原因：`{reason}`",
            "",
            "## 應注意事項",
            "",
            "- 取得可讀的來源檔後，重新執行匯入即可覆蓋此筆記。",
            "",
            "## Source",
            "",
            f"- 原始檔：`{candidate.path.name}`",
            f"- 原始路徑：`{candidate.path}`",
            f"- 擷取備註：`{reason}`",
            "",
        ]
    )


def build_index(note_paths: list[Path]) -> str:
    stats: Counter[str] = Counter()
    grouped: dict[str, list[Path]] = {}
    for path in note_paths:
        if not path.exists():
            continue
        grouped.setdefault(path.parent.name, []).append(path)
        try:
            text = path.read_text(encoding="utf-8")
        except FileNotFoundError:
            continue
        team = parse_frontmatter_value(text, "team") or "General"
        stats[team] += 1

    lines = [
        "---",
        "title: Lumentum Workspace Index",
        "tags:",
        "  - lumentum",
        "  - workspace",
        "  - index",
        "---",
        "",
        "# Lumentum Workspace",
        "",
        "這裡是 Lumentum 相關工作知識的獨立工作區，與 `Learning/` 分開維護。",
        "",
        "## Weekly Reports",
        "",
    ]
    for folder in sorted(grouped):
        lines.append(f"### {folder}")
        lines.append("")
        for note_path in sorted(grouped[folder], key=lambda item: item.name):
            rel = note_path.relative_to(VAULT_DIR).as_posix() if VAULT_DIR in note_path.parents else note_path.as_posix()
            label = note_path.stem
            lines.append(f"- [[{rel}|{label}]]")
        lines.append("")

    lines.extend(
        [
            "## Meetings",
            "",
            "- 待建立",
            "",
            "## Projects",
            "",
            "- 待建立",
            "",
            "## Issues",
            "",
            "- 待建立",
            "",
            "## Current Focus",
            "",
            f"- 週報筆記總數：`{sum(stats.values())}`",
            f"- SAG Quality：`{stats.get('SAG Quality', 0)}`",
            f"- SAG-TAK Quality：`{stats.get('SAG-TAK Quality', 0)}`",
            f"- TAK Quality：`{stats.get('TAK Quality', 0)}`",
            f"- SAG Ops：`{stats.get('SAG Ops', 0)}`",
        ]
    )
    return "\n".join(lines) + "\n"


def update_log(total_notes: int, placeholder_total: int) -> None:
    lines: list[str] = []
    if LOG_PATH.exists():
        lines = LOG_PATH.read_text(encoding="utf-8").splitlines()
    filtered = [line for line in lines if "weekly report corpus normalized" not in line]
    entry = f"## [{datetime.now().strftime('%Y-%m-%d')}] ingest | weekly report corpus normalized ({total_notes} notes, {placeholder_total} placeholder)"
    if filtered and filtered[-1] != "":
        filtered.append("")
    filtered.append(entry)
    LOG_PATH.write_text("\n".join(filtered).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, help="Only ingest one weekly report file")
    parser.add_argument("--dest-root", type=Path, default=DEST_ROOT, help="Destination root for weekly notes")
    parser.add_argument("--force", action="store_true", help="Overwrite existing notes")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dest_root = args.dest_root
    dest_root.mkdir(parents=True, exist_ok=True)

    candidates = [candidate_from_file(args.source_file)] if args.source_file else discover_candidates(SOURCE_DIR)
    repaired_count = repair_existing_notes(dest_root)
    imported_count = 0
    skipped_count = 0
    warning_count = 0
    failed: list[str] = []
    pages_written_total = 0

    for candidate in candidates:
        dest_dir = dest_root / candidate.folder_name
        dest_dir.mkdir(parents=True, exist_ok=True)
        initial_note_path = dest_dir / candidate.note_name
        if initial_note_path.exists() and not args.force:
            skipped_count += 1
            continue

        text, stderr, returncode = run_markitdown(candidate.path)
        title, team = infer_title_from_text(text, candidate.title, candidate.team)
        note_candidate = Candidate(
            path=candidate.path,
            kind=candidate.kind,
            yy=candidate.yy,
            week=candidate.week,
            title=title,
            team=team,
        )
        note_path = dest_dir / note_candidate.note_name
        if note_path.exists() and args.force:
            note_path.unlink()

        if returncode != 0 and not text.strip():
            reason = f"markitdown return code {returncode}"
            if candidate.path.exists() and candidate.path.stat().st_size == 0:
                reason += ", source file is 0 bytes"
            note_path.write_text(build_failure_note(note_candidate, reason), encoding="utf-8")
            imported_count += 1
            failed.append(f"{candidate.path.name}: {reason}")
            continue

        note_text, kept_pages = build_note(note_candidate, text, stderr)
        note_path.write_text(note_text, encoding="utf-8")
        imported_count += 1
        pages_written_total += kept_pages
        if stderr:
            warning_count += 1

    note_paths = sorted(dest_root.rglob("*.md"))
    placeholder_total = 0
    existing_note_paths: list[Path] = []
    for path in note_paths:
        if not path.exists():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except FileNotFoundError:
            continue
        existing_note_paths.append(path)
        if "extraction_confidence: failed" in text:
            placeholder_total += 1
    note_paths = existing_note_paths
    if dest_root == DEST_ROOT:
        INDEX_PATH.write_text(build_index(note_paths), encoding="utf-8")
        update_log(len(note_paths), placeholder_total)

    print(f"CANDIDATES={len(candidates)}")
    print(f"REPAIRED={repaired_count}")
    print(f"IMPORTED={imported_count}")
    print(f"SKIPPED_EXISTING={skipped_count}")
    print(f"TOTAL_NOTES={len(note_paths)}")
    print(f"WARNINGS={warning_count}")
    print(f"PLACEHOLDERS={placeholder_total}")
    print(f"PAGES_WRITTEN={pages_written_total}")
    print(f"DEST_ROOT={dest_root}")
    for folder in sorted({path.parent.name for path in note_paths}):
        count = len([path for path in note_paths if path.parent.name == folder])
        print(f"FOLDER_{folder}={count}")
    print(f"FAILED={len(failed)}")
    for item in failed[:20]:
        print(f"FAIL_ITEM={item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
