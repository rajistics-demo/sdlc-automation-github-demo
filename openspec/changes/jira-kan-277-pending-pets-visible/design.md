# Design

## Context

The Petstore demo includes a catalog search function in `app/petstore_app/catalog.py` with a default parameter `status: str = "available"`. The implementation correctly filters pets, but test coverage doesn't explicitly verify that:

1. Default searches (no parameters) exclude pending pets
2. Species filters without status parameter exclude pending pets  
3. Searching for Nova by name returns empty when status defaults to available

The log evidence (`docs/logs/pending-pet-visible.ndjson`) shows a `PENDING_PET_VISIBLE` error occurred, indicating this regression scenario needs explicit test coverage. The wiki (`docs/wiki/petstore-catalog-availability.md`) confirms that Nova (pet-103) is the canonical pending pet for this demo.

## Decision

- Add three focused regression tests to `app/tests/test_pet_catalog.py`
- Use `assert "pet-103" not in [pet.id for pet in results]` to explicitly verify Nova exclusion
- Keep tests simple and focused on the regression scenario
- Use descriptive test names that explain what regression they prevent
- No changes to application code - implementation is already correct

## Risks

- **False sense of security**: These tests verify current behavior but don't guarantee protection against all possible catalog bugs. Mitigation: Tests target the specific PENDING_PET_VISIBLE regression scenario documented in logs.
  
- **Test brittleness**: Tests depend on Nova (pet-103) remaining the pending demo pet. Mitigation: This is an explicit demo contract documented in the wiki.

## Validation Plan

- Run `python3 -m pytest -xvs app/tests/test_pet_catalog.py` to verify all tests pass
- Verify new tests specifically check for Nova exclusion
- Confirm test names clearly describe the regression they prevent
