# Catalog Spec Delta

## ADDED Requirements

### Requirement: Default search must exclude pending pets

The default pet search with `status="available"` must not return pets that have `status="pending"`.

#### Scenario: Default search with species filter excludes pending pets

- Given a catalog containing both available and pending pets of the same species
- When a customer searches for pets by species without explicitly requesting pending status
- Then only pets with `status="available"` are returned

#### Scenario: Explicit pending search continues to work

- Given a catalog containing pets with various statuses
- When support explicitly searches for `status="pending"`
- Then only pets with `status="pending"` are returned

#### Scenario: Default search without filters excludes all pending pets

- Given a catalog containing both available and pending pets
- When a customer performs a default search
- Then no pets with `status="pending"` appear in results
