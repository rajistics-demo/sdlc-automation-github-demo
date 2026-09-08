# Petstore Catalog Spec Delta

## ADDED Requirements

### Requirement: Default catalog search excludes pending pets

The default customer-facing catalog search must return only pets with `status="available"`. Pending pets must not appear in search results unless explicitly requested with `status="pending"`.

#### Scenario: Default search excludes pending pets

- Given a catalog with available pets (Scout, Whiskers, Goldie) and pending pet (Nova)
- When a customer searches without specifying status (uses default `status="available"`)
- Then only available pets are returned
- And Nova (pet-103, status="pending") is not included

#### Scenario: Empty string status does not bypass filtering

- Given a catalog with available pets and pending pet Nova
- When `search_pets()` is called with `status=""`
- Then the status filter is still applied
- And pending pets are not returned
- And the result matches pets with `status=""` (which is none)

#### Scenario: Explicit pending search returns pending pets

- Given a catalog with available pets and pending pet Nova
- When a customer searches with `status="pending"`
- Then only pending pets like Nova are returned
- And available pets are excluded

## MODIFIED Requirements

### Requirement: Status filtering must handle edge cases defensively

The status filtering logic must treat empty string as a specific filter value, not as a signal to bypass filtering. This ensures the function cannot be misused to expose pets that should not be visible.

#### Scenario: Status filter applies consistently

- Given any input to the status parameter (default, explicit value, empty string, whitespace)
- When `search_pets()` processes the filter
- Then the status filter is always applied after normalization
- And falsy status values do not bypass the filter logic
