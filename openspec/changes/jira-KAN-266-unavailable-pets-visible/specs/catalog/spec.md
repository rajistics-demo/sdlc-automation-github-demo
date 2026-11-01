# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default pet catalog must exclude pending pets

Customer-facing catalog searches must return only pets with `status="available"` by default.

#### Scenario: Default search with no parameters

- Given the Petstore has pets with various statuses including "available" and "pending"
- When a customer performs a default search with no status filter
- Then only pets with `status="available"` are returned
- And Nova (pet-103) with `status="pending"` is NOT included

#### Scenario: Search by species without explicit status

- Given Nova (pet-103) is a dog with `status="pending"`
- And Scout (pet-101) is a dog with `status="available"`
- When a customer searches for species="dog" without specifying status
- Then only Scout is returned
- And Nova is NOT included

#### Scenario: Empty query search

- Given the catalog contains both available and pending pets
- When a customer performs a search with an empty query string
- Then only pets with `status="available"` are returned
- And no pending pets appear in the results

## UNCHANGED Requirements

### Requirement: Explicit pending-pet searches must continue to work

Support and operations staff need access to pending pets for workflow purposes.

#### Scenario: Explicit pending status search

- Given Nova (pet-103) has `status="pending"`
- When a support user explicitly searches with `status="pending"`
- Then Nova is included in the results
- And the search behavior matches documented support workflows

## UNCHANGED Requirements  

### Requirement: Adoption order validation must reject non-available pets

Backend validation must prevent adoption attempts on pending pets.

#### Scenario: Attempt to adopt pending pet

- Given Nova (pet-103) has `status="pending"`
- When a customer attempts to create an adoption order for Nova
- Then the system raises a ValueError
- And the error message states "pet is not available for adoption"
