# Design

## Context

The Petstore catalog search function (`app/petstore_app/catalog.py`) has a status filter that defaults to `"available"`. However, the filter implementation uses `if normalized_status and normalized_status != pet.status:` which treats empty strings as falsy, causing all pets (including pending ones) to be returned.

Product rules from `docs/wiki/petstore-catalog-availability.md`:
- Default customer-facing catalog search must show only pets with `status="available"`
- Pending pets should only appear when explicitly requested via `status="pending"`
- Nova (pet-103) is the demo pending pet

Log evidence from `docs/logs/pending-pet-visible.ndjson`:
- Error code: `PENDING_PET_VISIBLE`
- Bug signal indicates catalog availability regression
- Customer impact: Pending pets visible in available-pets experience

## Decision

- Change the status filter condition from `if normalized_status and normalized_status != pet.status:` to `if normalized_status != pet.status:`
- This ensures that even when `normalized_status` is an empty string (after `.strip().lower()`), the filter still applies
- The default parameter value `status="available"` ensures correct behavior for typical calls
- This is the minimal change that fixes the bug without altering the API

## Risks

- Low: The change is a single-line fix to filter logic
- Mitigation: Existing tests verify species, tag, and explicit status filtering still work
- Mitigation: New regression tests confirm empty status doesn't bypass filter

## Validation Plan

- Run existing test suite: `python3 -m pytest -q app/tests/test_pet_catalog.py`
- Run full test suite: `python3 -m pytest -q`
- Verify new regression tests pass
- Manual reproduction test to confirm empty status no longer returns pending pets
