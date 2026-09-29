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
    """Regression test: default search must not show pending pets.
    
    This validates the fix for KAN-198 where customers were seeing
    pets that should not be available yet (e.g., Nova/pet-103).
    """
    results = search_pets()
    
    result_ids = [pet.id for pet in results]
    assert "pet-103" not in result_ids, "Nova (pending pet) should not appear in default search"
    
    result_statuses = {pet.status for pet in results}
    assert result_statuses == {"available"}, "Default search should only return available pets"


def test_species_filter_excludes_pending_pets() -> None:
    """Regression test: species filtering must still respect status=available default.
    
    Even when filtering by species, pending pets should not appear unless
    explicitly requested with status='pending'.
    """
    results = search_pets(species="dog")
    
    assert len(results) == 1, "Should find exactly one available dog"
    assert results[0].name == "Scout", "Should find Scout, not Nova (pending)"
    assert results[0].status == "available"
