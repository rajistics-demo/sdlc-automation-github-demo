# Design

## Context

The Petstore catalog provides a `search_pets()` function that filters pets by various criteria including status. According to `docs/wiki/petstore-catalog-availability.md`, the default customer-facing search must show only `status="available"` pets. Support and operations may explicitly request `status="pending"` when needed, but pending pets must never appear in default results.

The current implementation has a bug where the status filter is not correctly excluding pending pets in some search scenarios. Log evidence in `docs/logs/pending-pet-visible.ndjson` confirms the `PENDING_PET_VISIBLE` error with Nova (pet-103) appearing in available results.

## Decision

- Examine the current filtering logic in `search_pets()` to identify why pending pets are appearing.
- Ensure the status filter is applied correctly and consistently for all search paths.
- The fix should be minimal: correct the filtering logic without changing the function signature or test interface.
- Preserve the ability to explicitly search for `status="pending"` when requested.

## Risks

- **Risk**: Breaking existing explicit pending searches used by support/operations.
  - **Mitigation**: Keep the existing test `test_search_pets_can_find_pending_pets_when_requested()` and verify it still passes.

- **Risk**: Introducing performance degradation.
  - **Mitigation**: The fix involves only conditional logic; no additional loops or operations.

## Validation Plan

- Run existing test suite: `pytest app/tests/test_pet_catalog.py -v`
- Add new regression test that verifies pending pets don't appear in default searches.
- Verify the specific scenario: `search_pets(species="dog")` should return only Scout (pet-101), not Nova (pet-103).
