# Design

## Context

The Petstore catalog search in `app/petstore_app/catalog.py` provides a `search_pets()` function with a default parameter `status: str = "available"`. The function iterates through all pets and filters them based on status, species, and tag criteria.

The current implementation at line 50 uses:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

This guard has a critical flaw: when `normalized_status` is an empty string (falsy), the entire condition short-circuits to `False`, completely bypassing the status filter. This allows pending pets to leak into results that should be available-only.

The web UI (`app/web/app.js`) already has its own client-side filter (`pet.status === "available"`) and is unaffected by this backend bug.

## Decision

- **Remove the `normalized_status and` guard**: Change line 50 to `if normalized_status != pet.status:` so the filter is always applied
- **Keep the default parameter**: `status: str = "available"` remains unchanged; this protects the common no-argument call path
- **No API signature changes**: Existing callers are unaffected; the fix corrects an unintended behavior (empty string bypass)
- **Add regression test**: Create `test_search_pets_empty_status_does_not_bypass_filter()` to prevent recurrence

This is the smallest safe fix. A more robust long-term design would use `status: str | None = "available"` to make "no filter" explicit via `None`, but that requires type signature changes and is out of scope for this urgent bug fix.

## Risks

- **Risk**: Unknown callers may be passing `status=""` intentionally to mean "all statuses"
  - **Mitigation**: Investigation found no such callers; the incident log shows this was an unintended bug, not a feature. If such a caller exists, they should be updated to use explicit status values or refactored to use a future `None`-based API.

- **Risk**: The fix might not catch all edge cases (e.g., `None` passed explicitly)
  - **Mitigation**: The current type signature (`status: str`) prevents `None` from being passed. Future improvements can add explicit `None` support with proper typing.

## Validation Plan

1. Run existing catalog tests to ensure no regressions: `python -m pytest app/tests/test_pet_catalog.py -v`
2. Add and run new test `test_search_pets_empty_status_does_not_bypass_filter`
3. Verify the incident scenario no longer occurs: search with empty status must exclude pending pets
