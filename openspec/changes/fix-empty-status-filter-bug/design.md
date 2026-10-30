# Design

## Context

The pet catalog search function in `app/petstore_app/catalog.py` has a status parameter with a default value of "available". However, when an empty string or whitespace-only string is explicitly passed, the current implementation treats it as falsy and skips status filtering entirely. This allows all pets (including pending ones) to be returned.

The product rule is: "Default pet search returns only available pets." The static UI correctly filters to available pets, but the backend API has this bug that could be exploited by direct API calls or incorrect UI integration.

## Decision

- Normalize the status parameter after stripping whitespace: if it becomes empty, default it to "available"
- This ensures empty string and whitespace-only strings are treated the same as the default parameter
- Keep the existing logic for explicit status values (available, pending, etc.)
- Add regression tests that verify empty and whitespace-only status values return only available pets
- No changes to function signature or existing behavior for explicit status values

## Risks

- **Backward compatibility**: If any caller is intentionally passing status="" to get all pets, this breaks that behavior
  - **Mitigation**: This is a bug fix. The product rule requires filtering to available pets by default. Any caller depending on the bug should be fixed.
- **Test coverage**: The existing tests don't cover the empty string edge case
  - **Mitigation**: Adding explicit regression tests for empty and whitespace status parameters

## Validation Plan

- Run `python3 -m pytest -q app/tests/test_pet_catalog.py` to verify all catalog tests pass
- Run `python3 -m pytest -q` to verify full test suite passes
- Manual smoke test: verify `search_pets(status="")` returns only available pets
- Manual smoke test: verify `search_pets(status="   ")` returns only available pets
- Manual smoke test: verify `search_pets(status="pending")` still returns only pending pets
