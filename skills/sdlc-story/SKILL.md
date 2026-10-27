---
name: sdlc-story
description: Turn sparse GitHub or Jira bug reports and requests into OpenSpec-style change artifacts, a scoped implementation, tests, and a human-reviewable draft PR.
triggers:
  - openhands-build
  - open spec
  - open specification
  - bug to pr
  - story to pr
  - sparse issue
---

# SDLC Request To PR

Use this skill when OpenHands turns a GitHub or Jira issue into a small reviewable PR.

The customer-facing story is: a sparse business-language bug report becomes an OpenSpec-style change proposal, spec delta, design, and task list, then an implementation branch, then a PR that humans review and merge.

## Workflow

0. Understand the issue and identify the highest-value uncertainty. For Jira-triggered stories, use at least one native read-only sub-agent investigation when the tool is available; follow the fallback below when it is unavailable.
1. Read `README.md`, `AGENTS.md`, and the relevant repository guidance, then synthesize any delegated findings. For a bug report, reproduce the behavior through the actual application entry point, including relevant input variants; a passing default-path test or copied logic does not establish that the reported defect is absent.
2. **Before editing application code, create the OpenSpec-style change folder** using the skill references: proposal, design, task list, and spec delta, including assumptions and human gates appropriate to the request. These are required deliverables, not optional follow-up documentation.
3. Validate the change artifacts with `python3 skills/sdlc-story/scripts/validate_open_spec.py <change-folder>`.
4. Implement the smallest safe change that satisfies the spec delta and add focused tests. For a bug fix, retain a reproduction that fails on the original code and passes after the change. If the defect cannot be reproduced, report the investigation and its limits rather than claiming a test-only change fixes it.
5. Run the narrowest useful validation first, expanding only when risk or repository guidance requires it. Update `tasks.md` as results become known; keep human approvals pending until a person grants them.
6. Open a draft PR with the source issue, evidence waypoints, validation results, assumptions, and human-review notes.
7. After opening or updating the PR, add `openhands-review` as the final GitHub mutation so code review starts as a separate conversation. Do not add `openhands-qa`; the review work cell owns that handoff. A parent-child supervisor may explicitly override this when it owns downstream orchestration itself.
8. **Complete the applicable workflow before reporting success.** Confirm the required artifacts exist, update tasks to reflect actual results, and summarize validation and handoff status. If a required step is incomplete or blocked, report that explicitly rather than declaring the workflow complete. Keep pending human approvals distinct from completed agent work.

## OpenSpec Lineage

This skill intentionally follows the Fission-AI/OpenSpec project:

- Project: `https://github.com/Fission-AI/OpenSpec`
- Site: `https://openspec.pro`
- Upstream pattern: `openspec/changes/<change-id>/proposal.md`, `design.md`, `tasks.md`, and `specs/.../spec.md`

For live OpenHands Automations, do not run `npm install`, `npm install -g @fission-ai/openspec`, or `openspec init/update` inside the timed label-triggered run. Those steps add network and toolchain variance to a customer demo. Instead, create the OpenSpec-style artifacts directly from `references/open-spec-template.md` and validate them with `scripts/validate_open_spec.py`.

If the OpenSpec CLI is preinstalled and the operator explicitly asks to use it, it is acceptable to run read-only or already-installed CLI validation. Otherwise, keep the live automation deterministic and explain in the PR that the artifacts follow OpenSpec lineage without invoking the CLI during the run.

## Inputs

- GitHub or Jira issue title, body, labels, and comments
- repository default branch
- target source branch
- acceptance criteria when present
- linked PRs or previous automation comments when present

Sparse issues are the primary demo path. The ticket should not need repo names, file paths, log codes, or implementation clues. For bug-shaped issues, first identify the violated behavior, repo-local docs, and any fixture/log evidence before editing code. Infer the smallest safe implementation, but write the assumptions, spec delta, task list, and human gates into the OpenSpec-style change folder before editing code.

## GitHub Boundaries

- Trigger label: `openhands-build`
- Status labels: `openhands:ready`, `openhands:in-progress`, `openhands:needs-human`, `openhands:done`
- Use event context; do not poll GitHub.
- Avoid result comments that repeat the exact trigger text.
- Use runtime secret `GITHUB_TOKEN` for GitHub API calls, pushes, PRs, labels, and comments. For `gh`, supply that same credential as `GH_TOKEN` for the command and set `GH_PROMPT_DISABLED=1`; PR creation must specify `--head <source-branch>` and `--base <target-branch>` so it cannot pause for a push destination. Do not create credentials or run interactive login. If authentication is missing or returns 401, stop and report the failure without printing credentials.
- Do not run `git remote -v`, `gh auth status`, or any command that prints token-bearing remote URLs. Use GitHub tools or API calls for PR creation and label/comment updates, and never echo auth-bearing remotes, token previews, or authorization headers.
- Never merge, bypass review, change branch protection, or alter deployment settings.

