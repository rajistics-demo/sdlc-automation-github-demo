# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default pet search must return only available pets

The customer-facing catalog search must exclude pets with status other than "available" when no explicit status is requested or when an empty status is provided.

#### Scenario: Default search excludes pending pets

- Given the catalog contains pets with various statuses including pending
- When a customer searches without specifying a status
- Then only pets with status="available" are returned
- And pets with status="pending" are excluded from results

#### Scenario: Empty status parameter defaults to available

- Given the catalog contains pets including Nova (pet-103) with status="pending"
- When search_pets() is called with an empty string for status
- Then only pets with status="available" are returned
- And Nova does not appear in the results

#### Scenario: Whitespace-only status parameter defaults to available

- Given the catalog contains pets with multiple status values
- When search_pets() is called with a whitespace-only status (e.g., "   ")
- Then only pets with status="available" are returned

## PRESERVED Requirements

### Requirement: Explicit pending searches must continue to work

Support and operations staff need to query pending pets for their workflows.

#### Scenario: Explicit pending search returns pending pets

- Given Nova (pet-103) has status="pending"
- When search_pets() is called with status="pending"
- Then Nova appears in the results
- And available pets are excluded from results
