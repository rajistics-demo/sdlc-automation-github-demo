# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default catalog search must exclude pending pets

The default pet search must return only pets with `status="available"`. Pending pets must never appear in default search results.

#### Scenario: Default search excludes pending pets

- Given a catalog with available and pending pets
- When a user performs a default search (using default status="available")
- Then only pets with status="available" are returned
- And pets with status="pending" are not included

#### Scenario: Explicit pending search returns only pending pets

- Given a catalog with available and pending pets
- When a user explicitly requests status="pending"
- Then only pets with status="pending" are returned
- And pets with status="available" are not included

#### Scenario: Empty status parameter behaves as default

- Given a catalog with available and pending pets
- When a search is performed with an explicit empty string status=""
- Then the behavior matches the default (available pets only)
- And pending pets are not included

## FIXED Defects

### Defect: Empty string status bypasses filter

**Previous behavior:**
- Passing status="" would bypass the status filter entirely due to falsy check
- All pets (available and pending) would be returned

**Fixed behavior:**
- Empty string status is now treated consistently with the default
- Only available pets are returned

### Defect: Pending pets visible in available search

**Previous behavior:**
- Bug allowed pending pets like Nova (pet-103) to appear in available search results
- Logged as error code PENDING_PET_VISIBLE

**Fixed behavior:**
- Pending pets are correctly filtered out of default available search
- Status filter works correctly for all status values including edge cases
