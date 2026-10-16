#!/usr/bin/env python3
"""Exercise the actual GTK reader in its Flatpak or source runtime."""
from pathlib import Path
import json,os,sys,tempfile,time
app=Path(os.environ.get('PRINT_VIEW_TEST_APP',Path(__file__).resolve().parents[1]/'app'))
sys.path.insert(0,str(app))
import cairo
from main import PDFWindow,GLib,Gtk,load_css
from pypdf import PdfReader,PdfWriter
from pypdf.annotations import Text
from pypdf.generic import NameObject,TextStringObject
from imposition import create_booklet

checks={};errors=[];started=time.monotonic();state='open'
with tempfile.TemporaryDirectory(prefix='linuxit-smoke-') as directory:
    root=Path(directory);raw=root/'raw.pdf';pdf=root/'fixture.pdf'
    surface=cairo.PDFSurface(str(raw),420,595);cr=cairo.Context(surface);cr.set_font_size(18)
    for text in ['alvo texto alvo','segunda página']:
        cr.move_to(40,70);cr.show_text(text);cr.show_page()
    surface.finish()
    writer=PdfWriter();writer.append(raw);writer.add_outline_item('ALVO marcador',1)
    note=Text(rect=(40,40,100,80),text='alvo em comentário');note[NameObject('/Subj')]=TextStringObject('Assunto separado')
    writer.add_annotation(0,note);writer.write(pdf)
    load_css();window=PDFWindow(str(pdf));window._error=lambda message:errors.append(str(message))
    def finish(message=None):
        if message:errors.append(message)
        window.destroy()
        return False
    def step():
        global state
        try:
            if errors:return finish()
            if state=='open' and window.displayed_page==0 and window.current_pixbuf:
                checks['opened_and_rendered']=window.page_count==2 and window.get_title().endswith(' — Linuxit PDF')
                window.find_entry.set_text('alvo');state='highlight'
            elif state=='highlight' and not window.search_running and len(window.search_hits)==2:
                def painted():
                    surface=cairo.ImageSurface(cairo.FORMAT_ARGB32,window.current_pixbuf.get_width(),window.current_pixbuf.get_height())
                    window._interaction_draw(window.interaction_layer,cairo.Context(surface));surface.flush()
                    data=surface.get_data();values=[]
                    for hit in window.search_hits:
                        x0,y0,x1,y1=window._pdf_rect_to_display(hit['rects'][0],hit)
                        offset=int((y0+y1)/2)*surface.get_stride()+int((x0+x1)/2)*4
                        values.append(int.from_bytes(data[offset:offset+4],sys.byteorder)>>24)
                    return [value>0 for value in values]
                both=painted()==[True,True]
                window.find_highlight_all.set_active(False)
                first=painted()==[True,False]
                window._find_next();second=painted()==[False,True]
                window.find_highlight_all.set_active(True)
                checks['search_highlight_preference']=both and first and second and painted()==[True,True]
                window.find_options['include_page_text'].set_active(False)
                window.find_options['include_bookmarks'].set_active(True)
                window.find_entry.set_text('alvo');state='bookmark'
            elif state=='bookmark' and not window.search_running and window.search_hits and window.displayed_page==1:
                checks['bookmark_scope_navigation']=len(window.search_hits)==1 and window.search_hits[0]['source']=='bookmark'
                window.find_options['include_bookmarks'].set_active(False)
                window.find_options['include_comments'].set_active(True)
                window.find_entry.set_text('assunto');state='comment'
            elif state=='comment' and not window.search_running and window.search_hits and window.displayed_page==0:
                checks['comment_subject_navigation']=len(window.search_hits)==1 and window.search_hits[0]['source']=='comment'
                output=root/'booklet.pdf';create_booklet(str(pdf),str(output))
                reader=PdfReader(output)
                checks['booklet_pdf_written']=len(reader.pages)==2 and 'alvo texto' in ''.join(p.extract_text() for p in reader.pages)
                return finish()
            return True
        except Exception as error:return finish(str(error))
    GLib.timeout_add(20,step)
    GLib.timeout_add_seconds(25,lambda:finish('Application smoke timeout'))
    Gtk.main()
report={'passed':len(checks)==5 and all(checks.values()) and not errors,'checks':checks,'errors':errors,
        'elapsed_sec':time.monotonic()-started,'inside_flatpak':Path('/.flatpak-info').exists(),
        'foxit_differential_test':False,'physical_printing_verified':False}
print(json.dumps(report,ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
