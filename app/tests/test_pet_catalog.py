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


def test_search_pets_with_empty_status_excludes_pending_pets() -> None:
    """Regression test: empty status string should not bypass the status filter."""
    results = search_pets(status="")

    pet_ids = [pet.id for pet in results]
    assert "pet-103" not in pet_ids, "Nova (pending) should not appear with empty status"
    assert len(results) == 0, "Empty status should match no pets (none have empty status)"


def test_default_search_excludes_pending_pets() -> None:
    """Regression test: default search should exclude pending pets like Nova."""
    results = search_pets()

    pet_ids = [pet.id for pet in results]
    assert "pet-103" not in pet_ids, "Nova (pending) should not appear in default search"
    assert len(results) == 3, "Should return 3 available pets by default"


def test_species_search_with_default_status_excludes_pending_pets() -> None:
    """Regression test: species search with default status excludes pending pets."""
    results = search_pets(species="dog")

    assert len(results) == 1
    assert results[0].id == "pet-101"
    assert results[0].name == "Scout"
