#!/usr/bin/env python3
"""Read-only release plan; never retarget a tested candidate to bypass permissions."""
import argparse
import json
import os
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request

REPOSITORY = 'airtonbp19edu/Linuxit-PDF'


def release_plan(manifest, get):
    commit = manifest['source_commit']
    tag = manifest['distribution']['tag']
    artifact = manifest['artifact']
    assert re.fullmatch(r'[0-9a-f]{40}', commit), 'Candidate must pin a full commit'
    assert tag == f"v{manifest['version']}-devel" and re.fullmatch(r'v\d+\.\d+\.\d+-devel', tag)
    assert Path(artifact['file']).name == artifact['file']
    assert re.fullmatch('[0-9a-f]{64}', artifact['sha256']) and artifact['bytes'] > 0

    def optional(path):
        status, data = get(path)
        if status == 404:
            return None
        assert status == 200, f'GET {path}: HTTP {status}'
        return data

    def required(path):
        status, data = get(path)
        assert status == 200, f'GET {path}: HTTP {status}'
        return data

    reference = optional('/git/ref/tags/' + tag)
    if reference:
        obj = reference['object']
        for _ in range(8):
            if obj['type'] == 'commit':
                break
            assert obj['type'] == 'tag', 'Tag is neither a commit nor annotated tag'
            obj = required('/git/tags/' + obj['sha'])['object']
        assert obj['type'] == 'commit' and obj['sha'] == commit, 'Existing tag points at an untested commit'

    # Include drafts visible to the job token; paginate rather than guessing first 30.
    matches = []
    for page in range(1, 101):
        releases = required(f'/releases?per_page=100&page={page}')
        matches.extend(r for r in releases if r['tag_name'] == tag)
        if len(releases) < 100:
            break
    else:
        raise ValueError('Release pagination limit exceeded')
    assert len(matches) <= 1, 'Multiple releases use the candidate tag; owner review required'
    plan = {'tag': tag, 'source_commit': commit, 'release_id': '', 'existing_tag': bool(reference)}
    if matches:
        release = matches[0]
        assets = [a for a in release['assets'] if a['name'] == artifact['file']]
        assert len(assets) <= 1, 'Duplicate asset names'
        if assets:
            asset = assets[0]
            assert (asset['state'] == 'uploaded' and asset['size'] == artifact['bytes']
                    and asset.get('digest') == 'sha256:' + artifact['sha256']), 'Existing asset differs from tested bytes'
        plan['release_id'] = release['id']
        if release['draft']:
            assert release['target_commitish'] == commit, 'Draft must explicitly pin the tested commit'
            plan['mode'] = 'draft_ready' if assets else 'upload_draft'
        else:
            assert reference and assets and release['prerelease'], 'Published release is incomplete or not a development release'
            plan['mode'] = 'already_published'
        return plan

    repo = required('')
    default_branch = urllib.parse.quote(repo['default_branch'], safe='')
    main_sha = required('/git/ref/heads/' + default_branch)['object']['sha']

    def workflow_tree(sha):
        for part in ('.github', 'workflows'):
            tree = required('/git/trees/' + sha)
            assert not tree.get('truncated'), 'Git tree response truncated'
            entries = [e for e in tree['tree'] if e['path'] == part]
            if not entries:
                return None
            assert len(entries) == 1 and entries[0]['type'] == 'tree', 'Workflows path is not a directory'
            sha = entries[0]['sha']
        return sha

    plan.update(default_branch=repo['default_branch'], default_commit=main_sha,
                target_workflow_tree=workflow_tree(commit), default_workflow_tree=workflow_tree(main_sha))
    plan['mode'] = ('create_release' if plan['target_workflow_tree'] == plan['default_workflow_tree']
                    else 'owner_draft_required')
    return plan


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert os.environ.get('GITHUB_REPOSITORY') == REPOSITORY
    token = os.environ['GH_TOKEN']

    def get(path):
        req = urllib.request.Request('https://api.github.com/repos/' + REPOSITORY + path,
            headers={'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json',
                     'X-GitHub-Api-Version': '2022-11-28', 'User-Agent': 'Linuxit-release-preflight'})
        try:
            response = urllib.request.urlopen(req, timeout=30)
        except urllib.error.HTTPError as exc:
            response = exc
        with response:
            return response.code, json.load(response)

    plan = release_plan(json.loads(args.manifest.read_text(encoding='utf-8')), get)
    args.output.write_text(json.dumps(plan, indent=2) + '\n', encoding='utf-8')
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as out:
            for key in ('mode', 'release_id'):
                out.write(f'{key}={plan[key]}\n')
    message = {
        'already_published': 'Release já publicada; tag e asset conferem. Nenhuma alteração necessária.',
        'draft_ready': 'Rascunho já contém o pacote correto. O dono deve publicá-lo pela página Releases.',
        'upload_draft': 'Rascunho do dono confere; somente anexar o pacote testado.',
        'create_release': 'Workflows do candidato e da branch padrão coincidem; publicação automática elegível.',
        'owner_draft_required': 'Ação do dono necessária: criar rascunho com tag e SHA testados. GITHUB_TOKEN não pode criar a release nesse commit porque os workflows diferem da branch padrão. Não houve publicação.'
    }[plan['mode']]
    print('::notice::' + message)
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a', encoding='utf-8') as out:
            out.write(f"### Plano de publicação: `{plan['mode']}`\n\n{message}\n\n"
                      f"Tag: `{plan['tag']}`; commit testado: `{plan['source_commit']}`.\n")


if __name__ == '__main__':
    main()
