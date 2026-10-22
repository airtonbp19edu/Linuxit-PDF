"""Relocatable per-user GTK/Python environment; no system settings are changed."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
RUNTIME=ROOT/'runtime'
BIN=RUNTIME/'bin'
os.environ['PATH']=str(BIN)+os.pathsep+os.environ.get('PATH','')
os.environ['GI_TYPELIB_PATH']=str(RUNTIME/'lib/girepository-1.0')
os.environ['GSETTINGS_SCHEMA_DIR']=str(RUNTIME/'share/glib-2.0/schemas')
os.environ['XDG_DATA_DIRS']=str(RUNTIME/'share')
os.environ['FONTCONFIG_PATH']=str(RUNTIME/'etc/fonts')
if (RUNTIME/'etc/ssl/openssl.cnf').is_file():os.environ['OPENSSL_CONF']=str(RUNTIME/'etc/ssl/openssl.cnf')
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
    from pdf_form_javascript import available
    result=dict(schema='linuxit-windows-installed-probe-v1',version=VERSION,checks={})
    result['checks']['gtk_initialized']=bool(Gtk.init_check()[0])
    result['checks']['quickjs_calculation']=_quickjs.Context().eval('[1,2,3].reduce((a,b)=>a+b,0)')==6
    result['checks']['quickjs_worker_dependency']=available()
    with tempfile.TemporaryDirectory(prefix='linuxit-installed-') as folder:
        path=Path(folder)/'fixture.pdf';writer=PdfWriter();writer.add_blank_page(200,200);writer.write(path)
        document=Poppler.Document.new_from_file(path.as_uri(),None)
        result['checks']['poppler_pdf_opened']=document.get_n_pages()==1
        surface=cairo.ImageSurface(cairo.FORMAT_ARGB32,200,200);document.get_page(0).render(cairo.Context(surface))
        result['checks']['cairo_rendered']=surface.get_width()==200 and len(PdfReader(path).pages)==1
    result['passed']=all(result['checks'].values())
    Path(destination).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return 0 if result['passed'] else 1


if __name__=='__main__':
    configure_pixbuf()
    if len(sys.argv)==3 and sys.argv[1]=='--probe':raise SystemExit(probe(sys.argv[2]))
    from main import main
    main()
