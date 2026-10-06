# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default search returns only available pets

#### Scenario: Search with default parameters excludes pending pets

- Given a catalog containing pets with various statuses including "pending"
- When a search is performed with default parameters (no status specified)
- Then only pets with status="available" are returned
- And pets with status="pending" are excluded

#### Scenario: Search with empty status string defaults to available

- Given a catalog containing pets with various statuses
- When a search is performed with status="" (empty string)
- Then only pets with status="available" are returned
- And pets with status="pending" are excluded

#### Scenario: Search with explicit pending status returns pending pets

- Given a catalog containing pets with status="pending"
- When a search is performed with status="pending"
- Then only pets with status="pending" are returned
- And pets with status="available" are excluded

### Requirement: Status filter is always applied

#### Scenario: Status filter cannot be bypassed

- Given the search_pets function with a status parameter
- When the function is called with any status value including empty strings
- Then the status filter is always applied
- And no pets are returned that don't match the normalized status value
