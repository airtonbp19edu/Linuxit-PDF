#!/usr/bin/env python3
"""Ephemeral Linux desktop: native chooser, actual portal call and selected PDF."""
import argparse,json,os
from pathlib import Path
import subprocess,sys,tempfile,time


def child():
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'app'))
    from folder_dialogs import choose_pdf_native,Gtk
    parent=Gtk.Window(title='Linuxit portal test parent');parent.show_all()
    try:
        result=choose_pdf_native(parent)
        print('LINUXIT_PORTAL_RESULT '+json.dumps(dict(path=result)),flush=True)
    finally:parent.destroy()


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--child',action='store_true')
    parser.add_argument('--output',type=Path);args=parser.parse_args()
    if args.child:child();return 0
    if args.output is None or args.output.exists():parser.error('Use a new output')
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'app'))
    from pdf_dependency import configure_pdf_library
    configure_pdf_library();from pypdf import PdfWriter
    with tempfile.TemporaryDirectory(prefix='linuxit-portal-test-') as directory:
        root=Path(directory);source=root/'portal-fixture.pdf';writer=PdfWriter();writer.add_blank_page(200,200);writer.write(source)
        env={**os.environ,'GTK_USE_PORTAL':'1','G_DBUS_DEBUG':'message','XDG_CURRENT_DESKTOP':'GNOME'}
        subprocess.run(['dbus-update-activation-environment','DISPLAY','XAUTHORITY','XDG_CURRENT_DESKTOP'],check=True,env=env,timeout=10)
        log=root/'portal-client.log'
        with log.open('wb') as output:
            process=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'--child'],stdout=output,stderr=subprocess.STDOUT,env=env)
            observed_window=None;deadline=time.monotonic()+20
            try:
                while time.monotonic()<deadline and process.poll() is None:
                    probe=subprocess.run(['xdotool','search','--onlyvisible','--name','^Abrir PDF pelo seletor do sistema$'],capture_output=True,text=True,timeout=3)
                    matches=probe.stdout.splitlines()
                    if matches:
                        observed_window=matches[-1];break
                    time.sleep(.1)
                if observed_window:
                    subprocess.run(['xdotool','windowactivate','--sync',observed_window],check=True,timeout=5)
                    subprocess.run(['xdotool','key','--clearmodifiers','ctrl+l'],check=True,timeout=5)
                    subprocess.run(['xdotool','type','--clearmodifiers','--',str(source)],check=True,timeout=5)
                    subprocess.run(['xdotool','key','--clearmodifiers','Return'],check=True,timeout=5)
                    try:process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        subprocess.run(['xdotool','key','--clearmodifiers','Return'],check=True,timeout=5)
                        process.wait(timeout=5)
            except (subprocess.SubprocessError,OSError):pass
            finally:
                if process.poll() is None:process.kill();process.wait()
        raw=log.read_text(errors='replace');line=next((line for line in raw.splitlines() if line.startswith('LINUXIT_PORTAL_RESULT ')),None)
        result=json.loads(line.partition(' ')[2]) if line else {}
        call='org.freedesktop.portal.FileChooser' in raw and 'OpenFile' in raw
        response='org.freedesktop.portal.Request' in raw and 'Response' in raw
        report=dict(schema='linuxit-native-portal-v1',passed=process.returncode==0 and result.get('path')==str(source) and call and response,
                    native_chooser_used=True,portal_open_file_observed=call,portal_response_observed=response,
                    selected_expected_synthetic_pdf=result.get('path')==str(source),window_seen=observed_window is not None,
                    client_returncode=process.returncode,foxit_executed=False,flatpak_test=False,
                    limitations=['Ephemeral X11 desktop portal; no physical desktop/persistent Flatpak permission acceptance.'])
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
        args.output.with_suffix('.log').write_text(raw)
        print(json.dumps(report));return 0 if report['passed'] else 1


if __name__=='__main__':raise SystemExit(main())
