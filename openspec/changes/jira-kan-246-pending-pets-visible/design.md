# Design

## Context

The Petstore catalog stores pet availability in the `status` field. The `search_pets` function in `catalog.py` has a default parameter `status="available"` and filters pets by status. However, the status filtering logic has a bug:

```python
normalized_status = status.strip().lower()
if normalized_status and normalized_status != pet.status:
    continue
```

When `status=""` is passed, `normalized_status` becomes `""`, the condition evaluates to `False`, and the status check is skipped entirely. This allows pending pets to appear in results.

## Decision

- Add validation that rejects empty status values after normalization
- Fail fast with a clear ValueError when status is empty or whitespace-only
- Preserve the default `status="available"` behavior unchanged
- Preserve explicit `status="pending"` searches for support workflows
- Add test coverage for the empty status case

## Risks

- **Risk**: A broad fix could hide pending pets from support workflows that explicitly request them  
  **Mitigation**: Only reject empty strings; explicit `status="pending"` calls unchanged

- **Risk**: Unknown callers might depend on empty status behavior  
  **Mitigation**: Empty status bypassing the filter is a bug, not a feature; existing tests show only explicit status values are used

## Validation Plan

- Add test: empty status raises ValueError with clear message
- Run existing catalog tests: default available-only, explicit pending, species, tag filtering
- Verify Nova (pet-103) excluded from default search
- Run full pytest suite before opening PR
