# Design

## Context

The `search_pets()` function in `app/petstore_app/catalog.py` filters pets by status using a default parameter `status="available"`. The current implementation has a bug at line 50 where the condition `if normalized_status and normalized_status != pet.status:` uses a truthy check. When `status=""` is passed, the truthy check fails and the filter is bypassed, allowing pending pets to appear in search results.

The petstore product rules require that default pet search returns only available pets, and pending pets should only be shown when explicitly requested.

## Decision

- Remove the truthy check on line 50 and change `if normalized_status and normalized_status != pet.status:` to `if normalized_status != pet.status:`
- This ensures the status filter is always applied regardless of whether the value is an empty string
- Empty string will match no pets (since no pet has an empty status), which is safe behavior
- Keep the default parameter `status="available"` unchanged

## Risks

- **Breaking change:** Code that relies on `status=""` to bypass filtering will now get empty results
- **Mitigation:** The parameter default is `status="available"`, so callers should use the default or explicitly pass `status="pending"` when needed. Bypassing the status filter was never documented behavior.
- **Risk level:** Low - the fix enforces existing product rules

## Validation Plan

- Add regression test that verifies `search_pets(status="")` returns no pets
- Run existing test suite to ensure no breakage: `python3 -m pytest -q app/tests/test_pet_catalog.py`
- Verify adoption flow still blocks pending pets with existing tests
- Run full test suite: `python3 -m pytest -q`
