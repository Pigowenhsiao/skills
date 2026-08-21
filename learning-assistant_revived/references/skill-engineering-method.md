# Skill Engineering Method — yao framework

## 5 分鐘創作流程

### 流程步驟

1. **Raw Note → SKILL.md + agents/interface.yaml**
   - 從用戶需求產出基礎 SKILL.md
   - 從 SKILL.md 推導 interface.yaml

2. **Validate Trigger**
   - 確認觸發條件夠精確，不會誤觸也不會漏觸
   - 檢查名稱是否描述了真正的工作而非工具

3. **Export Adapters**
   - 確認 canonical_format 正確
   - 檢查 degradation 策略是否合理

4. **Compare with Examples**
   - 對照 simple-note-cleanup 的完整度
   - 確認必備區塊齊備

### 必備區塊（Checklist）

- [ ] name + description
- [ ] trigger conditions（觸發條件）
- [ ] workflow（工作流程）
- [ ] output quality risk control（輸出品質風險）
- [ ] failure library（失敗模式）
- [ ] agents/interface.yaml

### 評估維度

- **Trigger Precision**：觸發條件精確度（0-10）
- **Context Budget**：上下文消耗（max 1000）
- **Governance Maturity**：治理成熟度（root/100）
