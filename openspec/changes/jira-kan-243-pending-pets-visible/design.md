# Design

## Context

The Petstore catalog's `search_pets()` function filters pets by name, species, status, and tags. The default `status` parameter is `"available"`, but the filtering logic uses `if normalized_status and normalized_status != pet.status:` which treats empty strings as falsy and skips the status filter entirely.

When `status=""` is passed (empty string), the normalized value is also an empty string, which is falsy in Python. The condition `if normalized_status and ...` short-circuits, and the status filter is bypassed, allowing both available AND pending pets to be returned.

The Petstore product rules (from `AGENTS.md` and `docs/wiki/petstore-catalog-availability.md`) state:
- Default pet search returns only available pets.
- Pending pets can be shown only when explicitly requested and cannot be adopted.

## Decision

Normalize empty or whitespace-only status strings to `"available"` early in the `search_pets()` function:

```python
normalized_status = (status.strip().lower() if status.strip() else "available")
```

This ensures:
- `status="available"` → `"available"` (default behavior, unchanged)
- `status=""` → `"available"` (bugfix: now filters correctly)
- `status="pending"` → `"pending"` (support workflow, unchanged)
- `status="  "` (whitespace) → `"available"` (robust edge case handling)

The existing filter logic then works correctly:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

## Risks

- **Low implementation risk**: This is a one-line change to status normalization logic.
- **No breaking changes**: Function signature and default parameter values remain unchanged.
- **No schema changes**: Pet data structure is unchanged.
- **Backward compatible**: Explicit `status="pending"` still works for support workflows.
- **No UI changes required**: The static UI (`app/web/app.js`) already filters for `status === "available"`.

## Validation Plan

1. Add a regression test proving `search_pets(species="dog", status="")` returns only available pets.
2. Verify existing tests still pass (default available, explicit pending, species filtering).
3. Run full catalog test suite: `pytest app/tests/test_pet_catalog.py -v`.
4. Manual verification with Python REPL to confirm edge case behavior.
