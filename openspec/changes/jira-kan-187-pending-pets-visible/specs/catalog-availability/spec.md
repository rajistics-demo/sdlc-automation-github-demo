# Catalog Availability Spec Delta

## VERIFIED Requirements

### Requirement: Default pet search returns only available pets

#### Scenario: Search without status parameter

- Given the catalog contains pets with various status values including "available" and "pending"
- When a customer searches pets without specifying a status parameter
- Then only pets with `status="available"` are returned
- And pets with `status="pending"` are excluded from results

**Current Implementation**: ✅ VERIFIED - `catalog.py` line 31 defaults to `status="available"`

#### Scenario: Frontend catalog display

- Given Nova (pet-103) has `status="pending"`
- When a customer views the available pets in the web UI
- Then Nova does not appear in the results
- And only available pets (Mochi, Scout, Pip) are shown

**Current Implementation**: ✅ VERIFIED - `app.js` line 17 filters to `status === "available"`

### Requirement: Pending pets can be searched explicitly

#### Scenario: Explicit pending status search

- Given Nova (pet-103) has `status="pending"`
- When support staff searches with `status="pending"`
- Then Nova appears in the search results
- And available pets are excluded

**Current Implementation**: ✅ VERIFIED - Backend correctly honors explicit status parameter

### Requirement: Adoption orders validate pet availability

#### Scenario: Attempt to adopt a pending pet

- Given Nova (pet-103) has `status="pending"`
- When someone attempts to create an adoption order for Nova
- Then the system raises ValueError "pet is not available for adoption"
- And no adoption order is created

**Current Implementation**: ✅ VERIFIED - `adoptions.py` line 34-35 validates availability

## ADDED Requirements

### Requirement: Comprehensive validation prevents regressions

#### Scenario: Automated validation of catalog filtering

- Given the catalog implementation and tests
- When validation tests run
- Then default searches must exclude all pending pets
- And explicit pending searches must work correctly
- And frontend filtering must match backend behavior

**Implementation**: Add validation test to ensure coverage remains comprehensive
