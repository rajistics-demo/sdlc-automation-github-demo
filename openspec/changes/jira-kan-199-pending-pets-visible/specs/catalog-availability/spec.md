# Petstore Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default catalog search excludes unavailable pets

Catalog search MUST exclude pending pets from the default available-pets experience.

#### Scenario: Default available-pets view excludes pending pets

- Given Nova (pet-103) has status `pending`
- And Mochi, Scout, and Pip have status `available`
- When the page loads with no filters applied
- Then Mochi, Scout, and Pip are displayed
- And Nova is not displayed

#### Scenario: Name search for pending pet shows empty state

- Given Nova has status `pending`
- When a customer searches for "Nova" by name
- Then no results are shown
- And the empty state message "No available pets match this search." is displayed

#### Scenario: Species filter excludes pending pets

- Given Scout (dog) has status `available`
- And Nova (dog) has status `pending`
- When a customer filters for species "dog"
- Then Scout is displayed
- And Nova is not displayed

#### Scenario: Explicit pending-pet search still works (backend API)

- Given Nova has status `pending`
- When backend `search_pets(status="pending")` is called
- Then Nova is included in the results
- Note: This is only available through backend API, not default UI

## MODIFIED Requirements

None. The requirement for default available-only search exists but was not being enforced in the UI.

## REMOVED Requirements

None.
