# Design

## Context

The Petstore catalog search function (`search_pets()` in `app/petstore_app/catalog.py`) has a default parameter `status: str = "available"`. However, the filtering logic on lines 50-51 uses a falsy check that skips the status filter when an empty string is passed:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

When `status=""` is passed (or any whitespace-only string), `normalized_status` becomes `""` which is falsy, causing the entire filter to be skipped. This allows pending pets like Nova (pet-103) to appear in search results where they shouldn't.

## Decision

- Normalize empty or whitespace-only status values to the default "available" status immediately after the strip operation.
- Keep the default parameter `status: str = "available"` unchanged.
- Add explicit handling: `if not normalized_status: normalized_status = "available"`.
- This ensures the status filter always applies unless explicitly overridden with a valid non-empty status.

## Alternatives Considered

1. **Remove the falsy check**: Change line 50 to `if normalized_status != pet.status:` - This would work but would make the logic less clear about what happens when status is None.
2. **Validate at parameter level**: Reject empty status values - This is too strict and would break backwards compatibility if any code relies on empty strings falling back to default.
3. **Use `status or "available"`**: This is Pythonic but doesn't handle whitespace-only strings like `"  "`.

## Risks

- Low risk: This is a focused change to a single normalization step.
- Regression risk: Explicit status searches (like `status="pending"`) are unaffected.
- Backward compatibility: Any code passing empty status will now correctly get only available pets instead of all pets (this is the desired fix).

## Validation Plan

- Add regression test: `test_search_pets_with_empty_status_returns_only_available()` verifying empty string returns only available pets.
- Verify existing test `test_search_pets_can_find_pending_pets_when_requested()` still passes, confirming explicit pending searches work.
- Run full test suite: `python -m pytest app/tests/test_pet_catalog.py -v`.
