# Petstore Catalog Spec Delta

## ADDED Requirements

### Requirement: Empty status parameter must not bypass availability filter

When the catalog search is called with an empty status parameter, pending pets must not be included in results.

#### Scenario: Search with empty status string excludes pending pets

- Given the catalog contains Nova (pet-103) with status "pending"
- And the catalog contains Scout (pet-101) with status "available"
- When a user searches for dogs with status=""
- Then only Scout appears in results
- And Nova does not appear in results

#### Scenario: Default search excludes pending pets

- Given the catalog contains Nova (pet-103) with status "pending"
- And the catalog contains available pets
- When a user searches without specifying a status parameter
- Then only available pets appear in results
- And Nova does not appear in results

### Requirement: Explicit pending status search continues to work

Support and operations workflows that explicitly request pending pets must continue to function.

#### Scenario: Explicit pending search returns pending pets

- Given the catalog contains Nova (pet-103) with status "pending"
- When a user searches with status="pending"
- Then Nova appears in results

## MODIFIED Requirements

None. The intended behavior already exists in documentation; this change enforces what was always required.

## REMOVED Requirements

None.
