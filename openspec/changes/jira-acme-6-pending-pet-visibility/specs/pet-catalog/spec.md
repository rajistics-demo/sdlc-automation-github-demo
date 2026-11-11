# Pet Catalog Spec Delta

## ADDED Requirements

### Requirement: Default UI search must exclude pending pets

Default customer-facing catalog searches in the UI must only show pets with `status="available"`, matching the backend behavior.

#### Scenario: Default search returns only available pets

- Given the UI loads with the pet data including Nova (pet-103) with status "pending"
- When the user performs a default search with no explicit status filter
- Then the results must include only pets with status "available" (Mochi, Scout, Pip)
- And the results must not include Nova (pet-103)

#### Scenario: Species filter with default status

- Given the UI loads with pet data
- When the user filters by species "dog" without specifying status
- Then the results must include only Scout (pet-101) which is available
- And the results must not include Nova (pet-103) which is pending

#### Scenario: Empty query with default status

- Given the UI loads with pet data
- When the user searches with an empty query string
- Then the results must include only available pets (Mochi, Scout, Pip)
- And the results must not include Nova (pet-103)

## MODIFIED Requirements

None - the backend already enforces correct status filtering. This change aligns the UI with the existing backend contract.

## DELETED Requirements

None - no existing requirements are being removed.
