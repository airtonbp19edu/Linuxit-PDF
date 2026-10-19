#!/usr/bin/env python3
"""Ephemeral own Flatpak: persistent document grant, association, upgrade/rollback."""
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile,time,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
APP='io.github.airtonbp19edu.LinuxitPDF';REF=APP+'//devel'


def run(arguments,check=True,timeout=60):
    return subprocess.run(arguments,check=check,capture_output=True,text=True,timeout=timeout)


def inside(path):
    code='from pathlib import Path;import hashlib,sys;print(hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest())'
    return run(['flatpak','run','--user','--nofilesystem=host','--nofilesystem=home','--command=linuxit-python',REF,'-c',code,str(path)],check=False,timeout=30)


def install(manifest):
    from delivery_bundle import resolve_bundle
    artifact=manifest['artifact'];bundle=resolve_bundle(ROOT,manifest,download=True)
    if bundle.stat().st_size!=artifact['bytes'] or hashlib.sha256(bundle.read_bytes()).hexdigest()!=artifact['sha256']:
        raise ValueError('Published bundle identity does not match examined metadata')
    run(['flatpak','install','--user','--noninteractive','--reinstall','-y','--no-related',str(bundle)],timeout=120)
    code='import sys;sys.path.insert(0,"/app/share/linuxit-pdf");from version import VERSION;print(VERSION)'
    actual=run(['flatpak','run','--user','--command=linuxit-python',REF,'-c',code]).stdout.strip()
    if actual!=manifest['version']:raise ValueError('Installed own version differs')
    return actual


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True,type=Path);args=parser.parse_args()
    if args.output.exists() or os.environ.get('LINUXIT_EPHEMERAL_DESKTOP')!='1':parser.error('New output and explicit ephemeral CI desktop required')
    report=dict(schema='linuxit-desktop-integrations-v1',passed=False,checks={},errors=[],foxit_executed=False,physical_desktop=False)
    server=None;doc_id=None;window_instances=set();old_default=None
    args.output.parent.mkdir(parents=True,exist_ok=True)
    sys.path.insert(0,str(ROOT/'app'))
    from pdf_dependency import configure_pdf_library
    configure_pdf_library();from pypdf import PdfWriter
    os.environ['XDG_DATA_DIRS']=str(Path.home()/'.local/share/flatpak/exports/share')+':/var/lib/flatpak/exports/share:'+os.environ.get('XDG_DATA_DIRS','/usr/local/share:/usr/share')
    from gi.repository import Gio,GLib
    connection=Gio.bus_get_sync(Gio.BusType.SESSION,None)
    BUS='org.freedesktop.portal.Documents';OBJECT='/org/freedesktop/portal/documents'
    def call(method,parameters=None):return connection.call_sync(BUS,OBJECT,BUS,method,parameters,None,Gio.DBusCallFlags.NONE,10000,None).unpack()
    log=args.output.with_suffix('.portal.log').open('wb')
    def start_portal():
        executable=next((str(p) for p in [Path('/usr/libexec/xdg-document-portal'),Path('/usr/lib/xdg-document-portal')] if p.is_file()),None)
        if not executable:raise RuntimeError('Document portal executable missing')
        process=subprocess.Popen([executable,'--replace'],stdout=log,stderr=log)
        deadline=time.monotonic()+10
        while time.monotonic()<deadline:
            if process.poll() is not None:raise RuntimeError('Own document portal exited during startup')
            owned=connection.call_sync('org.freedesktop.DBus','/org/freedesktop/DBus','org.freedesktop.DBus','NameHasOwner',GLib.Variant('(s)',(BUS,)),None,Gio.DBusCallFlags.NONE,2000,None).unpack()[0]
            if owned:return process
            time.sleep(.1)
        process.terminate();process.wait(timeout=5);raise RuntimeError('Own portal did not acquire its private bus name')
    def instances():
        result=run(['flatpak','ps','--columns=instance,application'],check=False)
        return {row.split()[0] for row in result.stdout.splitlines() if len(row.split())==2 and row.split()[1]==APP}
    try:
        manifest=json.loads((ROOT/'releases/manifest.json').read_text())
        old=json.loads((ROOT/'testes/resultados/0.1.14/candidate.json').read_text())
        sentinel=Path.home()/'.var/app'/APP/'config'/('linuxit-rollback-'+uuid.uuid4().hex+'.txt');sentinel.parent.mkdir(parents=True,exist_ok=True);sentinel.write_text('preserve own synthetic preferences')
        try:
            versions=[install(old),install(manifest),install(old),install(manifest)]
            report['checks']['actual_upgrade_rollback_and_upgrade']=versions==[old['version'],manifest['version'],old['version'],manifest['version']]
            report['checks']['synthetic_preferences_survive_update']=sentinel.read_text()=='preserve own synthetic preferences'
            report['tested_versions']=versions
        finally:sentinel.unlink(missing_ok=True)
        with tempfile.TemporaryDirectory(prefix='linuxit-desktop-',dir=ROOT/'analysis-local') as directory:
            root=Path(directory);source=root/'portal.pdf';writer=PdfWriter();writer.add_blank_page(100,100);writer.write(source)
            digest=hashlib.sha256(source.read_bytes()).hexdigest()
            report['checks']['outside_home_denied_before_grant']=inside(source).returncode!=0
            server=start_portal()
            descriptor=os.open(source,os.O_PATH|os.O_CLOEXEC)
            try:
                descriptors=Gio.UnixFDList.new();number=descriptors.append(descriptor)
                result,_=connection.call_with_unix_fd_list_sync(BUS,OBJECT,BUS,'AddFull',GLib.Variant('(ahusas)',([number],3,APP,['read'])),None,Gio.DBusCallFlags.NONE,10000,descriptors,None)
                doc_ids,extra=result.unpack();doc_id=doc_ids[0]
            finally:os.close(descriptor)
            mount=bytes(call('GetMountPoint')[0]).rstrip(b'\0').decode()
            # Flatpak maps the host's document mount into its canonical runtime
            # directory even when the ephemeral host XDG_RUNTIME_DIR is in /tmp.
            portal_path=Path('/run/user')/str(os.getuid())/'doc'/doc_id/source.name
            check=inside(portal_path);report['checks']['granted_document_reads_expected_bytes']=check.returncode==0 and check.stdout.strip()==digest
            report['grant_probe']=dict(host_mount=mount,app_path=str(portal_path),returncode=check.returncode,stderr=check.stderr[-1500:])
            server.terminate();server.wait(timeout=10);server=None;time.sleep(.2)
            server=start_portal()
            check=inside(portal_path);report['checks']['persistent_grant_survives_portal_restart']=check.returncode==0 and check.stdout.strip()==digest
            report['restart_probe']=dict(returncode=check.returncode,stderr=check.stderr[-1500:])
            call('RevokePermissions',GLib.Variant('(ssas)',(doc_id,APP,['read'])))
            report['checks']['revoked_grant_denies_new_app_process']=inside(portal_path).returncode!=0
            report['checks']['portal_never_changes_source']=hashlib.sha256(source.read_bytes()).hexdigest()==digest
        desktop=Path.home()/'.local/share/flatpak/exports/share/applications'/(APP+'.desktop')
        application=Gio.DesktopAppInfo.new_from_filename(str(desktop))
        if application is None:raise RuntimeError('Installed desktop entry missing')
        old_default=Gio.AppInfo.get_default_for_type('application/pdf',False)
        application.set_as_default_for_type('application/pdf')
        selected=None;deadline=time.monotonic()+5
        while time.monotonic()<deadline:
            while GLib.MainContext.default().pending():GLib.MainContext.default().iteration(False)
            selected=Gio.AppInfo.get_default_for_type('application/pdf',False)
            if selected:break
            time.sleep(.1)
        report['checks']['pdf_association_points_to_installed_app']=selected is not None and selected.get_id()==application.get_id()
        if selected is None:raise RuntimeError('Installed PDF association is not discoverable through the desktop data directories')
        with tempfile.TemporaryDirectory(prefix='linuxit-association-',dir=Path.home()) as directory:
            source=Path(directory)/'association-fixture.pdf';writer=PdfWriter();writer.add_blank_page(100,100);writer.write(source)
            before=instances();Gio.AppInfo.launch_default_for_uri(source.as_uri(),None)
            deadline=time.monotonic()+20;found=False
            while time.monotonic()<deadline:
                window_instances|=instances()-before
                windows=run(['xdotool','search','--onlyvisible','--name','association-fixture.pdf.*Linuxit PDF'],check=False,timeout=3)
                if windows.returncode==0:found=True;break
                time.sleep(.2)
            report['checks']['associated_launch_opens_expected_reader_document']=found and bool(window_instances)
        report['tested_bundle']=manifest['artifact'];report['passed']=len(report['checks'])==9 and all(report['checks'].values())
    except Exception as exc:
        import traceback
        report['errors'].append(type(exc).__name__+': '+str(exc));traceback.print_exc()
    finally:
        for instance in window_instances:run(['flatpak','kill',instance],check=False,timeout=10)
        if old_default is not None:old_default.set_as_default_for_type('application/pdf')
        if doc_id:
            try:call('Delete',GLib.Variant('(s)',(doc_id,)))
            except Exception:pass
        if server is not None:
            server.terminate()
            try:server.wait(timeout=10)
            except subprocess.TimeoutExpired:server.kill();server.wait(timeout=5)
        log.close()
    args.output.write_bytes((json.dumps(report,indent=2)+'\n').encode());print(json.dumps(report));return 0 if report['passed'] else 1


if __name__=='__main__':raise SystemExit(main())
