#!/usr/bin/env python3
"""Build a relocatable UCRT64 payload and a per-user NSIS installer on a runner.

No installer is launched by this builder. Every included runtime file is hashed
and attributed to an installed MSYS2 package or the pinned QuickJS overlay.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'app'))
from version import VERSION

BINARIES=('python.exe','pythonw.exe','pdftocairo.exe','pdftotext.exe','pdfinfo.exe','pdfunite.exe',
          'openssl.exe','tesseract.exe','espeak-ng.exe','gdk-pixbuf-query-loaders.exe')
DIRECTORIES=('lib/girepository-1.0','lib/gdk-pixbuf-2.0','lib/gtk-3.0','lib/gio/modules','lib/gstreamer-1.0',
             'share/glib-2.0/schemas','share/fonts','share/fontconfig','share/icons/Adwaita','share/themes/Default',
             'share/locale','share/mime','share/tessdata','share/espeak-ng-data','share/licenses','etc/fonts','etc/ssl')


def sha(path):
    with Path(path).open('rb') as handle:return hashlib.file_digest(handle,'sha256').hexdigest()


def nsis(value):
    return str(value).replace('$','$$').replace('"','$\\"').replace('\n','')


def build(prefix,stage,output,makensis,compiler,quickjs_notices,pacman='pacman'):
    prefix,stage,output=Path(prefix).resolve(),Path(stage).resolve(),Path(output).resolve()
    if stage.exists() or output.exists():raise ValueError('Use novos caminhos; payload e instaladores anteriores são preservados.')
    if os.name!='nt':raise ValueError('O empacotamento exige Windows nativo UCRT64.')
    if not quickjs_notices.is_file():raise ValueError('Avisos completos QuickJS obrigatórios.')
    stage.mkdir(parents=True);runtime=stage/'runtime';origins={}
    def file(source,target):
        source=Path(source);target=Path(target)
        if not source.resolve().is_relative_to(prefix):raise ValueError('Runtime fora do prefixo UCRT64: '+str(source))
        target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
        origins[target.relative_to(stage).as_posix()]='/ucrt64/'+source.relative_to(prefix).as_posix()
    def tree(relative):
        origin=prefix/relative
        if origin.exists():
            for path in origin.rglob('*'):
                if path.is_file() and '__pycache__' not in path.parts and path.suffix not in ('.pyc','.pyo','.a','.h'):
                    file(path,runtime/path.relative_to(prefix))
    for name in BINARIES:
        if not (prefix/'bin'/name).is_file():raise ValueError('Ferramenta Windows ausente: '+name)
        file(prefix/'bin'/name,runtime/'bin'/name)
    for path in (prefix/'bin').glob('gspawn-*.exe'):file(path,runtime/'bin'/path.name)
    for path in (prefix/'bin').glob('*.dll'):file(path,runtime/'bin'/path.name)
    python_libraries=sorted((prefix/'lib').glob('python3.*'))
    if len(python_libraries)!=1:raise ValueError('Prefixo precisa de um runtime Python único.')
    tree(python_libraries[0].relative_to(prefix))
    for name in DIRECTORIES:tree(Path(name))
    if not list((runtime/'lib').glob('python3.*/site-packages/_quickjs*.pyd')):
        raise ValueError('QuickJS precisa ser compilado para o Python UCRT64 antes do build.')
    for language in ('por','eng'):
        if not (runtime/'share/tessdata'/f'{language}.traineddata').is_file():raise ValueError('OCR Windows sem idioma '+language)
    shutil.copytree(ROOT/'app',stage/'app',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    shutil.copy2(ROOT/'LICENSE',stage/'LICENSE')
    shutil.copy2(ROOT/'packaging/windows/windows_bootstrap.py',stage/'windows_bootstrap.py')
    shutil.copy2(quickjs_notices,stage/'quickjs-notices.txt')
    subprocess.run([str(compiler),'-municode','-mwindows','-O2',str(ROOT/'packaging/windows/launcher.c'),'-o',str(stage/'LinuxitPDF.exe'),'-lshell32'],check=True)
    listing=subprocess.run([pacman,'-Ql'],check=True,capture_output=True,text=True,encoding='utf-8').stdout
    ownership={}
    for line in listing.splitlines():
        owner,_,name=line.partition(' ')
        if name and not name.endswith('/'):ownership[name]=owner
    packages=sorted({ownership[source] for source in origins.values() if source in ownership})
    package_info=subprocess.run([pacman,'-Qi',*packages],check=True,capture_output=True,text=True,encoding='utf-8').stdout
    (stage/'runtime-package-info.txt').write_text(package_info,encoding='utf-8')
    records=[]
    for path in sorted(stage.rglob('*')):
        if not path.is_file():continue
        relative=path.relative_to(stage).as_posix();source=origins.get(relative)
        owner=ownership.get(source) if source else None
        if source and owner is None:
            if 'quickjs' not in path.name and not any('quickjs' in part for part in path.parts):
                raise ValueError('Runtime sem proveniência de pacote: '+relative)
            owner='python-quickjs-ng==0.15.1.1 (compiled UCRT64 overlay)'
        records.append(dict(path=relative,bytes=path.stat().st_size,sha256=sha(path),package=owner,source=source))
    manifest=dict(schema='linuxit-windows-payload-v1',version=VERSION,development=True,source_revision=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
                  native_windows=True,architecture='x86_64',runtime='MSYS2 UCRT64',administrator_required=False,
                  records=records,packages=packages,quickjs='python-quickjs-ng==0.15.1.1',
                  limitations=['Windows development candidate; unsigned installer.', 'Original Foxit and whole-family parity are not tested by this packaging.'])
    (stage/'windows-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    output.parent.mkdir(parents=True,exist_ok=True)
    include=output.with_suffix('.delete.nsh')
    allfiles=[path for path in stage.rglob('*') if path.is_file()]
    lines=['Delete "$INSTDIR\\'+nsis(str(path.relative_to(stage)))+'"' for path in allfiles]
    directories=sorted({parent for path in allfiles for parent in path.parents if parent!=stage and parent.is_relative_to(stage)},key=lambda p:len(p.parts),reverse=True)
    lines.extend('RMDir "$INSTDIR\\'+nsis(str(path.relative_to(stage)))+'"' for path in directories)
    include.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    subprocess.run([str(makensis),'/V2','/INPUTCHARSET','UTF8','/DVERSION='+VERSION,'/DPAYLOAD='+str(stage),'/DOUTPUT='+str(output),
                    '/DDELETE_INCLUDE='+str(include),str(ROOT/'packaging/windows/linuxit.nsi')],check=True)
    result=dict(schema='linuxit-windows-installer-build-v1',version=VERSION,path=str(output),bytes=output.stat().st_size,
                sha256=sha(output),payload_files=len(records),runtime_packages=len(packages),installed_or_published=False)
    output.with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result));return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prefix',required=True,type=Path);parser.add_argument('--stage',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path);parser.add_argument('--makensis',required=True,type=Path)
    parser.add_argument('--compiler',required=True,type=Path);parser.add_argument('--quickjs-notices',required=True,type=Path)
    args=parser.parse_args();build(args.prefix,args.stage,args.output,args.makensis,args.compiler,args.quickjs_notices)
