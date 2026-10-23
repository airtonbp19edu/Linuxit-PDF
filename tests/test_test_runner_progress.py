"""The checkpoint survives an abruptly terminated test, without approving it."""
import json,os,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class TestRunnerProgressTests(unittest.TestCase):
    def execute(self,body):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);root=Path(temp.name)
        (root/'scripts').mkdir();(root/'tests').mkdir()
        shutil.copy2(ROOT/'scripts/run_tests.py',root/'scripts/run_tests.py')
        (root/'tests/test_probe.py').write_text('import unittest,os\nclass Probe(unittest.TestCase):\n    def test_a(self):self.assertTrue(True)\n    def test_b(self):'+body+'\n',encoding='utf-8')
        final=root/'final.json';progress=root/'progress.json'
        process=subprocess.run([sys.executable,str(root/'scripts/run_tests.py'),'--output',str(final),'--progress-output',str(progress),'--temp-dir',str(root/'temp')],capture_output=True,timeout=30)
        return process,final,json.loads(progress.read_text())
    def test_abrupt_exit_keeps_completed_case_and_active_test_without_approval(self):
        process,final,progress=self.execute('os._exit(3)')
        self.assertEqual(process.returncode,3);self.assertFalse(final.exists())
        self.assertEqual(progress['schema'],'linuxit-test-progress-v1');self.assertFalse(progress['complete']);self.assertFalse(progress['approval_report'])
        self.assertEqual(progress['completed_records'],1);self.assertEqual(progress['cases'][0]['status'],'passed');self.assertTrue(progress['active_test'].endswith('.test_b'))
    def test_success_retains_normal_final_report_and_distinct_partial_schema(self):
        process,final,progress=self.execute('self.assertTrue(True)')
        self.assertEqual(process.returncode,0);report=json.loads(final.read_text())
        self.assertEqual(report['schema'],'linuxit-test-run-v1');self.assertEqual(report['run'],report['passed']);self.assertEqual(report['run'],2)
        self.assertEqual(progress['completed_records'],2);self.assertFalse(progress['approval_report'])
