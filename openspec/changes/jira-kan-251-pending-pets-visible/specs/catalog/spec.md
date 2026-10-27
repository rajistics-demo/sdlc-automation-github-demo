# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default pet search excludes pending pets

The default pet catalog search must return only pets with status="available", ensuring customers cannot see or attempt to adopt pets that are not yet ready for adoption.

#### Scenario: Initial page load shows only available pets

- Given the Petstore catalog contains Mochi (available), Scout (available), Pip (available), and Nova (pending)
- When a customer loads the catalog page without applying any filters
- Then the catalog displays only Mochi, Scout, and Pip
- And Nova (pending pet) is not displayed

#### Scenario: Species filter maintains availability constraint

- Given the catalog contains Scout (dog, available) and Nova (dog, pending)
- When a customer filters by species="dog"
- Then the catalog displays only Scout
- And Nova is not displayed despite matching the species filter

#### Scenario: Name search for pending pet returns empty result

- Given Nova is a pending pet
- When a customer searches for "nova" by name
- Then the catalog displays an empty state message
- And Nova is not displayed

### Requirement: Pending pets cannot be adopted

The adoption order creation must validate pet availability status and reject attempts to adopt pending pets, even if a customer obtains the pet ID through other means.

#### Scenario: Adoption attempt on pending pet is rejected

- Given Nova (pet-103) has status="pending"
- When a customer attempts to create an adoption order for pet-103
- Then the system rejects the order with error "pet is not available for adoption"
- And no adoption order is created

## UNCHANGED Requirements

### Requirement: Explicit pending pet searches remain supported

Support and operations staff can still explicitly request pending pets by specifying status="pending" in their search parameters. This functionality is preserved for operational workflows.

#### Scenario: Operations searches for pending pets explicitly

- Given Nova has status="pending"
- When an operations staff member searches with status="pending"
- Then Nova is included in the search results
