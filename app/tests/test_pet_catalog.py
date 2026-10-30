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
    """Regression test: default search must exclude pending pets like Nova."""
    results = search_pets()
    pet_ids = [pet.id for pet in results]

    assert "pet-103" not in pet_ids, "Nova (pet-103) is pending and must not appear in default search"
    assert "pet-101" in pet_ids, "Scout (pet-101) is available and must appear"


def test_empty_status_excludes_pending_pets() -> None:
    """Regression test: empty status must not bypass the availability filter."""
    results = search_pets(status="")
    pet_ids = [pet.id for pet in results]

    assert "pet-103" not in pet_ids, "Nova (pet-103) is pending and must not appear with empty status"


def test_dog_search_with_default_status_excludes_pending_dogs() -> None:
    """Regression test: species filter must respect default status filter."""
    results = search_pets(species="dog")
    pet_ids = [pet.id for pet in results]

    assert pet_ids == ["pet-101"], "Only Scout (available dog) should appear, not Nova (pending dog)"
