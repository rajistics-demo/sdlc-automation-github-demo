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
    """Regression test: Default search should exclude pending pets like Nova."""
    results = search_pets()

    pet_ids = [pet.id for pet in results]
    assert "pet-103" not in pet_ids, "Nova (pet-103) should not appear in default search"
    assert set(pet_ids) == {"pet-100", "pet-101", "pet-102"}


def test_empty_status_excludes_all_pets() -> None:
    """Regression test: Empty status parameter should not bypass filtering."""
    results = search_pets(status="")

    assert len(results) == 0, "Empty status should return no results"


def test_whitespace_status_excludes_all_pets() -> None:
    """Regression test: Whitespace-only status should not bypass filtering."""
    results = search_pets(status="  ")

    assert len(results) == 0, "Whitespace-only status should return no results"


def test_species_filter_with_default_status_excludes_pending() -> None:
    """Regression test: Species filter should still exclude pending pets by default."""
    results = search_pets(species="dog")

    pet_ids = [pet.id for pet in results]
    assert "pet-103" not in pet_ids, "Nova (pending dog) should not appear in species=dog search"
    assert pet_ids == ["pet-101"], "Only Scout (available dog) should appear"

