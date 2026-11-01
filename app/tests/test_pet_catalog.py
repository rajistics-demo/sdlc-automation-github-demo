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
    """Regression test for KAN-266: default search must exclude pending pets."""
    results = search_pets()

    result_ids = [pet.id for pet in results]
    result_statuses = [pet.status for pet in results]

    assert "pet-103" not in result_ids, "Nova (pet-103) should not appear in default search"
    assert all(status == "available" for status in result_statuses), "All results must have status='available'"
    assert len(results) == 3, "Should return exactly 3 available pets"


def test_species_search_excludes_pending_pets() -> None:
    """Regression test for KAN-266: species search must exclude pending pets."""
    results = search_pets(species="dog")

    result_ids = [pet.id for pet in results]

    assert result_ids == ["pet-101"], "Only Scout should match (Nova is pending)"
    assert "pet-103" not in result_ids, "Nova (pet-103) should not appear in dog species search"


def test_empty_query_search_excludes_pending_pets() -> None:
    """Regression test for KAN-266: empty query search must exclude pending pets."""
    results = search_pets("")

    result_ids = [pet.id for pet in results]
    result_names = [pet.name for pet in results]

    assert "Nova" not in result_names, "Nova should not appear in empty query search"
    assert "pet-103" not in result_ids, "pet-103 should not appear in empty query search"
    assert len(results) == 3, "Should return exactly 3 available pets"
