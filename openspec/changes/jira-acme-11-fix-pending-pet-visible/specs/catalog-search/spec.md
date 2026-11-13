# Catalog Search Spec Delta

## ADDED Requirements

### Requirement: Default catalog search returns only available pets

When a customer searches the pet catalog without specifying a status or with an empty status value, the system must return only pets with status="available".

#### Scenario: Empty status string excludes pending pets

- Given a catalog with both available and pending pets
- When a search is performed with status=""
- Then only available pets are returned
- And pending pets are excluded

#### Scenario: Default search excludes pending pets

- Given a catalog with both available and pending pets
- When a search is performed without specifying a status parameter
- Then only available pets are returned
- And pending pets are excluded

#### Scenario: Species search with default status excludes pending pets

- Given a catalog with available and pending dogs
- When a search is performed with species="dog" and default status
- Then only available dogs are returned
- And pending dogs are excluded

## PRESERVED Requirements

### Requirement: Explicit pending status search still works

Support and operations must be able to search for pending pets explicitly.

#### Scenario: Explicit pending status returns pending pets

- Given a catalog with both available and pending pets
- When a search is performed with status="pending"
- Then only pending pets are returned
- And available pets are excluded
