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
    """Regression test: default search must exclude Nova (pet-103, pending)."""
    results = search_pets()

    pet_ids = [pet.id for pet in results]
    assert "pet-103" not in pet_ids, "Nova (pending pet) must not appear in default search"
    assert "pet-100" in pet_ids
    assert "pet-101" in pet_ids
    assert "pet-102" in pet_ids


def test_species_filter_excludes_pending_pets() -> None:
    """Regression test: species=dog filter must exclude Nova (pet-103, pending)."""
    results = search_pets(species="dog")

    pet_ids = [pet.id for pet in results]
    assert pet_ids == ["pet-101"], "Only Scout (available dog) should be returned"
    assert "pet-103" not in pet_ids, "Nova (pending dog) must be excluded"


def test_searching_for_nova_by_name_returns_empty_when_status_is_default() -> None:
    """Regression test: searching for Nova by name with default status returns empty."""
    results = search_pets(query="nova")

    assert len(results) == 0, "Nova search with default status=available must return empty"
