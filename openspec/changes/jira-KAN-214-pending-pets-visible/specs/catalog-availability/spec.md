# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default pet search must return only available pets

Default catalog searches must exclude pets with any status other than "available", regardless of how the search is invoked.

#### Scenario: Default search excludes pending pets

- Given pets exist with various statuses including "pending"
- When a user searches without specifying a status parameter
- Then only pets with status="available" are returned
- And pending pets are not visible in the results

#### Scenario: Default search with species filter excludes pending pets

- Given a pending pet (Nova, pet-103) exists with species="dog"
- And an available pet (Scout, pet-101) exists with species="dog"
- When a user searches for species="dog" without specifying status
- Then only Scout (pet-101) is returned
- And Nova (pet-103) does not appear

#### Scenario: Empty status parameter defaults to available

- Given the search function receives an empty string for status
- When the search is executed
- Then only pets with status="available" are returned
- And pending pets are excluded

#### Scenario: Explicit pending search remains functional

- Given pending pets exist in the catalog
- When support explicitly searches with status="pending"
- Then pending pets are returned as expected
- And this support workflow is not affected by the fix
