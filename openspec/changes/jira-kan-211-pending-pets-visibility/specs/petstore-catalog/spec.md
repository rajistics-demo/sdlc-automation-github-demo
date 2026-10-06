# Petstore Catalog Spec Delta

## ADDED Requirements

### Requirement: Default pet search must exclude pending pets

The default catalog search must return only pets with `status="available"`. Pending pets must not appear unless explicitly requested by passing `status="pending"`.

#### Scenario: Default search excludes pending pets

- Given the petstore catalog contains pets with various statuses including pending
- When a customer searches without specifying a status (using the default)
- Then only pets with `status="available"` are returned
- And pending pets like Nova (pet-103) are not included in the results

#### Scenario: Species filter with default status excludes pending pets

- Given Nova (pet-103) is a dog with `status="pending"`
- And Scout (pet-101) is a dog with `status="available"`
- When a customer searches for dogs without specifying a status
- Then only Scout is returned
- And Nova is not included in the results

#### Scenario: Explicit pending search still works

- Given Nova (pet-103) has `status="pending"`
- When an operations user explicitly searches with `status="pending"`
- Then Nova is included in the results
- And available pets are not included

## UPDATED Requirements

### Requirement: Status filter must always be applied

The status filter in `search_pets()` must always be enforced, even when edge cases like empty strings occur.

#### Scenario: Empty status string should not bypass filter

- Given the status filter logic in `search_pets()`
- When the status parameter is normalized to an empty string (edge case)
- Then the filter should still be applied with the default "available" behavior
- And pending pets must not appear in results
