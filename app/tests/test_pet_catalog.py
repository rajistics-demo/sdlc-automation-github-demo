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


def test_search_pets_excludes_pending_by_default() -> None:
    """Regression test for KAN-184: pending pets must not appear in default searches."""
    results = search_pets()
    pet_ids = [pet.id for pet in results]
    
    assert "pet-103" not in pet_ids, "Nova (pet-103) with status='pending' should not appear in default search"
    assert "pet-101" in pet_ids, "Scout (pet-101) with status='available' should appear"


def test_search_pets_default_species_filter_excludes_pending() -> None:
    """Regression test for KAN-184: species filter with default status should exclude pending pets."""
    results = search_pets(species="dog")
    pet_names = [pet.name for pet in results]
    
    assert "Nova" not in pet_names, "Nova (pending) should not appear in dog search with default status"
    assert "Scout" in pet_names, "Scout (available) should appear in dog search"
    assert [pet.id for pet in results] == ["pet-101"], "Only Scout should be returned"

