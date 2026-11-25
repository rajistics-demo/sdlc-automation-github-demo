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


@pytest.mark.parametrize("tag_input", ["Indoor", "INDOOR", "indoor"])
def test_search_pets_normalizes_tag_case(tag_input: str) -> None:
    results = search_pets(tag=tag_input)

    assert [pet.name for pet in results] == ["Mochi", "Pip"]


@pytest.mark.parametrize("tag_input", [" indoor ", "\tindoor\n"])
def test_search_pets_normalizes_tag_whitespace(tag_input: str) -> None:
    results = search_pets(tag=tag_input)

    assert [pet.name for pet in results] == ["Mochi", "Pip"]


def test_search_pets_max_results_applies_after_tag_filter() -> None:
    results = search_pets(tag="indoor", max_results=1)

    assert len(results) == 1
    assert results[0].name in ["Mochi", "Pip"]
