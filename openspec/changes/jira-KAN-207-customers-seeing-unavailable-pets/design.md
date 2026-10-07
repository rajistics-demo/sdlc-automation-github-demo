# Design

## Context

The Petstore catalog stores pet availability in the `status` field. Default search behavior should return available pets only, while explicit status searches can inspect pending pets for support or operational workflows.

The bug is in `app/petstore_app/catalog.py` line 41 and 50. When `status` is normalized on line 41, an empty string becomes `""`. Then on line 50, the condition `if normalized_status and normalized_status != pet.status` fails to filter when `normalized_status` is empty because empty strings are falsy in Python.

## Decision

- Fix line 41 to ensure `normalized_status` is never empty: default to `"available"` when status is empty or whitespace-only.
- Change: `normalized_status = status.strip().lower()` to `normalized_status = status.strip().lower() if status and status.strip() else "available"`
- This ensures empty status calls behave the same as the default parameter.
- Preserve explicit `status="pending"` searches for support workflows.
- Add regression test for empty status parameter.

## Risks

- A broad fix could hide pending pets from support workflows that explicitly request them. Mitigation: the fix only affects empty/missing status; explicit `status="pending"` continues to work.
- Existing callers might depend on empty status returning all pets. Mitigation: product docs confirm default should be available-only, and the function signature already defaults to `"available"`.

## Validation Plan

- Add regression test: `test_search_pets_excludes_pending_by_default()` 
- Add regression test: `test_search_pets_excludes_pending_with_empty_status()`
- Run existing tests: `pytest app/tests/test_pet_catalog.py`
- Verify Nova (pet-103) does not appear in default results
- Verify explicit pending search still returns Nova
