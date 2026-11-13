# Catalog Search Spec Delta

## ADDED Requirements

### Requirement: Default catalog search excludes pending pets

#### Scenario: Default status parameter

- Given a catalog with 3 available pets and 1 pending pet (Nova)
- When a search is performed with the default `status="available"` parameter
- Then only the 3 available pets are returned
- And Nova (pending pet) is not included in results

#### Scenario: Empty status string

- Given a catalog with 3 available pets and 1 pending pet (Nova)
- When a search is performed with `status=""` (empty string)
- Then only the 3 available pets are returned
- And Nova (pending pet) is not included in results

#### Scenario: Whitespace-only status string

- Given a catalog with 3 available pets and 1 pending pet (Nova)
- When a search is performed with `status="  "` (whitespace only)
- Then only the 3 available pets are returned
- And Nova (pending pet) is not included in results

### Requirement: Explicit pending status search continues to work

#### Scenario: Operations searches for pending pets

- Given a catalog with 3 available pets and 1 pending pet (Nova)
- When a search is performed with `status="pending"`
- Then only the 1 pending pet (Nova) is returned
- And no available pets are included in results

### Requirement: Species filter works with status filter

#### Scenario: Species search excludes pending pets

- Given a catalog with 2 available dogs (Scout) and 1 pending dog (Nova)
- When a search is performed with `species="dog"` and default status
- Then only Scout is returned
- And Nova (pending) is not included in results
