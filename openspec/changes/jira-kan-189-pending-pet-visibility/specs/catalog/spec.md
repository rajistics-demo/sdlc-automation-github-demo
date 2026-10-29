# Catalog Spec Delta

## MODIFIED Requirements

### Requirement: Default pet search must exclude pending pets

The catalog search must return only pets with `status="available"` by default, regardless of how the status parameter is specified.

#### Scenario: Search with default status parameter

- Given the catalog contains pets with various statuses including "pending"
- When a user calls `search_pets()` without specifying status
- Then only pets with `status="available"` are returned
- And pending pets are excluded from results

#### Scenario: Search with explicit available status

- Given the catalog contains pets with various statuses
- When a user calls `search_pets(status="available")`
- Then only pets with `status="available"` are returned
- And pending pets are excluded from results

#### Scenario: Search with empty status string (edge case)

- Given the catalog contains pets with various statuses
- When a user calls `search_pets(status="")`
- Then only pets with `status="available"` are returned (default behavior)
- And pending pets are excluded from results
- And the empty string does not bypass the status filter

#### Scenario: Search for pending pets explicitly

- Given the catalog contains pending pets
- When a user calls `search_pets(status="pending")`
- Then only pets with `status="pending"` are returned
- And available pets are excluded from results
- And this explicit request is allowed per product rules

### Requirement: Status filtering must be consistent

The status filter implementation must be consistent with other filter parameters and not allow bypass through edge case inputs.

#### Scenario: Filter consistency validation

- Given the implementation has filters for species, status, and tag
- When comparing the filter patterns across parameters
- Then status filtering should not have special truthiness checks that allow bypass
- And empty or None values should be handled consistently with design intent
