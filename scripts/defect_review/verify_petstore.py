"""Run the Petstore fixture's contract checks after agent review and repair.

These supplied checks are a publication gate, not independent agent discovery.
"""
import argparse
import json
from pathlib import Path
import sys
import unittest

class PetAcceptance(unittest.TestCase):
    def test_default_catalog(self):
        from petstore import search_pets
        self.assertEqual([p['id'] for p in search_pets()], ['pet-100', 'pet-101'])
    def test_explicit_none_catalog(self):
        from petstore import search_pets
        self.assertEqual(search_pets(None), search_pets())
        self.assertTrue(all(p['status'] == 'available' for p in search_pets(None)))
    def test_pending_cannot_be_adopted(self):
        from petstore import create_adoption_order
        with self.assertRaises(ValueError):
            create_adoption_order('pet-102', 'a@example.test')
    def test_negative_donation(self):
        from petstore import create_adoption_order
        with self.assertRaises(ValueError):
            create_adoption_order('pet-100', 'a@example.test', -100)
    def test_integer_money(self):
        from petstore import create_adoption_order
        for value in [True, 1.5, '100', None]:
            with self.subTest(value=value), self.assertRaises((ValueError, TypeError)):
                create_adoption_order('pet-100', 'a@example.test', value)
    def test_preserves_valid_order(self):
        from petstore import create_adoption_order
        self.assertEqual(create_adoption_order('pet-100', 'a@example.test', 100)['total_cents'], 7600)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('repo', type=Path)
    parser.add_argument('--json', type=Path)
    args = parser.parse_args()
    sys.path.insert(0, str(args.repo.resolve()))
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(PetAcceptance)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if args.json:
        args.json.write_text(json.dumps({'tests': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors), 'passed': result.wasSuccessful()}, indent=2))
    sys.exit(0 if result.wasSuccessful() else 1)
