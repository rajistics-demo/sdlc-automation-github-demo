# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default search must exclude pending pets

Default customer-facing catalog search must return only pets with `status="available"`. Pending pets must be excluded from all default search results, regardless of how the search is invoked.

#### Scenario: Default search excludes pending pets

- Given a catalog containing available and pending pets
- When a customer performs a default search (no explicit status parameter)
- Then only pets with status="available" are returned
- And pending pets (like Nova/pet-103) are excluded from results

#### Scenario: Species filter with default status excludes pending pets

- Given a catalog containing both available and pending dogs
- When a customer searches for species="dog" without specifying status
- Then only available dogs are returned (Scout/pet-101)
- And pending dogs (Nova/pet-103) are excluded

#### Scenario: Empty status parameter does not bypass filter

- Given a catalog containing available and pending pets
- When search is called with an empty status string (status="")
- Then the search should still filter by the default status="available"
- And pending pets are excluded from results

## PRESERVED Requirements

### Requirement: Explicit pending search continues to work

Support and operations staff must be able to explicitly search for pending pets when investigating cases.

#### Scenario: Explicit pending search returns pending pets

- Given a catalog containing pending pets
- When support staff searches with status="pending"
- Then only pending pets are returned (Nova/pet-103)
- And available pets are excluded from results
