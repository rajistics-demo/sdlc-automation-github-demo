# Design

## Context

The `search_pets` function in `app/petstore_app/catalog.py` provides filtering by status with a default of `status="available"`. Log evidence (`docs/logs/pending-pet-visible.ndjson`) confirms `PENDING_PET_VISIBLE` error with pet-103 (Nova, status="pending") appearing in the available-pets catalog. The bug occurs when an empty status string bypasses the filter:

```python
normalized_status = status.strip().lower()  # Results in ""
if normalized_status and normalized_status != pet.status:  # Empty string is falsy!
    continue
```

## Decision

Replace the truthy check with an explicit empty-string check. If status is provided as an empty string after normalization, treat it as the default "available" status:

```python
# If status is empty, default to "available"
if not normalized_status:
    normalized_status = "available"

# Now always filter by status
if normalized_status != pet.status:
    continue
```

This approach:
- Explicitly converts empty strings to "available"
- Ensures the status filter always runs (no conditional bypass)
- Preserves backward compatibility with existing calls
- Maintains support workflows using `status="pending"`

## Risks

- **Risk:** Breaking change if any code relies on empty status returning all pets
- **Mitigation:** Review existing tests. The test suite shows explicit status requests only; no code appears to intentionally use empty status for all-pets queries

- **Risk:** UI or API layer may need updates if they pass empty strings
- **Mitigation:** The web UI (app.js) filters client-side; backend fix provides defense in depth

## Validation Plan

- Add regression test: `test_search_pets_with_empty_status_returns_only_available()`
- Run full test suite to verify no breaking changes
- Verify explicit `status="pending"` test still passes
