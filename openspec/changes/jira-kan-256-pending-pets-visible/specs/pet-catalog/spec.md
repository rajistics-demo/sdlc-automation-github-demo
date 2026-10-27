# Pet Catalog Spec Delta

## ADDED Requirements

### Requirement: Default search excludes pending pets

The `search_pets()` function must return only available pets when called with the default status parameter.

#### Scenario: Search with default status parameter

- Given a catalog containing both available and pending pets
- When `search_pets()` is called with `status="available"` (the default)
- Then only pets with `status="available"` are returned
- And pending pets are excluded from results

#### Scenario: Search with empty string status parameter

- Given a catalog containing both available and pending pets
- When `search_pets()` is called with `status=""`
- Then only pets with `status="available"` are returned (treating empty as default)
- And pending pets are excluded from results

### Requirement: Explicit pending pet searches still work

Support and operations must be able to explicitly query pending pets.

#### Scenario: Explicit pending status search

- Given a catalog containing both available and pending pets
- When `search_pets()` is called with `status="pending"`
- Then only pets with `status="pending"` are returned
- And available pets are excluded from results

### Requirement: Species filter with default status excludes pending pets

Species-filtered searches must respect the default status filter.

#### Scenario: Search by species with default status

- Given pet-101 (Scout, dog, available) and pet-103 (Nova, dog, pending)
- When `search_pets(species="dog")` is called with default status
- Then only Scout is returned
- And Nova (pending) is excluded
