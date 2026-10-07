# Jira repository review to repair

A KAN Task labeled `defect-review` names the repository and review scope.

1. Read the ticket and locate its repository.
2. Use `repo-defect-triage` to find and reproduce real defects.
3. Use `repo-defect-repair` to draft the repair spec and fix confirmed findings within scope.
4. Apply the existing code-review and QA guidance, then validate the original defects.
5. Save findings, spec, test evidence, and a draft PR description for human review.

The skills live in `.agents/skills/` in the configured SDLC demo checkout on `codex/jira-defect-triage`. The target repo supplies its own product rules. Only the configured Petstore and billing demo repos are in scope. If event context is absent, stop; an explicitly supplied synthetic event is allowed for rehearsals.

This demo saves publication drafts locally. Do not push fixes, post Jira/GitHub messages, open PRs, merge, or deploy. Do not archive this conversation or other conversations. Keep all demo conversations visible. Report real results and remaining defects; a PR draft file is not an opened PR.
