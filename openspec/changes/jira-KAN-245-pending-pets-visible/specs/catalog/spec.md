# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default search must exclude pending pets

#### Scenario: Default search with no status parameter
- Given a catalog with pets in "available" and "pending" status
- When search_pets() is called with default parameters
- Then only pets with status="available" are returned
- And pending pets (like Nova/pet-103) are not included

#### Scenario: Species filter with default status
- Given a catalog with available and pending pets
- When search_pets(species="dog") is called
- Then only available dogs are returned
- And pending dogs (like Nova) are excluded

### Requirement: Empty status cannot bypass filtering

#### Scenario: Search with empty status string
- Given a catalog with pets in various statuses
- When search_pets(status="") is called
- Then no pets are returned
- And the status filter is not bypassed

### Requirement: Explicit pending search must work for operations

#### Scenario: Support searches for pending pets
- Given a catalog with pending pets
- When search_pets(status="pending") is called
- Then only pending pets are returned
- And available pets are excluded

## Test Coverage

```python
def test_search_pets_filters_by_species_and_status() -> None:
    """Existing test - verifies default status excludes pending"""
    results = search_pets(species="dog")
    assert [pet.id for pet in results] == ["pet-101"]  # Scout only, not Nova

def test_search_pets_can_find_pending_pets_when_requested() -> None:
    """Existing test - verifies explicit pending search works"""
    results = search_pets(species="dog", status="pending")
    assert [pet.name for pet in results] == ["Nova"]

def test_search_pets_with_empty_status_returns_no_results() -> None:
    """New regression test - verifies empty status doesn't bypass filter"""
    results = search_pets(status="")
    assert len(results) == 0
```
