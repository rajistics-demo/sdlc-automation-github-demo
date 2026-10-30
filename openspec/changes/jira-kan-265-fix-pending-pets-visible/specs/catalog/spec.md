# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default catalog search must exclude pending pets

#### Scenario: Search with default status parameter

- Given a catalog with available pets (Mochi, Scout, Pip) and a pending pet (Nova)
- When a user calls `search_pets()` without specifying a status parameter
- Then only available pets (Mochi, Scout, Pip) are returned
- And the pending pet (Nova) is not included in the results

#### Scenario: Search with explicit available status

- Given a catalog with available pets and a pending pet (Nova)
- When a user calls `search_pets(status="available")`
- Then only available pets are returned
- And the pending pet (Nova) is not included in the results

#### Scenario: Search with empty string status parameter

- Given a catalog with available pets and a pending pet (Nova)
- When a user calls `search_pets(status="")`
- Then only available pets are returned
- And the pending pet (Nova) is not included in the results

### Requirement: Explicit pending status searches must continue to work

#### Scenario: Support staff searches for pending pets

- Given a catalog with available pets and a pending pet (Nova)
- When a support user calls `search_pets(status="pending")`
- Then only pending pets (Nova) are returned
- And available pets are not included in the results

### Requirement: Status filter must not be bypassed by falsy values

#### Scenario: Empty string status does not bypass filter

- Given the status parameter defaults to "available"
- When the status parameter is set to an empty string
- Then the filter should still apply the "available" default
- And pending pets must not appear in results
