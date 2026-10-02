# Design

## Context

The Petstore catalog provides a `search_pets()` function in `app/petstore_app/catalog.py` that filters pets by various criteria including status. The function has a default parameter `status="available"` to ensure customers only see adoptable pets by default.

The current implementation has a bug on line 50:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

The truthy check (`if normalized_status and ...`) allows an empty string to bypass the status filter entirely. When `status=""` is passed (after stripping), the condition evaluates to `False` and the filter is skipped, allowing all pets including those with `status="pending"` to appear in results.

## Decision

**Fix the truthy check on line 50** to ensure the status filter always applies when a status parameter is provided.

The cleanest fix is to change:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

To:
```python
if normalized_status != pet.status:
    continue
```

This ensures the status filter applies whenever `normalized_status` has any value (including empty string), preventing bypass.

**Alternative considered:** We could add validation to reject empty status strings earlier, but the simpler fix is to ensure the filter always applies, treating empty string as a non-matching status value.

## Rationale

- Minimal change: One-line fix removes the truthy check.
- Consistent with intent: The default parameter is `status="available"`, not `None`, indicating status filtering should always occur.
- Matches other optional filters: Parameters like `species` and `tag` are `None` by default, making truthy checks appropriate there, but `status` has a string default.
- Safe: Empty string won't match any pet's actual status, so no pets are returned (correct behavior).

## Risks

- **Risk**: Changing filter logic could affect existing callers.
  - **Mitigation**: All existing tests pass because they rely on default `status="available"` or explicit valid status values. No existing code passes empty strings.

- **Risk**: Empty string now returns no results instead of all results.
  - **Mitigation**: This is the correct behavior. Empty string is not a valid pet status in our data model.

## Validation Plan

1. Run existing test suite: `python3 -m pytest app/tests/test_pet_catalog.py -v`
2. Add new test: `test_search_pets_excludes_pending_by_default()`
3. Add new test: `test_search_pets_default_species_filter_excludes_pending()`
4. Verify log evidence scenario no longer occurs
