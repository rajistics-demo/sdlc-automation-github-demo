# Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default search excludes pending pets

#### Scenario: Default search with no status parameter
- Given the catalog contains both available and pending pets
- When a search is performed with default parameters
- Then only pets with status="available" are returned

#### Scenario: Search with empty status string
- Given the catalog contains both available and pending pets  
- When a search is performed with status=""
- Then only pets with status="available" are returned (empty string is treated as default)

#### Scenario: Species filter with default status
- Given the catalog contains dogs with both available and pending status
- When a search is performed for species="dog" without specifying status
- Then only available dogs are returned (pending dogs like Nova are excluded)

### Requirement: Explicit pending search still works

#### Scenario: Support workflow searches for pending pets
- Given the catalog contains pending pets
- When a search is performed with status="pending"
- Then pending pets are returned
- And available pets are excluded

## UNCHANGED Requirements

### Requirement: Other search filters continue to work

- Query name filtering remains unchanged
- Species filtering remains unchanged  
- Tag filtering remains unchanged
- max_results validation remains unchanged
