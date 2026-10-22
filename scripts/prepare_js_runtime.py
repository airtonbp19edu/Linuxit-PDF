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
import tempfile

VERSION='0.15.1.1'
PINS=Path(__file__).resolve().parents[1]/'docs/proveniencia-quickjs.json'

def download_verified(pin):
    if not pin['url'].startswith('https://files.pythonhosted.org/'):raise ValueError('Invalid package host')
    with urllib.request.urlopen(pin['url'],timeout=60) as reply:data=reply.read(pin['bytes']+1)
    if len(data)!=pin['bytes'] or hashlib.sha256(data).hexdigest()!=pin['sha256']:raise ValueError('Pinned QuickJS digest/size mismatch')
    return data


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target',type=Path,required=True)
    args=parser.parse_args();target=args.target.resolve()
    if target.exists():raise SystemExit('New runtime directory required')
    target.mkdir(parents=True)
    pins=json.loads(PINS.read_text(encoding='utf-8'));source=pins['source'];wheel=pins['linux_x86_64_wheel']
    archive=download_verified(source)
    with tempfile.TemporaryDirectory(prefix='linuxit-js-download-') as folder:
        package=Path(folder)/wheel['url'].rsplit('/',1)[1];package.write_bytes(download_verified(wheel))
        subprocess.run([sys.executable,'-m','pip','install','--disable-pip-version-check','--no-index','--no-deps','--no-compile',
            '--target',str(target),'--report',str(target/'pip-install.json'),str(package)],check=True)
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
        'source_url':source['url'],'source_sha256':source['sha256'],'source_bytes':len(archive),'wheel_sha256':wheel['sha256'],
        'notices_sha256':hashlib.sha256((target/'quickjs-notices.txt').read_bytes()).hexdigest()},indent=2)+'\n')


if __name__=='__main__':main()
