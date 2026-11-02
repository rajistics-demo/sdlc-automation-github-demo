# Design

## Context

The Petstore catalog search function in `app/petstore_app/catalog.py` filters pets by status with a default of "available". The current implementation has a subtle bug on line 50:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

When `normalized_status` is an empty string (from `status=""`), the condition evaluates to `False` because empty strings are falsy in Python, causing the status filter to be skipped entirely. This allows pending pets like Nova (pet-103) to appear in results that should only show available pets.

The issue was identified through:
- Jira ticket KAN-268 describing customer-facing confusion
- Log evidence in `docs/logs/pending-pet-visible.ndjson` with error code `PENDING_PET_VISIBLE`
- Wiki documentation in `docs/wiki/petstore-catalog-availability.md` establishing the availability rules
- Reproduction confirming `search_pets(status="")` returns Nova alongside available pets

## Decision

- Change the filter condition from `if normalized_status and normalized_status != pet.status:` to `if normalized_status != pet.status:`.
- This ensures the status filter always applies, treating empty strings as meaningful filter values that must match the pet's status.
- Since no pet has `status=""`, an empty status parameter will exclude all pets unless other filters match, which is the correct defensive behavior.
- Actually, reconsidering: we want empty status to behave like the default (show only available). Better approach: normalize empty status to "available" explicitly.
- Final decision: Change to `if status and normalized_status != pet.status:` and add explicit handling for empty status strings.
- Simplest fix: Remove the `normalized_status and` check, making the filter always apply. Empty status won't match any pet status, effectively excluding all pets, which is safe. But this changes behavior - existing callers passing empty status would get no results.
- Best approach: Check `if normalized_status` is falsy and treat it as the default "available". This maintains backward compatibility while fixing the bug.

Final implementation:
```python
# Treat empty status as "available" (the default behavior)
if not normalized_status:
    normalized_status = "available"
    
# Apply status filter consistently
if normalized_status != pet.status:
    continue
```

## Risks

- **Backward compatibility**: If any code currently relies on `status=""` to return all pets regardless of status, this fix will break that behavior. Mitigation: The product rules and tests show this was never intended; empty status should return available pets like the default.
- **Performance**: No impact - same number of comparisons.
- **Test coverage**: Existing tests don't cover the empty status case. Mitigation: Add explicit regression tests.

## Validation Plan

- Add test case: `test_search_pets_with_empty_status_excludes_pending()` to verify `search_pets(status="")` excludes Nova.
- Add test case: `test_search_pets_default_excludes_pending()` to explicitly document default behavior.
- Run existing test suite: `python3 -m pytest -q app/tests/test_pet_catalog.py`
- Run full test suite: `python3 -m pytest -q`
- Verify the fix doesn't break adoption validation tests in `app/tests/test_adoptions.py`.
