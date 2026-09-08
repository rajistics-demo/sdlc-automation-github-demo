# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Status filter must not be bypassable via empty string

The `search_pets()` function must apply status filtering consistently, even when edge-case inputs like empty strings are provided.

#### Scenario: Default search returns only available pets

- Given the catalog contains pets with various statuses including "available" and "pending"
- When a caller invokes `search_pets()` with no explicit status parameter
- Then only pets with `status="available"` are returned

#### Scenario: Empty string status does not bypass filter

- Given the catalog contains both available and pending pets
- When a caller invokes `search_pets(status="")`
- Then the search does not return pending pets
- And the default "available" status filter is still applied

#### Scenario: Pending pets are excluded from default searches

- Given Nova (pet-103) has `status="pending"`
- When a caller invokes `search_pets()` or `search_pets(status="available")`
- Then Nova (pet-103) is not included in the results

#### Scenario: Pending pets can be explicitly requested

- Given Nova (pet-103) has `status="pending"`
- When a caller invokes `search_pets(status="pending")`
- Then Nova (pet-103) is included in the results

## MODIFIED Requirements

### Requirement: Status filter condition must be robust

**Before:** The filter used `if normalized_status and normalized_status != pet.status:` which allowed empty strings to bypass filtering

**After:** The filter uses `if normalized_status != pet.status:` which always applies the comparison when a status value is provided (including the default "available")

## Acceptance Criteria

- ✅ Default `search_pets()` returns only available pets
- ✅ Explicit `search_pets(status="available")` returns only available pets
- ✅ Explicit `search_pets(status="pending")` returns only pending pets
- ✅ Edge case `search_pets(status="")` does not bypass the filter
- ✅ Nova (pet-103) is excluded from default and available searches
- ✅ Nova (pet-103) is included in pending searches
- ✅ All existing catalog tests continue to pass
