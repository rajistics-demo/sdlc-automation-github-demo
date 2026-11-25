# Design

## Context

The Petstore catalog (`app/petstore_app/catalog.py`) normalizes all search inputs including tags by calling `.strip().lower()` on the input before comparison. The catalog has an existing test suite (`app/tests/test_pet_catalog.py`) that uses `pytest.mark.parametrize` for validation edge cases.

Existing test data in `PETS`:
- Mochi (cat): tags `("calm", "indoor")`
- Pip (rabbit): tags `("quiet", "indoor")`
- Scout (dog): tags `("active", "family")`
- Nova (dog): tags `("active", "training")`

The test suite already validates max_results range (1-50) but does not verify that the limit applies after filtering.

## Decision

- Use `pytest.mark.parametrize` to test multiple tag input variations efficiently
- Follow existing test patterns (see `test_search_pets_validates_max_results`)
- Add three focused test functions: case normalization, whitespace normalization, and max_results interaction
- Use the existing "indoor" tag (matches Mochi and Pip) for consistent test data

## Risks

- None - test-only change with no production code modifications
- Tests confirm existing behavior rather than changing it

## Validation Plan

1. Run new tests in isolation: `python3 -m pytest -q app/tests/test_pet_catalog.py::test_search_pets_normalizes_tag_case`
2. Run full test suite: `python3 -m pytest -q app/tests`
3. Run offline preflight: `python3 scripts/validation/preflight_github_demo.py --offline`
