# Design

## Context

The Petstore catalog search function (`app/petstore_app/catalog.py`) implements filtering by pet status. Product rules require:
- Default search returns only available pets
- Pending pets can be shown only when explicitly requested (`status="pending"`)
- Pending pets cannot be adopted

The current implementation has a logic error in the status filter condition that allows empty string to bypass filtering.

## Root Cause

Line 50 in `catalog.py`:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

When `status=""` is passed:
1. `normalized_status` becomes `""` (empty string)
2. The condition `normalized_status and ...` evaluates to `False` (empty string is falsy)
3. The filter is bypassed, returning ALL pets including pending ones

The log evidence (`PENDING_PET_VISIBLE` error for pet-103) confirms this regression occurred.

## Decision

- Change the condition from `if normalized_status and normalized_status != pet.status:` to `if normalized_status != pet.status:`
- This ensures empty string is compared to pet status, and since no pets have empty status, they will be filtered out
- Wait - that won't work correctly. Let me reconsider...

Actually, the better fix is to normalize empty status to "available":
- Add a line after line 41 to convert empty status to available: `if not normalized_status: normalized_status = "available"`
- This treats empty string the same as the default parameter value
- Preserves all existing behavior for explicit status values

## Risks

- **Risk**: Breaking existing explicit status filtering
- **Mitigation**: Add regression test for empty status; run full test suite

- **Risk**: Unintended behavior change for other edge cases
- **Mitigation**: Minimal change to logic; well-defined transformation

## Validation Plan

1. Run existing catalog tests: `python3 -m pytest -q app/tests/test_pet_catalog.py`
2. Add and run new test for empty status string
3. Verify Nova (pet-103) is excluded from `search_pets(status="")`
4. Verify explicit `status="pending"` still works for operations use case
5. Run full test suite: `python3 -m pytest -q`
