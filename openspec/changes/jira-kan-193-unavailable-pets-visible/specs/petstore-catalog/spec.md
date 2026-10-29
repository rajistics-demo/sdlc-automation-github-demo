# Catalog Status Filter Spec Delta

## MODIFIED Requirements

### Requirement: Status filter must not allow empty strings to bypass the filter

The `search_pets()` function must treat empty or whitespace-only status values as defaulting to "available" behavior. Empty strings must not bypass the status filter entirely.

#### Scenario: Empty status string defaults to available-only

- Given the Petstore catalog contains Nova (pet-103) with status="pending"
- And the catalog contains other pets with status="available"
- When `search_pets(status="")` is called with an empty status string
- Then the results must include only pets with status="available"
- And Nova must not appear in the results
- And the behavior must match the default `search_pets()` behavior

#### Scenario: Whitespace-only status defaults to available-only

- Given the Petstore catalog contains pets with various statuses
- When `search_pets(status="  ")` is called with whitespace-only status
- Then the results must include only pets with status="available"
- And the behavior must match the default behavior

#### Scenario: Default search continues to work correctly

- Given the Petstore catalog contains Nova (pet-103) with status="pending"
- And the catalog contains other pets with status="available"
- When `search_pets()` is called without status parameter
- Then the results must include only pets with status="available"
- And Nova must not appear in the results

#### Scenario: Explicit status values continue to work

- Given the Petstore catalog contains Nova (pet-103) with status="pending"
- When `search_pets(status="pending")` is called
- Then the results must include Nova and other pending pets
- And available pets must be excluded

## Implementation Changes

### Backend Changes (`app/petstore_app/catalog.py`)

**Line 41** - Changed from:
```python
normalized_status = status.strip().lower()
```

To:
```python
normalized_status = status.strip().lower() if status.strip() else "available"
```

**Line 50** - Changed from:
```python
if normalized_status and normalized_status != pet.status:
```

To:
```python
if normalized_status != pet.status:
```

### Test Coverage (`app/tests/test_pet_catalog.py`)

Added two new regression tests:

1. `test_search_pets_default_returns_only_available()` - Verifies default behavior returns only available pets
2. `test_search_pets_empty_status_should_use_default()` - Verifies empty status string doesn't bypass the filter

## Acceptance Criteria

- [x] Empty status string returns only available pets
- [x] Whitespace-only status string returns only available pets
- [x] Default search (no status parameter) continues to work correctly
- [x] Explicit status="pending" searches continue to work
- [x] All existing tests continue to pass (backward compatibility)
- [x] New regression tests prevent the bug from reoccurring

## Test Results

Before fix:
- `test_search_pets_empty_status_should_use_default` **FAILED** - returned 4 pets including Nova

After fix:
- All 7 catalog tests **PASS** ✓
- All 4 adoption tests **PASS** ✓
- Backward compatibility maintained ✓

## Notes

This fix addresses the root cause where the truthy check on `normalized_status` allowed empty strings to bypass the status filter entirely. The minimal change ensures empty values default to the expected "available" behavior while preserving all existing functionality.
