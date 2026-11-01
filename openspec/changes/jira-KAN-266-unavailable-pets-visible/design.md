# Design

## Context

The Petstore demo catalog has four pets: three with `status="available"` (Mochi, Scout, Pip) and one with `status="pending"` (Nova/pet-103). The product rule states that default customer-facing searches must show only available pets.

Backend investigation shows:
- `app/petstore_app/catalog.py`: `search_pets()` correctly defaults to `status="available"` and filters properly.
- `app/petstore_app/adoptions.py`: `create_adoption_order()` validates `pet.status != "available"` and raises an error.
- `app/web/app.js`: The UI filter on line 17 checks `pet.status === "available"`.

The error log `docs/logs/pending-pet-visible.ndjson` shows error code `PENDING_PET_VISIBLE` for `pet-103` in the `petstore-web` component, suggesting the UI is the source of the issue.

## Decision

- Add comprehensive test coverage for the default search behavior to verify pending pets are excluded.
- Add a test that specifically checks Nova (pet-103) does not appear in default searches.
- Verify the UI filter works correctly by ensuring test coverage exists for frontend behavior.
- Keep backend code unchanged since it already implements the correct filter.

The backend is already correctly implemented. The fix focuses on:
1. Adding explicit regression tests that would catch this bug
2. Ensuring test coverage for all default-search scenarios
3. Documenting the expected behavior clearly

## Risks

- **False negative**: If the UI filter is working correctly but tests don't cover all scenarios, the bug might still exist in edge cases.
- **Mitigation**: Add multiple test scenarios (default search, empty query, species filter).

- **Test-only change**: Adding only tests without fixing code assumes the current code is correct.
- **Mitigation**: Run the tests to verify current behavior matches requirements.

## Validation Plan

```bash
# Run existing catalog tests
python3 -m pytest -q app/tests/test_pet_catalog.py

# Run new regression tests
python3 -m pytest -q app/tests/test_pet_catalog.py::test_default_search_excludes_pending_pets
python3 -m pytest -q app/tests/test_pet_catalog.py::test_species_search_excludes_pending_pets

# Run all tests
python3 -m pytest -q
```

For UI verification (if Playwright or similar tooling is available):
```bash
python3 skills/sdlc-qa/scripts/with_server.py \
  --server "python3 -m http.server 4173 --directory app/web" \
  --port 4173 \
  -- python3 skills/sdlc-qa/scripts/static_ui_smoke.py --url http://localhost:4173
```
