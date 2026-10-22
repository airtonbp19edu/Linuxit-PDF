#!/usr/bin/env python3
"""Install the pinned MIT QuickJS binding and retain complete source notices."""
import argparse
import hashlib
from io import BytesIO
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import urllib.request
import re

VERSION='0.15.1.1'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target',type=Path,required=True)
    args=parser.parse_args();target=args.target.resolve()
    if target.exists():raise SystemExit('New runtime directory required')
    target.mkdir(parents=True)
    subprocess.run([sys.executable,'-m','pip','install','--disable-pip-version-check','--no-deps',
        '--target',str(target),'--report',str(target/'pip-install.json'),f'python-quickjs-ng=={VERSION}'],check=True)
    with urllib.request.urlopen(f'https://pypi.org/pypi/python-quickjs-ng/{VERSION}/json',timeout=45) as reply:
        metadata=json.load(reply)
    source=next(row for row in metadata['urls'] if row['packagetype']=='sdist')
    assert source['url'].startswith('https://files.pythonhosted.org/') and source['size']<20*1024**2
    with urllib.request.urlopen(source['url'],timeout=60) as reply:archive=reply.read(20*1024**2+1)
    assert len(archive)==source['size'] and hashlib.sha256(archive).hexdigest()==source['digests']['sha256']
    notices=[]
    with tarfile.open(fileobj=BytesIO(archive),mode='r:gz') as source_tar:
        for member in source_tar.getmembers():
            if member.isfile() and Path(member.name).name.upper() in ('LICENSE','LICENSE.TXT','COPYING'):
                assert member.size<1024**2
                notices.append(member.name+'\n'+source_tar.extractfile(member).read().decode('utf-8'))
            elif member.isfile() and member.name.endswith(('.c','.h')):
                head=source_tar.extractfile(member).read(32768).decode('utf-8',errors='replace')
                comment=re.match(r'\s*(/\*.*?\*/)',head,re.S)
                if comment and 'copyright' in comment[1].lower():
                    notices.append(member.name+'\n'+comment[1])
    assert notices and any('Bellard' in n for n in notices), 'QuickJS engine notice missing'
    (target/'quickjs-notices.txt').write_text('\n\n'.join(notices),encoding='utf-8')
    (target/'quickjs-provenance.json').write_text(json.dumps({'name':'python-quickjs-ng','version':VERSION,
        'source_url':source['url'],'source_sha256':source['digests']['sha256'],'source_bytes':len(archive),
        'notices_sha256':hashlib.sha256((target/'quickjs-notices.txt').read_bytes()).hexdigest()},indent=2)+'\n')


if __name__=='__main__':main()
