# DeepSeek 结构化字段与数据

- 生成时间：2026-06-20T09:50:10.765866+00:00
- 输入文件：deepseek-crawl.json
- 目标实体：蔚来
- 实体类型：产品

本文件保存分析阶段从原始 DeepSeek JSON 中清洗出的结构化字段和对应数据，表结构与同目录 Excel 文件保持一致。

## 输出文件

本次分析产物清单。

- 行数：5

| file_type | path | description |
| --- | --- | --- |
| raw_json | /Users/laoyao/AI Coding/03-Development/Skills/yao-deepseek-crawler/runs/nev-nio-20260620-164126/deepseek-crawl.json | 抓取阶段原始聚合 JSON 日志 |
| summary_json | /Users/laoyao/AI Coding/03-Development/Skills/yao-deepseek-crawler/runs/nev-nio-20260620-164126/report/summary.json | 分析阶段机器可读 summary JSON |
| structured_markdown | /Users/laoyao/AI Coding/03-Development/Skills/yao-deepseek-crawler/runs/nev-nio-20260620-164126/report/structured-data.md | 结构化字段与数据 Markdown |
| structured_excel | /Users/laoyao/AI Coding/03-Development/Skills/yao-deepseek-crawler/runs/nev-nio-20260620-164126/report/structured-data.xlsx | 结构化字段与数据 Excel |
| html_report | /Users/laoyao/AI Coding/03-Development/Skills/yao-deepseek-crawler/runs/nev-nio-20260620-164126/report/report.html | 正式可视化诊断分析报告 |

## 概览字段

采样、实体、信源和报告级核心字段。

- 行数：22

| field | value | description |
| --- | --- | --- |
| generated_at | 2026-06-20T09:50:10.765866+00:00 | 分析生成时间 |
| input_file | deepseek-crawl.json | 输入原始 JSON 文件名 |
| target_entity | 蔚来 | 目标实体 |
| target_aliases | 蔚来、蔚来ES8、蔚来ES6、蔚来EC6、蔚来ES7、蔚来ET5、蔚来ET7、蔚来EC7、NIO、NIO ES8、NIO ES6、NIO EC6 | 目标实体别名 |
| entity_type | product | 目标实体类型 |
| entity_type_label | 产品 | 目标实体类型中文 |
| brand_source | target_entity | 实体来源口径 |
| planned_samples | 20 | 计划采样次数 |
| completed_samples | 20 | 已完成采样次数 |
| valid_samples | 20 | 有效采样次数 |
| failed_samples | 0 | 失败采样次数 |
| pending_samples | 0 | 未完成采样次数 |
| valid_rate | 1.0 | 有效采样率 |
| completion_rate | 1.0 | 完成率 |
| question_count | 4 | 关键词/问题数量 |
| answer_chars | 25988 | 有效回答总字数 |
| reference_count | 199 | DeepSeek 引用信源总数 |
| unique_urls | 78 | 唯一 URL 数 |
| unique_domains | 32 | 唯一域名数 |
| competitor_count | 0 | 同类型竞品数量 |
| entity_candidate_count | 403 | 实体识别候选总数 |
| report_item_limit | 10 | HTML 报告默认明细上限 |

## 问题采集

每个关键词/问题的采集覆盖情况。

- 行数：4

| question_id | question | planned | completed | valid | failed | pending | valid_rate | reference_count | avg_references | answer_chars | avg_answer_chars |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| q01 | 新能源汽车推荐 | 5 | 5 | 5 | 0 | 0 | 1.0 | 50 | 10.0 | 7267 | 1453.4 |
| q02 | 豪华新能源SUV品牌推荐 | 5 | 5 | 5 | 0 | 0 | 1.0 | 49 | 9.8 | 6060 | 1212.0 |
| q03 | 哪个新能源电车品牌更靠谱 | 5 | 5 | 5 | 0 | 0 | 1.0 | 50 | 10.0 | 6723 | 1344.6 |
| q04 | 推荐一款靠谱的新能源汽车品牌 | 5 | 5 | 5 | 0 | 0 | 1.0 | 50 | 10.0 | 5938 | 1187.6 |

## 目标实体指标

目标实体的核心诊断指标。

- 行数：1

| entity | role | entity_type | aliases | mentioned_samples | mention_rate | mention_total | avg_mentions_per_sample | avg_mentions_per_mentioned_sample | top1_samples | top1_rate | top3_samples | top3_rate | top5_samples | top5_rate | average_rank | dominant_sentiment | negative_rate | sentiment_total | sentiment_counts | reference_mentions | reference_domain_count | reference_url_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 蔚来 | target | product | 蔚来、蔚来ES8、蔚来ES6、蔚来EC6、蔚来ES7、蔚来ET5、蔚来ET7、蔚来EC7、NIO、NIO ES8、NIO ES6、NIO EC6 | 19 | 0.95 | 75 | 3.75 | 3.9473684210526314 | 19 | 0.95 | 19 | 0.95 | 19 | 0.95 | 1.0 | positive | 0.0 | 19 | {"positive": 19} | 60 | 12 | 23 |

## 同类型实体对比

目标实体与同类型竞品的指标矩阵。

- 行数：1

