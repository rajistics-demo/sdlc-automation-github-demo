# Jira Defect Review → Validated Repair

> Review existing code, prove the defects, and produce a tested repair for human review.

A KAN Task labeled `defect-review` supplies the repository and review scope.

| Step | Agent action | Reviewable output |
| --- | --- | --- |
| 1. Discover | Read the ticket and use `repo-defect-triage` | Reproduced, prioritized findings |
| 2. Specify | Use `repo-defect-repair` to plan scoped fixes | Repair spec linked to finding IDs |
| 3. Repair | Add failing regression tests, then fix the code | Bounded changes on a repair branch |
| 4. Validate | Apply existing code-review and QA guidance | Before/after test evidence and remaining risks |
| 5. Prepare PR | Use the repair skill’s PR template; publish after exact-content approval | Draft GitHub PR with links in both directions |

## Workflow guidance

The skills live in `.agents/skills/` in the configured SDLC demo checkout on `codex/jira-defect-triage`. The target repo supplies its own product rules. Only the configured Petstore and billing demo repos are in scope. If event context is absent, stop; an explicitly supplied synthetic event is allowed for rehearsals.

## Demo boundaries

Write the complete PR body using `.agents/skills/repo-defect-repair/references/pr-description-template.md`. Include the verified current conversation URL supplied by the runtime or operator. If it is unavailable, report the missing link. Show the exact PR title, body, repository, and branches for approval. After approval, publish the validated repair branch, open or update a draft PR, verify its conversation backlink, and return the actual clickable PR URL here. Follow repository outbound-communication rules. Do not post additional Jira/GitHub comments, merge, or deploy. Do not archive this conversation or any related conversation; keep demo history visible.

Report actual results and remaining defects. A PR draft file is not an opened PR, and self-review is not independent agent review.
