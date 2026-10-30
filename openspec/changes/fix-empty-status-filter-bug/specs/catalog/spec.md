# Pet Catalog Spec Delta

## ADDED Requirements

### Requirement: Empty status parameter must default to available pets only

When the status parameter is an empty string (or whitespace-only string), the search must return only pets with status="available", not all pets regardless of status.

#### Scenario: Empty status string returns only available pets

- Given a catalog with available pets and pending pets
- When a search is performed with status=""
- Then only pets with status="available" are returned
- And pending pets are excluded from results

#### Scenario: Whitespace-only status string returns only available pets

- Given a catalog with available pets and pending pets  
- When a search is performed with status="   " (whitespace only)
- Then only pets with status="available" are returned
- And pending pets are excluded from results

#### Scenario: Explicit pending status still works for support workflows

- Given a catalog with available pets and pending pets
- When a search is performed with status="pending"
- Then only pets with status="pending" are returned
- And available pets are excluded from results

#### Scenario: Default status parameter returns only available pets

- Given a catalog with available pets and pending pets
- When a search is performed without specifying status (using default)
- Then only pets with status="available" are returned
- And pending pets are excluded from results
