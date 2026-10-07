# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Empty status parameter must not bypass availability filter

When the catalog search receives an empty status string, it must treat it as a filter value that matches nothing, not as a signal to skip filtering.

#### Scenario: Empty status string returns only available pets

- Given the catalog contains available pets (pet-100, pet-101, pet-102) and pending pets (pet-103)
- When a search is performed with `status=""`
- Then only available pets are returned
- And pending pets are not included in results

#### Scenario: Default status parameter continues to work

- Given the catalog contains available pets and pending pets
- When a search is performed without specifying status (using default)
- Then only available pets are returned
- And the behavior matches historical default searches

#### Scenario: Explicit pending status continues to work

- Given the catalog contains pending pets (pet-103)
- When a search is performed with `status="pending"`
- Then pending pets are returned as expected
- And existing functionality is preserved

## MODIFIED Requirements

None. The requirement that default searches return only available pets already exists; this change fixes a regression where empty strings bypassed that requirement.

## REMOVED Requirements

None.

## Acceptance Criteria

- ✅ Default catalog searches (no status parameter) return only available pets
- ✅ Explicit `status="available"` searches return only available pets
- ✅ Explicit `status="pending"` searches return pending pets when explicitly requested
- ✅ Empty `status=""` searches return only available pets (NEW - regression fix)
- ✅ All existing tests continue to pass
- ✅ New regression test verifies empty status string behavior
- ✅ Frontend Playwright tests continue to pass unchanged
