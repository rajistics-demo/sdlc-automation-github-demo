# Spec Delta: Pet Catalog Availability Filtering

## MODIFIED Requirements

### Requirement: Default search returns only available pets

#### Scenario: Default search excludes pending pets
- Given: The catalog has Nova (pet-103) with status="pending"
- When: A customer searches with default parameters
- Then: Nova does not appear in results

#### Scenario: Empty status string defaults to available filtering
- Given: The catalog has Nova (pet-103) with status="pending"
- When: A search is made with status=""
- Then: Nova does not appear in results
- And: Only pets with status="available" are returned

#### Scenario: Explicit pending search still works
- Given: The catalog has Nova (pet-103) with status="pending"
- When: A support workflow searches with status="pending"
- Then: Nova appears in results

#### Scenario: Species filter with default status excludes pending
- Given: The catalog has Nova (pet-103, dog, pending) and Scout (pet-101, dog, available)
- When: A customer searches for species="dog" with default status
- Then: Only Scout appears in results
- And: Nova does not appear

## Behavioral Changes

### Before (Buggy Behavior)
- Calling `search_pets(status="")` bypasses status filtering
- Empty status string allows pending pets to leak into results
- Line 50 check `if normalized_status and ...` fails when status is empty

### After (Fixed Behavior)
- Empty status string defaults to "available" filtering
- `search_pets(status="")` now returns only available pets
- Explicit `status="pending"` still works for support workflows

## Test Coverage

New regression tests:
1. `test_search_pets_defaults_empty_status_to_available()` - Verify empty string defaults to available
2. `test_search_pets_excludes_pending_from_default_search()` - Verify Nova excluded by default

Existing tests preserved:
- `test_search_pets_can_find_pending_pets_when_requested()` - Explicit pending search still works
- `test_search_pets_filters_by_species_and_status()` - Species+status filtering works

## Residual Risks

- None identified. The fix is minimal and preserves all existing explicit-status behavior.
