# Petstore Catalog Spec Delta

## ADDED Requirements

### Requirement: Default catalog search excludes unavailable pets

Catalog search MUST exclude pending pets from the default available-pets experience.

#### Scenario: Default search with no status parameter excludes pending pets

- Given Nova (pet-103) has status `pending`
- And Mochi, Scout, and Pip have status `available`
- When catalog search is called with no status parameter
- Then only Mochi, Scout, and Pip are returned
- And Nova is not included in the results

#### Scenario: Empty status parameter behaves as default

- Given Nova (pet-103) has status `pending`
- When catalog search is called with `status=""`
- Then only available pets are returned
- And Nova is not included in the results

#### Scenario: Explicit pending search still works for support workflows

- Given Nova (pet-103) has status `pending`
- When catalog search is called with `status="pending"`
- Then Nova is included in the results
- And available pets are excluded

#### Scenario: Available species search excludes pending pets of same species

- Given Scout is an available dog and Nova is a pending dog
- When catalog search is called for `species="dog"` with default status
- Then Scout is included and Nova is excluded
