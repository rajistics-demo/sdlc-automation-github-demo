# Catalog Spec Delta

## ADDED Requirements

### Requirement: Default search returns only available pets

#### Scenario: Customer browses available pets
- Given a customer uses the default pet search
- When no status parameter is provided
- Then only pets with `status="available"` are returned
- And Nova (pet-103, status="pending") is excluded

#### Scenario: Empty status defaults to available
- Given the search is called with an empty status parameter
- When `search_pets(status="")`
- Then only pets with `status="available"` are returned
- And pending pets are excluded

### Requirement: Explicit pending search works for support

#### Scenario: Support views pending pets
- Given support needs to view pending pets
- When `search_pets(status="pending")`
- Then only pets with `status="pending"` are returned
- And Nova (pet-103) is included

### Requirement: Combined filters work correctly

#### Scenario: Species filter with default status
- Given combined filters are used
- When `search_pets(species="dog")`
- Then only available dogs are returned
- And Scout (pet-101) is included
- And Nova (pet-103) is excluded
