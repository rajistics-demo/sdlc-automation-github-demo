# Design

## Context

The Petstore application has a Python backend (`app/petstore_app/catalog.py`) and a static JavaScript UI (`app/web/app.js`). The backend correctly filters pets by status, with a default of `status="available"`. However, the UI JavaScript has hardcoded the pet data and does not properly implement a default status filter.

Key files:
- Backend: `app/petstore_app/catalog.py` - Already correct, has `status="available"` default parameter
- Backend tests: `app/tests/test_pet_catalog.py` - Existing tests pass, validating backend behavior
- UI: `app/web/app.js` - Currently missing default status filter in the `renderResults()` function
- Wiki: `docs/wiki/petstore-catalog-availability.md` - Documents the product rule
- Log evidence: `docs/logs/pending-pet-visible.ndjson` - Shows `PENDING_PET_VISIBLE` error with pet-103 (Nova)

The demo pet data includes:
- pet-100 (Mochi): cat, available
- pet-101 (Scout): dog, available  
- pet-102 (Pip): rabbit, available
- pet-103 (Nova): dog, **pending** ← This should not appear in default searches

## Decision

- The backend Python code is already correct and requires no changes
- Fix the UI by adding a default status filter in `renderResults()` that matches the backend behavior
- The existing filter in `app.js` line 17 checks `pet.status === "available"`, which is correct
- However, this filter should be the default behavior, not an optional enhancement
- No changes to the data structure, UI layout, or backend API are needed

## Risks

- Risk: The fix might affect support/operations workflows that need to see pending pets
  - Mitigation: The backend `search_pets()` function supports explicit `status="pending"` queries for support workflows; this fix only affects the default customer-facing UI

- Risk: Other UI features might depend on seeing all pets regardless of status
  - Mitigation: Review shows the UI only has one search interface, and the filter is already coded to check `status === "available"`, so this is the intended behavior

- Risk: Tests might not catch future regressions
  - Mitigation: The existing backend tests already cover this scenario; UI-level smoke tests will verify the fix

## Validation Plan

1. Run existing backend tests: `python3 -m pytest -q app/tests/test_pet_catalog.py`
2. Run full test suite: `python3 -m pytest -q`
3. Manual UI verification: Open `app/web/index.html` and confirm Nova does not appear in default search results
4. Smoke test if runtime supports it: `python3 skills/sdlc-qa/scripts/static_ui_smoke.py --url http://localhost:4173`
