# Design

## Context

The Petstore catalog has a `search_pets()` function that accepts multiple filter parameters including `status`. The default value for `status` is `"available"`, which should ensure that only available pets appear in default searches.

The current bug: The status filter condition uses `if normalized_status and ...`, which treats empty strings as falsy and skips the filter entirely. This allows pending pets to leak into results when `status=""` is passed explicitly.

The UI (`app/web/app.js`) already correctly hardcodes `pet.status === "available"` in its filter, so the UI is not affected by this backend bug.

## Decision

- Change the status filter condition from `if normalized_status and normalized_status != pet.status:` to `if normalized_status != pet.status:`
- This ensures the filter is always applied, even when `status=""` is passed
- Since the default parameter value is `"available"`, empty strings will be normalized and compared against pet status
- Preserve all other filter behavior (species, tag, query) unchanged

## Risks

- **Backward compatibility**: If any code relies on passing `status=""` to bypass the filter, that code will break. Mitigation: This is the desired behavior change; bypassing the filter was the bug.
- **Test coverage**: The existing tests don't cover the empty-string case. Mitigation: Add explicit regression tests for default status, explicit available status, and empty status scenarios.

## Validation Plan

- Run existing catalog tests: `python3 -m pytest -q app/tests/test_pet_catalog.py`
- Add new regression tests for:
  - Default search excludes pending pets
  - Explicit available-only search excludes pending pets  
  - Empty string status does not bypass filter
- Run full test suite: `python3 -m pytest -q`
- No UI changes needed (UI already correct)
