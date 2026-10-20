#!/usr/bin/env python3
"""Manual E29 probe: create only disposable drafts, then remove owned drafts.

Never creates Git refs, publishes releases, uploads assets, or persists tokens.
Only the three run-specific draft IDs in this receipt may be removed.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import time
import urllib.error
import urllib.request

REPOSITORY = 'airtonbp19edu/Linuxit-PDF'
OLD = 'dec46c979e56d722482a465563c6df97b898dcdc'
HEADERS = ('X-Accepted-GitHub-Permissions', 'X-GitHub-Request-Id',
           'X-RateLimit-Remaining', 'X-RateLimit-Reset')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt', type=Path, required=True)
    parser.add_argument('--cleanup-only', action='store_true')
    args = parser.parse_args()
    assert os.environ.get('GITHUB_REPOSITORY') == REPOSITORY
    run = os.environ['GITHUB_RUN_ID']
    attempt = os.environ['GITHUB_RUN_ATTEMPT']
    assert run.isdigit() and attempt.isdigit()
    prefix = f'diag-403-{run}-{attempt}-'
    token = os.environ['GH_TOKEN']
    base = f'https://api.github.com/repos/{REPOSITORY}'

    def request(path, method='GET', payload=None):
        assert path.startswith('/')
        req = urllib.request.Request(base + path, method=method,
            data=json.dumps(payload).encode() if payload is not None else None,
            headers={'Authorization': 'Bearer ' + token,
                     'Accept': 'application/vnd.github+json',
                     'X-GitHub-Api-Version': '2022-11-28',
                     'Content-Type': 'application/json', 'User-Agent': 'Linuxit-E29'})
        try:
            response = urllib.request.urlopen(req, timeout=30)
        except urllib.error.HTTPError as exc:
            response = exc
        with response:
            raw = response.read()
            return {'status': response.code,
                    'headers': {k: response.headers.get(k) for k in HEADERS},
                    'body': json.loads(raw) if raw else None}

    def save():
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')

    def published_snapshot():
        # All pages, so a new public release cannot be hidden by truncation.
        records = []
        for page in range(1, 100):
            res = request(f'/releases?per_page=100&page={page}')
            assert res['status'] == 200, res
            for release in res['body']:
                if not release['draft']:
                    records.append({k: release[k] for k in
                        ('id', 'tag_name', 'target_commitish', 'published_at')}
                        | {'assets': [{k: a.get(k) for k in ('id', 'name', 'size', 'digest')}
                                      for a in release['assets']]})
            if len(res['body']) < 100:
                return records
        raise RuntimeError('Pagination limit exceeded')

    def cleanup():
        failures = []
        for case in data['cases']:
            if not case.get('created_id') or case.get('deleted'):
                continue
            release_id = case['created_id']
            assert isinstance(release_id, int)
            for retry in range(3):
                current = request(f'/releases/{release_id}')
                if current['status'] == 404:
                    case['deleted'] = True
                    break
                body = current['body']
                if not (current['status'] == 200 and body['draft'] is True
                        and body['tag_name'] == case['tag_name']
                        and case['tag_name'].startswith(prefix)):
                    failures.append({'id': release_id, 'reason': 'ownership/draft guard'})
                    break
                case['delete_response'] = request(f'/releases/{release_id}', 'DELETE')
                if case['delete_response']['status'] == 204:
                    case['deleted'] = True
                    break
                time.sleep(1 + retry)
            if not case.get('deleted') and not any(f['id'] == release_id for f in failures):
                failures.append({'id': release_id, 'reason': 'delete failed'})
            save()
        data['cleanup_failures'] = failures
        save()
        if failures:
            raise RuntimeError('Owned diagnostic drafts need cleanup; see receipt')

    if args.cleanup_only:
        if not args.receipt.exists():
            return
        data = json.loads(args.receipt.read_text(encoding='utf-8'))
        assert data['prefix'] == prefix
        cleanup()
        return

    assert not args.receipt.exists(), 'New receipt required'
    data = {'schema': 'linuxit-e29-probe-v1', 'prefix': prefix,
            'started_at_utc': datetime.now(timezone.utc).isoformat(),
            'run_id': run, 'run_attempt': attempt, 'workflow_sha': os.environ['GITHUB_SHA'],
            'cases': [], 'permission_profile': 'contents:write, metadata:read'}
    data['published_before'] = published_snapshot()
    head = request('/git/ref/heads/main')
    assert head['status'] == 200
    sha = head['body']['object']['sha']
    assert re.fullmatch('[0-9a-f]{40}', sha)
    data['main_sha'] = sha
    save()
    try:
        for index, target in enumerate((None, sha, OLD), 1):
            tag = prefix + str(index)
            assert request('/git/ref/tags/' + tag)['status'] == 404
            case = {'tag_name': tag, 'target_commitish': target}
            data['cases'].append(case)
            save()
            payload = {'tag_name': tag, 'name': tag, 'draft': True,
                       'prerelease': True, 'body': 'E29 disposable permission probe; never publish.'}
            if target:
                payload['target_commitish'] = target
            result = request('/releases', 'POST', payload)
            case['response'] = result
            if result['status'] == 201:
                assert result['body']['draft'] is True
                case['created_id'] = result['body']['id']
            save()
            print(json.dumps({'case': index, 'target': target, 'status': result['status'],
                              'message': (result['body'] or {}).get('message')}), flush=True)
            cleanup()
            case['tag_after_status'] = request('/git/ref/tags/' + tag)['status']
            assert case['tag_after_status'] == 404, 'Draft unexpectedly created a Git ref'
            save()
    finally:
        cleanup()
        data['published_after'] = published_snapshot()
        data['published_unchanged'] = data['published_before'] == data['published_after']
        data['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
        save()
    assert data['published_unchanged'], 'Published release inventory changed during probe'


if __name__ == '__main__':
    main()
