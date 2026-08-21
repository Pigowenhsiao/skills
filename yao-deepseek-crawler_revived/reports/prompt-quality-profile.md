# Prompt Quality Profile

Skill: `yao-deepseek-crawler`
Relevance: `prompt-heavy`
Overall quality score: `91.0/100`

## Primary Task Family

**Creative generation**
- Matched keywords: copy, title, content

## Complexity

- Band: `expert`
- Score: `10`
- Reason: multiple task families plus governance, evaluation, or expert-level constraints

## Need Model

- Explicit Need: Run multiple DeepSeek web AI-search queries repeatedly, normalize the crawl records, and turn them into GEO probability evidence.
- Implicit Need: The reusable skill needs a stable role, task, and output contract rather than a one-off prompt.
- Scenario: A list of questions, per-question repeat count, OpenCLI Browser Bridge profile, optional target brand list, optional crawler script path.
- User Level: infer from examples and standards; ask only if it changes output depth
- Success Standard: Every run must expose query count, repeat count, completed sample count, answer/reference totals, brand Top 1 and Top 3 rates, source/domain/channel distribution, and title features.

## RTF To Skill Mapping

- Role: Use a taste-aware creator role with clear audience, tone, and originality boundaries.
- Task: Generate variants, explain selection logic, and preserve the user's distinctive constraints.
- Format: Return options with rationale, selection criteria, and refinement paths.

## Quality Matrix

### Completeness — 100/100
- Matched signals: input, output, constraint, example
- Repair: Name missing inputs, outputs, constraints, or success standards before deepening the package.

### Clarity — 90/100
- Matched signals: clear, specific
- Repair: Replace broad verbs with observable actions and define what done means.

### Consistency — 85/100
- Matched signals: boundary
- Repair: Check that role, task, format, exclusions, and examples do not contradict each other.

### Practicality — 95/100
- Matched signals: execute, use, workflow
- Repair: Add runnable steps, examples, or verification cues instead of abstract advice.

### Specificity — 85/100
- Matched signals: domain
- Repair: Anchor wording in the user's audience, domain nouns, and target outcome.

## Matched Task Families

### Creative generation
- Score: `3`
- Keywords: copy, title, content
- Role: Use a taste-aware creator role with clear audience, tone, and originality boundaries.
- Task: Generate variants, explain selection logic, and preserve the user's distinctive constraints.
- Format: Return options with rationale, selection criteria, and refinement paths.

### Prompt engineering
- Score: `3`
- Keywords: prompt, role, format
- Role: Use a prompt engineer role only when role design materially improves execution.
- Task: Map Role, Task, and Format into skill behavior rather than copying a large prompt template.
- Format: Return a compact prompt contract plus tests, quality matrix, and usage notes.

### Execution operation
- Score: `2`
- Keywords: workflow, execute
- Role: Use an operator role with explicit boundaries, inputs, outputs, and failure handling.
- Task: Convert the job into ordered steps with validation checks and stop conditions.
- Format: Return a runbook-like handoff with commands, checks, owners, and next actions when relevant.

### Dialogue interaction
- Score: `2`
- Keywords: dialogue, chat
- Role: Use a conversational role that asks only high-leverage questions and remembers the user's goal.
- Task: Clarify intent, resolve uncertainty, and converge toward a recommendation instead of a long option list.
- Format: Return concise prompts, decision points, and reviewer-visible assumptions.

## Self-Repair Checks

- Check explicit need, implicit need, scenario, user level, and success standard before deepening.
- Map Role, Task, and Format into skill behavior, not decorative prompt labels.
- Ask one focused clarification only when missing information changes the package boundary.
- Add tests or examples for prompt-heavy behavior before treating it as reusable.
- Keep prompt methodology in references and reports instead of bloating SKILL.md.

## Reviewer Note

Use this profile when the package depends on prompt behavior, role design, output contracts, or conversation quality.
