# Design

## Context

The Petstore catalog stores pet availability in the `status` field. Default search behavior should return available pets only, while explicit status searches can inspect pending pets for support or operational workflows.

Customer reports indicate that Nova (pet-103 with status="pending") is appearing in the default available-pets experience. The backend `search_pets()` function defaults to `status="available"` and the adoption flow correctly rejects pending pets, so the issue is in the frontend UI filter.

## Decision

- Verify the frontend `app/web/app.js` filter includes the status check: `pet.status === "available"`
- Ensure the filter applies on both initial page load and search button click
- Preserve explicit `status="pending"` searches in the backend API
- Keep backend defaults unchanged (already correct)
- Add no new dependencies or schema changes

## Risks

- **Low risk**: Frontend filter change is isolated and well-tested
- **Mitigation**: Backend already prevents pending pet adoptions
- **Regression protection**: Existing backend tests verify correct behavior
- **Rollback**: Simple revert if issues arise

## Validation Plan

- Run backend unit tests: `PYTHONPATH=app python3 -m pytest app/tests/ -v`
- If Playwright available: Run UI smoke test to verify Nova excluded from default view
- If Playwright unavailable: Document that UI evidence should be captured in deployment environment
