# Petstore Catalog Spec Delta

## ADDED Requirements

### Requirement: Empty status parameter returns only available pets

Empty or whitespace-only status parameters must be normalized to `"available"` so that customers never see pending pets in default search results.

#### Scenario: Empty status string returns only available pets

- Given the catalog contains pets with various statuses including pending
- When a caller invokes `search_pets(species="dog", status="")`
- Then only pets with `status="available"` are returned
- And pending pets (like Nova, pet-103) are NOT included

#### Scenario: Whitespace-only status returns only available pets

- Given the catalog contains pets with various statuses
- When a caller invokes `search_pets(status="   ")`
- Then only pets with `status="available"` are returned

#### Scenario: Default parameter continues to work correctly

- Given the catalog contains pets with various statuses
- When a caller invokes `search_pets()` with no status parameter
- Then only pets with `status="available"` are returned
- And this behavior is unchanged from before

## UNCHANGED Requirements

### Requirement: Explicit pending searches still work for support workflows

Support and operations teams must be able to explicitly search for pending pets when investigating cases.

#### Scenario: Explicit pending status returns pending pets

- Given the catalog contains pets with various statuses
- When a support agent invokes `search_pets(status="pending")`
- Then only pets with `status="pending"` are returned
- And this behavior is unchanged from before

#### Scenario: Species filter works with status filter

- Given the catalog contains pets with various statuses
- When a caller invokes `search_pets(species="dog")`
- Then only available dogs are returned
- And pending dogs (like Nova) are NOT included
