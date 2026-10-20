"""Release identity and permission guards, independent from GTK/Flatpak."""
import unittest
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location('release_preflight',
    Path(__file__).resolve().parents[1] / 'scripts' / 'release_preflight.py')
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
release_plan = _module.release_plan


class ReleasePreflightTests(unittest.TestCase):
    def setUp(self):
        self.commit = 'a' * 40
        self.main = 'b' * 40
        self.manifest = {'version': '0.1.17', 'source_commit': self.commit,
            'distribution': {'tag': 'v0.1.17-devel'},
            'artifact': {'file': 'LinuxitPDF-0.1.17-x86_64.flatpak', 'bytes': 123, 'sha256': 'c' * 64}}
        self.ref = None
        self.releases = []
        self.different_workflows = True

    def api(self, path):
        if path == '':
            return 200, {'default_branch': 'main'}
        if path == '/git/ref/heads/main':
            return 200, {'object': {'sha': self.main}}
        if path.startswith('/git/ref/tags/'):
            return (200, self.ref) if self.ref else (404, {})
        if path.startswith('/releases?'):
            return 200, self.releases
        if path == '/git/tags/annotated':
            return 200, {'object': {'type': 'commit', 'sha': self.commit}}
        if path.startswith('/git/trees/'):
            sha = path.rsplit('/', 1)[1]
            if sha in (self.commit, self.main):
                return 200, {'tree': [{'path': '.github', 'type': 'tree', 'sha': sha + '-github'}]}
            if sha.endswith('-github'):
                workflow_sha = ('new-workflows' if sha.startswith(self.main) and self.different_workflows
                                else 'tested-workflows')
                return 200, {'tree': [{'path': 'workflows', 'type': 'tree', 'sha': workflow_sha}]}
        self.fail('Unexpected read-only API request: ' + path)

    def release(self, draft=False):
        return {'id': 10, 'tag_name': 'v0.1.17-devel', 'draft': draft, 'prerelease': True,
                'target_commitish': self.commit,
                'assets': [{'name': self.manifest['artifact']['file'], 'size': 123,
                            'state': 'uploaded', 'digest': 'sha256:' + 'c' * 64}]}

    def test_changed_workflows_require_owner_without_retargeting(self):
        plan = release_plan(self.manifest, self.api)
        self.assertEqual(plan['mode'], 'owner_draft_required')
        self.assertEqual(plan['source_commit'], self.commit)

    def test_identical_workflows_allow_candidate_even_after_app_commits(self):
        self.different_workflows = False
        self.assertEqual(release_plan(self.manifest, self.api)['mode'], 'create_release')

    def test_published_matching_asset_and_annotated_tag_are_noop(self):
        self.ref = {'object': {'type': 'tag', 'sha': 'annotated'}}
        self.releases = [self.release()]
        self.assertEqual(release_plan(self.manifest, self.api)['mode'], 'already_published')

    def test_wrong_tag_refuses_even_when_asset_matches(self):
        self.ref = {'object': {'type': 'commit', 'sha': self.main}}
        self.releases = [self.release()]
        with self.assertRaisesRegex(AssertionError, 'untested commit'):
            release_plan(self.manifest, self.api)

    def test_wrong_published_bytes_refuse_replacement(self):
        self.ref = {'object': {'type': 'commit', 'sha': self.commit}}
        self.releases = [self.release()]
        self.releases[0]['assets'][0]['digest'] = 'sha256:' + 'd' * 64
        with self.assertRaisesRegex(AssertionError, 'differs'):
            release_plan(self.manifest, self.api)

    def test_owner_draft_accepts_upload_but_never_auto_publication(self):
        self.releases = [self.release(draft=True)]
        self.releases[0]['assets'] = []
        self.assertEqual(release_plan(self.manifest, self.api)['mode'], 'upload_draft')
        self.releases[0]['assets'] = self.release()['assets']
        self.assertEqual(release_plan(self.manifest, self.api)['mode'], 'draft_ready')

    def test_draft_with_wrong_target_refuses_upload(self):
        self.releases = [self.release(draft=True)]
        self.releases[0]['target_commitish'] = 'main'
        with self.assertRaisesRegex(AssertionError, 'explicitly pin'):
            release_plan(self.manifest, self.api)

    def test_api_permission_error_fails_closed(self):
        with self.assertRaisesRegex(AssertionError, 'HTTP 403'):
            release_plan(self.manifest, lambda path: (403, {}))


if __name__ == '__main__':
    unittest.main()
