# Petstore Catalog Spec Delta

## ADDED Requirements

### Requirement: Status parameter validation

Catalog search MUST reject empty status values to prevent bypassing the availability filter.

#### Scenario: Empty status raises ValueError

- Given catalog search is called with `status=""`
- When the search executes
- Then a ValueError is raised
- And the error message indicates status must not be empty

#### Scenario: Whitespace-only status raises ValueError

- Given catalog search is called with `status="  "`
- When the search executes
- Then a ValueError is raised
- And the error message indicates status must not be empty

### Requirement: Default catalog search excludes pending pets

Catalog search MUST exclude pending pets from the default available-pets experience.

#### Scenario: Default search excludes pending pets

- Given Nova (pet-103) has status `pending`
- When catalog search is called with default parameters
- Then Nova is not included in the results
- And only available pets are returned

#### Scenario: Available dog search excludes pending dogs

- Given Scout is available and Nova is pending
- When catalog search is called with `species="dog"` and default status
- Then Scout is included and Nova is excluded

### Requirement: Explicit pending search still works

Support and operations workflows MUST be able to search for pending pets explicitly.

#### Scenario: Explicit pending-pet search works

- Given Nova (pet-103) has status `pending`
- When catalog search is called with `status="pending"`
- Then Nova is included in the results
- And available pets are excluded
