# Design

## Context

The Petstore catalog stores pet availability in the `status` field. The `search_pets()` function in `catalog.py` has a default parameter `status="available"`, but when the status is normalized to an empty string (line 41), the filtering condition on line 50 (`if normalized_status and normalized_status != pet.status`) fails to apply any status filter because the truthiness check fails.

This means callers can bypass status filtering by passing `status=""`, allowing pending pets like Nova (pet-103) to appear in what should be available-only results.

## Root Cause

In `app/petstore_app/catalog.py`:

```python
def search_pets(
    query: str = "",
    *,
    species: str | None = None,
    status: str = "available",  # Default is correct
    tag: str | None = None,
    max_results: int = 10,
) -> list[Pet]:
    # ...
    normalized_status = status.strip().lower()  # Empty string becomes ""
    # ...
    if normalized_status and normalized_status != pet.status:  # BUG: empty string bypasses this
        continue
```

## Decision

- Change the status filtering logic to treat empty strings as `"available"`.
- Ensure the default `"available"` filter always applies unless explicitly overridden.
- Preserve explicit `status="pending"` searches for support workflows.
- Add regression test for `status=""` edge case.

## Implementation

Modify `catalog.py` line 41 to default empty status to "available":

```python
normalized_status = (status.strip().lower() if status.strip() else "available")
```

This ensures:
- Default calls get `"available"` filtering
- Empty string calls get `"available"` filtering (fixing the bug)
- Explicit `status="pending"` calls still work
- All other explicit status values work as before

## Risks

- A broad fix could hide pending pets from support workflows that explicitly request them.
  - **Mitigation**: We only change empty-string handling; explicit `status="pending"` is preserved.
- Existing callers relying on `status=""` bypassing the filter will change behavior.
  - **Mitigation**: This is the desired fix - `status=""` bypassing the filter was the bug.

## Validation Plan

- Add regression test: `test_search_pets_defaults_empty_status_to_available()`
- Add regression test: `test_search_pets_excludes_pending_from_default_search()`
- Run focused catalog tests: `python3 -m pytest -q app/tests/test_pet_catalog.py`
- Run full test suite: `python3 -m pytest -q app/tests`
- Confirm existing "pending" test still passes (explicit status="pending" still works)
