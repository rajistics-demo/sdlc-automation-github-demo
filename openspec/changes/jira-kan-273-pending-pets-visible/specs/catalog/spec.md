# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default catalog search excludes pending pets

#### Scenario: Default search returns only available pets

- Given the Petstore catalog contains Nova (pet-103) with `status="pending"`
- When a customer performs a default search with no status parameter
- Then Nova must not appear in the results
- And only pets with `status="available"` are returned

#### Scenario: Empty status parameter excludes pending pets

- Given the Petstore catalog contains Nova (pet-103) with `status="pending"`
- When a search is performed with an empty status string `status=""`
- Then Nova must not appear in the results
- And only pets with `status="available"` are returned

#### Scenario: Explicit available status excludes pending pets

- Given the Petstore catalog contains Nova (pet-103) with `status="pending"`
- When a search is performed with `status="available"`
- Then Nova must not appear in the results

### Requirement: Operations can still query pending pets explicitly

#### Scenario: Explicit pending status returns pending pets

- Given the Petstore catalog contains Nova (pet-103) with `status="pending"`
- When an operations user performs a search with `status="pending"`
- Then Nova must appear in the results

### Requirement: Species filter respects availability

#### Scenario: Species search with default status excludes pending pets

- Given the Petstore catalog contains Scout (available dog) and Nova (pending dog)
- When a customer searches for dogs with default status
- Then Scout appears in the results
- And Nova does not appear in the results
