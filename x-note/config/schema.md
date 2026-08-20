# x2-note Config Schema

x2-note 從 `.path-config.json` 讀取機器特定設定。

## 必要設定

```json
{
  "VAULT_ROOT": "E:\\obsidian",
  "AGENT_ROOT": "E:\\python_Code\\Agent",
  "DOWNLOADS": "C:\\Users\\pigow\\Downloads",
  "CDP_PORT": 19825,
  "CHROME_PROFILE_NAME": "Hsiaopigo",
  "CHROME_EXE": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "TWITTER_HANDLE_FILE": "E:\\python_Code\\Agent\\name.md",
  "X_COOKIES_FILE": "C:\\Users\\pigow\\Downloads\\x_cookies_logged_in.json"
}
```

## 設定優先順序

```
1. .path-config.json  ← 機器特定（不上 git）
2. VAULT/_config/x2-note-handles.md  ← 帳號清單 fallback
3. AGENT_ROOT/name.md  ← 預設帳號清單
```

## 欄位說明

| 變數 | 用途 | 預設 |
|------|------|------|
| `VAULT_ROOT` | Vault 根目錄 | 必填 |
| `AGENT_ROOT` | Agent 根目錄 | 必填 |
| `DOWNLOADS` | cookies / fetch 暫存 | 必填 |
| `CDP_PORT` | Chrome Debug Port | 19825 |
| `CDP_START_WAIT` | CDP 啟動後等待秒數 | 5 |
| `CHROME_PROFILE_NAME` | Chrome Profile 名稱 | Hsiaopigo |
| `CHROME_EXE` | Chrome 執行檔路徑 | Program Files 預設 |
| `CHROME_USER_DATA_DIR` | Chrome User Data 根 | %LOCALAPPDATA%\\Google\\Chrome\\User Data |
| `TWITTER_HANDLE_FILE` | 帳號清單路徑 | name.md |
| `X_COOKIES_FILE` | 已登入 cookies | x_cookies_logged_in.json |
| `X2_MIN_SCORE` | 過濾分數門檻 | 6.5 |
| `X2_LIMIT_HANDLES` | 測試用帳號上限 | 5 |
| `X2_DRY_RUN` | 只抓不寫 | false |
| `X2_HEADLESS` | 無頭模式 | true |
| `X2_FXTWITTER_HOST` | fxtwitter API host | https://api.fxtwitter.com |

## 範例

```json
{
  "_note": "user config",
  "VAULT_ROOT": "E:\\obsidian",
  "AGENT_ROOT": "E:\\python_Code\\Agent",
  "DOWNLOADS": "C:\\Users\\pigow\\Downloads",
  "CDP_PORT": 19825,
  "CHROME_PROFILE_NAME": "Hsiaopigo",
  "CHROME_EXE": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "TWITTER_HANDLE_FILE": "E:\\python_Code\\Agent\\name.md",
  "X_COOKIES_FILE": "C:\\Users\\pigow\\Downloads\\x_cookies_logged_in.json",
  "X2_MIN_SCORE": 6.5,
  "X2_LIMIT_HANDLES": 5,
  "X2_HEADLESS": true
}
```
