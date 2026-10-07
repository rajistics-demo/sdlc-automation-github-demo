# Catalog Filtering Spec Delta

## ADDED Requirements

### Requirement: Empty status parameter must default to available-only filtering

#### Scenario: Search called with empty status string

- Given the pet catalog contains pets with status="available" and status="pending"
- When search_pets is called with status="" (empty string)
- Then only pets with status="available" are returned

#### Scenario: Search called without status parameter uses default

- Given the pet catalog contains pets with status="available" and status="pending"
- When search_pets is called with no status parameter
- Then only pets with status="available" are returned

#### Scenario: Explicit pending status search still works

- Given the pet catalog contains pets with status="available" and status="pending"
- When search_pets is called with status="pending"
- Then only pets with status="pending" are returned

## MODIFIED Requirements

### Requirement: Status filtering must handle falsy values correctly

The existing status filter condition must treat empty strings as equivalent to the default "available" status, not as a bypass of the filter.
