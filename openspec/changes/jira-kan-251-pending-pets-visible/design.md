# Design: Fix Pending Pets Visibility

## Investigation Summary

### Stop 1 - Ticket
- **Source**: Jira KAN-251
- **Report**: Support reports customers seeing unavailable pets, creating confusion and operational overhead
- **Key clue**: "pets that should not be available yet" indicates a status filtering issue

### Stop 2 - Wiki/Docs
- **Checked**: `docs/wiki/petstore-catalog-availability.md`
- **Finding**: Product rule states "Default customer-facing catalog search must show only pets with status='available'"
- **Evidence**: Nova (pet-103) with status="pending" should not appear in available-pets experience

### Stop 3 - Logs
- **Checked**: `docs/logs/pending-pet-visible.ndjson`
- **Finding**: Error code `PENDING_PET_VISIBLE` logged for pet-103
- **Signal**: `catalog_availability_regression` with `safe_to_fix: true`

### Stop 4 - Repo/Files

#### Backend Analysis (`app/petstore_app/catalog.py`)
- `search_pets()` function has `status="available"` as default parameter ✓
- Status normalization and filtering logic present (lines 41-51) ✓
- **Assessment**: Backend filtering appears correct

#### Frontend Analysis (`app/web/app.js`)
- Hardcoded pets array includes Nova with `status: "pending"` (line 5)
- `renderResults()` filters with `pet.status === "available"` (line 17)
- **Assessment**: Frontend filtering appears correct

#### Test Coverage Analysis
- Backend tests verify species+status filtering
- Backend tests verify explicit pending pet searches work
- **Gap**: No explicit test that default search excludes pending pets
- **Gap**: No frontend/UI test coverage in the automated test suite

## Root Cause Analysis

After investigation, the current code appears to correctly filter pending pets in both backend and frontend. However:

1. **Test Coverage Gap**: No explicit regression test verifies that the default search excludes pending pets
2. **Documentation**: Implementation map notes this as a "Common Bug Slice" suggesting it's a known regression point
3. **Historical Evidence**: Log evidence shows this bug occurred, even if code is currently correct

## Implementation Strategy

### Approach: Add Regression Tests + Documentation

Since the filtering logic appears correct, the fix strategy is to:

1. **Add explicit backend test** that verifies default search excludes pending pets
2. **Add explicit frontend test** that verifies the initial page load excludes Nova
3. **Document the filtering logic** with inline comments explaining the availability constraint
4. **Run existing Playwright test** to confirm UI behavior matches expectations

### Files to Modify

| File | Change | Risk |
|------|--------|------|
| `app/tests/test_pet_catalog.py` | Add test_default_search_excludes_pending_pets | Low - test only |
| `app/web/app.js` | Add explanatory comment on line 17 | Low - documentation |
| `app/petstore_app/catalog.py` | Add explanatory comment on status filter | Low - documentation |

### Non-Changes

- No changes to data model or persistence
- No changes to UI layout or styling
- No changes to adoption validation (already correctly rejects pending pets)
- No new dependencies

## Validation Plan

1. Run backend tests: `PYTHONPATH=app python -m pytest app/tests/ -v`
2. Run Playwright UI test if available: `node app/web/tests/catalog-search.playwright.mjs`
3. Verify test output confirms:
   - Default search returns only Mochi, Scout, Pip (not Nova)
   - Species filter for "dog" returns only Scout (not Nova)
   - Searching for "nova" returns empty result

## Context

The Petstore catalog is a customer-facing feature where users browse and adopt pets. The availability status controls which pets customers can see and adopt. Historical logs show that pending pets (specifically Nova, pet-103) were visible to customers, creating confusion and support burden.

Current product rules require:
- Default catalog search shows only available pets
- Pending pets visible only when explicitly requested (operations use case)
- Adoption orders must reject pending pets

## Decision

**Primary Decision**: Add explicit regression tests rather than modify filtering logic.

**Rationale**: Investigation shows both backend and frontend correctly filter by status="available". The issue is lack of explicit test coverage, making this a known regression point. Adding focused tests prevents future regressions while keeping changes minimal and safe.

**Alternative Considered**: Refactor filtering logic to make it more defensive. Rejected because current implementation is correct and refactoring adds unnecessary risk.

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| False positive - bug still exists | Low | High | Run Playwright UI test to verify actual browser behavior |
| Test doesn't catch real regression pattern | Low | Medium | Model test scenarios directly from logged bug evidence |
| Documentation insufficient to prevent future issues | Medium | Low | Add inline comments and reference product rules in tests |

## Rollback Plan

If tests fail or issues arise:
- Revert test additions (safe - test-only changes)
- Revert documentation comments (safe - comment-only changes)
