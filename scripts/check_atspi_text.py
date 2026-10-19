#!/usr/bin/env python3
"""Cross-process AT-SPI probe of the real Linuxit accessible text widget."""
import argparse,json,os
from pathlib import Path
import subprocess,sys,time

TITLE='Linuxit AT-SPI synthetic probe'
TEXT='Linuxit synthetic accessible text 2026'


def child():
    import gi
    gi.require_version('Atspi','2.0')
    from gi.repository import Atspi
    Atspi.init()
    deadline=time.monotonic()+10
    def visit(node,depth=0,inside=False):
        if node is None or depth>32:return None
        name=node.get_name();inside=inside or name==TITLE
        if inside and name=='Texto extraído da página PDF':
            interface=node.get_text_iface()
            if interface and Atspi.Text.get_text(interface,0,-1)==TEXT:
                return dict(name=name,role=node.get_role_name(),text=TEXT)
        for index in range(min(node.get_child_count(),1000)):
            found=visit(node.get_child_at_index(index),depth+1,inside)
            if found:return found
        return None
    while time.monotonic()<deadline:
        result=visit(Atspi.get_desktop(0))
        if result:print(json.dumps(result));return 0
        time.sleep(.1)
    print(json.dumps(dict(error='Widget/text not found through AT-SPI')));return 1


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--child',action='store_true');parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if args.child:return child()
    if args.output is None or args.output.exists():parser.error('Choose a new output path')
    os.environ.pop('NO_AT_BRIDGE',None);os.environ['GTK_MODULES']='atk-bridge'
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'app'))
    from accessible_reader import AccessibleTextWindow,Gtk
    window=AccessibleTextWindow(None);window.set_title(TITLE);window.text.get_buffer().set_text(TEXT);window.show_all()
    process=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'--child'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    deadline=time.monotonic()+15
    try:
        while process.poll() is None and time.monotonic()<deadline:
            while Gtk.events_pending():Gtk.main_iteration_do(False)
            time.sleep(.01)
        if process.poll() is None:process.kill()
        stdout,stderr=process.communicate(timeout=5)
        try:observation=json.loads(stdout)
        except ValueError:observation=dict(error='No structured AT-SPI observation')
        report=dict(schema='linuxit-atspi-text-v1',passed=process.returncode==0,observed=observation,
                    stderr=stderr[-4000:],cross_process=True,foxit_executed=False,
                    physical_screen_reader_test=False,limitations=['Synthetic widget text; no Orca/physical desktop or complete PDF reading-order acceptance.'])
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(report));return 0 if report['passed'] else 1
    finally:
        if process.poll() is None:process.kill();process.wait()
        window.destroy()


if __name__=='__main__':raise SystemExit(main())
