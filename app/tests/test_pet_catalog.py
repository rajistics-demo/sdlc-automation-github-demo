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


def test_search_pets_excludes_pending_pets_by_default() -> None:
    """Default search should only return available pets, excluding pending."""
    results = search_pets()

    pet_ids = [pet.id for pet in results]
    assert "pet-100" in pet_ids  # Mochi - available
    assert "pet-101" in pet_ids  # Scout - available
    assert "pet-102" in pet_ids  # Pip - available
    assert "pet-103" not in pet_ids  # Nova - pending, should be excluded


def test_search_pets_handles_empty_string_status() -> None:
    """Empty string status should be treated as default 'available'."""
    results = search_pets(status="")

    pet_ids = [pet.id for pet in results]
    assert "pet-100" in pet_ids  # Mochi - available
    assert "pet-101" in pet_ids  # Scout - available
    assert "pet-102" in pet_ids  # Pip - available
    assert "pet-103" not in pet_ids  # Nova - pending, should be excluded


def test_search_pets_with_species_and_empty_status_excludes_pending() -> None:
    """Species filter with empty string status should exclude pending pets."""
    results = search_pets(species="dog", status="")

    assert len(results) == 1
    assert results[0].id == "pet-101"  # Scout - available dog
    assert results[0].name == "Scout"
    # Nova (pet-103) is a pending dog and should not appear

