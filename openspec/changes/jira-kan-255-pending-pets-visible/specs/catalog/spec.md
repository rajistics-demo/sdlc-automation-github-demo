# Pet Catalog Availability Spec Delta

## ADDED Requirements

### Requirement: Default catalog search returns only available pets

The default pet search must return only pets with `status="available"`, ensuring customers see only pets ready for adoption.

#### Scenario: Default search excludes pending pets

- **Given** a catalog containing pets with various statuses including "pending"
- **When** a user performs a default search without specifying a status
- **Then** only pets with `status="available"` are returned
- **And** pets with `status="pending"` are excluded from results

#### Scenario: Empty status parameter enforces available-only filter

- **Given** a catalog containing both available and pending pets
- **When** a user performs a search with an empty status parameter (`status=""`)
- **Then** only pets with `status="available"` are returned
- **And** the empty status does not bypass the availability filter

#### Scenario: Whitespace-only status parameter enforces available-only filter

- **Given** a catalog containing both available and pending pets  
- **When** a user performs a search with a whitespace-only status parameter (`status="  "`)
- **Then** only pets with `status="available"` are returned
- **And** the whitespace status does not bypass the availability filter

### Requirement: Operations can explicitly search for pending pets

Support and operations workflows must be able to explicitly search for pending pets when investigating cases.

#### Scenario: Explicit pending status search returns pending pets

- **Given** a catalog containing both available and pending pets
- **When** a user performs a search with `status="pending"`
- **Then** only pets with `status="pending"` are returned
- **And** pets with `status="available"` are excluded from results

## UNCHANGED Requirements

### Requirement: Catalog search filters by species

Pet search continues to support species filtering (e.g., "dog", "cat", "rabbit").

### Requirement: Catalog search filters by tags

Pet search continues to support tag filtering (e.g., "indoor", "active").

### Requirement: Catalog search respects max_results bounds

The `max_results` parameter must remain between 1 and 50.
