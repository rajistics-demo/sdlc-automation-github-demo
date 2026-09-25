# Design

## Context

The Petstore demo has catalog search behavior in `app/petstore_app/catalog.py`:

- **Backend**: `search_pets()` function with default `status="available"` parameter (line 31).
- **Status filtering**: Lines 41-50 normalize and apply the status filter.
- **Product rule**: Default pet search returns only available pets. Pending pets can be shown only when explicitly requested and cannot be adopted.
- **Known fixture**: Nova is `pet-103` with `status="pending"` (per `catalog.py` line 23).

## Investigation Findings

### Backend Code Review

The bug is in the status filter logic:

**Line 41**: `normalized_status = status.strip().lower()`
- When `status=""` is passed, this results in an empty string after stripping and lowering.

**Line 50**: `if normalized_status and normalized_status != pet.status:`
- The truthy check `if normalized_status` means when `normalized_status` is an empty string (falsy), the entire status filter is skipped.
- This allows ALL pets (including pending ones) to pass through when `status=""` is explicitly passed.

### Test Evidence

Created two new tests to reproduce the bug:

1. `test_search_pets_default_returns_only_available()` - Verifies default behavior works correctly
2. `test_search_pets_empty_status_should_use_default()` - **This test fails before the fix**, confirming the bug

Before the fix, passing `status=""` returned 4 pets (including Nova with status="pending"), when it should only return 3 available pets.

### Frontend Code Review

- `app/web/app.js` line 17: `&& pet.status === "available"` correctly filters to available pets only ✓
- No frontend changes needed.

## Decision

Fix the backend `search_pets()` function to prevent empty status strings from bypassing the filter:

1. **Line 41**: Change to `normalized_status = status.strip().lower() if status.strip() else "available"`
   - This ensures empty or whitespace-only status values default to "available"

2. **Line 50**: Change to `if normalized_status != pet.status:`
   - Remove the truthy check since `normalized_status` is now guaranteed to have a value
   - Always apply the status filter

This is the smallest safe change that:
- Preserves the default behavior when no status is provided
- Fixes the bug when empty strings are explicitly passed
- Maintains backward compatibility for all explicit status values
- Keeps existing functionality unchanged

## Risks

- **Low risk**: The change is minimal and well-tested.
- **Backward compatibility**: All existing tests continue to pass.
- **Edge case**: Whitespace-only strings like `"  "` now default to "available" (desirable behavior).

## Validation Plan

- [x] Add regression tests that reproduce the bug
- [x] Run backend tests before fix: `python3 -m pytest app/tests/test_pet_catalog.py` - confirmed failure
- [x] Implement the fix in `catalog.py`
- [x] Run backend tests after fix: all 7 catalog tests pass ✓
- [x] Run adoption tests: all 4 tests pass ✓
- [ ] Validate OpenSpec artifacts with `python3 skills/sdlc-story/scripts/validate_open_spec.py`
