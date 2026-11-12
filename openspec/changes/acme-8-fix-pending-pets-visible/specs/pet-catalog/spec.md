# Pet Catalog Spec Delta

## ADDED Requirements

### Requirement: Empty status parameter should not bypass filtering

The `search_pets()` function must enforce status filtering even when an empty string is passed for the `status` parameter.

#### Scenario: Default search returns only available pets

- Given the petstore has pets with various statuses
- When `search_pets()` is called with no status parameter
- Then only pets with `status="available"` are returned

#### Scenario: Empty status string returns no results

- Given the petstore has pets with various statuses
- When `search_pets(status="")` is called with an empty string
- Then no pets are returned (empty string matches no valid status)

#### Scenario: Explicit pending search works correctly

- Given the petstore has pets with `status="pending"`
- When `search_pets(status="pending")` is called
- Then only pets with `status="pending"` are returned

## CHANGED Requirements

### Requirement: Status filter must always be applied

**Before:** The status filter had a truthy check that could be bypassed with empty strings

**After:** The status filter is applied unconditionally, ensuring every search filters by status