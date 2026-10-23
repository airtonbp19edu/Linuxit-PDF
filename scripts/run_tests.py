#!/usr/bin/env python3
"""Run real regression tests and persist counts, failures and skips separately."""
import argparse,json,os,sys,tempfile,time,unittest
from pathlib import Path
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--app',type=Path,help='Test an extracted runtime payload instead of source app/')
parser.add_argument('--pattern',default='test*.py',help='unittest filename pattern; a subset is not the full suite')
parser.add_argument('--temp-dir',type=Path,help='Writable parent for isolated temporary test directories')
parser.add_argument('--traceback-after',type=int,default=0,help='Optional diagnostic stack dump interval in seconds')
parser.add_argument('--progress-output',type=Path,help='Optional atomic partial checkpoint; never an approval report')
args=parser.parse_args();root=Path(__file__).resolve().parents[1]
if args.traceback_after:
    import faulthandler
    faulthandler.dump_traceback_later(max(1,args.traceback_after),repeat=True)
if args.output.exists():parser.error('Use a new result path to preserve previous evidence')
if args.app:os.environ['PRINT_VIEW_TEST_APP']=str(args.app.resolve())
# No modal system dialog can be answered during a test run.
os.environ['LINUXIT_NONINTERACTIVE']='1'
if args.temp_dir:
    args.temp_dir.mkdir(parents=True,exist_ok=True)
    tempfile.tempdir=str(args.temp_dir.resolve())
    # Nested workers must use the same explicitly writable test area.
    for name in ('TMPDIR','TEMP','TMP'):os.environ[name]=tempfile.tempdir
class RecordedResult(unittest.TextTestResult):
    def progress(self,active=None):
        if args.progress_output is None:return
        data={'schema':'linuxit-test-progress-v1','complete':False,'active_test':active,
              'completed_records':len(self.records),'cases':self.records,'updated_at_epoch':time.time(),
              'approval_report':False,'final_report_expected':str(args.output)}
        args.progress_output.parent.mkdir(parents=True,exist_ok=True)
        pending=args.progress_output.with_name(args.progress_output.name+'.pending')
        pending.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');os.replace(pending,args.progress_output)
    def startTest(self,test):self.started=time.monotonic();super().startTest(test);self.progress(test.id())
    def addSuccess(self,test):self.records.append({'id':test.id(),'status':'passed','elapsed_sec':time.monotonic()-self.started});super().addSuccess(test);self.progress()
    def addError(self,test,err):self.records.append({'id':test.id(),'status':'error'});super().addError(test,err);self.progress()
    def addFailure(self,test,err):self.records.append({'id':test.id(),'status':'failed'});super().addFailure(test,err);self.progress()
    def addSkip(self,test,reason):self.records.append({'id':test.id(),'status':'skipped','reason':reason});super().addSkip(test,reason);self.progress()
    def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self.records=[]
suite=unittest.defaultTestLoader.discover(str(root/'tests'),pattern=args.pattern);started=time.monotonic()
result=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(suite)
if args.traceback_after:faulthandler.cancel_dump_traceback_later()
report={'schema':'linuxit-test-run-v1','tested_app':str((args.app or root/'app').resolve()),'python':sys.version.split()[0],
        'test_pattern':args.pattern,'full_suite_requested':args.pattern=='test*.py',
        'display_present':bool(os.environ.get('DISPLAY')),'run':result.testsRun,'passed':sum(x['status']=='passed' for x in result.records),
        'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),
        'elapsed_sec':time.monotonic()-started,'cases':result.records,
        'foxit_differential_test':False,'limitations':['Tests own application behavior with generated fixtures; no original Foxit execution equivalence is asserted.']}
args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
raise SystemExit(0 if result.wasSuccessful() and result.testsRun else 1)
