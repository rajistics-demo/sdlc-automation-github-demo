# Catalog Spec Delta

## ADDED Requirements

### Requirement: Empty status parameter must not bypass availability filtering

When a pet search is performed with an empty status string, the search must apply the default availability filter rather than returning all pets regardless of status.

#### Scenario: Empty status string defaults to available-only filter

- Given the pet catalog contains available and pending pets
- When a search is performed with `status=''` (empty string)
- Then only pets with `status="available"` are returned
- And pending pets are excluded from results

#### Scenario: Whitespace-only status string defaults to available-only filter

- Given the pet catalog contains available and pending pets
- When a search is performed with `status='   '` (whitespace only)
- Then only pets with `status="available"` are returned
- And pending pets are excluded from results

### Requirement: Explicit status values continue to work correctly

The fix must not break existing behavior for explicit status parameter values.

#### Scenario: Explicit available status returns only available pets

- Given the pet catalog contains available and pending pets
- When a search is performed with `status='available'`
- Then only pets with `status="available"` are returned

#### Scenario: Explicit pending status returns only pending pets

- Given the pet catalog contains available and pending pets
- When a search is performed with `status='pending'`
- Then only pets with `status="pending"` are returned

#### Scenario: Species search with default status excludes pending pets

- Given Nova (pet-103) is a dog with pending status
- And Scout (pet-101) is a dog with available status
- When a search is performed with `species='dog'` and default status
- Then only Scout is returned
- And Nova is excluded
