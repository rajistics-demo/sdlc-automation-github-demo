# Agent Instructions

This is the GitHub-native SDLC Automation Demo. Customer-facing language should say "SDLC Automation Demo" and should not use "software factory."

## Repository Shape

- Petstore app: `app/petstore_app/`
- Backend tests: `app/tests/`
- Static UI: `app/web/`
- GitHub automations: `automations/github/`
- Repo-local OpenHands skills: `skills/`
- Setup and registration scripts: `scripts/`
- Demo docs: `docs/`
- Durable repo memory: `docs/repo-memory/`

## Automation Rules

- Humans approve scope, reviews, PRs, merges, deployments, and production changes.
- OpenHands may create branches, tests, comments, reports, and draft PRs when the relevant GitHub label or comment asks it to.
- Do not push directly to `main`.
- Do not print or commit secrets.
- Prefer deterministic scripts and preflight checks before spending LLM calls.
- Use `docs/repo-memory/` and `skills/sdlc-context-reuse/SKILL.md` before broad exploration; use lower-cost scout/model profiles for context gathering when available.
- Use event-driven GitHub triggers instead of polling.
- Avoid dependency installation in automation helper scripts unless a prompt explicitly authorizes it.

## Start From Existing Context

For story-to-PR work, start with `skills/sdlc-story/SKILL.md` and `docs/repo-memory/petstore-intelligence.md`; use the linked implementation map before broad file discovery.

App tests run directly from the checkout with `python3 -m pytest -q app/tests`. The sandbox setup should provide pytest before the conversation starts; this repository does not support `pip install -e .`. If pytest is missing, report the setup gap rather than trying packaging workarounds.

Automation checkouts can be shallow. Check `git rev-parse --is-shallow-repository` before treating history as evidence; a grafted root does not show when its files were introduced.

## Petstore Product Rules

- Default pet search returns only available pets.
- Pending pets can be shown only when explicitly requested and cannot be adopted.
- Money is represented as integer cents.
- UI-visible changes need UI evidence, not only unit tests.
