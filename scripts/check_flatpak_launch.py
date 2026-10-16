#!/usr/bin/env python3
"""Check the installed Flatpak launcher on a virtual X11 display; capture own fixture UI."""
import os,subprocess,time,json,re,signal
from pathlib import Path
import gi
gi.require_version('Gdk','3.0');gi.require_version('GdkX11','3.0')
from gi.repository import Gdk,GdkX11
repo=Path(__file__).resolve().parents[1];out=Path(os.environ.get('LINUXIT_LAUNCH_RESULTS',repo/'testes/resultados'));out.mkdir(parents=True,exist_ok=True);fixture=repo/'testes/fixtures/busca-escopos.pdf'
command=['dbus-run-session','--','flatpak','run','--user','--filesystem='+str(fixture.parent)+':ro','io.github.airtonbp19edu.LinuxitPDF//devel',str(fixture)]
checks={};image_path=out/'linuxit-flatpak-0.1.0.png'
with (out/'normal-launch.log').open('wb') as log:
 proc=subprocess.Popen(command,stdout=log,stderr=log,start_new_session=True)
 try:
  until=time.monotonic()+15;window_id=None
  while time.monotonic()<until:
   tree=subprocess.check_output(['xwininfo','-display',os.environ.get('DISPLAY',':101'),'-root','-tree'],text=True)
   line=next((v for v in tree.splitlines() if 'busca-escopos.pdf' in v and 'Linuxit PDF' in v),None)
   if line:window_id=int(re.search(r'0x[0-9a-f]+',line).group(),16);break
   if proc.poll() is not None:raise RuntimeError('Application exited '+str(proc.returncode))
   time.sleep(.1)
  if window_id is None:raise RuntimeError('Expected document window did not appear')
  time.sleep(1)
  window=GdkX11.X11Window.foreign_new_for_display(Gdk.Display.get_default(),window_id)
  pixbuf=Gdk.pixbuf_get_from_window(window,0,0,window.get_width(),window.get_height())
  if pixbuf is None:raise RuntimeError('No rendered window pixels')
  pixbuf.savev(str(image_path),'png',[],[])
  checks={'expected_document_window':True,'captured_window_pixels':True,'normal_flatpak_command':True}
 finally:
  if proc.poll() is None:os.killpg(proc.pid,signal.SIGTERM)
  proc.wait(timeout=10)
(out/'flatpak-normal-launch.json').write_text(json.dumps({'passed':all(checks.values()) and len(checks)==3,'checks':checks,'extra_access':'Read-only own synthetic fixture directory','screenshot':'linuxit-flatpak-0.1.0.png','foxit_differential_test':False},indent=2)+'\n')
print(json.dumps(checks))
