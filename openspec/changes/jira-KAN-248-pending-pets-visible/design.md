# Design

## Context

The Petstore catalog stores pet availability in the `status` field. Default search behavior should return available pets only, while explicit status searches can view pending pets for support workflows. The bug occurs in `search_pets()` when empty status strings bypass the filter.

## Decision

- Update status normalization to treat empty strings as "available"
- Change line 41 in `catalog.py`: `normalized_status = (status.strip() or "available").lower()`
- Preserve default parameter value `status="available"`
- Maintain explicit `status="pending"` searches for support workflows
- Add regression test for empty status parameter

## Risks

- Low risk: single line change with focused scope
- Existing tests verify backward compatibility
- No deployment, schema, or auth changes

## Validation Plan

- Run `pytest app/tests/test_pet_catalog.py -v` for catalog tests
- Verify existing tests pass
- New test confirms empty status returns only available pets
- Verify Nova (pet-103) excluded from default search
- Full test suite before opening PR
