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


def test_search_pets_default_excludes_pending_pets() -> None:
    """Regression test: default search must not return pending pets (ACME-6)."""
    results = search_pets()
    
    pet_ids = [pet.id for pet in results]
    assert "pet-103" not in pet_ids, "Nova (pet-103) with status='pending' must not appear in default search"
    assert "pet-100" in pet_ids
    assert "pet-101" in pet_ids
    assert "pet-102" in pet_ids


def test_search_pets_species_filter_excludes_pending_pets() -> None:
    """Regression test: species filter with default status must exclude pending pets (ACME-6)."""
    results = search_pets(species="dog")
    
    assert len(results) == 1, "Only one available dog (Scout)"
    assert results[0].id == "pet-101", "Only Scout (available) should appear, not Nova (pending)"
    assert results[0].name == "Scout"
