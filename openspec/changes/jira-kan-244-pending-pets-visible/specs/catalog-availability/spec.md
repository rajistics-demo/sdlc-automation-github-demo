# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Empty status defaults to available-only filtering

When the search function receives an empty status string, it must return only pets with `status="available"`, equivalent to the default behavior.

#### Scenario: Customer searches for dogs with empty status

- Given the catalog contains pet-101 (Scout, dog, available) and pet-103 (Nova, dog, pending)
- When a user calls `search_pets(species="dog", status="")`
- Then only pet-101 (Scout) is returned
- And pet-103 (Nova) is NOT returned

#### Scenario: Support searches for pending dogs explicitly

- Given the catalog contains pet-101 (Scout, dog, available) and pet-103 (Nova, dog, pending)
- When support calls `search_pets(species="dog", status="pending")`
- Then only pet-103 (Nova) is returned
- And pet-101 (Scout) is NOT returned
