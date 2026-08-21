---
name: transcript-cleaner
version: 1.0.0
description: |
  處理/清理語音直播文字稿（transcript），解決 NotebookLM 匯入失敗的問題。
  核心功能：將過長的 transcript 行（>200 字）重新分段，並清理噪音行（純標點、極短行），
  使其符合 NotebookLM Markdown parser 的限制。
  適用場景：x-note 產出的 transcript 匯入 NotebookLM 失敗、直播/演講/訪談文字稿
  沒有自然斷行導致 Markdown parser 無法解析。
  觸發詞：「transcript 匯入失敗」「NotebookLM error」「transcript 太長」「語音稿清理」
  「直播文字稿」「長行」「x-note transcript」「清理 transcript」
triggers:
  - "transcript-cleaner"
  - "transcript clean"
  - "清理 transcript"
  - "NotebookLM 匯入失敗"
---

## Description

處理 / 清理語音直播文字稿（transcript），解決 NotebookLM 匯入失敗的問題。

**核心功能**：將過長的 transcript 行（>200 字）重新分段，並清理噪音行（純標點、極短行），使其符合 NotebookLM Markdown parser 的限制。

**觸發時機**：「transcript 匯入失敗」「NotebookLM error」「transcript 太長」「語音稿清理」「直播文字稿」「長行」「x-note transcript」「清理 transcript」。

# transcript-cleaner

## Purpose

`transcript-cleaner` 解決一個非常具體的問題：**x-note 產出的語音直播文字稿匯入 NotebookLM 時一直 `error`**。

問題根因：語音識別 transcript 沒有自然斷行，每段話連成一行 500-1000+ 字。NotebookLM 的 Markdown parser 對超長行（>200 字）處理不穩定，會直接 `error` 拒收。

**注意：這個 skill 處理的「行」是物理行，不是段落。** x-note transcript 是把整段話擠成一行，所以即使有「句號」，物理上還是同一行。

## 為什麼需要這個 skill

### 失敗症狀

```
notebooklm source add file.txt
→ Added source: <id>

（等待 30-60 秒後）
notebooklm source list
→ status: error  ❌
```

### 失敗原因

```python
with open(file) as f:
    lines = f.read().splitlines()
print(max(len(l) for l in lines))
# >>> 939  # 太長！
```

NotebookLM 的 Markdown parser 對超長行（>200 字）會回傳 `null` 結果，整個檔案處理失敗。

### 真實案例

| 檔案 | 最大行長 | 結果 |
|------|---------|------|
| `小翠時政財經2025-09-06 14_10_13.txt` | 789 字 | ❌ error |
| `小翠時政財經2025-10-18 16_32_39.txt` | 939 字 | ❌ error |
| `小翠時政財經 2026-02-13.txt` | 1,167 字 | ❌ error |
| `小翠時政財經 2026-03-20.txt` | 865 字 | ❌ error |
| `直播A_宏觀經濟與聯準會兜底.txt` | 842 字 | ❌ error |

清理後（max 200 字）→ 全部 `ready` ✅

## Core Boundary

`transcript-cleaner` 負責：

- ✅ 偵測 transcript 是否有長行問題
- ✅ 自動備份原檔
- ✅ 清理 transcript（行長 ≤200 字）
- ✅ 驗證清理後的行長
- ✅ 報告清理結果

`transcript-cleaner` **不**負責：

- ❌ 語音識別（這是 x-note 2.0 的工作）
- ❌ 翻譯（這是 x-note-translate 的工作）
- ❌ NotebookLM 帳號認證（CLI 已處理）
- ❌ 內容分類/標籤（這是 note-update 的工作）

## 使用方式

### 1. 快速模式（推薦）

**單一檔案清理**：
```bash
python3 ~/Documents/Agent/skills/transcript-cleaner/scripts/clean_transcript.py /path/to/transcript.txt
```

**目錄批量處理**：
```bash
python3 ~/Documents/Agent/skills/transcript-cleaner/scripts/clean_transcript.py /path/to/directory/
```

**掃描多個目錄**：
```bash
python3 ~/Documents/Agent/skills/transcript-cleaner/scripts/clean_transcript.py \
  /home/pigo/公共/ \
  /home/pigo/下載/
```

### 2. 整合 NotebookLM 流程

