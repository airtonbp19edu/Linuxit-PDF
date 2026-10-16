#!/usr/bin/env python3
"""Run real regression tests and persist counts, failures and skips separately."""
import argparse,json,os,sys,time,unittest
from pathlib import Path
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--app',type=Path,help='Test an extracted runtime payload instead of source app/')
args=parser.parse_args();root=Path(__file__).resolve().parents[1]
if args.output.exists():parser.error('Use a new result path to preserve previous evidence')
if args.app:os.environ['PRINT_VIEW_TEST_APP']=str(args.app.resolve())
class RecordedResult(unittest.TextTestResult):
    def startTest(self,test):self.started=time.monotonic();super().startTest(test)
    def addSuccess(self,test):self.records.append({'id':test.id(),'status':'passed','elapsed_sec':time.monotonic()-self.started});super().addSuccess(test)
    def addError(self,test,err):self.records.append({'id':test.id(),'status':'error'});super().addError(test,err)
    def addFailure(self,test,err):self.records.append({'id':test.id(),'status':'failed'});super().addFailure(test,err)
    def addSkip(self,test,reason):self.records.append({'id':test.id(),'status':'skipped','reason':reason});super().addSkip(test,reason)
    def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self.records=[]
suite=unittest.defaultTestLoader.discover(str(root/'tests'));started=time.monotonic()
result=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(suite)
report={'schema':'linuxit-test-run-v1','tested_app':str((args.app or root/'app').resolve()),'python':sys.version.split()[0],
        'display_present':bool(os.environ.get('DISPLAY')),'run':result.testsRun,'passed':sum(x['status']=='passed' for x in result.records),
        'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),
        'elapsed_sec':time.monotonic()-started,'cases':result.records,
        'foxit_differential_test':False,'limitations':['Tests own application behavior with generated fixtures; no original Foxit execution equivalence is asserted.']}
args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
raise SystemExit(0 if result.wasSuccessful() and result.testsRun else 1)
