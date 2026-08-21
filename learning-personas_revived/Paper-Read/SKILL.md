# Skill Definition: Academic-Omni-Router

> **Description**: The central dispatcher that routes user queries to specialized radar modules stored in the reference directory.
> **Author**: Gemini-Prime
> **Version**: 3.2.0 (Path-Aware)
> **Format**: YAML Configuration

---

```yaml
skill_definition:
  metadata:
    name: "Academic-Omni-Router"
    id: "skill_omni_router_v3_2"
    description: "Intelligent router that loads specialized audit protocols from the reference directory."
    language: "Traditional Chinese (繁體中文)"

  # ==========================================
  # 檔案路徑配置 (File Path Configuration)
  # ==========================================
  file_system:
    base_directory: "reference/"
    modules:
      psychology: "Psychology_Radar.md"
      biology: "Bio_Radar.md"

  # ==========================================
  # 路由邏輯 (Router Logic)
  # ==========================================
  router_rules:
    - rule_id: "MODE_PSYCH"
      trigger_keywords:
        - "心理"
        - "認知"
        - "行為"
        - "社會科學"
        - "憂鬱"
        - "Psychology"
        - "Neuroscience (Cognitive)"
      action:
        target_file: "reference/Psychology_Radar.md"
        description: "Load Psychology Audit Protocol"

    - rule_id: "MODE_BIO"
      trigger_keywords:
        - "生科"
        - "醫學"
        - "基因"
        - "癌症"
        - "免疫"
        - "Biology"
        - "Clinical"
        - "Mechanism"
      action:
        target_file: "reference/Bio_Radar.md"
        description: "Load Bio-Medical Audit Protocol"

  # ==========================================
  # 執行工作流 (Execution Workflow)
  # ==========================================
  workflow:
    step_1_analysis:
      action: "Intent Detection"
      instruction: "Analyze the user's prompt to identify the primary research domain (Psychology vs. Biology)."

    step_2_routing:
      action: "Module Selection"
      logic: |
        IF keywords match MODE_PSYCH THEN set target = reference/Psychology_Radar.md
        ELSE IF keywords match MODE_BIO THEN set target = reference/Bio_Radar.md
        ELSE ask user for clarification.

    step_3_loading:
      action: "Context Ingestion"
      instruction: "Read/Retrieve the content of the [target_file] from the reference directory. Apply its YAML rules as the current system instruction."

    step_4_execution:
      action: "Radar Execution"
      instruction: "Execute the 'Audit Workflow' defined in the loaded submodule using the user's specific topic."

  # ==========================================
  # 觸發範例 (Triggers)
  # ==========================================
  triggers:
    - user_input: "幫我查一下最新的阿茲海默症代謝研究"
      system_process:
        1. Detect: "代謝", "阿茲海默" -> Matches MODE_BIO
        2. Load: reference/Bio_Radar.md
        3. Execute: Bio-Sci-Radar Protocol

    - user_input: "啟動雷達，分析社群媒體的同溫層效應"
      system_process:
        1. Detect: "社群", "同溫層" -> Matches MODE_PSYCH
        2. Load: reference/Psychology_Radar.md
        3. Execute: Psy-Scholar-Radar Protocol