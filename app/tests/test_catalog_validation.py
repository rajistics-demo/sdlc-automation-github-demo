"""
Comprehensive validation test for catalog availability requirements.

This test serves as:
1. Regression prevention - ensures pending pets stay out of default searches
2. Documentation - codifies product requirements from AGENTS.md and wiki docs
3. Confidence builder - proves current behavior matches business rules

Related to Jira KAN-187: Customers are seeing pets that are not available
"""

from __future__ import annotations

import pytest

from petstore_app.adoptions import create_adoption_order
from petstore_app.catalog import search_pets, PETS


class TestCatalogAvailabilityValidation:
    """Validates that catalog availability rules prevent pending pets from appearing in default searches."""

    def test_default_search_excludes_all_pending_pets(self) -> None:
        """Default pet search must return only available pets, excluding all pending pets."""
        # Given: Catalog contains both available and pending pets
        all_pets = list(PETS)
        available_pets = [pet for pet in all_pets if pet.status == "available"]
        pending_pets = [pet for pet in all_pets if pet.status == "pending"]
        
        # Sanity check: Ensure we have test data for both statuses
        assert len(available_pets) > 0, "Test requires at least one available pet"
        assert len(pending_pets) > 0, "Test requires at least one pending pet"
        
        # When: Searching without status parameter (uses default)
        results = search_pets()
        
        # Then: Only available pets are returned
        result_ids = {pet.id for pet in results}
        available_ids = {pet.id for pet in available_pets}
        pending_ids = {pet.id for pet in pending_pets}
        
        assert result_ids == available_ids, (
            f"Default search must return only available pets. "
            f"Expected {available_ids}, got {result_ids}"
        )
        
        # And: No pending pets appear in results
        assert result_ids.isdisjoint(pending_ids), (
            f"Default search must not include pending pets. "
            f"Found pending pets: {result_ids & pending_ids}"
        )

    def test_nova_specifically_excluded_from_default_search(self) -> None:
        """Nova (pet-103) must not appear in default search results.
        
        This is the specific case mentioned in logs/pending-pet-visible.ndjson
        and relates to Jira KAN-187.
        """
        # Given: Nova is pet-103 with status="pending"
        nova = next((pet for pet in PETS if pet.id == "pet-103"), None)
        assert nova is not None, "Nova (pet-103) must exist in test data"
        assert nova.name == "Nova", f"pet-103 should be Nova, got {nova.name}"
        assert nova.status == "pending", f"Nova should be pending, got {nova.status}"
        
        # When: Performing default search
        results = search_pets()
        
        # Then: Nova does not appear
        result_ids = [pet.id for pet in results]
        assert "pet-103" not in result_ids, (
            "Nova (pet-103) must not appear in default search results"
        )
        
        # When: Searching for dogs without status (uses default "available")
        dog_results = search_pets(species="dog")
        
        # Then: Nova does not appear in dog results
        dog_ids = [pet.id for pet in dog_results]
        assert "pet-103" not in dog_ids, (
            "Nova (pet-103) must not appear in species-filtered default search"
        )

    def test_pending_pets_searchable_when_explicitly_requested(self) -> None:
        """Support staff must be able to search pending pets by explicitly requesting status="pending"."""
        # Given: Catalog contains pending pets
        pending_pets = [pet for pet in PETS if pet.status == "pending"]
        assert len(pending_pets) > 0, "Test requires at least one pending pet"
        
        # When: Explicitly searching for pending pets
        results = search_pets(status="pending")
        
        # Then: Pending pets are returned
        result_ids = {pet.id for pet in results}
        pending_ids = {pet.id for pet in pending_pets}
        assert result_ids == pending_ids, (
            f"Explicit pending search must return all pending pets. "
            f"Expected {pending_ids}, got {result_ids}"
        )

    def test_adoption_validation_blocks_pending_pets(self) -> None:
        """Adoption orders cannot be created for pending pets."""
        # Given: Nova (pet-103) is pending
        nova = next((pet for pet in PETS if pet.id == "pet-103"), None)
        assert nova is not None and nova.status == "pending"
        
        # When: Attempting to create an adoption order for Nova
        # Then: System raises ValueError
        with pytest.raises(ValueError, match="pet is not available for adoption"):
            create_adoption_order(
                pet_id="pet-103",
                adopter_email="customer@example.com"
            )

    def test_frontend_data_consistency(self) -> None:
        """Verify frontend pet data matches backend and Nova is marked as pending.
        
        This test documents the expectation that app.js should filter out pending pets.
        Actual frontend testing requires Playwright or similar browser automation.
        """
        # Given: Nova in backend catalog
        nova = next((pet for pet in PETS if pet.id == "pet-103"), None)
        assert nova is not None
        assert nova.name == "Nova"
        assert nova.status == "pending"
        
        # Note: Frontend (app.js line 17) must filter to pet.status === "available"
        # This ensures Nova won't appear even if the data includes her
        # Frontend tests are in app/web/tests/catalog-search.playwright.mjs

    def test_catalog_availability_acceptance_criteria(self) -> None:
        """End-to-end validation of all acceptance criteria from spec.md"""
        # AC1: Default search returns only available pets
        default_results = search_pets()
        assert all(pet.status == "available" for pet in default_results), (
            "All default search results must have status='available'"
        )
        
        # AC2: Pending pets excluded from default search
        default_ids = {pet.id for pet in default_results}
        pending_ids = {pet.id for pet in PETS if pet.status == "pending"}
        assert default_ids.isdisjoint(pending_ids), (
            "Default search must not include any pending pets"
        )
        
        # AC3: Explicit pending search works
        pending_results = search_pets(status="pending")
        assert all(pet.status == "pending" for pet in pending_results), (
            "Explicit pending search must return only pending pets"
        )
        
        # AC4: Nova specifically excluded from defaults
        assert "pet-103" not in default_ids, "Nova must not appear in default search"
        
        # AC5: Nova searchable when explicitly requesting pending
        pending_result_ids = {pet.id for pet in pending_results}
        assert "pet-103" in pending_result_ids, (
            "Nova must appear in explicit pending search"
        )
        
        # AC6: Adoption validation prevents pending pet orders
        with pytest.raises(ValueError, match="pet is not available for adoption"):
            create_adoption_order(pet_id="pet-103", adopter_email="test@example.com")
