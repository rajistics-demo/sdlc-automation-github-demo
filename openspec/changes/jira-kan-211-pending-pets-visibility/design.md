# Design

## Context

The Petstore catalog module (`app/petstore_app/catalog.py`) provides a `search_pets()` function that filters pets by name, species, status, and tags. The function has a default parameter `status="available"` to ensure only available pets are shown by default.

The current implementation has a conditional check `if normalized_status and normalized_status != pet.status:` that allows the status filter to be bypassed when `normalized_status` evaluates to a falsy value (empty string). While the default parameter is "available", edge cases where an empty string could be passed or computed could cause pending pets to appear incorrectly.

Product rules from `docs/wiki/petstore-catalog-availability.md`:
- Default customer-facing catalog search must show only pets with `status="available"`
- Support and operations workflows may explicitly request `status="pending"`
- Pending pets must not appear in the default available-pets experience

Evidence from `docs/logs/pending-pet-visible.ndjson` shows error code `PENDING_PET_VISIBLE` with `pet-103` (Nova, status="pending") appearing in available-pets results.

## Decision

- Remove the `if normalized_status and` check on the status filter condition, changing from:
  ```python
  if normalized_status and normalized_status != pet.status:
  ```
  to:
  ```python
  if normalized_status != pet.status:
  ```

- This ensures the status filter is always applied with the default "available" value, preventing any edge case from bypassing the filter.

- The fix is minimal, preserves all existing behavior (default available, explicit pending), and prevents the bug without changing function signatures or adding complexity.

## Risks

- **Breaking change risk**: LOW - The fix only tightens existing behavior; it doesn't change the API or normal usage patterns.
- **Regression risk**: LOW - Existing tests verify both default available searches and explicit pending searches; new test adds specific coverage for the default behavior excluding pending pets.
- **Edge case risk**: MITIGATED - By removing the falsy check, we ensure the status filter is always active.

## Validation Plan

1. Run existing catalog tests to ensure no regressions:
   ```bash
   python -m pytest app/tests/test_pet_catalog.py -v
   ```

2. Add a new focused regression test that verifies default searches exclude pending pets:
   ```python
   def test_default_search_excludes_pending_pets() -> None:
       """Default search must not return pending pets like Nova."""
       results = search_pets()
       pet_ids = [pet.id for pet in results]
       assert "pet-103" not in pet_ids  # Nova (pending) must not appear
       assert "pet-100" in pet_ids  # Mochi (available) should appear
   ```

3. Verify the fix resolves the `PENDING_PET_VISIBLE` issue scenario.
