# Design

## Context

The Petstore catalog search function in `app/petstore_app/catalog.py` has a status filter on lines 50-51. The current implementation uses:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

The problem: when `normalized_status` is an empty string (from `status=""` or `status="  ".strip()`), the condition `if normalized_status` evaluates to `False` because empty strings are falsy in Python. This causes the entire status filter to be skipped, allowing pending pets to appear in search results.

Documentation in `docs/wiki/petstore-catalog-availability.md` clearly states that default customer-facing catalog search must show only available pets. Log evidence in `docs/logs/pending-pet-visible.ndjson` confirms the bug has occurred with error code `PENDING_PET_VISIBLE`.

## Decision

**Option A (Recommended): Normalize empty status to default**
At the top of the function, after normalization, replace any empty status with the default:

```python
normalized_status = status.strip().lower()
if not normalized_status:
    normalized_status = "available"
```

Then simplify the filter to:

```python
if normalized_status != pet.status:
    continue
```

This approach:
- Makes the intent explicit: empty means use the default
- Keeps the filter logic simple and readable
- Ensures the status filter always applies
- Matches the function signature default of `status="available"`

**Option B (Rejected): Remove the truthiness check**
Simply change line 50 to `if normalized_status != pet.status:` without normalizing empty strings. This would make empty status match ALL pets (wrong behavior).

**Option C (Rejected): Add validation**
Raise an error when status is empty. Too strict - breaks the default parameter pattern.

## Risks

- **Behavior change for empty string callers**: If any code explicitly passes `status=""` expecting to bypass the filter, that code will break. Mitigation: Investigation shows no current callers pass empty strings.
- **Type hint mismatch**: The function signature allows `status: str = "available"` but doesn't prevent empty strings. Mitigation: Runtime normalization handles this gracefully.
- **Performance**: Adding normalization adds minimal overhead (one string check). Mitigation: Acceptable for catalog search use case.

## Validation Plan

1. Run existing tests to ensure no regression:
   ```bash
   cd /workspace/project/sdlc-automation-github-demo && python -m pytest app/tests/test_pet_catalog.py -v
   ```

2. Add new test cases for edge cases:
   - `test_search_pets_with_empty_status_defaults_to_available()`
   - `test_search_pets_with_whitespace_status_defaults_to_available()`

3. Verify the fix prevents the PENDING_PET_VISIBLE error:
   ```python
   # Should return only Scout (pet-101), not Nova (pet-103)
   results = search_pets(species="dog", status="")
   assert all(pet.status == "available" for pet in results)
   ```
