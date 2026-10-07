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


def test_search_pets_with_empty_status_excludes_pending() -> None:
    """Regression test for KAN-189: empty status should not bypass filter."""
    results = search_pets(species="dog", status="")
    pet_ids = [pet.id for pet in results]
    
    # Nova (pet-103) is pending and should not appear with empty status
    assert "pet-103" not in pet_ids, "Pending pet Nova should not appear with empty status"
    # Scout (pet-101) is available but won't match empty status either
    assert len(pet_ids) == 0, "Empty status should not match any pets"
