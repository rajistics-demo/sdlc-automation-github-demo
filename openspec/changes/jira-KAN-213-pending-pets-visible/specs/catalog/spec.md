# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default pet search returns only available pets

#### Scenario: Customer searches for all pets without specifying status

- Given the pet catalog contains pets with various statuses (available, pending)
- When a customer searches without explicitly setting a status parameter
- Then only pets with `status="available"` are returned

#### Scenario: Customer searches by species without specifying status

- Given the pet catalog contains dogs with different statuses
- When a customer searches for `species="dog"` without setting status
- Then only available dogs are returned (Scout, not Nova)

#### Scenario: Empty status string does not bypass availability filter

- Given the search function receives an empty string for status
- When the status filter is applied
- Then the search defaults to available pets and excludes pending pets

### Requirement: Support can explicitly search for pending pets

#### Scenario: Support staff searches for pending pets

- Given Nova is a pending pet (pet-103)
- When support searches with `status="pending"`
- Then Nova appears in the results

#### Scenario: Mixed status searches work correctly

- Given pets exist with available and pending status
- When different status values are explicitly provided
- Then results match the requested status exactly
