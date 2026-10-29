# Pet Catalog Spec Delta

## ADDED Requirements

### Requirement: Empty status parameter must be treated as "available"

When the `search_pets()` function receives an empty string or whitespace-only string for the `status` parameter, it must filter results to only include pets with `status="available"`.

#### Scenario: Empty status string excludes pending pets

- Given pet data including Nova (pet-103) with `status="pending"`
- When `search_pets(status="")` is called
- Then only pets with `status="available"` are returned
- And Nova (pet-103) is NOT in the results

#### Scenario: Whitespace status string excludes pending pets

- Given pet data including Nova (pet-103) with `status="pending"`
- When `search_pets(status="  ")` is called with whitespace
- Then only pets with `status="available"` are returned
- And Nova (pet-103) is NOT in the results

### Requirement: Default status parameter behavior must be verified

The default `status="available"` parameter must correctly filter to only available pets.

#### Scenario: Default search excludes pending pets

- Given pet data including Nova (pet-103) with `status="pending"`
- When `search_pets()` is called without status argument
- Then only pets with `status="available"` are returned
- And Nova (pet-103) is NOT in the results

#### Scenario: Species filter with default status excludes pending pets

- Given pet data including Scout (available dog) and Nova (pending dog)
- When `search_pets(species="dog")` is called with default status
- Then only Scout (pet-101) is returned
- And Nova (pet-103) is NOT in the results

## UNCHANGED Requirements

### Requirement: Explicit status parameter values must be honored

When an explicit non-empty status value is provided, that exact status must be used for filtering (no changes to existing behavior).

#### Scenario: Explicit pending status returns only pending pets

- Given pet data including Nova (pet-103) with `status="pending"`
- When `search_pets(status="pending")` is called
- Then only pets with `status="pending"` are returned
- And Nova is included in the results

## Evidence

- **Wiki rule:** `docs/wiki/petstore-catalog-availability.md` states "Default customer-facing catalog search must show only pets with status='available'"
- **Log evidence:** `docs/logs/pending-pet-visible.ndjson` with error code `PENDING_PET_VISIBLE` confirms pet-103 (Nova) appearing incorrectly
- **Reproduction:** `search_pets(status="")` currently returns all 4 pets including Nova (pending), violating the availability rule
