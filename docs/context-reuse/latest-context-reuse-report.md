# Context Scout Issue Brief

This brief turns the issue into the context the next OpenHands work cell needs. The scout uses repo memory, skills, prior evidence, and targeted search internally; the visible output stays focused on the decision and handoff.

## Issue

- Event: `issues.labeled`
- Item: `#63`
- Source: https://github.com/rajistics-demo/sdlc-automation-github-demo/issues/63
- Title: Customers are seeing pets that are not available
- Labels: `type:bug`, `openhands-context`
- Body signal: Support says Nova is showing up in the available pets list even though she should not be adoptable. Logs mention PENDING_PET_VISIBLE. Please run the context scout before implementation so we can reuse repo memory, prior evidence, and targeted search.

## What The Issue Needs

- Investigate why a pending or unavailable pet is appearing in the available-pets experience, then preserve the default available-only catalog behavior.
- Learned from: issue title/body, `AGENTS.md`, and `docs/repo-memory/petstore-intelligence.md`.
- Treat the issue and its comments as the source of truth; ask a human only if scope, credentials, or production action is unclear.

## Relevant Product Context

- Default pet search returns only available pets. (Sources: `AGENTS.md`, `docs/repo-memory/petstore-intelligence.md`)
- Pending pets can be shown only when explicitly requested and cannot be adopted. (Sources: `AGENTS.md`, `docs/repo-memory/petstore-intelligence.md`)
- Humans approve scope, PR review, merge, deployment, and risky follow-up decisions. (Sources: `AGENTS.md`, `docs/repo-memory/petstore-intelligence.md`)
- UI-visible changes need UI evidence, not only backend tests. (Sources: `AGENTS.md`, `docs/repo-memory/petstore-intelligence.md`)

## Existing Code Or New PR?

- First check whether existing catalog code and tests already exclude pending pets from the default available-pets path.
- If existing code and tests already prove the behavior, do not open a code PR; post evidence and mark the issue complete or ask for the missing reproduction.
- If the issue reproduces, or if the regression test is missing, open a PR with a focused catalog fix and regression test.

## Likely Files And Tests

- `app/petstore_app/catalog.py`: catalog search, status, fee, and availability behavior. (Sources: `docs/repo-memory/petstore-intelligence.md`, targeted repo search)
- `app/tests/test_pet_catalog.py`: focused catalog regression tests. (Sources: `docs/repo-memory/petstore-intelligence.md`, targeted repo search)
- `app/web/app.js`: static UI catalog filter. (Sources: `docs/repo-memory/petstore-intelligence.md`, targeted repo search)
- `app/web/tests/catalog-search.playwright.mjs`: browser evidence pattern for catalog UI changes. (Sources: `docs/repo-memory/petstore-intelligence.md`, targeted repo search)
- `app/web/tests/README.md`: static UI surface or browser evidence path. (Sources: `docs/repo-memory/petstore-intelligence.md`, targeted repo search)
- `app/tests/test_adoptions.py`: adoption behavior tests. (Sources: `docs/repo-memory/petstore-intelligence.md`, targeted repo search)

## Cited Handoff Material

- Issue source: title/body/comments on the GitHub issue remain the source of truth.
- `app/petstore_app/catalog.py`: L23: Pet("pet-103", "Nova", "dog", "pending", ("active", "training"), 14, 11000),
- `app/petstore_app/catalog.py`: L50: if normalized_status and normalized_status != pet.status:
- `app/tests/test_pet_catalog.py`: L12: def test_search_pets_can_find_pending_pets_when_requested() -> None:
- `app/tests/test_pet_catalog.py`: L13: results = search_pets(species="dog", status="pending")
- `app/web/app.js`: L5: { id: "pet-103", name: "Nova", species: "dog", status: "pending", tags: ["active", "training"], fee: "$110" },
- `app/web/app.js`: L17: && pet.status === "available";
- `app/web/tests/catalog-search.playwright.mjs`: L155: scenarios.push("Default catalog shows available pets and excludes pending pets");
- `app/web/tests/catalog-search.playwright.mjs`: L175: assert(emptyText === "No available pets match this search.", "pending pet search should show empty state");
- `app/web/tests/README.md`: L15: - GIF preview when `ffmpeg` is available
- `app/web/tests/README.md`: L44: If the runtime does not already have Playwright or BrowserToolSet available,
- `app/tests/test_adoptions.py`: L19: def test_create_adoption_order_rejects_pending_pet() -> None:
- `app/tests/test_adoptions.py`: L20: with pytest.raises(ValueError, match="not available"):
- Memory source: `docs/repo-memory/previous-agent-runs.md` for prior lessons and reusable file-path hints.

## Reusable Memory

- `AGENTS.md` and `docs/repo-memory/petstore-intelligence.md` provide product rules and app map.
- Use `skills/sdlc-context-reuse/SKILL.md` first, then the specific build, QA, or review skill required by the next label.
- `docs/repo-memory/previous-agent-runs.md` captures prior lessons so the next agent does not rediscover file paths and demo guardrails.

## Recommended Next Steps

- If focused tests prove existing behavior already satisfies the issue, post evidence instead of opening a PR.
- Apply `openhands-build` only when reproduction or missing coverage shows a code change is needed.
- Run focused tests before broad QA; start with `python3 -m pytest -q` and the relevant Petstore test file.
- Apply `openhands-qa` on the PR if behavior is UI-visible or needs additional evidence.
- Keep production, deployment, and merge decisions with humans.

## Cost Routing

- Scout/context summary: lower-cost model or deterministic script.
- Code edits and risk-sensitive reasoning: coding model.
- Verification summaries: deterministic commands or lower-cost model.
- Approximate context avoided before coding: ~82847 tokens.

Exhaustive search provenance is intentionally omitted. The cited material above is the handoff raw material for deciding whether to open a PR and for drafting that PR if needed.

