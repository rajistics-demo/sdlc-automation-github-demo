# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default catalog search returns only available pets

#### Scenario: Default search with empty status

- Given the Petstore catalog contains pets with various statuses including "available" and "pending"
- When a customer searches without explicitly specifying a status, or passes an empty status string
- Then only pets with `status="available"` are returned
- And pets with `status="pending"` are excluded from results

#### Scenario: Explicit pending search continues to work

- Given the Petstore catalog contains pets with `status="pending"`
- When a support or operations user explicitly searches with `status="pending"`
- Then pets with `status="pending"` are returned
- And this behavior is unchanged from current functionality

#### Scenario: Species filter with default status

- Given the Petstore catalog contains both available and pending dogs
- When a customer searches for species="dog" without specifying status
- Then only available dogs are returned
- And pending dogs like Nova (pet-103) are excluded

## FIXED Defects

### Defect: Empty status string bypasses availability filter

- Current behavior: When `status=""` is passed, the filter on line 50-51 of `catalog.py` evaluates as falsy and doesn't apply, allowing all pets regardless of status to be returned.
- Expected behavior: Empty status should be treated as the default "available" status.
- Root cause: The condition `if normalized_status and normalized_status != pet.status` skips filtering when `normalized_status` is an empty string.
- Fix: Normalize empty or whitespace-only status values to the default "available".
