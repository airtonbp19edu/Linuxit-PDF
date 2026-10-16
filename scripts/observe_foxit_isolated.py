#!/usr/bin/env python3
"""Attempt a bounded offline observation; proprietary output remains local."""
import argparse, hashlib, json, os, shlex, shutil, subprocess, time
from pathlib import Path

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--reference',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--display',default=':101')
parser.add_argument('--timeout',type=int,default=30)
parser.add_argument('--zlib-root',type=Path,help='Verified libz-mingw-w64 package extraction')
parser.add_argument('--diagnose-imports',action='store_true')
parser.add_argument('--diagnose-startup',action='store_true',help='Retain Wine loader, process and exception diagnostics locally')
parser.add_argument('--diagnose-emulator',action='store_true',help='Retain QEMU system-call diagnostics locally')
parser.add_argument('--prefill-wine32','--prefill-wow64',dest='prefill_wow64',action='store_true',help='Populate a fresh prefix with the verified local Wine x86 builtins')
parser.add_argument('--qemu-root',type=Path,help='Verified local qemu-user extraction for an emulated WOW64 probe')
parser.add_argument('--wine32-root',type=Path,help='Verified Wine/i386 runtime; requires qemu-root')
parser.add_argument('--probe-cmd',choices=['x64','x86'],help='Exercise a Wine builtin command for the selected architecture')
parser.add_argument('--probe-wine',action='store_true',help='Run only Wine --version in exactly the same containment')
args=parser.parse_args()
if sum((args.probe_wine, bool(args.probe_cmd)))>1:parser.error('Select only one runtime probe')
if not 1 <= args.timeout <= 300:parser.error('Timeout must be between 1 and 300 seconds')
if args.wine32_root and not args.qemu_root:parser.error('wine32-root requires qemu-root')
if args.wine32_root and args.probe_cmd=='x64':parser.error('A win32 prefix cannot be used for an x64 probe')
reference=args.reference.resolve();output=args.output.resolve();target=reference/'FoxitPDFReader.exe'
sha=hashlib.sha256(target.read_bytes()).hexdigest()
if sha!='90208c9e8da92c8e546b76c8f4a2f8fb999105d124e663bbea6744fb6bb6b3a6':raise ValueError('Unrecognized original binary')
output.mkdir(parents=True,exist_ok=False);(output/'state').mkdir()
# Wine queries the account database even for --version. Supply a synthetic user,
# never the host's real passwd/group or an existing profile.
(output/'passwd').write_text(f'analyst:x:{os.getuid()}:{os.getgid()}:Analyst:/state:/bin/false\n')
(output/'group').write_text(f'analyst:x:{os.getgid()}:\n')
if args.zlib_root:
    architectures=([('i686-w64-mingw32','system32')] if args.wine32_root else
                   [('x86_64-w64-mingw32','system32'),('i686-w64-mingw32','syswow64')])
    for arch, system in architectures:
        dll=args.zlib_root/'usr'/arch/'lib/zlib1.dll'
        dest=output/'state/prefix/drive_c/windows'/system/'zlib1.dll'
        dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dll,dest)
tools='/workspace/release-tools/local'
if args.prefill_wow64:
    source=(args.wine32_root.resolve()/'usr/lib/i386-linux-gnu/wine/i386-windows' if args.wine32_root else
            Path(tools)/'usr/lib/x86_64-linux-gnu/wine/i386-windows')
    dest=output/('state/prefix/drive_c/windows/system32' if args.wine32_root else
                 'state/prefix/drive_c/windows/syswow64')
    dest.mkdir(parents=True,exist_ok=True)
    for builtin in source.iterdir():
        if builtin.is_file():shutil.copy2(builtin,dest/builtin.name)
command=['bwrap','--die-with-parent','--new-session','--unshare-all','--clearenv',
 '--ro-bind','/usr','/usr','--ro-bind','/bin','/bin','--ro-bind','/lib','/lib','--ro-bind','/lib64','/lib64',
 '--ro-bind',str(output/'passwd'),'/etc/passwd','--ro-bind',str(output/'group'),'/etc/group',
 '--ro-bind','/etc/fonts','/etc/fonts','--ro-bind','/etc/ld.so.cache','/etc/ld.so.cache',
 '--proc','/proc','--dev','/dev','--tmpfs','/tmp',
 '--ro-bind','/tmp/.X11-unix','/tmp/.X11-unix',
 '--ro-bind',tools,tools,'--ro-bind',str(reference),'/reference',
 '--bind',str(output/'state'),'/state',
 '--setenv','PATH','/usr/bin:/bin','--setenv','DISPLAY',args.display,
 '--setenv','WINEPREFIX','/state/prefix','--setenv','WINEARCH','win64',
 '--setenv','WINESERVER',tools+'/usr/lib/wine/wineserver64',
 '--setenv','WINELOADER',tools+'/usr/lib/wine/wine64',
 '--setenv','WINEDATADIR',tools+'/usr/share/wine',
 '--setenv','WINEDLLPATH',tools+'/usr/lib/x86_64-linux-gnu/wine',
 '--setenv','LD_LIBRARY_PATH',tools+'/usr/lib/x86_64-linux-gnu',
 '--setenv','WINEDLLOVERRIDES','mscoree,mshtml=',
 '--setenv','XDG_CACHE_HOME','/state/cache','--setenv','XDG_CONFIG_HOME','/state/config',
 '--setenv','WINEDEBUG',('-all,err+all,+process,+seh,+loaddll' if args.diagnose_startup else '-all,err+all,+module' if args.diagnose_imports else '-all,err+all'),
 '--chdir','/reference','--',tools+'/usr/lib/wine/wine64',r'Z:\reference\FoxitPDFReader.exe']
