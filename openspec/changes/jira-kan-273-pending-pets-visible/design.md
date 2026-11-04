# Design

## Context

The Petstore catalog search function in `app/petstore_app/catalog.py` filters pets by name, species, status, and tag. The `status` parameter defaults to `"available"`, but when an empty string is passed, the filter logic on line 50 fails to exclude non-available pets:

```python
if normalized_status and normalized_status != pet.status:
    continue
```

When `normalized_status` is an empty string, the condition `normalized_status and ...` evaluates to `False`, causing the filter to be skipped entirely. This allows pending pets to appear in results meant only for available pets.

The repository's product rules (from `docs/wiki/petstore-catalog-availability.md` and `docs/repo-memory/petstore-intelligence.md`) explicitly state that default searches must show only available pets.

## Decision

Change the status filter condition to:
```python
if normalized_status != pet.status:
    continue
```

This ensures the filter is always applied when `status` is provided, including when it's an empty string. The default parameter value `status="available"` already provides the correct behavior for callers who don't specify status.

### Why This Works

1. Default calls `search_pets()` use `status="available"` and correctly filter
2. Explicit `status="available"` continues to work
3. Empty string `status=""` now filters correctly (no pets match empty status)
4. Explicit `status="pending"` continues to work for operations
5. Minimal change to a single line reduces risk

## Risks and Mitigation

- **Risk**: Empty status string might be used intentionally to bypass filtering
- **Mitigation**: Product rules and tests establish that empty status should not bypass filters; if a "show all statuses" behavior is needed, it should be explicit, not via empty string

- **Risk**: Breaking existing callers who pass empty string expecting all results
- **Mitigation**: Repository tests show no such usage; the default parameter and explicit pending searches cover the legitimate use cases

## Validation Plan

1. Add regression test for empty status string - must exclude pending pets
2. Verify existing tests continue to pass
3. Run `python3 -m pytest -q app/tests/test_pet_catalog.py`
4. Validate OpenSpec artifacts with `python3 skills/sdlc-story/scripts/validate_open_spec.py openspec/changes/jira-kan-273-pending-pets-visible/`
