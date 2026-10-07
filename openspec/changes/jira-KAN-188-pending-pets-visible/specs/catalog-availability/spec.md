# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default catalog search excludes pending pets

#### Scenario: Empty string status parameter is treated as default available

- Given a pet catalog with both available and pending pets
- When `search_pets(status="")` is called with an empty string status
- Then only pets with `status="available"` are returned
- And pending pets are excluded from results

#### Scenario: Default search without status parameter excludes pending pets

- Given a pet catalog with both available and pending pets
- When `search_pets()` is called without a status parameter (uses default)
- Then only pets with `status="available"` are returned
- And pending pets are excluded from results

#### Scenario: Explicit pending status still returns pending pets

- Given a pet catalog with both available and pending pets
- When `search_pets(status="pending")` is called explicitly
- Then only pets with `status="pending"` are returned
- And available pets are excluded from results

#### Scenario: Species filter with empty string status excludes pending pets

- Given a pet catalog with available and pending dogs
- When `search_pets(species="dog", status="")` is called
- Then only available dogs are returned
- And pending dogs (like Nova/pet-103) are excluded

## UNCHANGED Requirements (Preserved)

### Requirement: Explicit status filters work correctly

- Passing `status="available"` returns only available pets
- Passing `status="pending"` returns only pending pets
- Species, tag, and query filters continue to work as expected
