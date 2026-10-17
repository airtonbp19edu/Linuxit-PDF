#!/usr/bin/env python3
"""Check an explicit Flatpak directory grant, without a cloud account or portal claim."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--folder',type=Path,required=True)
parser.add_argument('--expect-denied',action='store_true')
args=parser.parse_args()
sys.path.insert(0,os.environ.get('PRINT_VIEW_TEST_APP','/app/share/linuxit-pdf'))
from local_files import copy_local_document,file_stamp
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader

source=args.folder/'source.pdf';output=args.folder/'copy.pdf'
checks={'inside_flatpak':Path('/.flatpak-info').is_file(),
        'outside_home':not args.folder.resolve().is_relative_to(Path.home().resolve())}
if args.expect_denied:
    try:source.read_bytes();checks['ungranted_directory_is_unreadable']=False
    except (OSError,PermissionError):checks['ungranted_directory_is_unreadable']=True
else:
    raw=source.read_bytes();stamp=file_stamp(source)
    result=copy_local_document(source,{'destination':str(output),'source_stamp':stamp})
    checks.update(complete_copy=output.read_bytes()==raw,original_preserved=source.read_bytes()==raw,
                  pdf_reopens=len(PdfReader(output).pages)==1,
                  only_local_confirmation=result['saved_locally'] and result['remote_sync_confirmed'] is False)
    try:copy_local_document(source,{'destination':str(output),'source_stamp':stamp});checks['existing_copy_preserved']=False
    except FileExistsError:checks['existing_copy_preserved']=output.read_bytes()==raw
report={'schema':'linuxit-synced-folder-grant-v1','expected_denial':args.expect_denied,
        'passed':all(checks.values()),'checks':checks,'real_sync_client_used':False,
        'desktop_portal_interaction_tested':False,'original_foxit_executed':False}
print(json.dumps(report))
raise SystemExit(0 if report['passed'] else 1)
