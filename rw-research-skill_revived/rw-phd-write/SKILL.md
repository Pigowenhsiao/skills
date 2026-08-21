---
name: rw-phd-write
description: |
  根据用户提供的研究材料和可核验来源组织论文或 PhD 章节，不依赖个人本地语料。 Use when the user asks for “写 PhD 章节”、“修改论文论证”、“根据来源写学术段落”, or requests the rw-phd-write workflow. Runs without a private local workspace or preset research-lab; use user-provided material and bundled public-source methods.
---

# RW PhD Write

根据用户提供的研究材料和可核验来源组织论文或 PhD 章节，不依赖个人本地语料。

## 启动

1. 读取 `references/standalone.md`、`references/method.md` 和 `references/standards.md`。
2. 读取用户本轮提供的材料；没有材料时，只完成当前证据允许的部分。
3. 需要规则判断时检索 `references/atoms.jsonl`；遇到相似任务时读取 `references/cases.md`。
4. 需要选择方法或工具时读取 `references/domain-guide.md`，并使用 `assets/worksheet.md` 组织交付。
5. 读取 `references/acceptance.md`。`references/behavior-tests.json` 只用于测试，不作为用户任务事实。
6. 当前文献、API、报告规范和期刊要求可能变化时，打开 `references/source-map.md` 中的官方链接核验并记录日期。

## 工作阶段

1. 确认章节类型、章节功能、读者、目标主张和允许使用的材料。
2. 建立 claim-to-source 表，区分事实、作者解释、当前推断和未知事项。
3. 按章节功能组织论证移动、段落顺序和限制位置。
4. 先写论点和证据骨架，再写正文，不生成未核验引用。
5. 按研究类型检查相应报告规范、方法透明度和披露事项。
6. 运行来源、因果强度、前后一致性、作者语气和修改范围检查。

## 运行规则

- 写作从章节功能和主张开始，不从漂亮句子开始。
- 每个事实性主张都要有用户材料或可核验来源。
- 来源支持范围小于句子范围时，收窄句子。
- 结果、解释、推断和建议要使用不同的证据强度。
- Introduction 建立问题和缺口，不能提前假定研究结论。
- Methods 说明做了什么和为何这样做，不能用结果合理化方法。
- Results 报告预定和实际分析，不用 Discussion 语言解释。
- Discussion 先回答研究问题，再比较证据、解释限制和外推边界。
- 报告规范是最低透明度检查，不是段落模板。
- 用户修改要求优先保留原判断、证据和限制。
- 没有作者语料时使用克制的学术注册，不冒充个人指纹。
- 引用、作者贡献、利益冲突和 AI 使用按目标期刊当前规则核验。

## 输出

- 章节、段落或论证骨架。
- claim-to-source 表和引用缺口。
- 修改说明、未解决问题和合规检查。

## 停止条件

- 没有来源时，不生成事实性引用或伪造 DOI。
- 没有研究结果时，不写成研究已完成。
- 不为流畅删除限制、反例和不确定性。
- 不把 Skill 输出当成作者最终责任或期刊合规确认。

## 独立运行

- 默认不读取私人工作区、个人语料目录或预设 research-lab。
- 用户提供的文件、文本、链接和数据是当前任务输入，不是安装依赖。
- 网络不可用时，使用 Skill 内的稳定方法继续；需要当前事实的部分标记为待核验。
- 本包内其他科研 Skill 存在时可以接续；单独安装时直接返回下一步说明，不停止当前任务。

## 来源纪律

- 把用户材料、公开来源、当前推断和未知事项分开。
- 报告规范只检查报告透明度，不自动证明设计质量。
- 公开来源摘要保存在 Skill 内；需要版本、费用、政策、API 或期刊现状时回到官方页面。
- 不生成不存在的论文、数据、DOI、工具运行结果或期刊要求。
