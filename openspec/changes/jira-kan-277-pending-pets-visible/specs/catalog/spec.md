# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default pet search excludes pending pets

#### Scenario: Default search without status parameter

- Given the catalog contains available pets (Mochi, Scout, Pip) and pending pet Nova
- When a user calls `search_pets()` with no status parameter
- Then the results include only available pets
- And the results exclude Nova (pet-103)

#### Scenario: Species filter with default status

- Given the catalog contains available dog Scout and pending dog Nova
- When a user calls `search_pets(species="dog")` without specifying status
- Then the results include only Scout (pet-101)
- And the results exclude Nova (pet-103)

#### Scenario: Name search for pending pet with default status

- Given Nova (pet-103) has status="pending"
- When a user calls `search_pets(query="nova")` without specifying status
- Then the results are empty
- And Nova is not returned

### Requirement: Explicit pending status request still works

#### Scenario: Pending pets visible when explicitly requested

- Given Nova (pet-103) has status="pending"
- When a user calls `search_pets(status="pending")`
- Then the results include Nova
- And available pets are excluded

This requirement already has test coverage in `test_search_pets_can_find_pending_pets_when_requested()` and does not change.
