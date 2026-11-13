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


def test_default_search_excludes_pending_pets() -> None:
    """Default search should only return available pets, not pending ones."""
    results = search_pets()

    assert len(results) == 3
    assert all(pet.status == "available" for pet in results)
    assert "Nova" not in [pet.name for pet in results]


def test_empty_status_excludes_pending_pets() -> None:
    """Empty status string should behave like default and exclude pending pets."""
    results = search_pets(status="")

    assert len(results) == 3
    assert all(pet.status == "available" for pet in results)
    assert "Nova" not in [pet.name for pet in results]


def test_species_filter_with_default_status_excludes_pending_pets() -> None:
    """Species search with default status should exclude pending pets."""
    results = search_pets(species="dog")

    assert len(results) == 1
    assert results[0].name == "Scout"
    assert results[0].status == "available"
    assert "Nova" not in [pet.name for pet in results]
