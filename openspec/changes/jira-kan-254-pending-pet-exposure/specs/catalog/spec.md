# Catalog Spec Delta

## ADDED Requirements

### Requirement: Customer-facing UI must not expose pending pet data

#### Scenario: Default catalog view excludes pending pets from client-side data

- Given the customer-facing petstore UI
- When the page loads and pets array is initialized
- Then only pets with status "available" are present in the client-side data structure
- And pending pets are not present in the JavaScript source code

#### Scenario: Pending pet search shows empty state

- Given the customer-facing petstore UI
- When a customer searches for a pending pet by name (e.g., "Nova")
- Then the UI displays "No available pets match this search."
- And no pending pet information is visible or accessible
