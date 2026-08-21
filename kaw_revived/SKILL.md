---
name: kaw
description: KAW（Kanban Add to Vault）= 收到 URL 時自動建立 llm-wiki summary 任務到 execution board。觸發時機：收到「KAW <url>」或「kaw <url>」指令，解析 URL 並創建標準化 Kanban 任務。
version: 1.0.0
platforms: [linux, macos, telegram]
metadata:
  hermes:
    tags: [kanban, automation, x-note, quick-command]
    trigger: ["kaw <url>", "KAW <url>"]
    idempotency: "x-{status_id}"
---

# KAW — Kanban Add to Vault

## 觸發條件

收到以下任一指令：
- `kaw <url>`
- `KAW <url>`

URL 格式：`https://x.com/<handle>/status/<id>`

## 執行流程

1. 解析 URL，擷取 `handle` 和 `status_id`
2. 執行 `hermes kanban create` 創建任務
3. Task ID：`t_<hex>`
4. 回覆 Pigo 任務 ID

## 快捷方式

在 Telegram 傳送：
```
KAW https://x.com/AIwithSynthia/status/2057798813893702095
```

等於手動執行：
```bash
/home/pigo/bin/kaw "https://x.com/AIwithSynthia/status/2057798813893702095"
```

## Task 模板

```
標題：llm-wiki summary: @<handle> 推文
執行者：researcher
技能：llm-wiki、x-note
Body：完整步驟說明（見 bin/kaw）
idempotency-key：x-{status_id}
```

## 注意

- 重複 URL 不會建立兩條任務（idempotency-key 防呆）
- 任務會在 5 分鐘內被 Dispatcher 派發執行
- 完成後 Dispatcher 會主動通知 Pigo（memory 規則）