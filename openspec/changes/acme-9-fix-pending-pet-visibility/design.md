# Design

## Context

The Petstore app has a `search_pets()` function in `app/petstore_app/catalog.py` that filters pets by status. The product rule states "Default pet search returns only available pets." The function has a default parameter `status: str = "available"`.

However, when external code explicitly passes an empty string `status=""`, the current normalization logic creates an empty `normalized_status`, which then bypasses the status filter due to Python's falsy evaluation of empty strings.

## Decision

- Modify the status normalization at line 41 to treat empty or whitespace-only strings as "available"
- Use the pattern: `normalized_status = status.strip().lower() if status.strip() else "available"`
- This maintains backward compatibility while closing the correctness gap
- Add a regression test that explicitly verifies `search_pets(status="")` returns only available pets

## Risks

- **Low risk**: This is a defensive fix that enforces existing product rules
- **No breaking changes**: Callers using the default parameter or explicit "available"/"pending" are unaffected
- **Edge case coverage**: Empty string and whitespace-only strings now have well-defined behavior

## Validation Plan

- Add test: `test_search_pets_with_empty_status_returns_only_available()`
- Verify the test fails before the fix (reproduces the bug)
- Apply the fix and verify the test passes
- Run full test suite: `python3 -m pytest -q app/tests/test_pet_catalog.py`
- Confirm no pending pets (Nova) appear in results when `status=""`
