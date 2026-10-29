# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Catalog search must reject empty status values

Empty or whitespace-only status parameters must be rejected to prevent bypassing availability filters.

#### Scenario: Empty status string is rejected

- Given the pet catalog contains pets with various statuses
- When a caller invokes `search_pets(status="")`
- Then a `ValueError` is raised indicating status cannot be empty

#### Scenario: Whitespace-only status string is rejected

- Given the pet catalog contains pets with various statuses
- When a caller invokes `search_pets(status="   ")`
- Then a `ValueError` is raised indicating status cannot be empty

### Requirement: Default catalog search returns only available pets

The default catalog search behavior must exclude pending pets without requiring explicit status filtering.

#### Scenario: Default search excludes pending pets

- Given the catalog contains Nova (pet-103) with status "pending"
- And the catalog contains Scout (pet-101) with status "available"
- When a caller invokes `search_pets(species="dog")` without specifying status
- Then the results include only Scout
- And Nova is not included in the results

#### Scenario: Explicit available status search excludes pending pets

- Given the catalog contains pets with "available" and "pending" statuses
- When a caller invokes `search_pets(status="available")`
- Then only pets with "available" status are returned
- And no pending pets are included

## PRESERVED Requirements

### Requirement: Explicit pending status search returns pending pets

Support and operations workflows must be able to explicitly search for pending pets.

#### Scenario: Pending status search returns only pending pets

- Given the catalog contains Nova (pet-103) with status "pending"
- When a caller invokes `search_pets(status="pending")`
- Then Nova is included in the results
- And available pets are not included

### Requirement: Species and tag filters work with status filtering

Existing query, species, and tag filters must continue to work correctly with status filtering.

#### Scenario: Species filter combined with default status

- Given the catalog contains dogs with "available" and "pending" statuses
- When a caller invokes `search_pets(species="dog")`
- Then only available dogs are returned
