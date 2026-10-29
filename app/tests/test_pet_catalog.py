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


def test_search_pets_default_excludes_pending() -> None:
    """Default search should return only available pets, excluding pending ones."""
    results = search_pets()

    pet_ids = [pet.id for pet in results]
    assert "pet-103" not in pet_ids, "Nova (pending) should not appear in default search"
    assert "pet-101" in pet_ids, "Scout (available) should appear in default search"


def test_search_pets_empty_status_does_not_bypass_filter() -> None:
    """Empty status string should not bypass the status filter."""
    results = search_pets(status="")

    pet_ids = [pet.id for pet in results]
    assert len(pet_ids) == 0, "Empty status should not match any pets"


def test_search_pets_excludes_nova_from_default() -> None:
    """Nova (pet-103) with pending status should be excluded from available searches."""
    results_default = search_pets()
    results_available = search_pets(status="available")

    names_default = [pet.name for pet in results_default]
    names_available = [pet.name for pet in results_available]

    assert "Nova" not in names_default, "Nova should not appear in default search"
    assert "Nova" not in names_available, "Nova should not appear in available search"

    results_pending = search_pets(status="pending")
    names_pending = [pet.name for pet in results_pending]
    assert "Nova" in names_pending, "Nova should appear when explicitly searching for pending pets"
