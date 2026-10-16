#!/usr/bin/env python3
"""Attempt a bounded offline observation; proprietary output remains local."""
import argparse, hashlib, json, os, subprocess
from pathlib import Path

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--reference',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--display',default=':101')
parser.add_argument('--timeout',type=int,default=30)
parser.add_argument('--diagnose-imports',action='store_true')
parser.add_argument('--probe-wine',action='store_true',help='Run only Wine --version in exactly the same containment')
args=parser.parse_args()
reference=args.reference.resolve();output=args.output.resolve();target=reference/'FoxitPDFReader.exe'
sha=hashlib.sha256(target.read_bytes()).hexdigest()
if sha!='90208c9e8da92c8e546b76c8f4a2f8fb999105d124e663bbea6744fb6bb6b3a6':raise ValueError('Unrecognized original binary')
output.mkdir(parents=True,exist_ok=False);(output/'state').mkdir()
# Wine queries the account database even for --version. Supply a synthetic user,
# never the host's real passwd/group or an existing profile.
(output/'passwd').write_text(f'analyst:x:{os.getuid()}:{os.getgid()}:Analyst:/state:/bin/false\n')
(output/'group').write_text(f'analyst:x:{os.getgid()}:\n')
tools='/workspace/release-tools/local'
command=['bwrap','--die-with-parent','--new-session','--unshare-all','--clearenv',
 '--ro-bind','/usr','/usr','--ro-bind','/lib','/lib','--ro-bind','/lib64','/lib64',
 '--ro-bind',str(output/'passwd'),'/etc/passwd','--ro-bind',str(output/'group'),'/etc/group',
 '--ro-bind','/etc/fonts','/etc/fonts','--ro-bind','/etc/ld.so.cache','/etc/ld.so.cache',
 '--proc','/proc','--dev','/dev','--tmpfs','/tmp',
 '--ro-bind','/tmp/.X11-unix','/tmp/.X11-unix',
 '--ro-bind',tools,tools,'--ro-bind',str(reference),'/reference',
 '--bind',str(output/'state'),'/state',
 '--setenv','PATH','/usr/bin:/bin','--setenv','DISPLAY',args.display,
 '--setenv','WINEPREFIX','/state/prefix','--setenv','WINEARCH','win64',
 '--setenv','WINESERVER',tools+'/usr/lib/wine/wineserver64',
 '--setenv','WINEDATADIR',tools+'/usr/share/wine',
 '--setenv','WINEDLLPATH',tools+'/usr/lib/x86_64-linux-gnu/wine',
 '--setenv','LD_LIBRARY_PATH',tools+'/usr/lib/x86_64-linux-gnu',
 '--setenv','WINEDLLOVERRIDES','mscoree,mshtml=',
 '--setenv','XDG_CACHE_HOME','/state/cache','--setenv','XDG_CONFIG_HOME','/state/config',
 '--setenv','WINEDEBUG','-all,+module' if args.diagnose_imports else '-all',
 '--chdir','/reference','--',tools+'/usr/lib/wine/wine64','/reference/FoxitPDFReader.exe']
if args.probe_wine:command[-1]='--version'
# No credentials, session bus, account profiles or other workspace checkouts are mounted.
with (output/'stdout.log').open('wb') as stdout,(output/'stderr.log').open('wb') as stderr:
 try:
  run=subprocess.run(command,stdout=stdout,stderr=stderr,timeout=args.timeout)
  result={'status':'exited','exit_code':run.returncode}
 except subprocess.TimeoutExpired:
  result={'status':'timeout','exit_code':None}
result.update({'mode':'runtime_probe' if args.probe_wine else 'original_launch_attempt','target_loaded':None,'source_sha256':sha,'timeout_sec':args.timeout,'network':'separate namespace, no network access','original_mount':'read-only /reference','writable_state':'isolated /state and temporary /tmp','gui_shared':'dedicated virtual X server, no other app should use this display','functional_equivalence_verified':False,'ui_observation_requires_separate_confirmation':True})
(output/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
raise SystemExit(0 if result.get('exit_code')==0 else 1)
