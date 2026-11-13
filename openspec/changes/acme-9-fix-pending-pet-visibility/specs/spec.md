# Pet Catalog Status Filter Spec Delta

## ADDED Requirements

### Requirement: Empty status defaults to available pets only

#### Scenario: User searches with empty status string

- Given the pet catalog contains both available and pending pets
- When a user calls `search_pets(status="")`
- Then only pets with status "available" are returned
- And pets with status "pending" are excluded

#### Scenario: User searches with whitespace-only status string

- Given the pet catalog contains both available and pending pets
- When a user calls `search_pets(status="  ")`
- Then only pets with status "available" are returned
- And pets with status "pending" are excluded

## UNCHANGED Requirements

### Requirement: Explicit status values are respected

#### Scenario: User searches for pending pets

- Given the pet catalog contains pending pets
- When a user calls `search_pets(status="pending")`
- Then only pets with status "pending" are returned

#### Scenario: User searches with default parameter

- Given the pet catalog contains both available and pending pets
- When a user calls `search_pets()` without status parameter
- Then only pets with status "available" are returned (default behavior)
