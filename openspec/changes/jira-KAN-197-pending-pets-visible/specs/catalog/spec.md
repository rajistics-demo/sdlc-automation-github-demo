# Catalog Spec Delta

## ADDED Requirements

### Requirement: Empty status parameter must not bypass availability filter

The catalog search function must enforce the default availability filter even when called with an empty status string, ensuring pending pets remain hidden from default search results.

#### Scenario: Default search excludes pending pets

- Given the catalog contains both available and pending pets
- When `search_pets()` is called with no status parameter
- Then only pets with `status="available"` are returned

#### Scenario: Empty status string does not bypass filter

- Given the catalog contains both available and pending pets
- When `search_pets(status="")` is called with an empty string
- Then only pets with `status="available"` are returned
- And pets with `status="pending"` are excluded

#### Scenario: Explicit pending status returns pending pets

- Given the catalog contains pending pets
- When `search_pets(status="pending")` is called explicitly
- Then only pets with `status="pending"` are returned
- And this behavior remains unchanged (already correct)

## Context

Per Petstore product rules (AGENTS.md):
- Default pet search returns only available pets
- Pending pets can be shown only when explicitly requested and cannot be adopted

## Evidence

The investigation confirmed:
- Bug location: `app/petstore_app/catalog.py` line 50
- Root cause: The condition `if normalized_status and normalized_status != pet.status:` allows empty strings to bypass the filter
- Incident log: `docs/logs/pending-pet-visible.ndjson` confirms `pet-103` (Nova, pending) was exposed via `PENDING_PET_VISIBLE` error
