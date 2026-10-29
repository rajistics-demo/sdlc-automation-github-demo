# Catalog Search Spec Delta

## ADDED Requirements

### Requirement: Default search must exclude pending pets

#### Scenario: Default search returns only available pets

- Given pets exist with status "available" and "pending"
- When search_pets() is called with default parameters
- Then only pets with status="available" are returned

#### Scenario: Empty status parameter should not bypass filter

- Given pets exist with status "available" and "pending"
- When search_pets(status="") is called with empty string
- Then the search should default to available-only pets
- And pending pets must not appear in results

#### Scenario: Whitespace-only status should not bypass filter

- Given pets exist with status "available" and "pending"
- When search_pets(status="  ") is called with whitespace
- Then the search should default to available-only pets
- And pending pets must not appear in results

### Requirement: Explicit pending search must still work

#### Scenario: Explicit pending status returns only pending pets

- Given pets exist with status "available" and "pending"
- When search_pets(status="pending") is explicitly requested
- Then only pets with status="pending" are returned
- And available pets must not appear in results

## MODIFIED Requirements

None - this is a bug fix that enforces existing requirements.

## REMOVED Requirements

None.
