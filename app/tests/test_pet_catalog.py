import pytest

from petstore_app.catalog import search_pets


def test_search_pets_default_excludes_pending_pets() -> None:
    """Regression test: default search must exclude pending pets like Nova."""
    results = search_pets()

    pet_ids = [pet.id for pet in results]
    assert "pet-103" not in pet_ids, "Nova (pet-103, pending) should not appear in default search"
    assert "pet-100" in pet_ids  # Mochi (available)
    assert "pet-101" in pet_ids  # Scout (available)
    assert "pet-102" in pet_ids  # Pip (available)


def test_search_pets_empty_string_status_defaults_to_available() -> None:
    """Edge case: empty string status should behave like default (available only)."""
    results = search_pets(status="")

    pet_ids = [pet.id for pet in results]
    assert "pet-103" not in pet_ids, "Nova (pending) should not appear when status=''"
    assert len(pet_ids) == 3, "Should return only 3 available pets"


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
