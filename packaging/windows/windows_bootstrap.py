"""Relocatable per-user GTK/Python environment; no system settings are changed."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

def _short_path(path):
    """Windows 8.3 name of an existing path, or None when unavailable."""
    if os.name!='nt':return None
    import ctypes
    buffer=ctypes.create_unicode_buffer(32768)
    size=ctypes.windll.kernel32.GetShortPathNameW(str(path),buffer,len(buffer))
    return buffer.value if 0<size<len(buffer) else None


def _uninstall_key():
    try:version=json.loads((Path(os.path.abspath(__file__)).parent/'windows-manifest.json').read_text(encoding='utf-8'))['version']
    except (OSError,ValueError,KeyError):return None
    return r'Software\Microsoft\Windows\CurrentVersion\Uninstall\LinuxitPDF-'+version


def _ascii_alias(root):
    """ASCII-only path to the installation, or None.

    Poppler and OpenSSL derive their data/module folders from their own DLL
    location in the ANSI code page. Under a folder such as 'C:\\Users\\João' or
    'instalação' Poppler aborts while opening any PDF (CI 39899979222; the same
    installer in an ASCII folder renders). Prefer the 8.3 short name; otherwise
    create a directory junction (no administrator rights needed) in an ASCII
    shared folder and record it so the uninstaller removes the junction only.
    """
    text=str(root)
    if text.isascii():return root
    short=_short_path(root)
    if short and short.isascii():return Path(short)
    try:import _winapi,winreg
    except ImportError:return None
    token=hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]
    for base in (os.environ.get('PUBLIC'),os.environ.get('PROGRAMDATA')):
        if not base or not base.isascii():continue
        alias=Path(base)/'LinuxitPDF'/token
        try:
            if alias.exists():
                if os.path.realpath(alias)!=os.path.realpath(root):continue
            else:
                alias.parent.mkdir(parents=True,exist_ok=True)
                _winapi.CreateJunction(text,str(alias))
            key=_uninstall_key()
            if key:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER,key,0,winreg.KEY_SET_VALUE) as registry:
                    winreg.SetValueEx(registry,'AsciiAlias',0,winreg.REG_SZ,str(alias))
            return alias
        except OSError:continue
    return None


# Never resolve(): it would follow the junction back to the non-ASCII folder.
ROOT=Path(os.path.abspath(__file__)).parent
if os.name=='nt' and not str(ROOT).isascii() and os.environ.get('LINUXIT_ASCII_ALIAS')!='1':
    _alias=_ascii_alias(ROOT)
    if _alias is not None and _alias!=ROOT:
        _child=dict(os.environ,LINUXIT_ASCII_ALIAS='1')
        _python=_alias/'runtime'/'bin'/Path(sys.executable).name
        raise SystemExit(subprocess.call([str(_python),'-B','-I',str(_alias/'windows_bootstrap.py'),*sys.argv[1:]],env=_child,cwd=str(_alias)))
sys.dont_write_bytecode=True
RUNTIME=ROOT/'runtime'
BIN=RUNTIME/'bin'
os.environ['PATH']=str(BIN)+os.pathsep+os.environ.get('PATH','')
os.environ['GI_TYPELIB_PATH']=str(RUNTIME/'lib/girepository-1.0')
os.environ['GSETTINGS_SCHEMA_DIR']=str(RUNTIME/'share/glib-2.0/schemas')
os.environ['XDG_DATA_DIRS']=str(RUNTIME/'share')
os.environ['FONTCONFIG_PATH']=str(RUNTIME/'etc/fonts')
def _openssl_path(path):
    """Path that OpenSSL can read on any user folder.

    OpenSSL gets environment strings in the ANSI code page. A folder such as
    'C:\\Users\\João' or 'instalação' then reaches it as non-UTF-8 bytes, and the
    Rust layer of 'cryptography' panics while formatting the resulting error
    (CI 39897411096). ASCII paths are used as they are; otherwise the 8.3 short
    name; otherwise a copy under an ASCII-only per-user or shared folder.
    """
    text=str(path)
    if text.isascii():return text
    short=_short_path(path)
    if short and short.isascii():return short
    token=hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]
    for base in (os.environ.get('LOCALAPPDATA'),os.environ.get('PROGRAMDATA'),os.environ.get('PUBLIC')):
        if not base or not base.isascii():continue
        target=Path(base)/'LinuxitPDF-openssl'/token/Path(path).name
        try:
            if Path(path).is_dir():
                if not target.is_dir():shutil.copytree(path,target)
            else:
                target.parent.mkdir(parents=True,exist_ok=True)
                if not target.is_file():shutil.copy2(path,target)
            return str(target)
        except OSError:continue
    return None


OPENSSL_LIMITS=[]
for _name,_relative in (('OPENSSL_CONF','etc/ssl/openssl.cnf'),('OPENSSL_MODULES','lib/ossl-modules')):
    _source=RUNTIME/_relative
    if not _source.exists():continue
    _safe=_openssl_path(_source)
    if _safe:os.environ[_name]=_safe
    else:OPENSSL_LIMITS.append(_name)
if 'OPENSSL_MODULES' in OPENSSL_LIMITS:
    # Last resort: skip the legacy provider instead of crashing; RC4 PDFs are then unavailable.
    os.environ['CRYPTOGRAPHY_OPENSSL_NO_LEGACY']='1'
os.environ['GST_PLUGIN_PATH']=str(RUNTIME/'lib/gstreamer-1.0')
os.environ['PRINT_VIEW_WORKER_PYTHON']=str(BIN/'python.exe')
os.environ['PYTHONUTF8']='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
if (RUNTIME/'share/tessdata').is_dir():os.environ['TESSDATA_PREFIX']=str(RUNTIME/'share/tessdata')
_DLL_DIRECTORY=os.add_dll_directory(str(BIN))
sys.path.insert(0,str(ROOT/'app'))


def configure_pixbuf():
    query=BIN/'gdk-pixbuf-query-loaders.exe'
    loaders=sorted((RUNTIME/'lib/gdk-pixbuf-2.0').glob('*/loaders/*.dll'))
    if not query.exists() or not loaders:return
    cache=Path(os.environ.get('LOCALAPPDATA',Path.home()))/'Linuxit PDF'/'cache'
    cache.mkdir(parents=True,exist_ok=True)
    token=hashlib.sha256(str(ROOT).encode()).hexdigest()[:16]
    filename=cache/('pixbuf-'+token+'.cache')
    if not filename.is_file():
        result=subprocess.run([str(query),*map(str,loaders)],capture_output=True,timeout=20,creationflags=0x08000000)
        if result.returncode:raise RuntimeError('Não foi possível configurar os carregadores de imagem.')
        filename.write_bytes(result.stdout)
    os.environ['GDK_PIXBUF_MODULE_FILE']=str(filename)


def probe(destination):
    import gi
    gi.require_version('Gtk','3.0');gi.require_version('Poppler','0.18')
    from gi.repository import Gtk,Poppler
    import cairo,_quickjs
    from version import VERSION
    from pdf_dependency import configure_pdf_library
    configure_pdf_library()
    from pypdf import PdfWriter,PdfReader
    import tempfile
    from pdf_form_javascript import available,run_form_javascript
    result=dict(schema='linuxit-windows-installed-probe-v1',version=VERSION,checks={})
    result['checks']['gtk_initialized']=bool(Gtk.init_check()[0])
    result['checks']['quickjs_calculation']=_quickjs.Context().eval('[1,2,3].reduce((a,b)=>a+b,0)')==6
    result['checks']['quickjs_worker_dependency']=available()
    # RC4 lives in the OpenSSL 3 legacy provider; old encrypted PDFs need it.
    result['openssl_paths']={name:os.environ.get(name) for name in ('OPENSSL_CONF','OPENSSL_MODULES')}
    result['openssl_unresolved']=list(OPENSSL_LIMITS)
    try:
        try:from cryptography.hazmat.decrepit.ciphers.algorithms import ARC4
        except ImportError:from cryptography.hazmat.primitives.ciphers.algorithms import ARC4
        from cryptography.hazmat.primitives.ciphers import Cipher
        result['checks']['rc4_legacy_provider']=Cipher(ARC4(b'k'*16),mode=None).encryptor().update(b'abc')!=b'abc'
    except Exception as exc:
        result['rc4_error']=type(exc).__name__+': '+str(exc)[:300]
        result['checks']['rc4_legacy_provider']=False
    from pypdf.generic import DictionaryObject,NameObject,TextStringObject,ArrayObject
    form_document=PdfWriter();form_document.add_blank_page(200,200)
    action=DictionaryObject({NameObject('/S'):NameObject('/JavaScript'),NameObject('/JS'):TextStringObject('event.value="v="+event.value;')})
    field=DictionaryObject({NameObject('/FT'):NameObject('/Tx'),NameObject('/T'):TextStringObject('entry'),NameObject('/V'):TextStringObject('0'),NameObject('/AA'):DictionaryObject({NameObject('/F'):action})})
    form_document.root_object[NameObject('/AcroForm')]=DictionaryObject({NameObject('/Fields'):ArrayObject([form_document._add_object(field)])})
    values,display=run_form_javascript(form_document,{'entry':'4'})
    result['checks']['quickjs_worker_executed']=values.get('entry')=='4' and display.get('entry')=='v=4'
    # Windows keeps a file locked while Poppler holds it: release the document
    # before the folder is removed (CI 39899979222, ASCII control).
    with tempfile.TemporaryDirectory(prefix='linuxit-installed-',ignore_cleanup_errors=True) as folder:
        path=Path(folder)/'fixture.pdf';writer=PdfWriter();writer.add_blank_page(200,200);writer.write(path)
        document=Poppler.Document.new_from_file(path.as_uri(),None)
        result['checks']['poppler_pdf_opened']=document.get_n_pages()==1
        page=document.get_page(0)
        surface=cairo.ImageSurface(cairo.FORMAT_ARGB32,200,200);page.render(cairo.Context(surface))
        result['checks']['cairo_rendered']=surface.get_width()==200 and len(PdfReader(path).pages)==1
        del page,document,surface
        import gc;gc.collect()
    result['installation_root']=str(ROOT)
    result['ascii_alias_used']=os.environ.get('LINUXIT_ASCII_ALIAS')=='1'
    result['passed']=all(result['checks'].values())
    Path(destination).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return 0 if result['passed'] else 1


if __name__=='__main__':
    configure_pixbuf()
    if len(sys.argv)==3 and sys.argv[1]=='--probe':raise SystemExit(probe(sys.argv[2]))
    from main import main
    main()
