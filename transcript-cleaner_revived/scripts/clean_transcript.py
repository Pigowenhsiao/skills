#!/usr/bin/env python3
"""
transcript-cleaner: 清理語音直播文字稿，解決 NotebookLM 匯入失敗問題。

問題根因：x-note 產出的 transcript 沒有自然斷行，每段話連成一行 500-1000+ 字。
NotebookLM 的 Markdown parser 對超長行（>200 字）處理不穩定，會回傳 error。

這個工具：
1. 偵測 transcript 是否有長行問題
2. 自動備份原檔（預設 _backup_原檔/ 子目錄）
3. 將超長行重新分段（預設每段 ≤200 字）
4. 清理噪音行（純標點、極短行、連續空行）
5. 寫回原檔
6. 報告清理結果

用法:
    # 單一檔案
    python3 clean_transcript.py /path/to/transcript.txt

    # 目錄（遞迴處理所有 .txt）
    python3 clean_transcript.py /path/to/directory/

    # 多個路徑
    python3 clean_transcript.py /path/a/ /path/b/file.txt

    # 只偵測不清理
    python3 clean_transcript.py /path/to/file.txt --check-only

    # 自訂參數
    python3 clean_transcript.py /path/to/file.txt --max-line-length 150
    python3 clean_transcript.py /path/to/file.txt --no-backup
    python3 clean_transcript.py /path/to/file.txt --backup-dir /tmp/backup/

作者: transcript-cleaner skill v1.0.0
建立: 2026-06-15
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import NamedTuple


# 預設參數
DEFAULT_MAX_LINE_LENGTH = 200
DEFAULT_MIN_LINE_LENGTH = 10
DEFAULT_BACKUP_SUBDIR = "_backup_原檔"


class CleanStats(NamedTuple):
    """單一檔案的清理結果"""
    filepath: str
    orig_chars: int
    clean_chars: int
    orig_lines: int
    clean_lines: int
    orig_max_line: int
    clean_max_line: int
    orig_long_lines: int
    clean_long_lines: int
    was_modified: bool
    backup_path: str | None
    skipped: bool = False
    skip_reason: str | None = None


def detect_issues(content: str) -> dict:
    """偵測 transcript 的長行問題

    Returns:
        dict with keys:
            - max_line_length: 最長行的字元數
            - long_lines: 超過 200 字的行數
            - very_long_lines: 超過 500 字的行數
            - total_lines: 總行數
            - short_lines: 短於 10 字的非空行數
            - empty_lines: 空行數
            - needs_cleaning: 是否需要清理
            - severity: "ok" | "warning" | "error"
    """
    lines = content.split('\n')
    non_empty_lines = [l for l in lines if l.strip()]

    if not non_empty_lines:
        return {
            'max_line_length': 0,
            'long_lines': 0,
            'very_long_lines': 0,
            'total_lines': len(lines),
            'short_lines': 0,
            'empty_lines': 0,
            'needs_cleaning': False,
            'severity': 'ok',
        }

    max_line = max(len(l) for l in lines)
    long_lines = sum(1 for l in lines if len(l) > 200)
    very_long_lines = sum(1 for l in lines if len(l) > 500)
    short_lines = sum(1 for l in non_empty_lines if len(l) < 10)
    empty_lines = sum(1 for l in lines if not l.strip())

    needs_cleaning = long_lines > 0
    if very_long_lines > 0:
        severity = 'error'  # 極可能導致 NotebookLM error
    elif long_lines > 0:
        severity = 'warning'  # 可能導致 NotebookLM error
    else:
        severity = 'ok'

    return {
        'max_line_length': max_line,
        'long_lines': long_lines,
        'very_long_lines': very_long_lines,
        'total_lines': len(lines),
        'short_lines': short_lines,
        'empty_lines': empty_lines,
        'needs_cleaning': needs_cleaning,
        'severity': severity,
    }


def deep_clean(content: str, max_line_length: int = DEFAULT_MAX_LINE_LENGTH,
               min_line_length: int = DEFAULT_MIN_LINE_LENGTH) -> str:
    """清理 transcript 內容

    清理策略：
    1. 跳過純標點/數字行
    2. 跳過極短行（< min_line_length 字，可能是語音識別錯誤噪音）
    3. 將超長行重新分段（每段 ≤ max_line_length 字）
    4. 合併連續空行（最多保留一個）
    5. 保留原始用語風格（不修改文字內容）
    """
    lines = content.split('\n')
    cleaned = []
    prev_empty = False

    for line in lines:
        line = line.strip()

        # 跳過空行（最多保留一個連續空行）
        if not line:
            if not prev_empty:
                cleaned.append('')
                prev_empty = True
            continue
        prev_empty = False

        # 跳過純標點/數字行
        if re.match(r'^[，。、！？：；""\'\'（）【】…—\-\d\s]+$', line):
            continue

        # 跳過極短行
        if len(line) < min_line_length:
            continue

        # 將超長行分段（嚴格保證每段 ≤ max_line_length）
        if len(line) > max_line_length:
            # 預先切成固定大小的塊，最後一個塊可能較短
            chunks = [line[i:i + max_line_length] for i in range(0, len(line), max_line_length)]
            for chunk in chunks:
                chunk = chunk.strip()
                if not chunk:
                    continue
                # 如果短塊 + 前一行會超過 max_line_length，單獨成行
                # 否則可以與前一行合併（讓行長更接近 max_line_length）
                if (cleaned
                    and cleaned[-1]
                    and len(cleaned[-1]) + len(chunk) <= max_line_length):
                    cleaned[-1] = cleaned[-1] + chunk
                else:
                    cleaned.append(chunk)
        else:
            cleaned.append(line)

    return '\n'.join(cleaned)


def backup_file(filepath: str, backup_dir: str | None = None) -> str | None:
    """備份原檔

    Args:
        filepath: 要備份的檔案路徑
        backup_dir: 自訂備份目錄，若 None 則使用 <filepath>/_backup_原檔/

    Returns:
        備份檔案路徑，若跳過則返回 None
    """
    src = Path(filepath)
    if not src.exists():
        return None

    if backup_dir:
        backup_root = Path(backup_dir)
    else:
        if src.is_dir():
            backup_root = src / DEFAULT_BACKUP_SUBDIR
        else:
            backup_root = src.parent / DEFAULT_BACKUP_SUBDIR

    backup_root.mkdir(parents=True, exist_ok=True)
    backup_path = backup_root / src.name

    # 避免覆蓋既有備份（加時間戳）
    if backup_path.exists():
        import time
        ts = int(time.time())
        backup_path = backup_root / f"{src.stem}_{ts}{src.suffix}"

    # 複製檔案
    import shutil
    shutil.copy2(src, backup_path)
    return str(backup_path)


def process_file(filepath: str, max_line_length: int = DEFAULT_MAX_LINE_LENGTH,
                 min_line_length: int = DEFAULT_MIN_LINE_LENGTH,
                 do_backup: bool = True, backup_dir: str | None = None,
                 check_only: bool = False, force: bool = False) -> CleanStats:
    """處理單一檔案

    Args:
        filepath: 檔案路徑
        max_line_length: 最大行長
        min_line_length: 最小行長
        do_backup: 是否備份
        backup_dir: 自訂備份目錄
        check_only: 只偵測不清理
        force: 強制清理（即使 max_line_length 已達標）

    Returns:
        CleanStats 物件
    """
    src = Path(filepath)
    if not src.exists() or not src.is_file():
        return CleanStats(
            filepath=filepath, orig_chars=0, clean_chars=0,
            orig_lines=0, clean_lines=0, orig_max_line=0, clean_max_line=0,
            orig_long_lines=0, clean_long_lines=0,
            was_modified=False, backup_path=None,
            skipped=True, skip_reason="file not found"
        )

    # 讀取檔案
    try:
        with open(src, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(src, 'r', encoding='gbk') as f:
                content = f.read()
        except Exception as e:
            return CleanStats(
                filepath=filepath, orig_chars=0, clean_chars=0,
                orig_lines=0, clean_lines=0, orig_max_line=0, clean_max_line=0,
                orig_long_lines=0, clean_long_lines=0,
                was_modified=False, backup_path=None,
                skipped=True, skip_reason=f"encoding error: {e}"
            )

    orig_lines = content.splitlines()
    orig_chars = len(content)
    orig_max = max((len(l) for l in orig_lines), default=0)
    orig_long = sum(1 for l in orig_lines if len(l) > 200)
    issues = detect_issues(content)

    # 決定是否需要清理
    needs_cleaning = issues['needs_cleaning'] or force
    if not needs_cleaning:
        return CleanStats(
            filepath=filepath, orig_chars=orig_chars, clean_chars=orig_chars,
            orig_lines=len(orig_lines), clean_lines=len(orig_lines),
            orig_max_line=orig_max, clean_max_line=orig_max,
            orig_long_lines=orig_long, clean_long_lines=orig_long,
            was_modified=False, backup_path=None, skipped=False
        )

    if check_only:
        return CleanStats(
            filepath=filepath, orig_chars=orig_chars, clean_chars=orig_chars,
            orig_lines=len(orig_lines), clean_lines=len(orig_lines),
            orig_max_line=orig_max, clean_max_line=orig_max,
            orig_long_lines=orig_long, clean_long_lines=orig_long,
            was_modified=False, backup_path=None, skipped=False
        )

    # 備份
    backup_path = None
    if do_backup:
        backup_path = backup_file(filepath, backup_dir)

    # 清理
    cleaned = deep_clean(content, max_line_length, min_line_length)
    clean_lines = cleaned.splitlines()
    clean_chars = len(cleaned)
    clean_max = max((len(l) for l in clean_lines), default=0)
    clean_long = sum(1 for l in clean_lines if len(l) > max_line_length)

    # 寫回原檔
    with open(src, 'w', encoding='utf-8') as f:
        f.write(cleaned)

    return CleanStats(
        filepath=filepath, orig_chars=orig_chars, clean_chars=clean_chars,
        orig_lines=len(orig_lines), clean_lines=len(clean_lines),
        orig_max_line=orig_max, clean_max_line=clean_max,
        orig_long_lines=orig_long, clean_long_lines=clean_long,
        was_modified=True, backup_path=backup_path
    )


def find_text_files(path: str) -> list[str]:
    """遞迴找出所有 .txt 檔案"""
    p = Path(path)
    if p.is_file():
        return [str(p)]
    if p.is_dir():
        # 跳過備份目錄
        return sorted([
            str(f) for f in p.rglob('*.txt')
            if DEFAULT_BACKUP_SUBDIR not in f.parts
            and not any(part.startswith('.') for part in f.parts)
        ])
    return []


def print_report(stats_list: list[CleanStats], check_only: bool = False):
    """列印處理報告"""
    if not stats_list:
        print("⚠️  沒有找到任何 .txt 檔案")
        return

    total = len(stats_list)
    modified = [s for s in stats_list if s.was_modified]
    skipped = [s for s in stats_list if s.skipped]
    ok = [s for s in stats_list if not s.was_modified and not s.skipped]

    print("═" * 70)
    mode = "🔍 偵測報告" if check_only else "🧹 清理報告"
    print(f"  {mode}")
    print("═" * 70)
    print(f"總計: {total} 個檔案")
    if check_only:
        need_clean = [s for s in stats_list if s.orig_long_lines > 0]
        print(f"  ⚠️  需要清理: {len(need_clean)}")
        print(f"  ✅ 已經正常: {total - len(need_clean)}")
    else:
        print(f"  ✅ 已清理: {len(modified)}")
        print(f"  ⊖  無需清理: {len(ok)}")
        if skipped:
            print(f"  ⏭️  跳過: {len(skipped)}")

    # 詳細列表
    if modified:
        print("\n" + "─" * 70)
        print(f"{'檔案':<45} {'原行長':>8} {'新行長':>8} {'原超長':>6} {'新超長':>6}")
        print("─" * 70)
        for s in modified:
            name = os.path.basename(s.filepath)
            if len(name) > 43:
                name = name[:40] + "..."
            print(f"{name:<45} {s.orig_max_line:>8} {s.clean_max_line:>8} "
                  f"{s.orig_long_lines:>6} {s.clean_long_lines:>6}")

    # 警告
    warning_files = [s for s in stats_list if s.orig_very_long_lines() > 0] if hasattr(CleanStats, 'orig_very_long_lines') else []
    if check_only and need_clean:
        print("\n⚠️  以下檔案有 NotebookLM 匯入失敗風險，建議清理：")
        for s in need_clean:
            print(f"   • {s.filepath}")
            print(f"     max_line: {s.orig_max_line}, "
                  f"long_lines: {s.orig_long_lines}, "
                  f"very_long: {sum(1 for l in open(s.filepath, 'r', encoding='utf-8').read().splitlines() if len(l) > 500)}")

    # 備份資訊
    if modified and any(s.backup_path for s in modified):
        print("\n📦 備份位置：")
        backup_paths = set()
        for s in modified:
            if s.backup_path:
                backup_paths.add(str(Path(s.backup_path).parent))
        for bp in sorted(backup_paths):
            print(f"   {bp}/")

    print("═" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="清理語音直播文字稿，解決 NotebookLM 匯入失敗問題",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例:
  %(prog)s /path/to/transcript.txt
  %(prog)s /path/to/directory/
  %(prog)s /path/a/ /path/b/file.txt --check-only
  %(prog)s /path/to/file.txt --max-line-length 150
  %(prog)s /path/to/file.txt --no-backup
        """
    )
    parser.add_argument('paths', nargs='+', help='檔案或目錄路徑（可多個）')
    parser.add_argument('--max-line-length', type=int, default=DEFAULT_MAX_LINE_LENGTH,
                        help=f'最大行長度（預設 {DEFAULT_MAX_LINE_LENGTH}）')
    parser.add_argument('--min-line-length', type=int, default=DEFAULT_MIN_LINE_LENGTH,
                        help=f'最小行長度，過短行會被視為噪音（預設 {DEFAULT_MIN_LINE_LENGTH}）')
    parser.add_argument('--no-backup', action='store_true', help='不備份原檔（不推薦）')
    parser.add_argument('--backup-dir', type=str, default=None,
                        help='自訂備份目錄')
    parser.add_argument('--check-only', action='store_true', help='只偵測不清理')
    parser.add_argument('--force', action='store_true', help='強制清理（即使行長已達標）')

    args = parser.parse_args()

    # 找出所有 .txt 檔案
    all_files = []
    for path in args.paths:
        files = find_text_files(path)
        all_files.extend(files)

    if not all_files:
        print("⚠️  沒有找到任何 .txt 檔案")
        sys.exit(1)

    # 處理
    stats_list = []
    for filepath in all_files:
        try:
            stats = process_file(
                filepath,
                max_line_length=args.max_line_length,
                min_line_length=args.min_line_length,
                do_backup=not args.no_backup,
                backup_dir=args.backup_dir,
                check_only=args.check_only,
                force=args.force,
            )
            stats_list.append(stats)
        except Exception as e:
            print(f"❌ 處理 {filepath} 時發生錯誤: {e}", file=sys.stderr)
            stats_list.append(CleanStats(
                filepath=filepath, orig_chars=0, clean_chars=0,
                orig_lines=0, clean_lines=0, orig_max_line=0, clean_max_line=0,
                orig_long_lines=0, clean_long_lines=0,
                was_modified=False, backup_path=None,
                skipped=True, skip_reason=str(e)
            ))

    # 報告
    print_report(stats_list, check_only=args.check_only)

    # 退出碼：有錯誤或需要清理時返回非零
    if args.check_only:
        needs_clean = any(s.orig_long_lines > 0 for s in stats_list)
        sys.exit(2 if needs_clean else 0)
    else:
        errors = [s for s in stats_list if s.skipped and s.skip_reason != "file not found"]
        sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
