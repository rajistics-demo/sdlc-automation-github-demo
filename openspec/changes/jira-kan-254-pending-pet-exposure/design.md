# Design

## Context

The Petstore demo has a static customer-facing UI (`app/web/`) with hardcoded pet data. The current pets array includes:
- pet-100 (Mochi, cat, available)
- pet-101 (Scout, dog, available)
- pet-102 (Pip, rabbit, available)
- pet-103 (Nova, dog, **pending**)

The JavaScript filter at runtime excludes pending pets from the display, but the data is present in the client-side source code.

Product rule: "Default pet search returns only available pets. Pending pets can be shown only when explicitly requested and cannot be adopted."

## Decision

- Remove the pet-103 (Nova) entry from the `pets` array in `app/web/app.js`
- Keep the filter logic unchanged (defensive programming - no harm in keeping the status check)
- Update no other files; backend code is already correct

This is the smallest safe fix that prevents pending pet data exposure.

## Risks

- **Low**: Removing pending pets from client-side data could affect support/operations workflows that rely on this UI
  - **Mitigation**: The product rule states pending pets are for "support and operations workflows" with explicit requests; the customer-facing UI is not that workflow
  
- **Low**: Tests might depend on pending pets being present in the data
  - **Mitigation**: Playwright test searches for "nova" and expects empty results, so removing Nova from the array should not break it

## Validation Plan

1. Backend tests: `python3 -m pytest -q app/tests/test_pet_catalog.py app/tests/test_adoptions.py`
2. Playwright UI test: Verify pending pet search shows empty state
3. Visual confirmation: Serve the UI and verify only Mochi, Scout, and Pip appear by default
