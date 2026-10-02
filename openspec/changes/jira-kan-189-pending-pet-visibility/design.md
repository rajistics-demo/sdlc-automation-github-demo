# Design

## Context

The Petstore catalog search function in `app/petstore_app/catalog.py` provides filtering by species, status, tag, and text query. The product requirement is that default searches return only available pets. Pending pets should only appear when explicitly requested with `status="pending"`.

The current implementation has a bug at line 50 where the status filter uses a truthiness check:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

This pattern differs from the intended behavior because:
- The `status` parameter has type `str` with default value `"available"`
- Other optional filters (species, tag) use `str | None` type and correctly use truthiness checks
- The truthiness check on `normalized_status` allows empty strings to bypass filtering
- When `status=""` is passed, `normalized_status` becomes `""` (falsy), and the entire condition short-circuits to `False`

## Decision

**Remove the truthiness check from the status filter to match the parameter's type contract.**

Change line 50 from:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

To:
```python
if normalized_status != pet.status:
    continue
```

This makes the status filter consistent with its type signature (`str`, not `str | None`) and ensures that:
- Empty strings are treated as a status value to match against (which will exclude all pets since no pet has `status=""`)
- The default value `"available"` continues to work correctly
- Explicit status values like `"pending"` continue to work correctly
- The filter cannot be bypassed

**Alternative considered and rejected**: Adding validation to raise `ValueError` for empty strings would be more defensive but would be a breaking change for any code that currently relies on the bypass (even if unintentionally). The chosen fix maintains API compatibility while closing the security gap.

## Risks

**Risk**: Code that explicitly passes `status=""` and expects it to return all pets will now get empty results.

**Mitigation**: 
- Low likelihood - this is almost certainly unintentional behavior being exploited
- Frontend code uses hardcoded `status === "available"` check and is not affected
- Adoption flow already validates status correctly
- If legitimate use cases exist, they should use `status="available"` or `status="pending"` explicitly

**Risk**: The fix might not match the exact intended behavior for empty strings.

**Mitigation**:
- Empty string matching no pets is safe and closes the vulnerability
- If future requirements specify that empty strings should default to "available", we can add explicit normalization before the comparison
- Current fix is minimal and safe

## Validation Plan

1. Run existing tests to ensure no regressions:
   ```bash
   cd app && python -m pytest tests/test_pet_catalog.py -v
   ```

2. Add new regression test for empty status parameter:
   ```python
   def test_search_pets_with_empty_status_excludes_pending() -> None:
       results = search_pets(species="dog", status="")
       # Empty status should not bypass filter
       # Either returns nothing or only available (current fix: returns nothing)
       assert "pet-103" not in [pet.id for pet in results], "Nova (pending) should not appear"
   ```

3. Verify adoption flow still rejects pending pets:
   ```bash
   cd app && python -m pytest tests/test_adoptions.py::test_create_adoption_order_rejects_pending_pet -v
   ```

4. Run all backend tests as final validation:
   ```bash
   cd app && python -m pytest tests/ -v
   ```
