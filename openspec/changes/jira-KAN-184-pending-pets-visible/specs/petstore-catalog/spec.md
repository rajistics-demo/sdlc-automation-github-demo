# Petstore Catalog Spec Delta

## ADDED Requirements

### Requirement: Default pet search excludes pending pets

The default catalog search must return only pets with `status="available"`. Pending pets must never appear in results unless explicitly requested.

#### Scenario: Default search excludes pending pets

- Given Nova (`pet-103`) exists with `status="pending"`
- And Scout (`pet-101`) exists with `status="available"`
- When a customer searches pets with default parameters
- Then Scout appears in results
- And Nova does not appear in results

#### Scenario: Species search with default status excludes pending pets

- Given Nova is a dog with `status="pending"`
- And Scout is a dog with `status="available"`
- When a customer searches for dogs without specifying status
- Then Scout appears in results
- And Nova does not appear in results

#### Scenario: Explicit pending search still works

- Given Nova (`pet-103`) exists with `status="pending"`
- When a system process searches with `status="pending"`
- Then Nova appears in results

## MODIFIED Behavior

### Requirement: Status filter is always applied

The status filter in `search_pets()` must apply even when status is an empty string or other edge-case value.

#### Scenario: Empty status string does not bypass filter

- Given the catalog has pets with various statuses
- When `search_pets(status="")` is called with an empty status string
- Then the status filter is not bypassed
- And only valid status matches are returned (or no results if "" is invalid)

## Acceptance Criteria

- ✅ Default `search_pets()` returns only available pets
- ✅ `search_pets(species="dog")` returns only available dogs, excluding Nova
- ✅ `search_pets(status="pending")` correctly returns pending pets when explicitly requested
- ✅ Status filter cannot be bypassed with empty strings or falsy values
- ✅ All existing tests continue to pass
- ✅ New regression tests verify pending pet exclusion
