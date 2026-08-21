---
name: "Scholar Evaluation"
description: "基於 ScholarEval 架構的學術研究評估技能。提供針對論文、文獻回顧與研究計畫的系統性評分標準與工作流程。"
tags: ["research", "academic", "evaluation", "peer-review", "scholar-eval"]
version: "1.0"
---

# Scholar Evaluation

## Overview

Apply the ScholarEval framework to systematically evaluate scholarly and research work. This skill provides structured evaluation methodology based on peer-reviewed research assessment criteria, enabling comprehensive analysis of academic papers, research proposals, literature reviews, and scholarly writing.

## When to Use This Skill

Use this skill when:
* Evaluating research papers for quality and rigor.
* Assessing literature review comprehensiveness and quality.
* Reviewing research methodology design.
* Scoring data analysis approaches.
* Evaluating scholarly writing and presentation.
* Providing structured feedback on academic work.
* Benchmarking research quality against established criteria.
* Assessing publication readiness for target venues.

---

## Visual Enhancement with Scientific Schematics

**Policy:** Always consider adding scientific diagrams to enhance visual communication.

* **Tool:** Use the `scientific-schematics` skill.
* **Command:** `python scripts/generate_schematic.py "diagram description" -o figures/output.png`
* **Use Cases:** Evaluation frameworks, decision trees, workflow visualizations, scoring rubrics.

---

## Evaluation Workflow

### Step 1: Initial Assessment and Scope Definition
Identify the work type (Full paper, Proposal, Review) and scope (Comprehensive, Targeted, Comparative).

### Step 2: Dimension-Based Evaluation
Systematically evaluate the work across these core dimensions:

1.  **Problem Formulation & Research Questions:** Clarity, specificity, theoretical significance.
2.  **Literature Review:** Comprehensiveness, critical synthesis (vs summarization), gap identification.
3.  **Methodology & Research Design:** Rigor, validity, reproducibility, ethical considerations.
4.  **Data Collection & Sources:** Sample size, representativeness, source credibility.
5.  **Analysis & Interpretation:** Analytical rigor, logical coherence, alternative explanations.
6.  **Results & Findings:** Clarity, statistical rigor, visualization quality.
7.  **Scholarly Writing & Presentation:** Academic tone, clarity, logical flow.
8.  **Citations & References:** Completeness, accuracy, balance.

### Step 3: Scoring and Rating
For each dimension, provide qualitative assessment (strengths/weaknesses) and a quantitative score (1-5 scale):
* **5:** Excellent (Exemplary, publishable in top venues)
* **4:** Good (Strong with minor improvements)
* **3:** Adequate (Acceptable with notable areas for improvement)
* **2:** Needs Improvement (Significant revisions required)
* **1:** Poor (Fundamental issues)

### Step 4: Synthesize Overall Assessment
Provide an integrated summary including Overall Quality, Major Strengths, Critical Weaknesses, and Publication Readiness.

### Step 5: Provide Actionable Feedback
Feedback should be Specific, Actionable, Prioritized, Balanced, and Evidence-based.

### Step 6: Contextual Considerations
Adjust evaluation based on Development Stage (Draft vs Final), Purpose (Journal vs Grant), and Discipline Norms (STEM vs Humanities).

---

## Resources

* `references/evaluation_framework.md`: Detailed evaluation criteria and rubrics.
* `scripts/calculate_scores.py`: Python script for calculating aggregate scores.

---

## Best Practices

1.  **Maintain Objectivity:** Base evaluations on criteria, not personal preference.
2.  **Be Comprehensive:** Evaluate all applicable dimensions systematically.
3.  **Provide Evidence:** Support assessments with specific examples.
4.  **Stay Constructive:** Frame weaknesses as opportunities for improvement.
5.  **Consider Context:** Adjust expectations based on work stage and purpose.

---

## Integration with Scientific Writer

* **After Paper Generation:** Use as an alternative to peer review to generate `SCHOLAR_EVALUATION.md`.
* **During Revision:** Re-evaluate specific dimensions to track score improvements.
* **Publication Preparation:** Assess readiness for target journals.

---

## Citation

This skill is based on the ScholarEval framework introduced in:
**Moussa, H. N., et al. (2025).** *ScholarEval: Research Idea Evaluation Grounded in Literature*. arXiv preprint arXiv:2510.16234.