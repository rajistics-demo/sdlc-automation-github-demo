# Design

## Context

The Petstore catalog provides a `search_pets()` function that filters pets by multiple criteria including status. The function has a default parameter `status="available"` to ensure the default customer experience shows only available pets.

The bug occurs at line 50 in `catalog.py`:
```python
if normalized_status and normalized_status != pet.status:
    continue
```

When `normalized_status` is an empty string, it evaluates to `False` in the boolean context, causing the entire status filter to be skipped. This allows pending pets to leak into results.

## Decision

- Change the condition from `if normalized_status` to `if normalized_status is not None and normalized_status != pet.status`
- This ensures the filter is applied unless status is explicitly None (meaning no status filter wanted)
- Empty string will now be treated as a valid status filter value

Alternative considered: Normalize empty string to "available" in the parameter processing. Rejected because it's less explicit and might hide other bugs.

## Risks

- **Low risk**: The change is minimal and localized to the filter logic
- **Mitigation**: Comprehensive test coverage for default, explicit, and edge cases
- **Breaking change check**: Existing callers using default parameter are unaffected
- **Edge case check**: Empty string now filters correctly rather than being ignored

## Validation Plan

Run focused catalog tests:
```bash
python -m pytest app/tests/test_pet_catalog.py -v
```

Specific validation:
1. Test default search excludes pending pets (new test)
2. Test explicit pending search works (existing test confirms)
3. Test empty string status doesn't bypass filter (new edge case test)
4. Verify existing species and tag filters still work (existing tests confirm)
