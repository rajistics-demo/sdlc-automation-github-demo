# Design

## Context

The petstore catalog search is implemented in `app/petstore_app/catalog.py`. The `search_pets()` function has a status parameter that defaults to `"available"`. The current implementation has a bug on line 50:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

When `status=""` (empty string), after normalization via `.strip().lower()`, `normalized_status` becomes an empty string. The condition `if normalized_status` evaluates to `False`, causing the entire status filter to be skipped. This allows pending pets to appear in results when they shouldn't.

The product rule states: "Default pet search returns only available pets. Pending pets can be shown only when explicitly requested and cannot be adopted."

## Decision

- Change the status filter condition to treat empty/whitespace status as "available" (the default)
- Update line 41 to set `normalized_status` to `"available"` when the trimmed status is empty
- This preserves the ability to explicitly search for pending pets while fixing the default behavior
- Keep the existing default parameter value unchanged for backward compatibility

## Implementation

Replace line 41 in `catalog.py`:

```python
# Before
normalized_status = status.strip().lower()

# After
normalized_status = status.strip().lower() or "available"
```

This ensures that an empty or whitespace-only status parameter is treated as `"available"`.

## Risks

- **Backward compatibility**: Callers currently passing `status=""` to get all pets will now get only available pets. Mitigation: This aligns with documented product behavior; explicit status values still work.
- **Test coverage**: Existing tests don't cover the empty status case. Mitigation: Add regression test for `search_pets(status="")`.

## Validation Plan

1. Add regression test: `test_search_pets_empty_status_defaults_to_available()`
2. Run existing test suite: `python3 -m pytest -q app/tests/test_pet_catalog.py`
3. Run full test suite: `python3 -m pytest -q`
4. Manual verification: Confirm `search_pets(status="")` excludes pending pets
