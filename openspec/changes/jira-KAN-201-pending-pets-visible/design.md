# Design

## Context

The `search_pets` function in `app/petstore_app/catalog.py` has a default parameter `status="available"` on line 31. However, the filter condition on line 50 is:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

When an empty string is passed for status (e.g., from a form submission or API call with `status=""`), the normalized value becomes `""` (line 41). In Python, empty strings are falsy, so the condition `if normalized_status and ...` evaluates to `False`, causing the status filter to be skipped entirely. This allows pending pets to appear in results.

The petstore product rule states: "Default pet search returns only available pets."

## Decision

- Change the filter condition from `if normalized_status and normalized_status != pet.status:` to `if normalized_status != pet.status:`
- This ensures the status filter always applies when a status parameter is provided or uses the default
- Empty strings will now be compared against pet.status, failing to match and filtering out non-available pets as expected
- The default parameter value of "available" ensures backward compatibility

## Risks

- **Low risk of regression**: Existing tests verify that explicit status values work correctly
- **Mitigation**: Add a new test specifically for empty status string to prevent future regressions
- **Compatibility**: The change strengthens existing behavior rather than changing the API

## Validation Plan

1. Run existing test suite to ensure no regressions: `python3 -m pytest app/tests/test_pet_catalog.py -v`
2. Add new test case `test_search_pets_empty_status_defaults_to_available`
3. Manual verification: Test `search_pets(status="")` returns only available pets
4. Verify explicit pending search still works: `search_pets(status="pending")` returns Nova
