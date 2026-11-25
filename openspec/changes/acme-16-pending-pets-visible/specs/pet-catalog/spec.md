# Pet Catalog Spec Delta

## ADDED Requirements

### Requirement: Status filter must not be bypassed by empty strings

The pet catalog search function must apply the status filter even when an empty string is provided, ensuring that pending pets are never visible unless explicitly requested.

#### Scenario: Empty status string returns no results

- Given the pet catalog contains available and pending pets
- When a caller searches with `status=""`
- Then the status filter is applied
- And no pets are returned (since no pet has an empty status)
- And pending pets are NOT visible in results

#### Scenario: Default search returns available pets only

- Given the pet catalog contains available and pending pets
- When a caller searches without specifying a status parameter
- Then only pets with `status="available"` are returned
- And pending pets are excluded from results

#### Scenario: Explicit pending search works correctly

- Given the pet catalog contains available and pending pets
- When a caller searches with `status="pending"`
- Then only pets with `status="pending"` are returned
- And available pets are excluded from results

## Implementation Delta

**File:** `app/petstore_app/catalog.py`

**Line 50 - Before:**
```python
if normalized_status and normalized_status != pet.status:
    continue
```

**Line 50 - After:**
```python
if normalized_status is not None and normalized_status != pet.status:
    continue
```

**Rationale:** Explicit None check ensures empty strings are treated as filter values, not bypassed.

## Test Coverage

### New Test
```python
def test_search_pets_empty_status_does_not_bypass_filter() -> None:
    """Regression test: empty status should not bypass the filter."""
    results = search_pets(status="")
    assert len(results) == 0  # No pet has status=""
```

### Existing Tests (Must Continue to Pass)
- `test_search_pets_filters_by_species_and_status()` - Default behavior
- `test_search_pets_can_find_pending_pets_when_requested()` - Explicit pending
- `test_search_pets_filters_by_tag()` - Other filters
- `test_search_pets_validates_max_results()` - Validation
