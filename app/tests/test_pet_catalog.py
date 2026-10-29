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


def test_search_pets_empty_status_defaults_to_available() -> None:
    """Regression test for KAN-253: empty status string should default to available."""
    results = search_pets(status="")

    # Should return only available pets, not pending ones
    assert len(results) == 3
    assert [pet.id for pet in results] == ["pet-100", "pet-101", "pet-102"]
    # Nova (pet-103) with status="pending" should not be in results
    assert "pet-103" not in [pet.id for pet in results]


def test_search_pets_whitespace_status_defaults_to_available() -> None:
    """Regression test for KAN-253: whitespace-only status should default to available."""
    results = search_pets(status="   ")

    # Should return only available pets
    assert len(results) == 3
    assert [pet.id for pet in results] == ["pet-100", "pet-101", "pet-102"]


def test_search_pets_explicit_pending_still_works() -> None:
    """Verify explicit pending status search continues to work for operations."""
    results = search_pets(status="pending")

    # Should return only Nova (pet-103)
    assert len(results) == 1
    assert results[0].id == "pet-103"
    assert results[0].name == "Nova"
