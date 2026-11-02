# Catalog Spec Delta

## ADDED Requirements

### Requirement: Default catalog search excludes pending pets

#### Scenario: Default search with no status parameter

- Given the catalog contains pets with various statuses including pending
- When a search is performed with default parameters
- Then only pets with status="available" are returned
- And pending pets (like Nova/pet-103) are not included in results

#### Scenario: Empty string status parameter is treated as default

- Given the catalog contains pets with various statuses
- When a search is performed with status=""
- Then only pets with status="available" are returned
- And pending pets are not included in results

#### Scenario: Whitespace-only status parameter is treated as default

- Given the catalog contains pets with various statuses
- When a search is performed with status="  "
- Then only pets with status="available" are returned
- And pending pets are not included in results

### Requirement: Explicit pending status searches still work

#### Scenario: Operations search for pending pets

- Given the catalog contains pending pets
- When a search is performed with status="pending" explicitly
- Then only pets with status="pending" are returned
- And available pets are not included in results

### Requirement: Species filtering preserves status filtering

#### Scenario: Species search excludes pending pets by default

- Given the catalog contains available and pending dogs
- When a search is performed with species="dog" and default status
- Then only available dogs are returned
- And pending dogs (like Nova/pet-103) are not included
