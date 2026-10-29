# Spec Delta: Pet Catalog Status Filtering

## Acceptance Criteria

### Must Have

**AC1: Default search excludes pending pets**
- GIVEN: A customer uses the default pet search (no status parameter)
- WHEN: search_pets() is called
- THEN: Only pets with status="available" are returned
- AND: Pending pets (like pet-103/Nova) are NOT included

**AC2: Empty status is treated as "available"**
- GIVEN: A caller explicitly passes status="" (empty string)
- WHEN: search_pets(status="") is called
- THEN: The result is identical to search_pets(status="available")
- AND: Pending pets are NOT included

**AC3: Explicit pending searches still work**
- GIVEN: Support staff needs to view pending pets
- WHEN: search_pets(status="pending") is called explicitly
- THEN: Only pending pets are returned (e.g., Nova)
- AND: Available pets are NOT included

**AC4: No regression in other filters**
- GIVEN: Existing species, tag, and query filters
- WHEN: Combined with status filtering
- THEN: All filters work correctly together
- AND: No existing test cases break

## Requirements

**REQ1:** The status filter in search_pets() must always be applied, never bypassed by falsy values

**REQ2:** Empty status strings must be normalized to "available" before filtering

**REQ3:** The function signature and default parameter `status="available"` remain unchanged for backward compatibility

**REQ4:** Comprehensive test coverage for default, empty, and explicit status values

## Test Scenarios

### Scenario 1: Default search behavior
```python
# No status parameter provided
results = search_pets()
assert all(pet.status == "available" for pet in results)
assert "pet-103" not in [p.id for p in results]  # Nova is pending
```

### Scenario 2: Empty status handling
```python
# Explicitly empty status
results = search_pets(status="")
assert all(pet.status == "available" for pet in results)
assert "pet-103" not in [p.id for p in results]
```

### Scenario 3: Explicit pending search
```python
# Support workflow
results = search_pets(status="pending")
assert all(pet.status == "pending" for pet in results)
assert "pet-103" in [p.id for p in results]  # Nova is pending
```

### Scenario 4: Combined filters
```python
# Species + default status
results = search_pets(species="dog")
assert [p.id for p in results] == ["pet-101"]  # Scout only, not Nova
```

## Out of Scope

- New pet statuses beyond "available" and "pending"
- UI changes or visual indicators
- Adoption flow modifications
- API contract changes beyond the internal fix