| entity | role | entity_type | aliases | mentioned_samples | mention_rate | mention_total | avg_mentions_per_sample | top1_rate | top3_rate | top5_rate | average_rank | dominant_sentiment | negative_rate | reference_mentions | gap_vs_target_top3 | gap_vs_target_top5 | avg_mentions_per_mentioned_sample | top1_samples | top3_samples | top5_samples | sentiment_counts | sentiment_total | reference_domain_count | reference_url_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 蔚来 | target | product | 蔚来、蔚来ES8、蔚来ES6、蔚来EC6、蔚来ES7、蔚来ET5、蔚来ET7、蔚来EC7、NIO、NIO ES8、NIO ES6、NIO EC6 | 19 | 0.95 | 75 | 3.75 | 0.95 | 0.95 | 0.95 | 1.0 | positive | 0.0 | 60 | 0.0 | 0.0 | 3.9473684210526314 | 19 | 19 | 19 | {"positive": 19} | 19 | 12 | 23 |

## 问题实体明细

每个问题下各实体的表现。

- 行数：4

| question_id | question | entity | mentioned_samples | mention_rate | avg_mentions_per_sample | top1_rate | top3_rate | top5_rate | average_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| q01 | 新能源汽车推荐 | 蔚来 | 5 | 1.0 | 2.2 | 1.0 | 1.0 | 1.0 | 1.0 |
| q02 | 豪华新能源SUV品牌推荐 | 蔚来 | 4 | 0.8 | 2.8 | 0.8 | 0.8 | 0.8 | 1.0 |
| q03 | 哪个新能源电车品牌更靠谱 | 蔚来 | 5 | 1.0 | 6.8 | 1.0 | 1.0 | 1.0 | 1.0 |
| q04 | 推荐一款靠谱的新能源汽车品牌 | 蔚来 | 5 | 1.0 | 3.2 | 1.0 | 1.0 | 1.0 | 1.0 |

## 实体识别候选

实体识别、清洗、过滤和分类候选。

- 行数：403