清理後直接用 `notebooklm` CLI 上傳：
```bash
# 1. 設定目標 notebook
notebooklm use <notebook-id>

# 2. 上傳清理後的檔案
for f in *.txt; do
  notebooklm source add "$f"
  sleep 3
done

# 3. 等 60 秒後檢查狀態
sleep 60
notebooklm source list
```

### 3. 進階選項

**只偵測不清理**（dry-run）：
```bash
python3 clean_transcript.py /path/to/file.txt --check-only
```

**自訂最大行長**（預設 200）：
```bash
python3 clean_transcript.py /path/to/file.txt --max-line-length 300
```

**跳過備份**（不推薦）：
```bash
python3 clean_transcript.py /path/to/file.txt --no-backup
```

**指定備份目錄**：
```bash
python3 clean_transcript.py /path/to/file.txt --backup-dir /home/pigo/backups/
```

## 清理演算法

```python
def deep_clean(content):
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
        if re.match(r'^[，。、！？：；""''（）【】…—\d\s]+$', line):
            continue

        # 跳過極短行（語音識別錯誤噪音）
        if len(line) < 10:
            continue

        # 將超長行分段
        if len(line) > 200:
            for i in range(0, len(line), 200):
                chunk = line[i:i+200].strip()
                if chunk:
                    cleaned.append(chunk)
        else:
            cleaned.append(line)

    return '\n'.join(cleaned)
```

### 演算法選擇理由

| 參數 | 預設值 | 理由 |
|------|-------|------|
| **最大行長** | 200 字 | NotebookLM parser 的安全閾值（200 字以下 100% 成功） |
| **極短行閾值** | 10 字 | 低於 10 字的「行」幾乎都是語音識別錯誤噪音 |
| **分段大小** | 200 字 | 與最大行長一致，避免產生超長行 |
| **空行保留** | 最多 1 連續 | 保留段落感，但避免無意義空行 |

## 為什麼是 200 字？

經實測：
- ✅ **≤200 字**：100% 成功匯入 NotebookLM
- ⚠️ **201-500 字**：時好時壞（取決於內容）
- ❌ **>500 字**：幾乎 100% 失敗

`200` 是**安全閾值**，留 2x buffer 避免 edge case。

## 與 x-note 的關係

`x-note` v7.2.0 的 transcript 產出格式**就是這個問題的源頭**。理想的長期方案是修改 `x-note` 在產出 transcript 時就做行長限制，但這需要：
- 修改 x-note 的 transcript 產出 pipeline
- 重新處理所有已存在的 transcript

`transcript-cleaner` 是**事後補救方案**，對現有檔案立即見效。

## 對 vault 的影響

清理後的 transcript 應該重新走 `note-update` 流程：
1. 清理 transcript
2. 匯入 NotebookLM（建立知識圖譜）
3. 用 NotebookLM 生成問答/摘要
4. 走 `note-update` 把筆記分類到 vault
5. 更新 vault-index

## Known Limitations

1. **不處理語音識別錯誤**：這個 skill 只分段，不修正 ASR 錯誤
2. **不翻譯**：保留原始語言
3. **不重組段落**：保留原 transcript 的語序（語音識別沒有段落標記）
4. **不支援非純文字**：不處理 PDF、Word、HTML 等格式

## Failure Modes

| 症狀 | 原因 | 解法 |
|------|------|------|
| 清理後仍 `error` | 編碼問題（GBK/Big5） | 確認檔案是 UTF-8 |
| 清理後 `ready` 但內容錯亂 | 200 字分段剛好在詞中間 | 用 `--max-line-length 150` |
| 檔案找不到 | 路徑錯誤 | 用絕對路徑 |

## 與其他 skill 的關係

| Skill | 關係 |
|-------|------|
| `x-note` | 產出 transcript（上游） |
| `x-note2` | 產出更高品質 transcript（上游） |
| `notebooklm` (CLI) | 接收清理後的 transcript（下游） |
| `nuwa-skill` | 用 transcript 蒸餾人物 skill（下游） |
| `note-update` | 處理 NotebookLM 生成的筆記（下游） |
| `vault-reshape` | 整理 vault 結構（下游） |

## Provenance

- provided_by_agent: 通用工具 skill
- provided_by_computer: Pigo workstation
- processing_skill: transcript-cleaner
- processed_at: 2026-06-15
- real_cases_tested: 8 個 transcript 從 `error` → `ready`
- trigger_event: 小翠直播 transcript 匯入 NotebookLM 連續 7 個失敗
