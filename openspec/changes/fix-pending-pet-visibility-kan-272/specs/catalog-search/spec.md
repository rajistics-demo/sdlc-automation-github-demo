# Catalog Search Spec Delta

## ADDED Requirements

### Requirement: Default search must exclude pending pets

#### Scenario: Default search without parameters

- Given a catalog with available pets (Mochi, Scout, Pip) and pending pets (Nova)
- When a user calls `search_pets()` with no parameters
- Then only available pets are returned
- And pending pet Nova is not in results

#### Scenario: Empty status string does not bypass filter

- Given a catalog with available and pending pets
- When a user calls `search_pets(status="")`
- Then only available pets are returned
- And pending pets are excluded despite empty status parameter

#### Scenario: Explicit pending status shows pending pets

- Given a catalog with pending pet Nova
- When a user calls `search_pets(status="pending")`
- Then pending pets are included in results
- And this behavior remains unchanged

### Requirement: Species filter works with status filter

#### Scenario: Species search excludes pending pets

- Given catalog with available dog Scout and pending dog Nova
- When a user calls `search_pets(species="dog")`
- Then only available dog Scout is returned
- And pending dog Nova is excluded

## UNCHANGED Requirements

The following existing requirements remain unchanged:

- Tag filtering works correctly
- Max results validation (1-50 range)
- Name query filtering
- Species filtering
- Multiple filter combination
