# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default Search Excludes Pending Pets

The `search_pets()` function MUST filter to `status="available"` by default and MUST NOT return pending pets in default searches.

#### Scenario: Customer Searches for Dogs

- Given the catalog contains Scout (pet-101, available dog) and Nova (pet-103, pending dog)
- When a customer searches with `search_pets(species="dog")`
- Then only Scout appears in results
- And Nova is excluded

#### Scenario: Default Search Without Parameters

- Given the catalog contains available and pending pets
- When a search is performed with `search_pets()`
- Then only available pets appear
- And all pending pets are excluded

### Requirement: Explicit Pending Requests Still Work

Operations workflows MUST be able to explicitly request pending pets.

#### Scenario: Operations Searches for Pending Dogs

- Given the catalog contains Scout (pet-101, available dog) and Nova (pet-103, pending dog)
- When operations searches with `search_pets(species="dog", status="pending")`
- Then only Nova appears in results
- And Scout is excluded

### Requirement: Status Filter Always Applied

The status filter MUST be applied regardless of the status value provided, including empty strings.

#### Scenario: Empty Status String Provided

- Given the catalog contains available and pending pets
- When a search is performed with `search_pets(status="")`
- Then the status filter is applied (not bypassed)
- And results match the empty status exactly (no pets match)
