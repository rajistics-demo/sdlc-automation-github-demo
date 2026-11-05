# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Empty status parameter must filter for available pets only

#### Scenario: Search with empty status string returns only available pets

- Given a catalog with pets of mixed status (available and pending)
- When a search is performed with `status=""`
- Then only pets with `status="available"` are returned
- And pending pets like Nova (pet-103) are excluded

#### Scenario: Search with no status parameter returns only available pets (existing)

- Given a catalog with pets of mixed status
- When a search is performed without specifying status parameter
- Then only pets with `status="available"` are returned
- And this behavior is unchanged from current implementation

#### Scenario: Search with explicit available status works as before (existing)

- Given a catalog with pets of mixed status
- When a search is performed with `status="available"`
- Then only pets with `status="available"` are returned

#### Scenario: Search with explicit pending status works as before (existing)

- Given a catalog with pets of mixed status
- When a search is performed with `status="pending"`
- Then only pets with `status="pending"` are returned
- And this supports operations staff use cases

## MODIFIED Requirements

None - this fix restores the intended behavior without changing the specification.

## REMOVED Requirements

None - all existing requirements remain valid.
