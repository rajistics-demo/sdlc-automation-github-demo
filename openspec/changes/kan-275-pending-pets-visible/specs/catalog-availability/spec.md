# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Status filter must be consistently applied

The catalog search status filter must be applied regardless of whether the status parameter is passed as the default value, explicitly provided, or an empty string.

#### Scenario: Default status filtering excludes pending pets

- Given a catalog with available and pending pets
- When a search is performed without explicitly passing a status parameter
- Then only pets with `status="available"` are returned

#### Scenario: Empty status string does not bypass filtering

- Given a catalog with available and pending pets
- When a search is performed with an empty status string
- Then the default `status="available"` filter is still applied
- And pending pets are not returned

#### Scenario: Explicit pending status works correctly

- Given a catalog with available and pending pets
- When a search is performed with `status="pending"`
- Then only pets with `status="pending"` are returned

## UPDATED Requirements

### Requirement: Status filter logic is not conditional

The status filter condition in `search_pets` must not check whether `normalized_status` is truthy before applying the filter, since status has a default value and should always be enforced.

#### Scenario: Species filter with default status

- Given a catalog with available dogs and pending dogs
- When searching for dogs without specifying status
- Then only available dogs are returned
- And pending dogs like Nova (pet-103) are excluded
