# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Empty status string must default to available pets only

The `search_pets()` function must treat an empty string status parameter the same as the default `"available"` status, ensuring pending pets are excluded from search results.

#### Scenario: Search with empty status string excludes pending pets

- Given the catalog contains Nova (pet-103) with status="pending"
- And the catalog contains 3 pets with status="available"  
- When a search is performed with `status=""`
- Then the results must contain only the 3 available pets
- And Nova (pet-103) must not be in the results

#### Scenario: Default search without status parameter excludes pending pets

- Given the catalog contains Nova (pet-103) with status="pending"
- And the catalog contains 3 pets with status="available"
- When a search is performed without specifying status
- Then the results must contain only the 3 available pets
- And Nova (pet-103) must not be in the results

### Requirement: Explicit pending status search must still work

Operations and support staff need the ability to explicitly search for pending pets when investigating cases.

#### Scenario: Explicit pending status search returns only pending pets

- Given the catalog contains Nova (pet-103) with status="pending"
- And the catalog contains 3 pets with status="available"
- When a search is performed with `status="pending"`
- Then the results must contain only Nova (pet-103)
- And available pets must not be in the results

## EXISTING Requirements (unchanged)

### Requirement: Default status parameter is "available"

The function signature default of `status="available"` remains unchanged and continues to filter to available pets only.

### Requirement: Status filter is case-insensitive

The `normalized_status = status.strip().lower()` normalization continues to work as designed.
