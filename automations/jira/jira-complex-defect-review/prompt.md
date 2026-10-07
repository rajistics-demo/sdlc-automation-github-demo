# Jira Defect Review → Validated Repair

> Review existing code, prove the defects, and produce a tested repair for human review.

A KAN Task labeled `defect-review-complex` selects Opus and supplies the repository and review scope.

| Step | Agent action | Reviewable output |
| --- | --- | --- |
| 1. Discover | Read the ticket and use `repo-defect-triage` | Reproduced, prioritized findings |
| 2. Specify | Use `repo-defect-repair` to plan scoped fixes | Repair spec linked to finding IDs |
| 3. Repair | Add failing regression tests, then fix the code | Bounded changes on a repair branch |
| 4. Validate | Apply existing code-review and QA guidance | Before/after test evidence and remaining risks |
| 5. Prepare PR | Use the repair skill’s PR template; publish within the user’s approved demo scope | Draft GitHub PR with links in both directions |

## Workflow guidance

The skills live in `.agents/skills/` in the configured SDLC demo checkout on `codex/jira-defect-triage`. The target repo supplies its own product rules. Only the configured Petstore and billing demo repos are in scope. If event context is absent, stop; an explicitly supplied synthetic event is allowed for rehearsals.

## Demo boundaries

Write the complete PR body using `.agents/skills/repo-defect-repair/references/pr-description-template.md`. Reconcile final test counts, specification, completed tasks, and limitations before publication. Copy the verified current conversation URL supplied by the runtime or operator exactly; if it is unavailable, report the missing link. Follow active user authorization and repository outbound-communication rules. When this demo’s publication is authorized, publish the validated repair branch, open or update a draft PR, read it back to verify the conversation link, and return the actual clickable PR URL here. Add authorized Jira completion links only after validation and PR verification. Human review controls merge and deployment. Do not archive this conversation or any related conversation; keep demo history visible.

Report actual results and remaining defects. A PR draft file is not an opened PR, and self-review is not independent agent review.
