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


def test_search_pets_filters_empty_status_to_available() -> None:
    """Empty status string should be treated as 'available', not bypass filtering."""
    results = search_pets(status="")

    assert all(pet.status == "available" for pet in results)
    assert "pet-103" not in [pet.id for pet in results]


def test_search_pets_filters_empty_status_with_species() -> None:
    """Empty status with species filter should still exclude pending pets."""
    results = search_pets(species="dog", status="")

    assert [pet.id for pet in results] == ["pet-101"]
    assert all(pet.status == "available" for pet in results)


def test_search_pets_default_status_excludes_pending() -> None:
    """Default call without status parameter should exclude pending pets."""
    results = search_pets()

    assert all(pet.status == "available" for pet in results)
    pet_ids = [pet.id for pet in results]
    assert "pet-103" not in pet_ids
    assert len(pet_ids) == 3
