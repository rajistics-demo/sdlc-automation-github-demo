# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default catalog search excludes pending pets

The default pet search must return only pets with status="available". Pending pets must not appear in results when status is not explicitly specified.

#### Scenario: Default search excludes pending pets

- Given the catalog contains pets with both "available" and "pending" status
- When a user performs a default search without specifying status
- Then only pets with status="available" are returned
- And pets with status="pending" are excluded

#### Scenario: Species search with default status excludes pending pets

- Given the catalog contains dogs with "available" status and dogs with "pending" status
- When a user searches for dogs without specifying status
- Then only dogs with status="available" are returned
- And dogs with status="pending" are excluded

### Requirement: Empty status parameter does not bypass filtering

The catalog search must not treat an empty status parameter as "no filter". An empty or whitespace-only status value must not return pets of all statuses.

#### Scenario: Empty status parameter

- Given the catalog contains pets with "available" and "pending" status
- When a user performs a search with status=""
- Then the status filter is still enforced
- And pending pets are not returned

### Requirement: Explicit pending status search works for support workflows

Support and operations must be able to explicitly search for pending pets when needed for case investigation.

#### Scenario: Explicit pending pet search

- Given the catalog contains pets with both "available" and "pending" status
- When a support user explicitly searches with status="pending"
- Then only pets with status="pending" are returned
- And this capability remains available for operations workflows
