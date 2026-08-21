---
name: self-critique-panel
description: Execute a structured self-critique workflow from a user task by generating an initial draft prompt, creating or using multiple personas, running persona-by-persona critique with supplementation and concrete fixes, and synthesizing everything into a corrected final output. Use when the user asks for 自我批評, 多角色批評, 顧問團 review, 紅隊審查, 角色辯論, stress-test, or when a proposal, report, plan, or draft should be improved through competing expert viewpoints.
---

# 自我批評

## Description

The `self-critique-panel` skill is for executing a structured self-critique workflow from a user task by generating an initial draft prompt, creating or using multiple personas, running persona-by-persona critique with supplementation and concrete fixes, and synthesizing everything into a corrected final output.

Execute a structured self-critique workflow from a user task by generating an initial draft prompt, creating or using multiple personas, running persona-by-persona critique with supplementation and concrete fixes, and synthesizing everything into a corrected final output. Use it when the user asks for 自我批評, 多角色批評, 顧問團 review, 紅隊審查, 角色辯論, stress-test, or when a proposal, report, plan, or draft should be improved through competing expert viewpoints.

## Objective

嚴格依照多角色自我批評流程執行任務。
這不是模擬流程，而是真實執行任務的工作流。
直接輸出，不需解釋流程本身。

## Runtime Assumptions

- Treat the user's message as `@task`.
- If personas are already supplied, use them.
- If personas are missing, create at least five clearly differentiated personas.
- Prefer Traditional Chinese Markdown.
- If canvas is available and useful for draft iteration, start it.

## Required Workflow

### Step 1: Initial Draft

1. Derive an initial prompt from the task as if asking a model how it should be instructed to complete the task.
2. Execute that prompt mentally and produce an initial draft.
3. Print:
   - `## 自我批評流程: {task}`
   - `## 角色人設清單:`
   - the persona object
   - `##### 初始draft:`
   - the derived prompt text
   - the initial draft content

### Step 2: Persona Critique Loop

For each persona:

1. Print `### {persona_name}`.
2. Enter that role cleanly and independently.
3. Review the current accumulated result.
4. Provide all three:
   - 詳盡補充
   - 明確批評
   - 具體解決方案

Do not let later personas collapse into the same voice as earlier personas.

### Step 3: Final Merge

After all personas have contributed:

1. Enter the role `萬能的小編`.
2. Read all persona outputs.
3. Absorb all key knowledge, critiques, and proposed corrections.
4. Repair the weaknesses identified by the personas.
5. Print one integrated final result in natural language.

## Persona Rule

If personas must be generated automatically, create at least five roles with different:

- incentives
- viewpoints
- expertise
- risk tolerance
- contribution style

Examples of valid spread:

- strategy
- user research
- technical architecture
- market operations
- legal or compliance

## Critique Quality Rule

Each persona must do more than point out problems.
Each persona must add missing detail, explain what is wrong, and propose a realistic correction.

## Merge Quality Rule

- Do not drop a persona's major contribution.
- Do not merely list comments.
- Produce a corrected and integrated final version.
- Preserve disagreements when they reflect real tradeoffs.

## References

- For default panel patterns and synthesis guidance, read [references/panel-patterns.md](references/panel-patterns.md).
- For quick persona scaffolding by task family, use [scripts/panel_scaffold.py](scripts/panel_scaffold.py).

## Example Requests

- `請對這份產品策略做自我批評`
- `先產生初稿，再用五位不同顧問批評與修正`
- `幫我把這份研究計畫走完多角色自我批評流程`
