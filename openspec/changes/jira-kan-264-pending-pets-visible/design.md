# Design

## Context

The Petstore catalog implements `search_pets()` in `app/petstore_app/catalog.py`. The function accepts optional filters including a `status` parameter that defaults to `"available"`.

The current implementation has a bug on line 50:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

When `status=""` is passed, after `.strip().lower()` the result is an empty string. In Python, empty strings are falsy, so `if normalized_status` evaluates to `False`, causing the entire status filter to be skipped. This allows pending pets to appear in results.

The product rule from `docs/wiki/petstore-catalog-availability.md` is clear: "Default customer-facing catalog search must show only pets with status='available'."

## Decision

- Change the filter condition to check if `normalized_status != pet.status` without the truthiness check
- This ensures the filter is always applied when a status parameter is provided
- The default value `status="available"` remains unchanged
- Empty strings will now properly compare against pet.status and filter correctly

Implementation change in `catalog.py` line 50:

```python
# Before:
if normalized_status and normalized_status != pet.status:
    continue

# After:
if normalized_status != pet.status:
    continue
```

This is the smallest safe change. The default parameter already ensures `status="available"` when not specified.

## Risks

- **False positive risk**: Low. All existing tests pass, and the change only makes the filter more strict.
- **Backward compatibility**: The default behavior (returning only available pets) is unchanged. Any code explicitly passing `status=""` to bypass the filter was relying on a bug and will now correctly filter to available pets only.
- **Test coverage**: Add regression tests to ensure empty status strings do not bypass the filter.

## Validation Plan

1. Run existing catalog tests: `python3 -m pytest -q app/tests/test_pet_catalog.py`
2. Add new regression tests for empty status scenarios
3. Run full test suite: `python3 -m pytest -q`
4. Verify Nova (pet-103) does not appear in default or empty-status searches
