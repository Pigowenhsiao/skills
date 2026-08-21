# 咨询报告视觉

```yaml
id: consulting-report-visual
name: 咨询报告视觉
input_modes: [text]
subjects: [concept, object, scene]
outputs: [cover, poster, editorial_page]
default_ratio: "2.35:1"
required_fields: [主题词, 画幅比例, 语言, 用途]
optional_fields: [副标题, 补充背景, 情绪倾向, 不想出现的元素]
source: skills/punk-cover/references/templates/consulting-report-visual.md
style_anchors:
  - high-end management consulting report cover
  - rational grid, matrix, path, coordinate, and framework logic
  - structured business metaphor such as value chain, funnel, flywheel, network, or strategic map
  - restrained professional colors with small accent
  - precise thin lines, nodes, arrows, labels, and section hierarchy
cover_shape_adaptation:
  - main title should interlock with a framework, path, matrix boundary, or strategic map
  - subtitle and supporting text should look like report cover deck and labels, not social-media decoration
  - visual metaphor should abstract the business system without becoming a full slide
must_preserve:
  - clear information hierarchy
  - professional restraint and credible business structure
  - title remains dominant over diagrams
avoid_when_applying_to_cover:
  - fake detailed data, dense charts, or unreadable small text
  - PPT template feel or course-cover feel
  - generic office scene, handshake, or stock business people
```

## Style Intent

咨询报告、管理框架和结构化商业分析风格。强调清晰层级、图形化秩序、专业信息密度和可信的企业视觉。该 style 只负责咨询报告式视觉语言和商业结构隐喻；平台适配、长文提炼和通用封面约束由 `punk-cover` 负责。

## Use For

- 商业策略、运营、产品分析、行业研究和方法论
- 公众号封面、报告题图、结构化商业文章头图
- 需要理性、清晰、专业的内容

## Avoid

- 虚假数据、复杂图表堆叠
- 过度装饰或社媒噪音
- 无关办公场景和廉价商务人物
