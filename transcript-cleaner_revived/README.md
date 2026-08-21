<!-- BEGIN AGENT_DIRECTORY_README -->
# transcript-cleaner

## Purpose

解決一個非常具體的問題：**x-note 產出的語音直播文字稿匯入 NotebookLM 時一直 `error`**。

問題根因：x-note transcript 沒有自然斷行，每段話連成一行 500-1000+ 字。NotebookLM 的 Markdown parser 對超長行（>200 字）處理不穩定，會回傳 null 結果，整個檔案處理失敗。

這個 skill 提供一個 Python 工具，能：
1. 偵測 transcript 是否有長行問題
2. 自動備份原檔
3. 將超長行重新分段（預設每段 ≤200 字）
4. 清理噪音行（純標點、極短行、連續空行）
5. 寫回原檔
6. 報告清理結果

## 目錄結構

```
transcript-cleaner/
├── SKILL.md                       # Skill 說明文件
├── README.md                      # 本檔案
└── scripts/
    └── clean_transcript.py        # 主要工具腳本
```

## 安裝

無需安裝。只需 Python 3.7+ 標準庫（已內建）。

## 快速開始

### 偵測問題檔案

```bash
python3 ~/Documents/Agent/skills/transcript-cleaner/scripts/clean_transcript.py \
  /home/pigo/公共/ \
  --check-only
```

輸出：
```
⚠️  需要清理: 7
✅ 已經正常: 0
```

### 清理單一檔案

```bash
python3 ~/Documents/Agent/skills/transcript-cleaner/scripts/clean_transcript.py \
  /path/to/transcript.txt
```

### 批量清理整個目錄

```bash
python3 ~/Documents/Agent/skills/transcript-cleaner/scripts/clean_transcript.py \
  /home/pigo/公共/ \
  /home/pigo/下載/
```

### 整合 NotebookLM 上傳流程

```bash
# 1. 清理
python3 ~/Documents/Agent/skills/transcript-cleaner/scripts/clean_transcript.py /path/to/transcripts/

# 2. 上傳
notebooklm use <notebook-id>
for f in /path/to/transcripts/*.txt; do
  notebooklm source add "$f"
  sleep 3
done

# 3. 驗證
sleep 60
notebooklm source list
```

## 參數說明

| 參數 | 預設值 | 說明 |
|------|-------|------|
| `paths` | (必填) | 檔案或目錄路徑（可多個） |
| `--max-line-length` | 200 | 最大行長度 |
| `--min-line-length` | 10 | 最小行長度（噪音過濾） |
| `--no-backup` | False | 不備份原檔（不推薦） |
| `--backup-dir` | None | 自訂備份目錄 |
| `--check-only` | False | 只偵測不清理 |
| `--force` | False | 強制清理（即使行長已達標） |

## 退出碼

| 退出碼 | 含義 |
|-------|------|
| 0 | 成功 / 所有檔案正常 |
| 1 | 有錯誤（編碼錯誤、檔案損壞等）|
| 2 | `--check-only` 模式下發現需要清理的檔案 |

## 與其他 Skill 的關係

```
x-note (產出 transcript)
  ↓
transcript-cleaner (清理超長行) ← 本 skill
  ↓
notebooklm (匯入並建立知識圖譜)
  ↓
nuwa-skill (蒸餾人物 skill)
```

## 已知限制

1. **不處理語音識別錯誤**：只分段，不修正 ASR 錯誤
2. **不翻譯**：保留原始語言
3. **不重組段落**：保留原 transcript 的語序
4. **不支援非純文字**：不處理 PDF、Word、HTML 等格式
5. **GBK/Big5 編碼**：自動 fallback 到 GBK，但建議先轉 UTF-8

## 觸發詞

- 「transcript 匯入失敗」
- 「NotebookLM error」
- 「transcript 太長」
- 「語音稿清理」
- 「直播文字稿」
- 「長行」
- 「x-note transcript」

## Provenance

- provided_by_agent: 通用工具 skill
- provided_by_computer: Pigo workstation
- processing_skill: transcript-cleaner
- processed_at: 2026-06-15
- real_cases_tested: 8 個 transcript 從 `error` → `ready`
- trigger_event: 小翠直播 transcript 匯入 NotebookLM 連續 7 個失敗
<!-- END AGENT_DIRECTORY_README -->
