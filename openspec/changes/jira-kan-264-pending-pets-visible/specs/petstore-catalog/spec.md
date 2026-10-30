# Petstore Catalog Spec Delta

## ADDED Requirements

### Requirement: Default catalog search returns only available pets

The default catalog search must filter to `status="available"` and exclude pending, adopted, or any other non-available pets.

#### Scenario: Default search excludes pending pets

- Given the catalog contains Nova (pet-103) with status="pending"
- When a customer performs a default search with no explicit status parameter
- Then Nova must not appear in the results

#### Scenario: Empty status search excludes pending pets

- Given the catalog contains Nova (pet-103) with status="pending"
- When a search is performed with an explicit empty status string
- Then Nova must not appear in the results

#### Scenario: Species filter with default status excludes pending pets

- Given the catalog contains Scout (pet-101, dog, available) and Nova (pet-103, dog, pending)
- When a customer searches for dogs with default status
- Then only Scout appears, not Nova

#### Scenario: Explicit pending status search includes pending pets

- Given the catalog contains Nova (pet-103) with status="pending"
- When support explicitly searches for status="pending"
- Then Nova appears in the results

### Requirement: Status filter must not be bypassed by empty strings

The status filter logic must properly handle empty status strings and enforce the default "available" filter in all cases where a valid explicit status is not provided.

#### Scenario: Empty or whitespace-only status defaults to available

- Given a search with status="" or status="   "
- When the search is executed
- Then only pets with status="available" are returned
