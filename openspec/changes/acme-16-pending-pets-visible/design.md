# Design

## Context

The `search_pets()` function in `app/petstore_app/catalog.py` filters pets by multiple criteria. The status filter (line 50) uses a truthy check that creates a bypass when empty strings are passed:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

When `status=""`, the condition `normalized_status and ...` evaluates to False (empty string is falsy), so the status filter is skipped entirely, allowing all pets (including pending ones) to be returned.

The function signature declares `status: str = "available"`, so the parameter is always a string in normal usage. The adoptions module (`adoptions.py`) already correctly validates that only available pets can be adopted (line 34-35).

## Decision

- Change line 50 from truthy check to explicit None check: `if normalized_status is not None and ...`
- Add a regression test that confirms `search_pets(status="")` returns no results (since no pet has an empty status)
- Keep the function signature unchanged to preserve the default behavior

## Risks

- **Low risk:** The fix is defensive; normal usage with the default parameter already works correctly
- **No breaking changes:** The function signature and default behavior remain unchanged
- **Test coverage:** Existing tests verify default and explicit pending searches continue to work

## Validation Plan

- Add test: `test_search_pets_empty_status_does_not_bypass_filter()` to verify empty string is treated as a filter value
- Run existing tests to ensure no regression (if pytest available)
- Manual code review of the one-line change
