import importlib.util
from pathlib import Path
import unittest

p = Path(__file__).resolve().parents[1] / "scripts/defect_review/resolve_request.py"
spec = importlib.util.spec_from_file_location("resolve_request", p)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class ReviewRequestTests(unittest.TestCase):
    def event(self, body):
        return {"issue": {"key": "KAN-999", "fields": {"description": body}}}
    def test_repo_and_mode(self):
        result = module.resolve(self.event("Repository: https://github.com/rajistics-demo/petstore-defect-demo\nMode: review-and-repair"))
        self.assertEqual(result["repository"], "rajistics-demo/petstore-defect-demo")
        self.assertEqual(result["mode"], "review-and-repair")
    def test_adf(self):
        result = module.resolve(self.event({"type": "doc", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "https://github.com/rajistics-demo/billing-defect-demo\nMode: review-only"}]}]}))
        self.assertEqual(result["mode"], "review-only")
    def test_unapproved_repo(self):
        with self.assertRaises(ValueError):
            module.resolve(self.event("https://github.com/someone/production\nMode: review-and-repair"))
    def test_missing_mode(self):
        with self.assertRaises(ValueError):
            module.resolve(self.event("https://github.com/rajistics-demo/petstore-defect-demo"))
    def test_ambiguous_repo(self):
        with self.assertRaises(ValueError):
            module.resolve(self.event("https://github.com/rajistics-demo/petstore-defect-demo\nhttps://github.com/rajistics-demo/billing-defect-demo\nMode: review-only"))
    def test_unsafe_ref(self):
        with self.assertRaises(ValueError):
            module.resolve(self.event("https://github.com/rajistics-demo/petstore-defect-demo\nRef: --upload-pack=evil\nMode: review-only"))
