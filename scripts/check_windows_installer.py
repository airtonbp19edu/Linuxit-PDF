#!/usr/bin/env python3
"""Install/probe/uninstall the candidate exclusively in an ephemeral CI runner."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--installer',required=True,type=Path);parser.add_argument('--stage',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path);args=parser.parse_args()
    if os.name!='nt' or os.environ.get('GITHUB_ACTIONS')!='true' or os.environ.get('RUNNER_OS')!='Windows':
        parser.error('Installation is allowed only on an ephemeral GitHub Windows runner')
    if args.output.exists():parser.error('Use a new report path')
    base=Path(os.environ['RUNNER_TEMP']).resolve()
    target=(base/'linuxit-installer-validation'/'installed app com espaços').resolve()
    if not target.is_relative_to(base) or target.exists():parser.error('Fresh installation inside RUNNER_TEMP required')
    target.parent.mkdir(parents=True,exist_ok=True)
    report=dict(schema='linuxit-windows-installer-validation-v1',passed=False,checks={},errors=[],
                ephemeral_ci=True,host_user_installation=False,administrator_required=False,physical_hardware_tested=False)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    try:
        # NSIS /D must be last and unquoted, including when the directory has
        # spaces. A raw Windows command line is not interpreted by a shell.
        install_command=subprocess.list2cmdline([str(args.installer.resolve()),'/S'])+' /D='+str(target)
        install=subprocess.run(install_command,capture_output=True,timeout=600)
        report['checks']['silent_install_exit_zero']=install.returncode==0
        manifest=json.loads((target/'windows-manifest.json').read_text(encoding='utf-8'))
        mismatches=[]
        for entry in manifest['records']:
            path=target/entry['path']
            if not path.resolve().is_relative_to(target) or not path.is_file() or path.stat().st_size!=entry['bytes']:
                mismatches.append(entry['path']);continue
            with path.open('rb') as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
            if digest!=entry['sha256']:mismatches.append(entry['path'])
        report['payload_mismatches']=mismatches
        report['checks']['installed_bytes_equal_payload']=not mismatches
        environment=os.environ.copy()
        environment['PATH']=str(Path(os.environ['SYSTEMROOT'])/'System32')+os.pathsep+os.environ['SYSTEMROOT']
        environment['XDG_CONFIG_HOME']=str(base/'linuxit-installed-config')
        environment['XDG_CACHE_HOME']=str(base/'linuxit-installed-cache')
        for key in ('PYTHONPATH','PYTHONHOME','GI_TYPELIB_PATH','GSETTINGS_SCHEMA_DIR','GDK_PIXBUF_MODULE_FILE','GST_PLUGIN_PATH'):
            environment.pop(key,None)
        probe=args.output.with_name('installed-probe.json').resolve()
        checked=subprocess.run([str(target/'runtime/bin/python.exe'),'-B','-I',str(target/'windows_bootstrap.py'),'--probe',str(probe)],
                               env=environment,cwd=str(base),capture_output=True,timeout=120)
        report['probe_stderr']=checked.stderr.decode('utf-8','replace')[-4000:]
        report['checks']['installed_native_probe']=checked.returncode==0 and probe.exists() and json.loads(probe.read_text(encoding='utf-8'))['passed']
        launcher_probe=args.output.with_name('installed-launcher-probe.json').resolve()
        launched=subprocess.run([str(target/'LinuxitPDF.exe'),'--probe',str(launcher_probe)],env=environment,cwd=str(base),capture_output=True,timeout=30)
        deadline=time.monotonic()+90
        launcher_result={}
        while time.monotonic()<deadline:
            try:launcher_result=json.loads(launcher_probe.read_text(encoding='utf-8'));break
            except (FileNotFoundError,json.JSONDecodeError):time.sleep(.2)
        report['checks']['installed_exe_launcher']=launched.returncode==0 and launcher_result.get('passed') is True
        import winreg
        key=r'Software\Microsoft\Windows\CurrentVersion\Uninstall\LinuxitPDF-'+manifest['version']
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,key) as registry:
            location,_=winreg.QueryValueEx(registry,'InstallLocation')
        report['checks']['per_user_uninstall_registered']=Path(location).resolve()==target
        # Prove the uninstaller removes only its own inventory, not unrelated
        # files later created by a user in the installation directory.
        retained=target/'user-created-preserve.txt';retained.write_text('keep',encoding='utf-8')
        uninstall=subprocess.run([str(target/'uninstall.exe'),'/S'],capture_output=True,timeout=120)
        deadline=time.monotonic()+90
        # The default NSIS uninstaller runs a temporary child. Its manifest can
        # disappear early; the registry key is removed by its final instruction.
        while time.monotonic()<deadline:
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER,key):pass
            except FileNotFoundError:break
            time.sleep(.2)
        remaining=[entry['path'] for entry in manifest['records'] if (target/entry['path']).exists()]
        report['remaining_owned_files']=remaining
        report['checks']['uninstaller_removes_owned_files']=uninstall.returncode==0 and not remaining
        report['checks']['uninstaller_preserves_foreign_files']=retained.read_text(encoding='utf-8')=='keep'
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,key):pass
            removed=False
        except FileNotFoundError:removed=True
        report['checks']['uninstall_registry_removed']=removed
        report['passed']=all(report['checks'].values()) and len(report['checks'])==8
    except Exception as exc:
        import traceback
        report['errors'].append(type(exc).__name__+': '+str(exc));traceback.print_exc()
    args.output.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report));return 0 if report['passed'] else 1


if __name__=='__main__':raise SystemExit(main())
