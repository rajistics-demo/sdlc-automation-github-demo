# Pet Catalog Search Spec Delta

## ADDED Requirements

### Requirement: Default search excludes pending pets

Default pet catalog searches SHALL return only pets with `status="available"`.

#### Scenario: Default search without status parameter

- Given the catalog contains Mochi (available), Scout (available), Pip (available), and Nova (pending)
- When `search_pets()` is called with no status parameter
- Then only Mochi, Scout, and Pip are returned
- And Nova is not in the results

### Requirement: Empty status string excludes pending pets

Empty status strings SHALL NOT bypass the status filter.

#### Scenario: Search with empty status string

- Given the catalog contains Mochi (available), Scout (available), Pip (available), and Nova (pending)
- When `search_pets(status="")` is called with an empty status string
- Then only Mochi, Scout, and Pip are returned
- And Nova is not in the results

### Requirement: Explicit pending status works

Explicit pending status searches SHALL return pending pets.

#### Scenario: Explicit pending pet search

- Given the catalog contains Nova (pending dog)
- When `search_pets(status="pending")` is called
- Then Nova is returned

### Requirement: Species filter respects default status

Species filters SHALL apply the default status filter.

#### Scenario: Dog search with default status

- Given the catalog contains Scout (available dog) and Nova (pending dog)
- When `search_pets(species="dog")` is called
- Then only Scout is returned
- And Nova is not in the results
