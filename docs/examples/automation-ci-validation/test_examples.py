"""Offline example checks only: no credentials, deployment or webhook delivery."""
import ast
import io
import json
from pathlib import Path
import tarfile
import unittest

HERE=Path(__file__).resolve().parent

class ExampleChecks(unittest.TestCase):
    def test_prompt_create_is_inactive_and_event_scoped(self):
        p=json.loads((HERE/'prompt.create.json').read_text())
        self.assertEqual(p['state'],'INACTIVE')
        self.assertIs(p['enabled'],False)
        self.assertEqual(p['trigger']['source'],'github')
        self.assertEqual(p['trigger']['on'],['issues.labeled'])
        self.assertIn('docs-ci-validation-only',p['trigger']['filter'])
        self.assertIn('REPLACE_WITH_APPROVED_COMMIT',p['repos'][0]['ref'])

    def test_prompt_patch_preserves_trigger_and_activation_by_omission(self):
        p=json.loads((HERE/'prompt.patch.json').read_text())
        self.assertEqual(set(p),{'prompt','timeout'})
        self.assertNotIn('repos',p)  # Not accepted by PATCH in the tested 1.19.1 service.

    def test_no_credentials_in_examples(self):
        for name in ['prompt.create.json','prompt.patch.json']:
            p=json.loads((HERE/name).read_text())
            self.assertFalse({'api_key','token','signing_secret','secrets'} & set(p))

    def test_custom_bundle_can_be_packaged_and_read(self):
        source='print("documentation fixture")\n'
        ast.parse(source)
        archive=io.BytesIO()
        with tarfile.open(fileobj=archive,mode='w:gz') as t:
            raw=source.encode(); member=tarfile.TarInfo('main.py')
            member.size=len(raw); member.mtime=0
            t.addfile(member,io.BytesIO(raw))
        with tarfile.open(fileobj=io.BytesIO(archive.getvalue()),mode='r:gz') as t:
            self.assertEqual(t.getnames(),['main.py'])
            self.assertEqual(t.extractfile('main.py').read().decode(),source)

if __name__=='__main__':
    unittest.main(verbosity=2)
