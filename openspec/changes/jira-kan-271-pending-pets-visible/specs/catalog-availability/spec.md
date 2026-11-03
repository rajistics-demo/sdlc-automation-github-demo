# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Empty status parameter must filter to available pets only

When the status parameter is an empty string, the catalog search must treat it as "available" and return only available pets.

#### Scenario: Empty status string filters correctly

- Given the pet catalog contains pets with various statuses including pending
- When a caller invokes `search_pets(status="")`
- Then the results must contain only pets with status="available"
- And pending pets like Nova (pet-103) must not appear in results

#### Scenario: Empty status with species filter

- Given the pet catalog contains both available and pending dogs
- When a caller invokes `search_pets(species="dog", status="")`
- Then the results must contain only available dogs
- And Nova (pet-103, pending dog) must not appear in results

### Requirement: Default status behavior must remain unchanged

The existing default behavior when status is not specified must continue to work.

#### Scenario: No status parameter provided

- Given the pet catalog contains pets with various statuses
- When a caller invokes `search_pets()` without a status parameter
- Then the results must contain only pets with status="available"
- And pending pets must not appear in results

### Requirement: Explicit pending status requests must continue to work

Support and operations workflows that explicitly request pending pets must continue to function.

#### Scenario: Explicit pending status request

- Given the pet catalog contains pending pets like Nova
- When a caller invokes `search_pets(status="pending")`
- Then the results must contain only pets with status="pending"
- And Nova (pet-103) must appear in results
