# Catalog Availability Specification Delta

## MODIFIED Requirements

### Requirement: Default pet search returns only available pets

The default `search_pets()` behavior and explicit empty string status must both return only available pets.

#### Scenario: Default search excludes pending pets

```python
results = search_pets()
assert "Nova" not in [pet.name for pet in results]
assert all(pet.status == "available" for pet in results)
```

#### Scenario: Explicit empty string status excludes pending pets

```python
results = search_pets(status="")
assert "Nova" not in [pet.name for pet in results]
assert all(pet.status == "available" for pet in results)
```

#### Scenario: Explicit pending status includes pending pets

```python
results = search_pets(status="pending")
assert "Nova" in [pet.name for pet in results]
assert all(pet.status == "pending" for pet in results)
```

#### Scenario: Species filter with default status excludes pending

```python
results = search_pets(species="dog")
assert results == [Scout]  # Only the available dog
assert "Nova" not in [pet.name for pet in results]
```

### Requirement: Nova (pet-103) must not appear in default search

#### Scenario: Customer available-pets search excludes Nova

- GIVEN Nova has `id="pet-103"` and `status="pending"`
- WHEN customers perform a default available-pets search
- THEN Nova does not appear in the results
- AND no `PENDING_PET_VISIBLE` error is logged

## Changed Behavior

**Before:** Calling `search_pets(status="")` would return ALL pets regardless of status, including pending pets.

**After:** Calling `search_pets(status="")` returns only available pets, matching the default behavior.

## No Change Required

- Web UI filtering logic (already correct in `app/web/app.js`)
- Explicit status filtering for pending, adopted, or other statuses
- Species, tag, query, and max_results filtering logic
