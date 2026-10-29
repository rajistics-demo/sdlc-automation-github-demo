# Design

## Context

The Petstore catalog uses an in-memory tuple of Pet objects in `app/petstore_app/catalog.py`. The `search_pets()` function filters pets based on query parameters including `status`, which defaults to `"available"`.

The current implementation has a bug at line 41-50:
```python
normalized_status = status.strip().lower()
# ...
if normalized_status and normalized_status != pet.status:
    continue
```

When `status=""` or `status="  "` is passed, `normalized_status` becomes an empty string (after `strip().lower()`), which is falsy in Python. This causes the `if normalized_status` condition to short-circuit, skipping the status filter entirely and exposing all pets including pending ones.

**Relevant constraints:**
- Product rule: Default pet search returns only available pets
- Operations must still be able to explicitly request `status="pending"`
- Money is represented as integer cents (unchanged)
- No persistence layer or database (in-memory only)
- Tests run with `python3 -m pytest -q`

## Decision

Normalize empty or whitespace-only status values to `"available"` at the normalization step:

```python
normalized_status = status.strip().lower() if status.strip() else "available"
```

Then use a straightforward status comparison:

```python
if normalized_status != pet.status:
    continue
```

This ensures:
1. Empty or whitespace-only status values are treated as `"available"`
2. Explicit status values like `"pending"` still work correctly for operations workflows
3. The default parameter value remains `"available"` for backwards compatibility
4. The filtering logic is simple and clear

**Alternative considered:**
Using a nested `if` to check for empty status was more complex and harder to understand. The normalization approach is cleaner.

## Risks

- **Risk:** Breaking existing callers that explicitly pass `status="pending"`
  - **Mitigation:** Existing test `test_search_pets_can_find_pending_pets_when_requested()` verifies this continues to work
  
- **Risk:** Performance impact from additional normalization check
  - **Mitigation:** Negligible - single conditional expression evaluated once per call

- **Risk:** Empty status might be semantically different from "show all"
  - **Mitigation:** Product rules and wiki docs explicitly state default must be available-only; "show all" is not a supported use case

## Validation Plan

1. Run existing tests to ensure no regressions:
   ```bash
   python3 -m pytest -q app/tests/test_pet_catalog.py
   ```

2. Add new regression tests:
   - `test_search_pets_default_excludes_pending()` - verifies default search excludes Nova
   - `test_search_pets_empty_status_excludes_pending()` - verifies empty string doesn't bypass filter
   - `test_search_pets_whitespace_status_excludes_pending()` - verifies whitespace doesn't bypass filter

3. Run full test suite:
   ```bash
   python3 -m pytest -q
   ```

4. Verify the fix with direct Python reproduction:
   ```python
   from app.petstore_app.catalog import search_pets
   # Should exclude pet-103 (Nova)
   assert "pet-103" not in [p.id for p in search_pets()]
   assert "pet-103" not in [p.id for p in search_pets(status="")]
   assert "pet-103" not in [p.id for p in search_pets(status="  ")]
   # Should include pet-103 when explicitly requested
   assert "pet-103" in [p.id for p in search_pets(status="pending")]
   ```
