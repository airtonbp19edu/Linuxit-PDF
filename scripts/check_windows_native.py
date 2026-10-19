#!/usr/bin/env python3
"""Own reader on native Windows GTK/Poppler; never starts the reference app."""
import argparse,hashlib,json,os,platform,sys,tempfile,time
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'app'),str(ROOT/'tests')]


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True,type=Path);args=parser.parse_args()
    if args.output.exists() or os.name!='nt':parser.error('New output and native Windows required')
    report=dict(schema='linuxit-windows-native-v1',passed=False,checks={},errors=[],foxit_executed=False,
                native_windows=True,platform=platform.platform(),physical_printing=False,whole_family_acceptance=False)
    try:
        import gi
        gi.require_version('Gtk','3.0');from gi.repository import Gtk,GLib,Gdk
        from test_attachment_search import text_pdf
        from main import PDFWindow,load_css
        from character_extraction import page_characters
        from rendering import document_info
        from pdf_changes import save_edited_copy
        from pypdf import PdfReader
        with tempfile.TemporaryDirectory(prefix='linuxit-own-windows-') as directory,patch.object(Gtk,'main_quit'):
            source=Path(directory)/'fixture.pdf';source.write_bytes(text_pdf(['ALPHA native Windows','BETA second page']))
            original=source.read_bytes();identity=hashlib.sha256(original).hexdigest()
            report['checks']['poppler_pdf_information']=document_info(str(source))['pages']==2
            chars=page_characters(str(source),0)
            report['checks']['native_character_geometry']=bool(chars['boxes']) and 'ALPHA' in chars['text']
            load_css();window=PDFWindow();errors=[];window._error=errors.append;window.open_document(str(source))
            try:
                deadline=time.monotonic()+45;context=GLib.MainContext.default()
                while time.monotonic()<deadline and window.displayed_page!=0:
                    while context.pending():context.iteration(False)
                    time.sleep(.02)
                report['checks']['actual_reader_page_rendered']=window.displayed_page==0 and window.page_count==2 and not errors
                window._zoom_100()
                for _ in range(50):
                    while context.pending():context.iteration(False)
                    time.sleep(.02)
                args.output.parent.mkdir(parents=True,exist_ok=True)
                surface=window.get_window()
                if surface:
                    shot=Gdk.pixbuf_get_from_window(surface,0,0,surface.get_width(),surface.get_height())
                    if shot:shot.savev(str(args.output.with_name('reader.png')),'png',[],[])
                destination=Path(directory)/'edited.pdf'
                save_edited_copy(source,destination,source_sha256=identity,operations=[dict(kind='add-note',page=0,rect=None,text='Own Windows note')])
                report['checks']['own_edited_copy_reopens']=len(PdfReader(destination).pages)==2
                report['checks']['source_preserved']=source.read_bytes()==original
                report['reader_errors']=errors
            finally:window.destroy()
        report['passed']=all(report['checks'].values()) and len(report['checks'])==5
    except Exception as exc:
        import traceback
        report['errors'].append(type(exc).__name__+': '+str(exc));traceback.print_exc()
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps(report));return 0 if report['passed'] else 1


if __name__=='__main__':raise SystemExit(main())
