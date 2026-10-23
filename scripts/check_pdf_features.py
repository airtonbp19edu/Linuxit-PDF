#!/usr/bin/env python3
"""Record the bounded four-feature regression set; never certify Foxit parity."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
MODULES=('test_redaction_hidden','test_vector_redaction','test_redaction_apply',
         'test_signature_vri','test_signature_vri_crypto','test_dss_validation','test_signature_preservation',
         'test_form_javascript_api','test_form_javascript','test_form_javascript_security',
         'test_xfa_positioned_formcalc','test_xfa_flow','test_xfa_flow_security','test_pdf_xfa')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--temp-dir',type=Path,required=True)
    parser.add_argument('--portable',action='store_true',help='Exclude suites requiring unavailable Poppler/OpenSSL; not full feature validation')
    args=parser.parse_args()
    if args.output.exists():parser.error('Preserve previous reports; use a new output path.')
    args.temp_dir.mkdir(parents=True,exist_ok=True);tempfile.tempdir=str(args.temp_dir.resolve())
    for key in ('TEMP','TMP','TMPDIR'):os.environ[key]=tempfile.tempdir
    sys.path.insert(0,str(ROOT/'tests'));sys.path.insert(0,str(ROOT/'app'))
    modules=list(MODULES)
    if args.portable:
        modules=[m for m in modules if m not in ('test_signature_vri_crypto','test_dss_validation','test_signature_preservation','test_redaction_apply')]
        modules.extend(('test_signature_preservation.PreservationTests.test_explicit_vri_selection_appends_key_for_full_contents_and_keeps_original_bytes',
                        'test_signature_preservation.PreservationTests.test_unknown_or_duplicate_vri_selection_never_publishes'))
    class Result(unittest.TextTestResult):
        def __init__(self,*a,**kw):super().__init__(*a,**kw);self.cases=[]
        def addSuccess(self,test):self.cases.append(dict(id=test.id(),status='passed'));super().addSuccess(test)
        def addSkip(self,test,reason):self.cases.append(dict(id=test.id(),status='skipped',reason=reason));super().addSkip(test,reason)
        def addError(self,test,err):self.cases.append(dict(id=test.id(),status='error'));super().addError(test,err)
        def addFailure(self,test,err):self.cases.append(dict(id=test.id(),status='failed'));super().addFailure(test,err)
    suite=unittest.defaultTestLoader.loadTestsFromNames(modules)
    result=unittest.TextTestRunner(verbosity=1,resultclass=Result).run(suite)
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    files={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
           for p in (ROOT/'app').glob('*.py')}
    report=dict(schema='linuxit-authorized-pdf-features-v1',observed_utc=datetime.now(timezone.utc).isoformat(),
                head=head,platform=sys.platform,python=sys.version,portable_selection=args.portable,modules=modules,
                run=result.testsRun,passed=sum(c['status']=='passed' for c in result.cases),
                failures=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),
                cases=result.cases,app_sha256=files,foxit_differential_test=False,
                full_feature_validation=not args.portable and result.wasSuccessful() and not result.skipped,
                limitations=['Generated fixtures; no original execution, physical device, legal/LTV or complete XFA/FormCalc/Acrobat API claim.'])
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return 0 if result.wasSuccessful() and result.testsRun else 1


if __name__=='__main__':raise SystemExit(main())
