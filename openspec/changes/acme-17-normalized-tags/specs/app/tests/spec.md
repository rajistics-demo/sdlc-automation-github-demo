# Pet Catalog Tag Search Spec Delta

## ADDED Requirements

### Requirement: Mixed-case tag inputs must match lowercase pet tags

#### Scenario: User searches with mixed-case tag

- Given a pet with tag `"indoor"`
- When searching with `tag="Indoor"`, `tag="INDOOR"`, or `tag="InDoOr"`
- Then all searches return the same pets (Mochi, Pip)

### Requirement: Tag inputs with whitespace must be normalized

#### Scenario: User searches with whitespace around tag

- Given a pet with tag `"indoor"`
- When searching with `tag=" indoor "` or `tag="\tindoor\n"`
- Then both searches return the same pets as `tag="indoor"`

### Requirement: max_results limit applies after tag filtering

#### Scenario: User applies both tag filter and result limit

- Given a tag filter that matches 2 pets (`tag="indoor"`)
- When `max_results=1` is specified
- Then exactly 1 pet is returned
- And the result is from the filtered set (Mochi or Pip)
