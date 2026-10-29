# Catalog Spec Delta

## ADDED Requirements

### Requirement: Default search must exclude pending pets

Default pet catalog search must return only pets with `status="available"`, excluding pets with `status="pending"`.

#### Scenario: Default search excludes pending pets

- Given the catalog contains pets with various statuses including "available" and "pending"
- When a search is performed with default status parameter
- Then only pets with status="available" are returned
- And pets with status="pending" like Nova (pet-103) are excluded

#### Scenario: Empty status string is treated as default available-only search

- Given the catalog contains both available and pending pets
- When a search is performed with an empty string for status
- Then the search defaults to available-only filtering
- And pending pets are excluded from results

#### Scenario: Explicit pending status search still works

- Given the catalog contains pets with status="pending"
- When a search is performed with status="pending" explicitly requested
- Then pending pets are returned
- And available pets are excluded

This maintains support and operations workflows while protecting the customer-facing experience.
