# Design

## Context

The Petstore catalog uses `app/petstore_app/catalog.py::search_pets()` to filter pets by status, species, and tags. Product requirements (`docs/wiki/petstore-catalog-availability.md`) state that default customer-facing searches must show only `status="available"` pets.

Current implementation:
- Line 31: Function parameter `status: str = "available"`
- Line 41: `normalized_status = status.strip().lower()`
- Line 50: `if normalized_status and normalized_status != pet.status:`

The bug: when `status=""` (empty string), the falsy check `if normalized_status and ...` skips the status filter entirely, allowing pending pets through.

## Decision

- Treat empty or whitespace-only status as "available" by modifying line 41
- Remove the falsy check from line 50 since normalized_status will never be empty
- Keep the function signature unchanged to preserve API compatibility
- Add regression tests for empty status and default behavior

Implementation:
```python
# Line 41 - treat empty status as "available"
normalized_status = status.strip().lower() if status.strip() else "available"

# Line 50 - remove falsy check since normalized_status is guaranteed non-empty
if normalized_status != pet.status:
    continue
```

## Risks

- **Low risk:** Single-line logic change with deterministic pass/fail criteria
- **No breaking changes:** API signature and explicit status values unchanged
- **UI unaffected:** The static UI already filters by `status === "available"` (app/web/app.js:17)
- **Mitigation:** Comprehensive test coverage for empty, default, and explicit status cases

## Validation Plan

```bash
python3 -m pytest -q app/tests/test_pet_catalog.py
python3 -m pytest -q
```

Tests to add:
1. `test_search_pets_default_excludes_pending` - verify default call excludes Nova
2. `test_search_pets_empty_status_excludes_pending` - verify `status=""` excludes Nova
3. Existing test `test_search_pets_can_find_pending_pets_when_requested` - verify explicit pending still works
