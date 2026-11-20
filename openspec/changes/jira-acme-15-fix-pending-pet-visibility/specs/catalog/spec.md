# Catalog Spec Delta

## MODIFIED Requirements

### Requirement: Default catalog search returns only available pets

#### Scenario: Search with default status parameter

- Given the catalog contains pets with various statuses
- When a user searches without specifying a status
- Then only pets with status "available" are returned

#### Scenario: Search with empty status parameter

- Given the catalog contains pets with various statuses
- When a user searches with an empty string or whitespace-only status parameter
- Then only pets with status "available" are returned
- And pending pets are excluded from results

#### Scenario: Search with explicit "pending" status

- Given the catalog contains pets with status "pending"
- When a user searches with status="pending"
- Then only pets with status "pending" are returned
- And available pets are excluded from results

## UNCHANGED Requirements

### Requirement: Explicit status searches return matching pets

- The ability to search for pets with explicit status values (e.g., "pending", "available", "adopted") remains unchanged
- Status filtering by species, tag, and query remains unchanged
