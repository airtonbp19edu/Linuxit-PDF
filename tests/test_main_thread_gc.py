"""E27: GTK objects in reference cycles must never be finalized by a worker thread."""
import json,os,subprocess,sys,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];APP=Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'));sys.path.insert(0,str(APP))
import main_thread_gc

SCENARIO=r'''
import gc,json,sys,threading,time
sys.path.insert(0,sys.argv[1])
import gi
gi.require_version('Gtk','3.0')
from gi.repository import GLib,Gtk
import main_thread_gc
if sys.argv[2]=='install':main_thread_gc.install(GLib)
finalized=[]
gc.collect()
class Holder:pass
holder=Holder();holder.label=Gtk.Label(label='ciclo');holder.label.cycle=holder   # wrapper <-> holder cycle
holder.label.weak_ref(lambda:finalized.append(threading.current_thread().name))
del holder
def churn():
    junk=[]
    for index in range(200000):
        item=[];item.append(item);junk.append(item)   # cyclic garbage crosses the gc thresholds
        if len(junk)>500:junk.clear()
worker=threading.Thread(target=churn,name='worker');worker.start();worker.join()
after_worker=list(finalized)
deadline=time.monotonic()+5
context=GLib.MainContext.default()
while not finalized and time.monotonic()<deadline:
    context.iteration(False);time.sleep(.01)
print(json.dumps({'after_worker':after_worker,'finalized':finalized,'gc_enabled':gc.isenabled()}))
'''


def scenario(mode):
    process=subprocess.run([sys.executable,'-c',SCENARIO,str(APP),mode],capture_output=True,text=True,timeout=60,
                           env={**os.environ,'PYTHONUTF8':'1'})
    if process.returncode:raise AssertionError(process.stderr[-2000:])
    return json.loads(process.stdout.strip().splitlines()[-1])


class GenerationPolicyTests(unittest.TestCase):
    def test_collects_the_oldest_generation_that_is_due(self):
        for counts,expected in (((10,0,0),None),((700,0,0),0),((700,10,0),1),((700,10,10),2),((699,99,99),None)):
            with self.subTest(counts=counts),patch('gc.get_count',return_value=counts),patch('gc.get_threshold',return_value=(700,10,10)):
                self.assertEqual(main_thread_gc._generation(),expected)

    def test_disabled_thresholds_never_collect(self):
        with patch('gc.get_count',return_value=(10**6,99,99)),patch('gc.get_threshold',return_value=(0,10,10)):
            self.assertIsNone(main_thread_gc._generation())


@unittest.skipUnless(os.environ.get('DISPLAY'),'Requires GTK3 and a display')
class MainThreadCollectionTests(unittest.TestCase):
    def test_without_install_a_worker_thread_finalizes_the_widget(self):
        # Documents the hazard the module removes: automatic GC runs in the worker.
        result=scenario('default')
        self.assertTrue(result['gc_enabled']);self.assertEqual(result['after_worker'],['worker'])

    def test_installed_collection_finalizes_the_widget_on_the_main_thread(self):
        result=scenario('install')
        self.assertFalse(result['gc_enabled']);self.assertEqual(result['after_worker'],[])
        self.assertEqual(result['finalized'],['MainThread'])

    def test_window_installs_main_thread_collection(self):
        from main import PDFWindow,Gtk
        with patch.object(Gtk,'main_quit'):
            window=PDFWindow()
            try:self.assertTrue(main_thread_gc.installed())
            finally:window.destroy()


if __name__=='__main__':unittest.main()
