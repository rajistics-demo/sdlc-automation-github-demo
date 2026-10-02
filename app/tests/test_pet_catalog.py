import pytest

from petstore_app.catalog import search_pets


def test_default_search_excludes_pending_pets() -> None:
    """Regression test for KAN-194: Default search must exclude pending pets."""
    results = search_pets()

    assert all(pet.status == "available" for pet in results)
    assert "pet-103" not in [p.id for p in results]  # Nova is pending


def test_empty_status_defaults_to_available() -> None:
    """Empty status string should be normalized to 'available'."""
    results = search_pets(status="")

    assert all(pet.status == "available" for pet in results)
    assert "pet-103" not in [p.id for p in results]  # Nova is pending


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
