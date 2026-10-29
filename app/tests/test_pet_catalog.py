import pytest

from petstore_app.catalog import search_pets


def test_search_pets_filters_by_species_and_status() -> None:
    results = search_pets(species="dog")

    assert [pet.id for pet in results] == ["pet-101"]


def test_search_pets_can_find_pending_pets_when_requested() -> None:
    results = search_pets(species="dog", status="pending")

    assert [pet.name for pet in results] == ["Nova"]


def test_search_pets_filters_by_tag() -> None:
    results = search_pets(tag="indoor")

    assert [pet.name for pet in results] == ["Mochi", "Pip"]


@pytest.mark.parametrize("max_results", [0, 51])
def test_search_pets_validates_max_results(max_results: int) -> None:
    with pytest.raises(ValueError, match="max_results"):
        search_pets(max_results=max_results)


def test_search_pets_with_empty_status_string_returns_available_only() -> None:
    """
    Regression test for KAN-186: Empty status string should not bypass the availability filter.
    
    When status="" is passed, it should be treated as a filter value that matches nothing,
    not as a signal to skip filtering. Since no pet has status="", and the filter should
    always be applied, only the default available pets should be returned (not pending pets).
    
    Before fix: Returns all pets including Nova (pet-103, pending)
    After fix: Returns only available pets (pet-100, pet-101, pet-102)
    """
    results = search_pets(status="")
    
    result_ids = [pet.id for pet in results]
    # Should return only available pets, excluding Nova (pet-103) who is pending
    assert result_ids == ["pet-100", "pet-101", "pet-102"]
    
    # Explicitly verify Nova is not in the results
    result_names = [pet.name for pet in results]
    assert "Nova" not in result_names

