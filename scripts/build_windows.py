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
import re
import ntpath

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


def native(path):
    """Backslash Windows path even under MSYS2 Python, whose ntpath keeps '/'."""
    return ntpath.normpath(str(path)).replace('/','\\')


def nsis(value):
    return str(value).replace('$','$$').replace('"','$\\"').replace('\n','')

def source_revision():
    revision=os.environ.get('GITHUB_SHA')
    if not revision:revision=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    if not re.fullmatch('[0-9a-f]{40}',revision):raise ValueError('Source revision must be a full commit SHA')
    return revision


CACHE_GROUPS={
    'schemas':('bin/glib-compile-schemas.exe','share/glib-2.0/schemas','*.xml'),
    'icons':('bin/gtk-update-icon-cache.exe','share/icons/Adwaita','*'),
    'mime':('bin/update-mime-database.exe','share/mime/packages','*.xml'),
    'gio':('bin/gio-querymodules.exe','lib/gio/modules','*.dll'),
    'immodules':('bin/gtk-query-immodules-3.0.exe','lib/gtk-3.0','*.dll'),
}

def cache_group(relative):
    if relative=='runtime/share/glib-2.0/schemas/gschemas.compiled':return 'schemas'
    if relative=='runtime/share/icons/Adwaita/icon-theme.cache':return 'icons'
    if relative.startswith('runtime/share/mime/') and '/packages/' not in relative:return 'mime'
    if relative=='runtime/lib/gio/modules/giomodule.cache':return 'gio'
    if relative.startswith('runtime/lib/gtk-3.0/') and relative.endswith('/immodules.cache'):return 'immodules'
    return None

def cache_inputs(prefix,ownership,group):
    generator,directory,pattern=CACHE_GROUPS[group]
    sources=[prefix/generator,*sorted((prefix/directory).rglob(pattern))]
    if group=='schemas':sources.extend(sorted((prefix/directory).rglob('*.gschema.override')))
    records=[]
    for path in sources:
        if not path.is_file():continue
        source='/ucrt64/'+path.relative_to(prefix).as_posix();owner=ownership.get(source)
        if owner is None:
            if path.name.endswith('.cache'):continue
            raise ValueError('Generated cache input without provenance: '+source)
        records.append(dict(source=source,sha256=sha(path),package=owner))
    if len(records)<2 or not (prefix/generator).is_file():raise ValueError('Generated cache needs its packaged generator and inputs: '+group)
    return dict(method='MSYS2 post-install generated cache; input bytes and packages recorded',generator='/ucrt64/'+generator,inputs=records)


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
                if path.name=='loaders.cache':continue  # Regenerated after relocation by windows_bootstrap.
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
    records=[];generated={}
    for path in sorted(stage.rglob('*')):
        if not path.is_file():continue
        relative=path.relative_to(stage).as_posix();source=origins.get(relative)
        owner=ownership.get(source) if source else None
        group=None
        if source and owner is None:
            group=cache_group(relative)
            if group:
                if group not in generated:generated[group]=cache_inputs(prefix,ownership,group)
                owner='generated-cache:'+group
            elif path.name.startswith('_quickjs') and path.suffix=='.pyd' or path.name=='quickjs-installation.json':
                owner='python-quickjs-ng==0.15.1.1 (compiled UCRT64 overlay)'
            else:raise ValueError('Runtime sem proveniência de pacote: '+relative)
        records.append(dict(path=relative,bytes=path.stat().st_size,sha256=sha(path),package=owner,source=source,generated_from=group))
    manifest=dict(schema='linuxit-windows-payload-v1',version=VERSION,development=True,source_revision=source_revision(),
                  native_windows=True,architecture='x86_64',runtime='MSYS2 UCRT64',administrator_required=False,
                  records=records,packages=packages,generated_cache_groups=generated,quickjs='python-quickjs-ng==0.15.1.1',
                  limitations=['Windows development candidate; unsigned installer.', 'Original Foxit and whole-family parity are not tested by this packaging.'])
    (stage/'windows-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    output.parent.mkdir(parents=True,exist_ok=True)
    include=output.with_suffix('.delete.nsh')
    allfiles=[path for path in stage.rglob('*') if path.is_file()]
    lines=['Delete "$INSTDIR\\'+nsis(str(path.relative_to(stage)))+'"' for path in allfiles]
    directories=sorted({parent for path in allfiles for parent in path.parents if parent!=stage and parent.is_relative_to(stage)},key=lambda p:len(p.parts),reverse=True)
    lines.extend('RMDir "$INSTDIR\\'+nsis(str(path.relative_to(stage)))+'"' for path in directories)
    include.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    # Keep the generated uninstall inventory in the same compilation unit;
    # the MSYS2 NSIS !include path resolver differs from native argv handling.
    template=(ROOT/'packaging/windows/linuxit.nsi').read_text(encoding='utf-8')
    needle='  !include "${DELETE_INCLUDE}"'
    if template.count(needle)!=1:raise ValueError('Uninstall template boundary changed')
    script=output.with_suffix('.generated.nsi')
    script.write_text(template.replace(needle,'\n'.join('  '+line for line in lines)),encoding='utf-8')
    if not include.is_file() or not script.is_file():raise ValueError('Generated installer source missing')
    subprocess.run([str(makensis),'/V2','/INPUTCHARSET','UTF8','/DVERSION='+VERSION,
                    '/DPAYLOAD='+native(stage),'/DOUTPUT='+native(output),
                    native(script)],check=True)
    result=dict(schema='linuxit-windows-installer-build-v1',version=VERSION,path=str(output),bytes=output.stat().st_size,
                sha256=sha(output),generated_nsis_sha256=sha(script),payload_files=len(records),runtime_packages=len(packages),installed_or_published=False)
    output.with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result));return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prefix',required=True,type=Path);parser.add_argument('--stage',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path);parser.add_argument('--makensis',required=True,type=Path)
    parser.add_argument('--compiler',required=True,type=Path);parser.add_argument('--quickjs-notices',required=True,type=Path)
    args=parser.parse_args();build(args.prefix,args.stage,args.output,args.makensis,args.compiler,args.quickjs_notices)