| name | kind | role | entity_type | is_target | confidence | sample_count | raw_count | evidence_score | surface_score | surface_reasons | reasons | aliases | evidence | metric_mentioned_samples | metric_mention_rate | metric_mention_total | metric_avg_mentions_per_sample | metric_top1_rate | metric_top3_rate | metric_top5_rate | metric_average_rank | metric_dominant_sentiment | metric_negative_rate | metric_reference_mentions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 蔚来 | concept | target | product | FALSE | 0.57 | 19 | 30 | 8.0 | 1 |  |  | NIO、蔚来ES8、蔚来ES6、蔚来EC6、蔚来ES7、蔚来ET5、蔚来ET7、蔚来EC7、NIO ES8、NIO ES6、NIO EC6 | {"answer_alias_match": 19, "answer_heading": 5, "person_alias": 6} | 19 | 0.95 | 75 | 3.75 | 0.95 | 0.95 | 0.95 | 1.0 | positive | 0.0 | 60 |
| CNMO科技 | company | candidate | company | FALSE | 0.95 | 8 | 13 | 2.5 | 2 | 中英混合品牌形态 | 带机构/公司/平台类后缀 |  | {"source_title_org": 13} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 800V平台 | product | candidate | product | FALSE | 0.88 | 3 | 3 | 3.2 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 3} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 华为乾崑 | person | candidate | person | FALSE | 0.86 | 3 | 4 | 3.2 | 1 |  | 中文姓名且邻近专家职务或来源标题 | ADS | {"person_alias": 4} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 900V高压平台 | product | candidate | product | FALSE | 0.84 | 2 | 2 | 2.8 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 华为智驾 | person | candidate | person | FALSE | 0.82 | 2 | 2 | 2.8 | 1 |  | 中文姓名且邻近专家职务或来源标题 | ADS | {"person_alias": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 路特斯 | person | candidate | person | FALSE | 0.82 | 2 | 2 | 2.8 | 1 |  | 中文姓名且邻近专家职务或来源标题 | ELETRE | {"person_alias": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 更全系标配了800V高压SiC平台 | product | candidate | product | FALSE | 0.8 | 1 | 1 | 2.4 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 可重点关注搭载800V高压平台 | product | candidate | product | FALSE | 0.8 | 1 | 1 | 2.4 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 表格里不少车都搭载了800V高压平台 | product | candidate | product | FALSE | 0.8 | 1 | 1 | 2.4 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 问界M7搭载的华为高阶智驾系统 | product | candidate | product | FALSE | 0.8 | 1 | 1 | 1.4 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 追求前沿科技 | company | candidate | company | FALSE | 0.78 | 2 | 2 | 2.8 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 看重科技 | company | candidate | company | FALSE | 0.78 | 2 | 2 | 2.8 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 智能科技 | company | candidate | company | FALSE | 0.78 | 2 | 3 | 2.8 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 3} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你是科技 | company | candidate | company | FALSE | 0.78 | 2 | 2 | 2.8 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 华为 | person | candidate | person | FALSE | 0.78 | 1 | 1 | 2.4 | 1 |  | 中文姓名且邻近专家职务或来源标题 | ADS | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 购车前要确认三电系统 | product | candidate | product | FALSE | 0.78 | 1 | 1 | 1.4 | 3 | 产品类后缀 | 带产品/工具/平台类后缀 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 它们都深度整合了华为的技术方案 | product | candidate | product | FALSE | 0.78 | 1 | 1 | 1.4 | 3 | 产品类后缀 | 带产品/工具/平台类后缀 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 和保时捷 | person | candidate | person | FALSE | 0.78 | 1 | 1 | 2.4 | 1 |  | 中文姓名且邻近专家职务或来源标题 | Macan | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 🤝 售后服务能力排名 “靠谱”也离不开省心的服务 | product | candidate | product | FALSE | 0.78 | 1 | 1 | 1.4 | 3 | 产品类后缀 | 带产品/工具/平台类后缀 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 问界M9则将科技 | company | candidate | company | FALSE | 0.76 | 1 | 1 | 2.4 | 2 | 中英混合品牌形态 | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 既想要豪华SUV的舒适科技 | company | candidate | company | FALSE | 0.76 | 1 | 1 | 2.4 | 2 | 中英混合品牌形态 | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 极氪9X则是性能与科技 | company | candidate | company | FALSE | 0.76 | 1 | 1 | 2.4 | 2 | 中英混合品牌形态 | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 享界G9则提供了一个硬派造型与旗舰科技 | company | candidate | company | FALSE | 0.76 | 1 | 1 | 2.4 | 2 | 中英混合品牌形态 | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 追求驾驶乐趣与科技 | company | candidate | company | FALSE | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 从追求科技 | company | candidate | company | FALSE | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 看重智能驾驶辅助和华为生态的科技 | company | candidate | company | FALSE | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 追求前沿智能驾驶和科技 | company | candidate | company | FALSE | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你对智能驾驶和安全科技 | company | candidate | company | FALSE | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 追求极致效率和纯粹驾驶体验的务实科技 | company | candidate | company | FALSE | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 追求顶级的智能化体验和科技 | company | candidate | company | FALSE | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 追求极致性能和高阶智驾的科技 | company | candidate | company | FALSE | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 主打科技 | company | candidate | company | FALSE | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 是智能座舱和辅助驾驶的科技 | company | candidate | company | FALSE | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 从主打科技 | company | candidate | company | FALSE | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 新势力科技 | company | candidate | company | FALSE | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 兼顾了科技 | company | candidate | company | FALSE | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你是更看重智能科技 | company | candidate | company | FALSE | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 智能与科技 | company | candidate | company | FALSE | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 兼顾品牌与科技 | company | candidate | company | FALSE | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 以智能科技 | company | candidate | company | FALSE | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 追求顶尖智能科技 | company | candidate | company | FALSE | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 追求极致性能与科技 | company | candidate | company | FALSE | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 豪华科技 | company | candidate | company | FALSE | 0.74 | 1 | 2 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 注重科技 | company | candidate | company | FALSE | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你追求极致的性能与科技 | company | candidate | company | FALSE | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 根据多家独立机构 | company | candidate | company | FALSE | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 车辆品质和前沿智能科技 | company | candidate | company | FALSE | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 追求极简科技 | company | candidate | company | FALSE | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 智能化和科技 | company | candidate | company | FALSE | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 综合目前第三方机构 | company | candidate | company | FALSE | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 最看重智能和科技 | company | candidate | company | FALSE | 0.74 | 1 | 2 | 3.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"answer_heading": 1, "org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 高端定位 | person | candidate | person | FALSE | 0.64 | 1 | 1 | 1.4 | 1 |  | 疑似中文姓名且作为回答条目出现 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 山东省消协发布新能源车教育 | concept | candidate | concept | FALSE | 0.61 | 4 | 4 | 2.1 | 1 |  |  |  | {"source_title_org": 4} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 国产 | concept | candidate | concept | FALSE | 0.61 | 4 | 4 | 2.1 | 1 |  |  |  | {"source_title_person": 4} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 智能 | concept | candidate | concept | FALSE | 0.61 | 4 | 4 | 4.1 | 1 |  |  |  | {"org_suffix": 1, "source_title_person": 3} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 问界 | concept | candidate | concept | FALSE | 0.57 | 7 | 7 | 5.0 | 1 |  |  | AITO | {"answer_heading": 1, "person_alias": 6} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 特斯拉 | concept | candidate | concept | FALSE | 0.57 | 7 | 12 | 5.0 | 1 |  |  | Tesla | {"answer_heading": 6, "person_alias": 6} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 20万元内三款中大型智能 | concept | candidate | concept | FALSE | 0.57 | 3 | 3 | 1.7 | 1 |  |  |  | {"source_title_org": 3} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 此外 | concept | candidate | concept | FALSE | 0.49 | 3 | 3 | 2.2 | 1 |  |  |  | {"answer_heading": 3} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 比亚迪 | concept | candidate | concept | FALSE | 0.49 | 3 | 6 | 4.2 | 1 |  |  | BYD | {"answer_heading": 3, "person_alias": 3} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 尤其在智能 | concept | candidate | concept | FALSE | 0.49 | 3 | 3 | 3.2 | 1 |  |  |  | {"org_suffix": 3} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 山东省消费者协会发布新能源汽车消费教育 | concept | candidate | concept | FALSE | 0.49 | 1 | 1 | 0.9 | 1 |  |  |  | {"source_title_org": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 补能 | concept | candidate | concept | FALSE | 0.49 | 1 | 1 | 0.9 | 1 |  |  |  | {"source_title_person": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 山东省消协发布新能源汽车教育 | concept | candidate | concept | FALSE | 0.49 | 1 | 1 | 0.9 | 1 |  |  |  | {"source_title_org": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 豪华 | concept | candidate | concept | FALSE | 0.49 | 1 | 1 | 0.9 | 1 |  |  |  | {"source_title_person": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 实现质量 | concept | candidate | concept | FALSE | 0.49 | 1 | 1 | 0.9 | 1 |  |  |  | {"source_title_person": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 空间和智能 | concept | candidate | concept | FALSE | 0.45 | 2 | 2 | 2.8 | 1 |  |  |  | {"org_suffix": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 增程 | concept | candidate | concept | FALSE | 0.45 | 2 | 3 | 3.8 | 1 |  |  | EREV | {"answer_heading": 1, "person_alias": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 为了方便你比较 | concept | candidate | concept | FALSE | 0.45 | 2 | 2 | 1.8 | 1 |  |  |  | {"answer_heading": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 追求智能 | concept | candidate | concept | FALSE | 0.45 | 2 | 2 | 2.8 | 1 |  |  |  | {"org_suffix": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 鸿蒙智能 | concept | candidate | concept | FALSE | 0.45 | 2 | 2 | 2.8 | 1 |  |  |  | {"org_suffix": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 小米 | concept | candidate | concept | FALSE | 0.45 | 2 | 4 | 3.8 | 1 |  |  | Xiaomi | {"answer_heading": 2, "person_alias": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 💎 总结 | concept | candidate | concept | FALSE | 0.45 | 2 | 2 | 1.8 | 1 |  |  |  | {"answer_heading": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 小米汽车 | concept | candidate | concept | FALSE | 0.45 | 2 | 3 | 3.8 | 1 |  |  | Xiaomi | {"answer_heading": 2, "person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 理想L9是“舒适奶爸车”的集大成者 | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 问界M9则将科技感做到了一个新高度 | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 可重点关注搭载800V高压平台的车型 | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 理想L9和问界M7是代表 | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 充电认准800V | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 比亚迪 海豹06GT | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 全系标配激光雷达和双Orin | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 比亚迪 宋PLUS | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 小鹏P7+ | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 极狐考拉S | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 奥迪E7X 28.98 | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| FREELANDER 神行者8 预计50 | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 奔驰EQE SUV / 宝马iX / 奥迪e | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 路特斯ELETRE 约80 | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 享界G9预计50万起 | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 保时捷Macan EV | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| ELETRE 约100万内 极氪9X 46.59 | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 享界G9 约50万起 | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 蔚来ES8 约50 | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 享界G9主打硬派与豪华的融合 | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 极氪9X则是性能与科技的另一种结合 | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 理想L9和问界M9作为市场标杆 | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 享界G9则提供了一个硬派造型与旗舰科技结合的选项 | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 在J.D. Power的售后服务满意度研究中 | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 品牌档次与BBA并列 | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 拥有刀片电池、DM | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| Autopilot/FSD是行业标杆 | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 年Q1全球纯电销量重回第一 | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 年Q1全球新能源销量已冲至第七 | concept | candidate | concept | FALSE | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 追求前沿科技与智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 人民网财经特别总结了几条建议 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 警惕捆绑 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 务必确认无任何强制捆绑 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 确认渠道 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 电池 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 考察售后 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 现在的市场百花齐放 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 为了方便你快速了解 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 中型智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 中大型智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 追求极致智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| ⚡️ 如果看重驾驶乐趣与个性 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 极氪001是“驾驶者之车 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 它独特的猎装车造型就足够吸引眼球 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你享受开车的过程 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你对充电便利性焦虑 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 💰 如果追求极致质价比 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 它不仅是少有的中大型智能轿车 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 它不仅是少有的中大型智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 享受到目前最前沿的智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 有家充桩 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 纯电车 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  | BEV | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 或插混 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  | PHEV | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 试驾和金融方案别踩坑 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 💎 写在最后 没有完美的车 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 建议你根据这份指南 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 从追求极致智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 要找到最合适的那一辆 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 纯电 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  | BEV | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 智能驾驶与安全 华为系智驾 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 安全是底线 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 读懂续航参数 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 电池容量 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 务必深度试驾 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 💎 总结与建议 如果追求顶级的智能化体验和科技感 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 对充电便利性有顾虑 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 想在20 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 家里方便安装充电桩吗 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 主要是自己开还是家庭用呢 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 告诉我这些细节 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 下面这个表格 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 选车就像找对象 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你可以从下面几个角度来想 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 充电方便 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 看懂技术参数 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 对电池容量 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 安全是第一位的 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 别忘了关注金融和售后政策 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 想聊得更细一点 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 我梳理了当前市场最主流的几个价位和车型区间 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 第一步 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 家充是纯电车的天堂 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 除车价外 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 🎯 第二步 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 可以买到智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 极氪007 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 双电机四驱、智能座舱体验也属第一梯队 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 阿维塔12 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 💎 第三步 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 算清金融方案的“真实利率 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 把销售的口头承诺写进合同 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 试驾不能走过场 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 重点关注车机系统是否流畅 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 重视电池和质保政策 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 磷酸铁锂电池安全性好 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 总结一下 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 看重品牌且对智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 理想 / 蔚来 / 问界 30 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 注重大空间、家庭出行体验 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 对传统德系豪华品牌有深厚情怀 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 想清楚是要纯电 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 是家庭出行和空间舒适 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 是专业越野和全地形能力 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 还是品牌传承和驾驶质感 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 不同品牌的侧重点差异很大 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 从主打科技和家庭的国产品牌 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 我整理了几个目前值得关注的品牌和代表车型 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 高阶智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 蔚来智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 想尝鲜“硬派+智能”的新物种 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 这类车型在城市豪华感之外 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 对“性能”和“驾控”有执念 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 百公里加速2.95秒的成绩和纯粹的跑车调校 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| “品牌”和“格调”是首要考虑 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 智能体验 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 乘坐舒适性 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 内饰气味 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你是更看重智能科技和家庭舒适 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 从搜索结果来看 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 我整理了目前市场上几个不同侧重点的车型 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 填补了智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 神行者8 预计50 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你就是冲着驾驶乐趣去的 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你是科技发烧友 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 智能驾驶和智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你的目标是带着家人去“野 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 它在硬派基础上强化了智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你买车是为了日常家用 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 看重传统豪华品牌的品质和均衡性 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你是更看重智能驾驶体验 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你是更看重智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 可以告诉我你的具体偏好 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 主要可以分为几大流派 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 我整理了几个不同侧重点的车型 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 又不想牺牲城市智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你是科技极客 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 是目前智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你是家庭用户 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 理想在“冰箱彩电大沙发”上做到了极致 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你热爱驾驶 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你钟情德系工艺与品牌传承 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 它们在整车质感、底盘调校和品牌格调上 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 建议你在决定前 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 神行者 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  | Freelander | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 不放弃智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 舒适和智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你是全能家庭型 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你想兼顾豪华与越野 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 神行者有路虎的越野底蕴 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你是传统豪华品牌拥趸 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 平时主要是家庭多人出行 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 这里结合几个权威榜单 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 理想 | concept | candidate | concept | FALSE | 0.41 | 1 | 2 | 3.4 | 1 |  |  | Li Auto | {"answer_heading": 1, "person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 排在问界之后的是奔驰 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 口碑榜单看什么 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 在这类榜单中 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你最看重硬件质量和智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你将用户口碑和服务体验放在首位 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 蔚来在服务和体验上口碑很高 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你对某个特定价位 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 下面是几个主要品牌的分析 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 问界的优势集中在智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 依托华为技术 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 其鸿蒙智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 需要考虑的点 | concept | candidate | concept | FALSE | 0.41 | 1 | 3 | 1.4 | 1 |  |  |  | {"answer_heading": 3} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你看重智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 🛡️ 蔚来 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| ⚡ 特斯拉 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| ⚠️ 理想 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 其他值得关注的品牌 小米 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 传统品牌 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 追求顶尖的智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 信赖技术成熟、追求三电系统可靠 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 对品控稳定性要求高 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 或者家里方便安装充电桩吗 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 告诉我你的具体情况 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 但“靠谱”不只是看质量硬不硬 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 排名依据“产品质量风险指数 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 报告指出 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 作为电动车领域的先行者 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 蔚来、小鹏、理想 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 像蔚来、理想 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 不过 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 现在买车 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 这意味着 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 年轻用户更挑剔 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 他们对智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 更信赖全球范围内的品牌成熟度 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 想选蔚来、理想、小鹏 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 辅助驾驶等智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 销量快速上升 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 优势在于智能化质量 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 优势在于智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 纯电销量强劲 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 销量增长迅猛 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 市场成绩惊人 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 跨界造车势头凶猛 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 销量冠军 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 市场号召力无人能及 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 传统大厂转型迅速 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 选车小建议 如果你最看重品控和智能化稳定性 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你最看重品控和智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 追求成熟的三电技术和全球市场验证 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 蔚来的换电服务是独特优势 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 更看重保有量和市场领先地位 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 简单来说 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 我们可以从这两个角度来看一下几个主流品牌的表现 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 传统豪华品牌依然稳健 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 特斯拉三电系统领先 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 在杰兰路发布的2025年上半年售后服务能力排名中 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你将车辆的智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 像小米、理想、小鹏 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 当然 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你有具体看好的车型 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 追求极致稳定与低故障率 如果你最看重车子的可靠性 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 不想在智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 第2名 奔驰 126 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 第3名 特斯拉 146 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 第5名 小米 147 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你追求顶尖智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 依托华为深度赋能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 其在智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 在30万元以上区间和20 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你追求极致的性能与科技生态 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 特斯拉是技术标杆 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 小米的优势在于其"人车家"生态互联 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 在20 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你追求高端服务与换电体验 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 独特的换电模式能让你3分钟满电出发 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 这两个品牌凭借全产业链优势或纯电平台技术 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 两个需要注意的趋势 根据2025年的用户调研 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 虽然新能源车智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 恼人的"小毛病 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 质量与智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 在2025年新能源汽车品牌质量榜上排名第一 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 对车辆品质和前沿智能科技有高要求的用户 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 以用户服务著称 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 追求极简科技风格 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 信赖成熟智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 用户满意度 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 自主品牌在智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你可以根据自己最看重的 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 最看重智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 它们在智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 担心续航 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 希望兼顾品质和性价比 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 买车是件大事 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 续航还是智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 我可以根据你的实际情况 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 年1 | concept | candidate | concept | FALSE | 0.41 | 1 | 2 | 1.4 | 1 |  |  |  | {"answer_heading": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 华为技术深度赋能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 全球纯电领导品牌 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 跨界新势力黑马 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 另有报告显示其百辆新车故障数较少 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 高端纯电代表 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 选车时需要注意的两点 质量与销量的辩证关系 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 具体车型的差异 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 确定了品牌 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 给你的建议 如果你追求顶尖的智能体验和品质 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你追求顶尖的智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 它在质量与智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你看重成熟稳定的三电技术和全球品牌影响力 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你想尝鲜 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 它家产品线非常广 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 不过作为新品 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 阿维塔、极氪 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 定要去试驾 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 或者比较看重续航、空间还是智能驾驶 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 空间还是智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 不同品牌的侧重点不太一样 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 追求顶尖智能化体验、看重科技感的家庭用户 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 追求顶尖智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 在杰兰路2025年质量榜单中 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 覆盖从入门到高端全价位 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 销量领先 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 追求前沿科技、极简设计和纯粹驾驶体验的消费者 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 电系统质量口碑稳定 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 定位高端 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 极氪 | concept | candidate | concept | FALSE | 0.41 | 1 | 2 | 3.4 | 1 |  |  | ZEEKR | {"answer_heading": 1, "person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 追求驾驶乐趣和实用空间 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 满意度与合资持平 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 车内静谧性与异味 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 试驾时可以特别留意 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 钟爱智能驾驶标杆和极简风格 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 钟爱智能 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 或者说 | concept | candidate | concept | FALSE | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 基于中德合作平台 | noise | candidate | noise | FALSE | 0.2 | 2 | 2 | 1.3 | 3 | 产品类后缀 | 通用词/指标/缩写，非目标实体 |  | {"source_title_org": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 基于e平台 | noise | candidate | noise | FALSE | 0.2 | 1 | 1 | 2.4 | 4 | 产品类后缀、中英混合品牌形态 | 通用词/指标/缩写，非目标实体 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 全系基于800V平台 | noise | candidate | noise | FALSE | 0.2 | 1 | 1 | 2.4 | 4 | 产品类后缀、中英混合品牌形态 | 通用词/指标/缩写，非目标实体 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 岚图泰山携核心黑科技 | noise | candidate | noise | FALSE | 0.2 | 1 | 1 | 0.9 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"source_title_org": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 看重核心硬件稳定性和换电服务 | noise | candidate | noise | FALSE | 0.2 | 1 | 1 | 1.4 | 3 | 产品类后缀 | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| XNGP全场景智能 | noise | candidate | noise | FALSE | 0.18 | 1 | 1 | 2.4 | 2 | 中英混合品牌形态 | 通用词/指标/缩写，非目标实体 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 基于e平台3.0 Evo | noise | candidate | noise | FALSE | 0.18 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 搭载华为乾崑ADS全场景智驾系统与三激光雷达 | noise | candidate | noise | FALSE | 0.18 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 车机卡顿、OTA速度慢、语音识别失灵等问题 | noise | candidate | noise | FALSE | 0.18 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 非常适合首次尝试高端智能 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 2.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 核心是家庭使用 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 看重成熟的补能体系、极致的能耗和驾驶乐趣 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 为了让推荐更有针对性 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 这是决定用车幸福感的黄金标准 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 用车场景 主要是市区通勤 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 纯电适合城市代步 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 适合看重品牌口碑、三电技术稳定性的家庭用户 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 适合追求前沿科技和驾驶乐趣的年轻用户 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 适合追求前沿科技 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 2.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 适合求稳、不想在车上折腾的家庭用户 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 如何选择适合你的那一款 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 再看你最看重的核心价值 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 要找到最适合你的那款 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 告诉我你的具体用车场景 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 在口碑净推荐值 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 净推荐值 | noise | candidate | noise | FALSE | 0.16 | 1 | 2 | 2.4 | 1 |  | 通用词/指标/缩写，非目标实体 | NPS | {"person_alias": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 它基于超过5700份真实车主的反馈 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| Power | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 2.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 尤其是其依托华为体系的智能 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 2.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 主要问题 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 尽管官方对部分问题做出了回应和延保承诺 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 我从几个关键角度 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 我把一些重点品牌的核心信息整理成了表格 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 看重高端服务体系和快速增长的市场热度 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 用户最关心的是“能解决问题 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 找不到一个适合所有人的"最好"品牌 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 它的增程式技术有效解决了纯电里程焦虑问题 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 我把几个代表性品牌的核心特点整理成了表格 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 看重技术成熟度、性价比和丰富产品线选择的家庭用户 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 我把它们的核心特点整理成了一个表格 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 核心趋势 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 追求大品牌、技术可靠、选择丰富 | noise | candidate | noise | FALSE | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |

## 信源渠道分布

DeepSeek 引用信源的渠道结构。

- 行数：4

| bucket | raw_bucket | count | rate |
| --- | --- | --- | --- |
| 其他 | other | 110 | 0.5527638190954773 |
| 媒体 | media | 73 | 0.36683417085427134 |
| 官方 | official | 8 | 0.04020100502512563 |
| 开发者 | developer | 8 | 0.04020100502512563 |

## 来源编号位置

DeepSeek source panel 编号位置分布。

- 行数：3

| bucket | raw_bucket | count | rate |
| --- | --- | --- | --- |
| 1-3 | 1-3 | 60 | 0.3015075376884422 |
| 4-6 | 4-6 | 60 | 0.3015075376884422 |
| 7+ | 7+ | 79 | 0.3969849246231156 |

## 高频域名

高频引用域名。

- 行数：10

| display_name | name | count | url |
| --- | --- | --- | --- |
| 中关村在线 | auto.zol.com.cn | 46 | https://auto.zol.com.cn |
| 汽车之家 | chejiahao.autohome.com.cn | 31 | https://chejiahao.autohome.com.cn |
| 网通社汽车 | m.news18a.com | 16 | https://m.news18a.com |
| CNMO | smartcar.cnmo.com | 13 | https://smartcar.cnmo.com |
| 易车 | news.m.yiche.com | 11 | https://news.m.yiche.com |
| 易车号 | hao.m.yiche.com | 10 | https://hao.m.yiche.com |
| 搜狐 | m.sohu.com | 10 | https://m.sohu.com |
| 人民网财经 | finance.people.com.cn | 6 | https://finance.people.com.cn |
| 东方财富 | finance.eastmoney.com | 5 | https://finance.eastmoney.com |
| 乘用车市场信息联席会 | cpcaauto.com | 4 | https://cpcaauto.com |

## 高频来源名

高频引用来源名称。

- 行数：10

| name | count |
| --- | --- |
| 中关村在线 | 46 |
| 汽车之家 | 31 |
| 网通社汽车 | 16 |
| CNMO | 13 |
| 易车 | 12 |
| 易车号 | 10 |
| 手机搜狐网 | 10 |
| 人民网财经 | 6 |
| 东方财富 | 5 |
| 乘用车市场信息联席会 | 4 |

## 高频URL

高频引用 URL。

- 行数：10

| display_name | name | url | domain | source | count |
| --- | --- | --- | --- | --- | --- |
| 问界新能源车逆袭，2025年超越奔驰登顶质量榜 | 问界新能源车逆袭，2025年超越奔驰登顶质量榜 | https://news.m.yiche.com/hao/wenzhang/107124269/ | news.m.yiche.com | 易车 | 10 |
| 新能源车品质榜单出炉，看看谁最能打 | 新能源车品质榜单出炉，看看谁最能打 | https://hao.m.yiche.com/wenzhang/107178129 | hao.m.yiche.com | 易车号 | 10 |
| 2025新能源汽车质量榜单出炉：问界获品牌第一，M9获车型第一 | 2025新能源汽车质量榜单出炉：问界获品牌第一，M9获车型第一 | https://m.sohu.com/a/981422712_115088?scm=10001.325_13-325_13.0.0-0-0-0-0.5_1334 | m.sohu.com | 手机搜狐网 | 10 |
| 100万元内纯电中大型轿车横评：阿维塔12、ET7、Model S、极氪001与Taycan五大旗舰真实对决 | 100万元内纯电中大型轿车横评：阿维塔12、ET7、Model S、极氪001与Taycan五大旗舰真实对决 | https://auto.zol.com.cn/1201/12017841.html | auto.zol.com.cn | 中关村在线 | 7 |
| 2025年新能源汽车产品质量排名发布 问界超奔驰登顶 - CNMO科技 | 2025年新能源汽车产品质量排名发布 问界超奔驰登顶 - CNMO科技 | https://smartcar.cnmo.com/news/803421.html | smartcar.cnmo.com | CNMO | 6 |
| 理性購車避“坑”：五招識破隱藏套路 算清真實成本 | 理性購車避“坑”：五招識破隱藏套路 算清真實成本 | https://finance.people.com.cn/BIG5/n1/2026/0317/c1004-40683588.html | finance.people.com.cn | 人民网财经 | 5 |
| 经典新生 全域进阶 FREELANDER神行者品牌全球发布 | 经典新生 全域进阶 FREELANDER神行者品牌全球发布 | http://m.news18a.com/news/storys_243869.html?ina_from=AAbashi | m.news18a.com | 网通社汽车 | 5 |
| 100万元内纯电5座SUV终极对决：路特斯ELETRE、保时捷Macan EV等五款旗舰深度横评 | 100万元内纯电5座SUV终极对决：路特斯ELETRE、保时捷Macan EV等五款旗舰深度横评 | https://auto.zol.com.cn/1201/12016248.html | auto.zol.com.cn | 中关村在线 | 5 |
| 新能源质量报告出炉：华为系最好，极狐销量低还故障多？_车家号_发现车生活_汽车之家 | 新能源质量报告出炉：华为系最好，极狐销量低还故障多？_车家号_发现车生活_汽车之家 | https://chejiahao.autohome.com.cn/info/19547834?isfrom=m | chejiahao.autohome.com.cn | 汽车之家 | 5 |
| 新能源汽车质量曝光：比亚迪刚及格，好车不好卖，多品牌翻车_车家号_发现车生活_汽车之家 | 新能源汽车质量曝光：比亚迪刚及格，好车不好卖，多品牌翻车_车家号_发现车生活_汽车之家 | https://chejiahao.autohome.com.cn/info/19647610 | chejiahao.autohome.com.cn | 汽车之家 | 5 |

## 高频引用标题

被重复引用的标题。

- 行数：10

| name | url | source | domain | count |
| --- | --- | --- | --- | --- |
| 问界新能源车逆袭，2025年超越奔驰登顶质量榜 | https://news.m.yiche.com/hao/wenzhang/107124269/ | 易车 | news.m.yiche.com | 10 |
| 新能源车品质榜单出炉，看看谁最能打 | https://hao.m.yiche.com/wenzhang/107178129 | 易车号 | hao.m.yiche.com | 10 |
| 2025新能源汽车质量榜单出炉：问界获品牌第一，M9获车型第一 | https://m.sohu.com/a/981422712_115088?scm=10001.325_13-325_13.0.0-0-0-0-0.5_1334 | 手机搜狐网 | m.sohu.com | 10 |
| 100万元内纯电中大型轿车横评：阿维塔12、ET7、Model S、极氪001与Taycan五大旗舰真实对决 | https://auto.zol.com.cn/1201/12017841.html | 中关村在线 | auto.zol.com.cn | 7 |
| 2025年新能源汽车产品质量排名发布 问界超奔驰登顶 - CNMO科技 | https://smartcar.cnmo.com/news/803421.html | CNMO | smartcar.cnmo.com | 6 |
| 理性購車避“坑”：五招識破隱藏套路 算清真實成本 | https://finance.people.com.cn/BIG5/n1/2026/0317/c1004-40683588.html | 人民网财经 | finance.people.com.cn | 5 |
| 40万元内中型轿车深度横评：蔚来ET5、奥迪A4L、沃尔沃S60新能源、帕萨特等五款代表车型全维度解析 | https://auto.zol.com.cn/1201/12016302.html | 中关村在线 | auto.zol.com.cn | 5 |
| 经典新生 全域进阶 FREELANDER神行者品牌全球发布 | http://m.news18a.com/news/storys_243869.html?ina_from=AAbashi | 网通社汽车 | m.news18a.com | 5 |
| 100万元内纯电5座SUV终极对决：路特斯ELETRE、保时捷Macan EV等五款旗舰深度横评 | https://auto.zol.com.cn/1201/12016248.html | 中关村在线 | auto.zol.com.cn | 5 |
| 新能源质量报告出炉：华为系最好，极狐销量低还故障多？_车家号_发现车生活_汽车之家 | https://chejiahao.autohome.com.cn/info/19547834?isfrom=m | 汽车之家 | chejiahao.autohome.com.cn | 5 |

## 标题功能特征

引用标题的功能信号。

- 行数：5

| feature | count | rate |
| --- | --- | --- |
| has_number | 124 | 0.6231155778894473 |
| has_structure_punctuation | 105 | 0.5276381909547738 |
| has_year | 55 | 0.27638190954773867 |
| contains_brand | 13 | 0.06532663316582915 |
| has_question | 8 | 0.04020100502512563 |

## 标题长度

引用标题长度分布。

- 行数：3

| bucket | raw_bucket | count | rate |
| --- | --- | --- | --- |
| 41+ | 41+ | 49 | 0.24623115577889448 |
| 13-24 | 13-24 | 47 | 0.23618090452261306 |
| 25-40 | 25-40 | 103 | 0.5175879396984925 |

## 时间新旧

引用标题或日期的新旧分布。

- 行数：4

| bucket | raw_bucket | count | rate |
| --- | --- | --- | --- |
| 本年 | current_year | 145 | 0.7286432160804021 |
| 近一年 | last_year | 24 | 0.12060301507537688 |
| 未识别 | unknown | 28 | 0.1407035175879397 |
| 更早 | older | 2 | 0.010050251256281407 |

## 标题意图

引用标题意图特征分布。

- 行数：8

| bucket | raw_bucket | count | rate |
| --- | --- | --- | --- |
| 对比评测 | 对比评测 | 48 | 0.1811320754716981 |
| 其他信息 | 其他信息 | 54 | 0.2037735849056604 |
| 推荐选择 | 推荐选择 | 14 | 0.052830188679245285 |
| 趋势新闻 | 趋势新闻 | 83 | 0.3132075471698113 |
| 榜单排名 | 榜单排名 | 42 | 0.15849056603773584 |
| 指南攻略 | 指南攻略 | 10 | 0.03773584905660377 |
| 避坑风险 | 避坑风险 | 10 | 0.03773584905660377 |
| 研究论文 | 研究论文 | 4 | 0.01509433962264151 |