if args.probe_wine:command[-1]='--version'
if args.probe_cmd:
    system='system32' if args.probe_cmd=='x64' or args.wine32_root else 'syswow64'
    command[-1:]=[rf'C:\windows\{system}\cmd.exe','/c','echo LINUXIT_RUNTIME_PROBE']
if args.qemu_root:
    qemu_root=args.qemu_root.resolve()
    qemu=qemu_root/('usr/bin/qemu-i386' if args.wine32_root else 'usr/bin/qemu-x86_64')
    if not qemu.is_file():raise ValueError('QEMU executable not found')
    loader=tools+'/usr/lib/wine/wine64'
    emulation=[str(qemu),'-cpu','max']
    mounts=['--ro-bind',str(qemu_root),str(qemu_root)]
    if args.wine32_root:
        runtime=args.wine32_root.resolve()
        # A separate byte-identical loader alias permits an overlay adapter at
        # Wine's compiled fallback path without recursing into that adapter.
        loader=str(runtime/'usr/lib/wine/wine-emulated-loader')
        if not Path(loader).is_file():raise ValueError('Missing byte-identical wine-emulated-loader alias')
        if Path(loader).read_bytes()!=(runtime/'usr/lib/wine/wine').read_bytes():
            raise ValueError('Emulated loader alias differs from the verified Wine loader')
        emulation+=['-L',str(runtime)]
        mounts+=['--ro-bind',str(runtime),str(runtime),'--setenv','WINEARCH','win32',
                 '--setenv','WINEDLLPATH',str(runtime/'usr/lib/i386-linux-gnu/wine'),
                 '--setenv','LD_LIBRARY_PATH',str(runtime/'usr/lib/i386-linux-gnu')+':'+tools+'/usr/lib/x86_64-linux-gnu']
        # Debian's fallback server script uses absolute installation paths.
        # Overlay only that script with a local path adapter; retain package bytes.
        server_wrapper=output/'state/wine-server'
        server_wrapper.write_text('#!/bin/sh\nexec '+shlex.quote(tools+'/usr/lib/wine/wineserver64')+' "$@"\n')
        server_wrapper.chmod(0o700)
        mounts+=['--ro-bind',str(server_wrapper),str(runtime/'usr/lib/wine/wineserver')]
    if args.diagnose_emulator:mounts+=['--setenv','QEMU_STRACE','1']
    wrapper=output/'state/wine-loader'
    wrapper.write_text('#!/bin/sh\nexec '+shlex.join(emulation+[loader])+' "$@"\n')
    wrapper.chmod(0o700)
    if args.wine32_root:
        mounts+=['--ro-bind',str(wrapper),str(runtime/'usr/lib/wine/wine')]
    separator=command.index('--')
    command[separator:separator]=mounts+['--setenv','WINELOADER','/state/wine-loader',
                                      '--setenv','WINELOADERNOEXEC','1']
    separator=command.index('--')
    command[separator+1:separator+2]=emulation+[loader]
# No credentials, session bus, account profiles or other workspace checkouts are mounted.
started=time.monotonic()
with (output/'stdout.log').open('wb') as stdout,(output/'stderr.log').open('wb') as stderr:
 try:
  run=subprocess.run(command,stdout=stdout,stderr=stderr,timeout=args.timeout)
  result={'status':'exited','exit_code':run.returncode}
 except subprocess.TimeoutExpired:
  result={'status':'timeout','exit_code':None}
result.update({'mode':'runtime_probe' if args.probe_wine or args.probe_cmd else 'original_launch_attempt','probe_architecture':args.probe_cmd,'target_loaded':None,'source_sha256':sha,'timeout_sec':args.timeout,'network':'separate namespace, no network access','original_mount':'read-only /reference','writable_state':'isolated /state and temporary /tmp','gui_shared':'dedicated virtual X server, no other app should use this display','functional_equivalence_verified':False,'ui_observation_requires_separate_confirmation':True})
result.update({'elapsed_sec':round(time.monotonic()-started,3),
               'emulation':('qemu-i386' if args.wine32_root else 'qemu-x86_64') if args.qemu_root else None,
               'emulated_cpu':'max' if args.qemu_root else None,
               'wine_prefix_architecture':'win32' if args.wine32_root else 'win64',
               'prefilled_wine32':args.prefill_wow64})
if args.probe_cmd:
    result['expected_marker_seen']=b'LINUXIT_RUNTIME_PROBE' in (output/'stdout.log').read_bytes()
    result['runtime_probe_passed']=result.get('exit_code')==0 and result['expected_marker_seen']
(output/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
raise SystemExit(0 if result.get('exit_code')==0 and (not args.probe_cmd or result['runtime_probe_passed']) else 1)
