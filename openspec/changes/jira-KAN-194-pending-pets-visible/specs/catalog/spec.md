# Catalog Status Filtering Spec Delta

## ADDED Requirements

### Requirement: Default search must exclude pending pets

Default pet catalog searches without explicit status filtering must return only pets with status="available", excluding all pending pets from customer-facing results.

#### Scenario: Customer searches without specifying status

- Given the catalog contains both available and pending pets
- When a customer calls search_pets() with no status parameter
- Then only pets with status="available" are returned
- And pets with status="pending" (like pet-103/Nova) are excluded

#### Scenario: Empty status is treated as default available

- Given a caller passes an empty status string
- When search_pets(status="") is called
- Then the behavior is identical to search_pets(status="available")
- And pending pets are excluded from results

### Requirement: Explicit pending searches must still work

Support and operations staff must be able to explicitly request pending pets for case investigation and workflow management.

#### Scenario: Support staff searches for pending pets

- Given support needs to investigate a pending adoption case
- When search_pets(status="pending") is called explicitly
- Then only pets with status="pending" are returned
- And available pets are excluded from results

### Requirement: Combined filters respect status filtering

When multiple filters are applied together, status filtering must work correctly with other filter criteria.

#### Scenario: Species filter with default status

- Given the catalog contains dogs with both available and pending status
- When search_pets(species="dog") is called with default status
- Then only available dogs are returned (pet-101/Scout)
- And pending dogs are excluded (pet-103/Nova not in results)

## MODIFIED Requirements

None - this is a bug fix restoring the documented behavior, not a behavior change.

## REMOVED Requirements

None
