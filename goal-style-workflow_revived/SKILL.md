---
name: goal-style-workflow
description: 目標導向迭代工作流。適用：複雜任務（研究、翻寫、代碼遷移）、需要驗證的多步任務、超過 3 個 sub-step 的任何工作。基於 Claude Code /goal 模式，適用於 Hermes 環境。
trigger: 當用戶說「研究某主題」、「目標導向」、「迭代直到完成」、「goal-style」時觸發
category: workflow
---

# Goal-Style Workflow Skill

**重要：所有輸出內容必須使用繁體中文。**

## 什麼是 Goal-Style Workflow

不同於一次性 prompt 的 Turn-based 模式，Goal-Style 是：

```
定義目標 → 拆解 sub-tasks → 執行每個 sub-task → 驗證每個結果 → 失敗就重做 → 全部通過才交付
```

核心精神：**獨立 verifier**，不是 agent 自己 critiques 自己。

---

## 觸發條件

滿足任一即觸發：
- 用戶說「研究 X」（超 500 字輸入）
- 任務超過 3 個 sub-step
- 任務需要交付可驗證的產出（不是「回答問題」而是「完成 artifact」）
- 用戶明確說「goal-style」或「目標導向」

---

## 執行流程（6 步）

### Step 1：定義 Goal

明確寫出：
- **目標**（Goal）：最終交付物是什麼？
- **成功標準**（Success Criteria）：怎麼算完成了？
- **最大迭代次數**（max_iterations）：失敗幾次後放棄？

```
Goal: 把這篇 Fable 5 文章轉化為 Hermes 行動項
Success Criteria:
  ✓ 4 種 loop types 全部正確識別
  ✓ 每種 loop 都有 ≥1 個 Hermes 對應
  ✓ 輸出是可執行的 action items，不是摘要
  ✓ vault note 的 frontmatter score ≥ 8.5
max_iterations: 3
```

### Step 2：拆解 Sub-Tasks

把 Goal 拆成 N 個獨立的 sub-task，每個 sub-task 要有：
- 明確的產出描述
- 獨立的可驗證標準

```
Sub-task 1: 解析文章內容（done → 11507 chars loaded）
Sub-task 2: 擷取 4 種 loop types
Sub-task 3: 映射到 Hermes cron/job components
Sub-task 4: 識別具體改進行動
Sub-task 5: 寫入 vault note
Sub-task 6: 驗證輸出品質
```

### Step 3：執行 Sub-Tasks

每個 sub-task 獨立執行。**每個 sub-task 完成後立即驗證**，失敗就重做，不要累積到最後。

```python
# 驗證模式（每個 sub-task 後）
def verify_subtask(output, criteria):
    if not criteria_check(output, criteria):
        return False, "failed: <reason>"
    return True, "passed"
```

### Step 4：驗證點（Checkpoint）

每個 sub-task 完成後記錄：

| Sub-task | 產出 | 驗證結果 |
|----------|------|---------|
| 1 | 11507 chars loaded | ✓ |
| 2 | 4 loop types extracted | ✓ |
| 3 | Hermes mappings identified | ✓ |
| 4 | 3 action items written | ✓ |
| 5 | vault note written (3494 bytes) | ✓ |
| 6 | 5/5 verification checks passed | ✓ |

### Step 5：失敗重做邏輯

```
if not verified:
    iteration += 1
    if iteration > max_iterations:
        deliver_partial()  # 把通過的部分交付，標記未完成
        break
    else:
        redo_subtask()  # 重做這個 sub-task
```

### Step 6：交付

達到 Success Criteria 後，交付包含：
- 最終產出（vault note / 文件 / 摘要）
- 驗證結果摘要
- 如有部分未通過，說明原因和替代方案

---

## 驗證標準模板

每個 Goal-Style 任務必須包含：

```
verification_criteria:
  - name: "<檢查項名>"
    method: "<如何驗證>"
    threshold: "<標準>"
```

---

## 已知失敗模式

### 1. Subagent 隔離 context 問題
**問題**：當用 `delegate_task` 派 subagent 時，subagent 的 context 與主 session 隔離，無法讀取主 session 的 `/tmp/` 檔案。

**徵兆**：subagent 報告 `file not found`，但檔案確實存在。

**解決**：在派 subagent 前，把必要的資料明確寫入 subagent 的 `context` 參數，或確保資料在 subagent 可見的路徑（如 `~/Downloads/`）。

**預防**：Goal-Style 的關鍵資料（評分公式、keep list、threshold）在派 subagent 前寫入 `context`，不要假設 subagent 能從 `/tmp/` 讀取。

### 2. 驗證點遺漏
**問題**：跳過 checkpoint 直接往前衝，失敗後不知道哪個 sub-task 出問題。

**解決**：嚴格執行 Step 4，每個 sub-task 完成後立即記錄驗證結果。

### 3. 過度交付
**問題**：把不相關的內容也寫進 vault note。

**解決**：Goal-Style 只交付符合 Success Criteria 的內容，其他資訊寫入「相關資料」章節，不混入主體。

---

## 與其他模式的區別

| 模式 | 觸發 | 停止條件 |
|------|------|---------|
| Turn-based | 用戶 prompt | Claude 自己覺得完成了 |
| Goal-Style | 明確 Goal + Success Criteria | 達標或 max_iterations 到 |
| Time-based | 時間間隔 | 手動取消或工作完成 |
| Proactive | 事件觸發 | 各任務達標後陸續退出 |

Goal-Style 適合 **一次性的複雜工作**；Time-based 適合 **重複性的常態工作**。

---

## 範例：Fable 5 Loop 設計文章

這次執行的完整案例：

**Goal**: 把 Fable 5 Loop 設計文章轉化為 Hermes 改進行動項
**Success Criteria**: 4 loop types × Hermes mapping + 3 action items + vault write
**max_iterations**: 2

**結果**：
- Sub-task 1-5 一次通過
- Sub-task 6 第一次 fail（firewall 問題），第二次通過
- 最終：vault note 3494 bytes，5/5 checks passed

---

## 與 cron quality gate 的配合

Goal-Style 適合：
- 複雜 research 任務
- 單篇文章的深度翻寫
- 需要迭代的 multi-step coding 任務

Cron Quality Gate 適合：
- 每日重複的攝入工作（KAW、晚報）
- 已經定義好品質標準的常態流程

**組合使用**：複雜任務走 Goal-Style；常態任務走 Time-based + quality gate。
