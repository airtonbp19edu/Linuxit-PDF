#!/usr/bin/env python3
"""Inspect default TLS trust inside an exact installed candidate, without requests."""
import argparse
import json
import os
from pathlib import Path
import subprocess
from check_desktop_integrations import install,REF

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--candidate-manifest',type=Path,required=True)
parser.add_argument('--candidate-bundle',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
if os.environ.get('LINUXIT_EPHEMERAL_DESKTOP')!='1' or args.output.exists():
    parser.error('Explicit ephemeral desktop and a new result path required')
manifest=json.loads(args.candidate_manifest.read_text())
if manifest.get('schema')!='linuxit-linux-candidate-v1':raise ValueError('Unexpected candidate manifest')
installed=install(manifest,args.candidate_bundle)
code=r'''import json, pathlib, re, ssl
context=ssl.create_default_context()
paths=ssl.get_default_verify_paths()
stats=context.cert_store_stats()
directory=pathlib.Path(paths.capath) if paths.capath else None
hashed_entries=bool(directory and directory.is_dir() and any(re.fullmatch(r"[0-9a-fA-F]{8}\\.[0-9]+",p.name) for p in directory.iterdir()))
print(json.dumps(dict(stats=stats,paths=paths._asdict(),check_hostname=context.check_hostname,
 verify_required=context.verify_mode==ssl.CERT_REQUIRED,lazy_hashed_capath=hashed_entries,
 trust_present=stats.get("x509_ca",0)>0 or hashed_entries)))
'''
result=subprocess.run(['flatpak','run','--user','--command=linuxit-python',REF,'-c',code],
                      check=True,capture_output=True,text=True,timeout=45)
observed=json.loads(result.stdout)
passed=observed['trust_present'] and observed['check_hostname'] and observed['verify_required']
report=dict(schema='linuxit-flatpak-tls-trust-v1',passed=passed,observed=observed,installed_version=installed,
    candidate_source_commit=manifest['source_commit'],tested_bundle=manifest['artifact'],network_requests_sent=0,
    scope='Default TLS context and available default CA sources inside the installed candidate; no external TSA acceptance.')
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report));raise SystemExit(0 if passed else 1)