## Jira Boundaries

- Treat Jira Tasks as source issues when the automation starts from a Jira webhook.
- Use the Jira issue key and URL in artifacts and comments.
- Keep Jira comments concise: status, evidence waypoints, PR link, tests, and any human questions.
- Do not require the Jira ticket to mention logs, docs, repository names, file paths, or error codes.
- For Jira API calls, use the configured `JIRA_API_BASE_URL`; use `JIRA_SITE_URL` only for human-facing issue links. Do not hard-code the Atlassian site URL as the API endpoint or derive it from the webhook.
- Honor `JIRA_AUTH_MODE` and use the configured runtime credentials. For basic auth, pass `JIRA_SERVICE_ACCOUNT_EMAIL` and `JIRA_API_TOKEN` to the HTTP client as username and password. For bearer auth, pass `JIRA_API_TOKEN` as the bearer token. Never construct a Basic header with shell `base64`, single-quote variable references, or print credentials or authorization headers.
- Encode the comment as valid JSON in a file before posting; use the body format required by the chosen Jira API version. Check the HTTP status and response before reporting that a comment was posted. On a 401, 403, or 404, check the configured API base URL, auth mode, and issue access; report the failure instead of treating it as transient or claiming success.

## Delegation and Context Gathering

Before creating change artifacts or editing files, identify what is uncertain about the request and what evidence would reduce that uncertainty. When the native `task` tool is available, every Jira-triggered story must launch at least one read-only sub-agent, normally using the `code-explorer` type. Choose each sub-agent's role, prompt, scope, and evidence request from the actual story rather than following a fixed decomposition.

Start with the highest-value independent investigation. Add a second concurrent sub-agent only when another perspective will materially improve the evidence; useful perspectives can include product requirements, repository documentation or logs, current code behavior, and focused test coverage. Use no more than two sub-agents, and give each only the issue context it needs. Never forward raw webhook payloads, secrets, credentials, environment values, or unrelated comments.

Sub-agents gather evidence and return concrete paths, relevant behavior, risks, confidence, and unanswered questions. They must not edit files, mutate git, install packages, call external services, create PRs, or update Jira. The parent owns synthesis and every mutation. A prepared task configuration, printed JSON, or task-tracker item is not a launched sub-agent: when delegating, confirm a native `task` call and its result. If the native `task` tool is unavailable, proceed with bounded direct investigation without announcing sub-agent availability issues. Use only exposed tools; never simulate or claim delegation that did not occur. If delegated investigations fail and missing evidence prevents a safe decision, ask for human input. For non-Jira requests, use bounded direct exploration when delegation would not add value.

## Evidence Waypoints

For bug-first demos, make the reasoning path visible. The conversation, PR body, and final issue comment should include these waypoints:

- `Stop 1 - Ticket`: the sparse issue and the business-language clues used.
- `Stop 2 - Wiki/Docs`: the wiki or docs checked, with relevant paths; if none are relevant or accessible, say so.
- `Stop 3 - Logs`: log attachments or fixtures checked, with relevant paths and any discovered error codes; if no logs are available, say so.
- `Stop 4 - Repo/Files`: the repo and files that explain the bug and fix.
- `Stop 5 - Tests/PR`: tests added or run, validation result, and draft PR link.

## OpenSpec-Style Change Artifacts

Use `references/open-spec-template.md` and `references/story-artifacts.md` for the required folder shape, headings, and demo-friendly language. The artifacts are not ceremony; they are the contract that connects the request, implementation, QA, review, and human follow-up.

The change folder must include:

- source issue/comment link
- proposal with why, what changes, impact, assumptions, and non-goals
- spec delta with acceptance criteria expressed as requirements and scenarios
- design notes for the smallest safe implementation
- task checklist
- human gates
- validation plan
- evidence checklist
- evidence waypoints for wiki/docs, logs, repo/files, tests, and PR

If a request has unresolved product, security, data, or environment questions, post the partial OpenSpec-style change and label `openhands:needs-human` instead of guessing.

## Repository Context and Examples

Use the target repository's instructions, documentation, code, and tests to establish its product rules. Examples illustrate the workflow; they do not supply requirements for an unrelated request.

For the Petstore demo, see [the implementation map](references/petstore-implementation-map.md).

## Stop Conditions

Ask for human input if the issue requires a product decision, schema migration, auth change, new dependency, environment change, secret access, or production mutation.

## PR Requirements

The PR body must show:

- OpenSpec change path
- evidence waypoints, including wiki/docs and logs checked
- assumptions and non-goals
- acceptance criteria status
- files changed
- tests run
- residual risks
- reminder that humans approve review and merge decisions

When the repo supports the chained automations, add `openhands-review` to the PR after it is created or updated. Code review then adds `openhands-qa` after posting its findings. These handoffs start bounded automation work only; they must not approve, merge, bypass branch protection, or remove human PR review.
