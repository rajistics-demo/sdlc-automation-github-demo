# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Empty status parameter must default to available-only filtering

When a customer searches the pet catalog without specifying a status or with an empty status string, the system must return only pets with status="available". Pending, adopted, or other non-available pets must not appear in these results.

#### Scenario: Search with empty status string returns only available pets

- Given the catalog contains pets with various statuses including "available" and "pending"
- And pet-103 (Nova) has status="pending"
- When a customer searches with status="" (empty string)
- Then the results include only pets where status="available"
- And pet-103 (Nova) is NOT in the results

#### Scenario: Search with no status parameter uses available-only default

- Given the catalog contains both available and pending pets
- When a customer searches without specifying a status parameter
- Then the results include only pets where status="available"
- And no pending pets appear in the results

#### Scenario: Explicit pending status request still works

- Given the catalog contains pending pets
- When support staff explicitly searches with status="pending"
- Then pending pets are included in the results
- And this behavior remains unchanged

## UNCHANGED Requirements

### Requirement: Species filtering works with default status

When filtering by species without an explicit status parameter, only available pets of that species are returned.

### Requirement: Explicit status filtering continues to work

When an explicit non-empty status is provided, the catalog filters to that status as before.
