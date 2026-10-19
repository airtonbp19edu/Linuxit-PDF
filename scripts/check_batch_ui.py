#!/usr/bin/env python3
"""Capture new own GTK workflows for visual review, separate from full suites."""
import argparse,json,os
from pathlib import Path
import sys,tempfile
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'app'),str(ROOT/'tests')]


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():parser.error('Use a new result')
    os.environ['LINUXIT_SEARCH_CAPTURE_DIR']=str(args.output.parent/'batch-ui')
    from main import PDFWindow,Gtk,GLib,load_css
    from test_search_extensions_gtk import wait_for,capture
    from test_advanced_edits import make_controls
    from pypdf.generic import NameObject,NumberObject
    from pdf_changes import inspect_editable_document
    from measurement_window import MeasurementWindow
    from signature_window import SignatureWindow
    from accessible_reader import AccessibleTextWindow
    from edit_dialogs import advanced_operation_dialog
    from test_measurement_layers_speech import layer_pdf
    checks=[];callback_errors=[]
    with tempfile.TemporaryDirectory(prefix='linuxit-batch-ui-') as directory,patch.object(Gtk,'main_quit'),patch.object(sys,'excepthook',lambda *exc:callback_errors.append(str(exc[1]))):
        root=Path(directory);source=root/'synthetic.pdf';writer,_,_,choices=make_controls(source)
        choices['combo'][NameObject('/Ff')]=NumberObject((1<<17)|(1<<18));writer.write(source)
        load_css();window=PDFWindow(str(source));children=[]
        def modal(title,action,name):
            def respond():
                dialog=next((w for w in Gtk.Window.list_toplevels() if isinstance(w,Gtk.Dialog) and w.get_title()==title),None)
                if not dialog:return True
                capture(dialog,name);dialog.response(Gtk.ResponseType.CANCEL);checks.append(name);return False
            timer=GLib.timeout_add(150,respond)
            try:action()
            finally:
                if not checks or checks[-1]!=name:GLib.source_remove(timer)
        try:
            wait_for(lambda:window.displayed_page==0 and window._pending_document is None)
            window._show_find();window.find_options['include_page_text'].set_active(False)
            window.find_options['include_comments'].set_active(True);window.find_entry.set_text('Original')
            wait_for(lambda:len(window.search_hits)==1 and not window.search_running)
            capture(window,'reader-comment-destination');checks.append('reader-comment-destination')
            info=inspect_editable_document(source)
            modal('Desenhar à mão livre',lambda:advanced_operation_dialog(window,'add-ink',info,0),'ink-pad')
            modal('Responder comentário',lambda:advanced_operation_dialog(window,'add-reply',info,0),'reply-dialog')
            modal('Preencher caixas e listas',lambda:advanced_operation_dialog(window,'fill-form-controls',info,0),'form-controls')
            modal('Preferências de leitura',window._reading_preferences,'reading-preferences')
            measurement=MeasurementWindow(window,window.current_pixbuf,window._page_dimensions_rotated(),'synthetic')
            children.append(measurement);measurement.points=[(10,10),(100,10),(100,100),(10,100)]
            measurement.kind.set_active_id('area');measurement._measure();measurement.show_all()
            capture(measurement,'calibrated-measurements');checks.append('calibrated-measurements');measurement.hide()
            signatures=SignatureWindow(window,source);children.append(signatures);signatures.show_all()
            capture(signatures,'local-signature-entry');checks.append('local-signature-entry');signatures.hide()
            accessible=AccessibleTextWindow(window);children.append(accessible);accessible.show_all()
            accessible.heading.set_text('Texto sintético para tecnologia assistiva e voz')
            accessible.text.get_buffer().set_text('Texto de demonstração: voz local em português e inglês, sem nuvem.')
            capture(accessible,'accessible-voice-entry');checks.append('accessible-voice-entry');accessible.hide()
            layers=root/'layers.pdf';layer_pdf(layers);window.open_document(layers)
            wait_for(lambda:window.filepath==str(layers.resolve()) and len(getattr(window,'layer_checks',[]))==2)
            window._show_side_panel(3);window.layer_checks[0].set_active(False)
            wait_for(lambda:window.document_session.info.get('layer_override') and not window._render_pending
                     and len(window.layer_checks)==2 and window.layer_checks[0].get_sensitive())
            capture(window,'reader-layer-hidden');checks.append('reader-layer-hidden')
        finally:
            for child in children:child.destroy()
            window.destroy()
    report=dict(schema='linuxit-batch-ui-captures-v1',passed=len(checks)==9 and not callback_errors,
                captures=checks,callback_errors=callback_errors,foxit_executed=False,
                full_suite_rerun=False,physical_desktop_verified=False)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report));return 0 if report['passed'] else 1


if __name__=='__main__':raise SystemExit(main())
