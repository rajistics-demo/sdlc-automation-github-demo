# Catalog Filtering Spec Delta

## ADDED Requirements

### Requirement: Default pet search must exclude pending pets

#### Scenario: Default available search excludes pending pets

- Given Nova (pet-103) has status="pending"
- And Scout (pet-101) has status="available"
- When a user searches for dogs with default status filter
- Then only Scout appears in results
- And Nova does not appear in results

#### Scenario: Explicit pending search shows pending pets

- Given Nova (pet-103) has status="pending"
- When a user explicitly requests status="pending" dogs
- Then Nova appears in results
- And available dogs do not appear

#### Scenario: Empty status parameter is invalid

- Given a search request with empty status string
- When the search is executed
- Then the system should reject the empty status or apply the default "available" filter
- And pending pets must not appear in results

## MODIFIED Requirements

### Requirement: Status filter must be enforced

Previously, the status filter could be bypassed with an empty string. Now:

- The normalized_status check must distinguish between "not provided" and "empty string"
- Empty strings should not bypass the filter
- Default "available" status must always be applied unless explicitly overridden

## Acceptance Criteria

1. `search_pets()` with default parameters returns only available pets
2. `search_pets(species="dog")` returns only Scout, not Nova
3. `search_pets(status="")` does not return pending pets
4. `search_pets(status="pending")` explicitly returns pending pets when requested
5. Test coverage includes regression test for PENDING_PET_VISIBLE scenario
