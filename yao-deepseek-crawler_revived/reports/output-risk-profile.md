# Output Risk Profile

Skill: `yao-deepseek-crawler`

## Why This Exists

Generated skills often fail in small output details: generic headings, cluttered citations, fragile screenshots, weak Markdown rendering, or missing execution assumptions. This profile predicts the most likely output mistakes before the skill is used heavily.

## Matched Risk Families

### Tone and specificity
- Matched keywords: copy, title, content, summary
- Score: `4`

### Markdown readability
- Matched keywords: md, table, report
- Score: `3`

### Citation and footnote clutter
- Matched keywords: citation, source, reference
- Score: `3`

### Screenshot and visual capture
- Matched keywords: screenshot, visual, screen
- Score: `3`

### Code and command safety
- Matched keywords: script, cli, api
- Score: `3`

## Likely Output Mistakes

- Headings and summaries can drift into generic, interchangeable language.
- The output can sound polished but lose the user's actual taste, audience, or scenario.
- Tables can render as dense grids with weak hierarchy or poor mobile readability.
- Long bullets can make the output look complete while hiding the actual decision logic.
- Footnote markers or dense citation notes can interrupt the reading flow.
- Evidence can be over-attached to obvious statements and under-attached to risky claims.

## Output Constraints To Apply

- Anchor titles and summaries in the user's audience, object, and concrete outcome.
- Avoid placeholder phrases such as comprehensive guide, ultimate solution, or key insights unless the source demands them.
- Use tables only when comparison is the main job; otherwise prefer compact cards or grouped bullets.
- Keep table cells short and move explanations below the table.
- Attach citations only to claims that need evidence, not to every sentence.
- Group source notes at the end of a section when inline markers would hurt readability.

## Self-Repair Checks

- Replace generic title candidates with scenario-specific alternatives.
- Delete any polished sentence that could fit almost any project unchanged.
- Preview whether each table still reads well when columns are narrow.
- Convert any table with paragraph-length cells into bullets or cards.
- Remove decorative citations that do not support a material claim.
- Move repeated source explanations into one compact source note.

## Reviewer Note

Use this report before deepening the package and again before approving example outputs.
