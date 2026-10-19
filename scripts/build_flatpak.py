#!/usr/bin/env python3
"""Bundle the Debian 13 Python/GTK runtime into a real Flatpak application."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
from version import VERSION
APP_ID = 'io.github.airtonbp19edu.LinuxitPDF'


def build(flatpak, stage, repo, extra):
    if stage.exists():
        raise RuntimeError('Use an empty staging location; existing files are preserved.')
    files = stage / 'files'
    for name in ['bin', 'lib', 'runtime-lib', 'libexec', 'share', 'etc']:
        (files / name).mkdir(parents=True, exist_ok=True)
    runtime_sources = {}

    def runtime_file(origin, target):
        shutil.copy2(origin, target)
        runtime_sources[target.relative_to(files).as_posix()] = Path(origin)

    def runtime_tree(origin, target, **options):
        origin = Path(origin)
        shutil.copytree(origin, target, **options)
        for path in target.rglob('*'):
            if path.is_file():
                runtime_sources[path.relative_to(files).as_posix()] = origin / path.relative_to(target)

    ignore = shutil.ignore_patterns('__pycache__', '*.pyc', 'test', 'tests', 'idlelib', 'tkinter')
    shutil.copytree(ROOT / 'app', files / 'share/linuxit-pdf', ignore=ignore)
    runtime_tree('/usr/lib/python3.13', files / 'python/lib/python3.13', ignore=ignore)
    site = files / 'python/lib/python3.13/site-packages'
    site.mkdir()
    for module in ['gi', 'cairo', 'PIL', 'cryptography', 'cffi', 'pycparser']:
        origin = Path('/usr/lib/python3/dist-packages') / module
        if origin.exists():
            runtime_tree(origin, site / module, ignore=ignore)
    for origin in Path('/usr/lib/python3/dist-packages').glob('_cffi_backend*.so'):
        runtime_file(origin, site / origin.name)
    adapter = extra / 'gi-cairo/usr/lib/python3/dist-packages/gi'
    for origin in adapter.glob('_gi_cairo*.so'):
        runtime_file(origin, site / 'gi' / origin.name)
    if not list((site / 'gi').glob('_gi_cairo*.so')):
        raise RuntimeError('python3-gi-cairo is required in the runtime overlay.')
    binaries = {'python3': Path('/usr/bin/python3.13')}
    for name in ('pdftocairo', 'pdftotext', 'pdfinfo', 'pdfunite', 'prlimit', 'lp', 'lpstat', 'lpoptions', 'openssl', 'tesseract', 'espeak-ng'):
        origin = str(Path('/usr/bin') / name) if (Path('/usr/bin') / name).exists() else str(extra / 'usr/bin' / name)
        if not Path(origin).exists():
            raise RuntimeError('Required executable missing: ' + name)
        with open(origin, 'rb') as source:
            if source.read(4) != b'\x7fELF':
                raise RuntimeError('An actual ELF executable is required: ' + origin)
        binaries[name] = Path(origin)
    for name, origin in binaries.items():
        runtime_file(origin, files / 'libexec' / name)
    runtime_tree('/usr/lib/x86_64-linux-gnu/girepository-1.0', files / 'lib/girepository-1.0')
    pix = Path('/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0')
    runtime_tree(pix, files / 'lib/gdk-pixbuf-2.0/2.10.0')
    cache = files / 'lib/gdk-pixbuf-2.0/2.10.0/loaders.cache'
    cache.write_text(cache.read_text().replace('/usr/lib/x86_64-linux-gnu/', '/app/lib/'))
    runtime_tree('/usr/share/glib-2.0/schemas', files / 'share/glib-2.0/schemas')
    runtime_tree('/usr/share/fonts/truetype/dejavu', files / 'share/fonts/truetype/dejavu')
    tessdata = [p for p in Path('/usr/share/tesseract-ocr').glob('*/tessdata')
                if all((p / (language + '.traineddata')).is_file() for language in ('por', 'eng'))]
    if len(tessdata) != 1:
        raise RuntimeError('One Tesseract data directory with Portuguese and English models is required.')
    runtime_tree(tessdata[0], files / 'share/tessdata')
    speech_data=Path('/usr/lib/x86_64-linux-gnu/espeak-ng-data')
    if not speech_data.is_dir():raise RuntimeError('eSpeak NG data directory is required.')
    runtime_tree(speech_data, files / 'share/espeak-ng-data')
    runtime_tree('/usr/share/icons/Adwaita', files / 'share/icons/Adwaita')
    runtime_tree('/usr/share/mime', files / 'share/mime')
    shutil.copytree(ROOT / 'assets/icons', files / 'share/icons/hicolor', dirs_exist_ok=True)
    for icon in (files / 'share/icons/hicolor').rglob('linuxit-pdf.png'):
        shutil.copy2(icon, icon.with_name(APP_ID + '.png'))
    (files / 'etc/fonts').mkdir()
    (files / 'etc/fonts/fonts.conf').write_text('''<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig><dir>/app/share/fonts</dir><dir>/usr/share/fonts</dir><dir>/run/host/fonts</dir>
<cachedir prefix="xdg">fontconfig</cachedir></fontconfig>
''')
    runtime_tree('/usr/lib/x86_64-linux-gnu/ossl-modules', files / 'runtime-lib/ossl-modules')
    # All ELF dependencies, including libc, are paired with their own loader.
    # This avoids mixing a newer host-built extension with a different runtime libc.
    probes = list((files / 'libexec').iterdir()) + list(files.rglob('*.so'))
    dynamic_gui = [Path('/usr/lib/x86_64-linux-gnu') / name for name in
                   ('libgtk-3.so.0', 'libgdk-3.so.0', 'libatk-1.0.so.0',
                    'libpangocairo-1.0.so.0', 'libgdk_pixbuf-2.0.so.0')]
    probes.extend(dynamic_gui)
    libraries = set(dynamic_gui)
    for probe in probes:
        result = subprocess.run(['ldd', str(probe)], capture_output=True, text=True)
        for path in re.findall(r'(?:=>\s+)?(/[^\s()]+)', result.stdout):
            if Path(path).is_file():
                libraries.add(Path(path))
    for library in sorted(libraries):
        runtime_file(library, files / 'runtime-lib' / library.name)
    loader = Path('/lib64/ld-linux-x86-64.so.2').resolve()
    runtime_file(loader, files / 'runtime-lib/ld-linux-x86-64.so.2')
    for name in binaries:
        wrapper = files / 'bin' / name
        wrapper.write_text('''#!/bin/sh
base="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
''' + ('export TESSDATA_PREFIX="$base/share/tessdata"\n' if name == 'tesseract' else '') + '''exec "$base/runtime-lib/ld-linux-x86-64.so.2" --library-path "$base/runtime-lib" "$base/libexec/''' + name + ('" --path="$base/share" "$@"\n' if name == 'espeak-ng' else '''" "$@"
''') + '''
''')
        wrapper.chmod(0o755)
    python = files / 'bin/linuxit-python'
    python.write_text('''#!/bin/sh
base="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
export PYTHONHOME="$base/python"
export PYTHONPATH="$base/python/lib/python3.13/site-packages"
export OPENSSL_MODULES="$base/runtime-lib/ossl-modules"
unset LD_LIBRARY_PATH
export GI_TYPELIB_PATH="$base/lib/girepository-1.0"
export GSETTINGS_SCHEMA_DIR="$base/share/glib-2.0/schemas"
cache_dir="${XDG_CACHE_HOME:-${TMPDIR:-/tmp}}/linuxit-pdf"
mkdir -p "$cache_dir"
cache_id="$(printf '%s' "$base" | cksum | cut -d ' ' -f 1)"
module_cache="$cache_dir/loaders-$cache_id.cache"
if [ ! -f "$module_cache" ]; then
  temp_cache="$(mktemp "$cache_dir/.loaders-XXXXXX")"
  sed "s#/app/#$base/#g" "$base/lib/gdk-pixbuf-2.0/2.10.0/loaders.cache" > "$temp_cache"
  mv -f "$temp_cache" "$module_cache"
fi
export GDK_PIXBUF_MODULE_FILE="$module_cache"
export FONTCONFIG_FILE="$base/etc/fonts/fonts.conf"
export XDG_DATA_DIRS="$base/share:/usr/share"
export PRINT_VIEW_WORKER_PYTHON="$base/bin/linuxit-python"
export PATH="$base/bin:$PATH"
exec "$base/bin/python3" "$@"
''')
    python.chmod(0o755)
    launcher = files / 'bin/linuxit-pdf'
    launcher.write_text('''#!/bin/sh
base="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
exec "$base/bin/linuxit-python" "$base/share/linuxit-pdf/main.py" "$@"
''')
    launcher.chmod(0o755)
    appdir = files / 'share/applications'
    appdir.mkdir()
    desktop = (ROOT / 'assets/linuxit-pdf.desktop').read_text().replace('Icon=linuxit-pdf', 'Icon=' + APP_ID)
    (appdir / (APP_ID + '.desktop')).write_text(desktop)
    metadata = files / 'share/metainfo'
    metadata.mkdir()
    shutil.copy2(ROOT / 'packaging' / (APP_ID + '.metainfo.xml'), metadata)
    docs = files / 'share/doc/linuxit-pdf'
    docs.mkdir(parents=True)
    for notice in ('cups-client-copyright.txt', 'pypdf-artifact.json', 'pypdf-LICENSE.txt', 'proveniencia-snowball.json'):
        shutil.copy2(ROOT / 'docs' / notice, docs / notice)
    shutil.copy2(ROOT / 'LICENSE', docs)
    shutil.copy2(ROOT / 'app/vendor/snowballstemmer/COPYING', docs / 'snowballstemmer-COPYING.txt')
    # Preserve installed Debian copyright notices for every bundled ELF package.
    notices = docs / 'runtime-copyright'
    notices.mkdir()
    # Resolve both names on merged-/usr Debian. Looking up only /lib paths
    # silently omitted most native dependencies from the previous manifest.
    # Track every copied runtime file, including Python/data/typelibs, rather
    # than asking dpkg about paths inside the staging directory.
    generated_inputs = {
        'mime': [*Path('/usr/share/mime/packages').glob('*.xml'), Path('/usr/bin/update-mime-database')],
        'schemas': [*Path('/usr/share/glib-2.0/schemas').glob('*.xml'),
                    *Path('/usr/share/glib-2.0/schemas').glob('*.gschema.override'),
                    Path('/usr/bin/glib-compile-schemas')],
        'icons': [Path('/usr/share/icons/Adwaita/index.theme')],
        'pixbuf': [*pix.glob('loaders/*.so'), Path('/usr/lib/x86_64-linux-gnu/libgdk_pixbuf-2.0.so.0')],
    }
    sources = set(runtime_sources.values()) | {p for group in generated_inputs.values() for p in group}
    lookup = {alias for p in sources for alias in (p, p.resolve())}
    result = subprocess.run(['dpkg-query', '-S', *map(str, sorted(lookup))], capture_output=True, text=True)
    owners_by_path = {}
    for line in result.stdout.splitlines():
        if ': ' not in line:
            continue
        # dpkg can also emit diversion notices; they are not package identities.
        identity, path = line.split(': ', 1)
        owners = [part.strip() for part in identity.split(',')]
        if all(re.fullmatch(r'[a-z0-9][a-z0-9+.-]*(?::[a-z0-9-]+)?', part) for part in owners):
            owners_by_path.setdefault(path, set()).update(owners)

    def owners(path):
        return owners_by_path.get(str(path), set()) | owners_by_path.get(str(path.resolve()), set())

    generated_owners = {}
    for group, inputs in generated_inputs.items():
        known = set()
        for path in inputs:
            if not owners(path):
                raise RuntimeError('Unowned input for generated runtime data: ' + str(path))
            known.update(owners(path))
        generated_owners[group] = known
    records, packages = [], set()
    for name, origin in sorted(runtime_sources.items()):
        package_owners, derivation, overlay_notice = owners(origin), None, None
        if not package_owners:
            if origin.is_relative_to(extra / 'gi-cairo'):
                overlay_notice = 'python3-gi-cairo.txt'
            elif origin.is_relative_to(Path('/usr/share/mime')) and not origin.is_relative_to(Path('/usr/share/mime/packages')):
                derivation = 'mime'
            elif origin == Path('/usr/share/glib-2.0/schemas/gschemas.compiled'):
                derivation = 'schemas'
            elif origin == Path('/usr/share/icons/Adwaita/icon-theme.cache'):
                derivation = 'icons'
            elif origin == pix / 'loaders.cache':
                derivation = 'pixbuf'
            else:
                raise RuntimeError('Missing Debian provenance for bundled file: ' + str(origin))
            if derivation:
                package_owners = generated_owners[derivation]
        packages.update(package_owners)
        payload = files / name
        records.append({'file': name, 'source': str(origin),
                        'source_resolved': str(origin.resolve()),
                        'packages': sorted(package_owners),
                        'generated_from_group': derivation, 'overlay_notice': overlay_notice,
                        'sha256': hashlib.sha256(payload.read_bytes()).hexdigest(),
                        'source_sha256': hashlib.sha256(origin.read_bytes()).hexdigest(),
                        'elf': payload.read_bytes()[:4] == b'\x7fELF'})
    package_versions = []
    for package in sorted(packages):
        copyright = Path('/usr/share/doc') / package.split(':')[0] / 'copyright'
        if not copyright.exists():
            raise RuntimeError('Missing copyright notice for bundled package: ' + package)
        shutil.copy2(copyright, notices / (package.replace(':', '_') + '.txt'))
        record = subprocess.run(['dpkg-query', '-W', '-f', '${binary:Package}\t${Version}\t${source:Package}\t${source:Version}\n', package],
                                check=True, capture_output=True, text=True)
        package_versions.append(record.stdout.strip())
    for path in (extra / 'gi-cairo/usr/share/doc/python3-gi-cairo/copyright',):
        if not path.exists():
            raise RuntimeError('Missing license for runtime overlay: ' + str(path))
        shutil.copy2(path, notices / 'python3-gi-cairo.txt')
    (docs / 'runtime-packages.tsv').write_text('binary_package\tversion\tsource_package\tsource_version\n' + '\n'.join(package_versions) + '\n')
    source_access=[]
    for line in package_versions:
        binary,version,source,source_version=line.split('\t')
        source=source or binary.split(':')[0];source_version=source_version or version
        source_access.append(dict(binary_package=binary,binary_version=version,source_package=source,
            source_version=source_version,corresponding_source_url='https://sources.debian.org/src/'+quote(source,safe='')+'/'+quote(source_version,safe='')+'/'))
    (docs / 'runtime-source-access.json').write_text(json.dumps(source_access,indent=2)+'\n')
    shutil.copy2(ROOT / 'docs/RUNTIME-SOURCE-ACCESS.md',docs / 'RUNTIME-SOURCE-ACCESS.md')
    (docs / 'runtime-origins.json').write_text(json.dumps({
        'schema': 'linuxit-bundled-runtime-origins-v1', 'all_files_attributed': True,
        'files_audited': len(records), 'elf_files_audited': sum(r['elf'] for r in records),
        'debian_packages': len(packages),
        'scope': 'Copied third-party runtime files; own source/assets, generated wrappers and notice files are recorded separately.',
        'generated_input_groups': {group: [{'file': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                                            for p in inputs] for group, inputs in generated_inputs.items()},
        'files': records}, indent=2) + '\n')
    shutil.copytree('/usr/share/common-licenses', docs / 'runtime-common-licenses')
    shutil.copy2(ROOT / 'docs/cups-client-copyright.txt', notices / 'cups-client.txt')
    (stage / 'metadata').write_text(f'''[Application]
name={APP_ID}
runtime=org.freedesktop.Platform/x86_64/25.08
sdk=org.freedesktop.Sdk/x86_64/25.08
command=linuxit-pdf

[Context]
shared=network;ipc;
sockets=wayland;fallback-x11;cups;
devices=dri;
filesystems=home;

[Session Bus Policy]
org.freedesktop.portal.*=talk
''')
    (stage / 'export').mkdir()
    export = stage / 'export/share'
    shutil.copytree(appdir, export / 'applications')
    shutil.copytree(metadata, export / 'metainfo')
    for icon in (files / 'share/icons/hicolor').rglob(APP_ID + '.png'):
        relative = icon.relative_to(files / 'share')
        target = export / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(icon, target)
    subprocess.run([flatpak, 'build-export', '--disable-sandbox', str(repo), str(stage), 'devel'], check=True)
    (ROOT / 'dist').mkdir(exist_ok=True)
    output = ROOT / 'dist' / f'LinuxitPDF-{VERSION}-x86_64.flatpak'
    subprocess.run([flatpak, 'build-bundle', '--runtime-repo=https://dl.flathub.org/repo/flathub.flatpakrepo',
                    str(repo), str(output), APP_ID, 'devel'], check=True)
    print(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--flatpak', default='flatpak')
    parser.add_argument('--stage', type=Path, default=ROOT / 'dist/flatpak-stage')
    parser.add_argument('--repo', type=Path, default=ROOT / 'dist/flatpak-repo')
    parser.add_argument('--extra-runtime', type=Path, required=True,
                        help='Runtime overlay with gi-cairo/ and optional usr/bin/lp*')
    args = parser.parse_args()
    build(args.flatpak, args.stage, args.repo, args.extra_runtime)
