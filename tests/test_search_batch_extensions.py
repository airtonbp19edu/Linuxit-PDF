"""Own passive formats, index maintenance and pinned Snowball integration."""
from io import BytesIO
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from test_attachment_search import request, text_pdf
from pypdf import PdfWriter
from attachment_formats import extract_passive_text
from attachment_search import search_attachment_text
import collection_index as index
from search_matching import query_spans, normalized
from search_engine import TextSearchIndex


def office(name, body, extra=None):
    out = BytesIO()
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(name, body)
        if extra:archive.writestr(*extra)
    return out.getvalue()


class SearchBatchExtensionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory();self.root = Path(self.temp.name)

    def tearDown(self):self.temp.cleanup()

    def test_docx_odt_and_html_search_without_extracting_or_executing_anything(self):
        path = self.root/'host.pdf';writer=PdfWriter();writer.add_blank_page(200,200)
        writer.add_attachment('body.docx', office('word/document.xml', '<doc><p><r><t>alvo</t></r></p></doc>'))
        writer.add_attachment('body.odt', office('content.xml', '<body><p>alvo &amp; texto</p></body>'))
        writer.add_attachment('body.html', b'<p>alvo</p><script>alvo</script><img src="https://invalid.example/">')
        writer.write(path);before=path.read_bytes()
        result=search_attachment_text(path,request())
        self.assertCountEqual([h['attachment_name'] for h in result['hits']], ['body.docx','body.odt','body.html'])
        self.assertEqual(len(result['omissions']),2)  # Office body-only contract.
        self.assertFalse(result['complete'])
        self.assertEqual(path.read_bytes(),before)
        self.assertEqual(list(self.root.iterdir()),[path])

    def test_bad_zip_entities_expansion_and_unsupported_encoding_are_rejected(self):
        for raw in [b'broken',office('word/document.xml','<!DOCTYPE a [<!ENTITY a "x">]><p>&a;</p>'),
                    office('word/document.xml','<p>ok</p>',('large','x'*3000000))]:
            with self.subTest(size=len(raw)),self.assertRaises(ValueError):extract_passive_text(raw,'.docx')
        with self.assertRaises(UnicodeError):extract_passive_text(b'\xff\xfea\x00','.html')

    def test_rich_runs_remain_adjacent_and_paragraphs_are_separated(self):
        raw=office('word/document.xml','<doc><p><r><t>docu</t></r><r><t>mento</t></r></p><p>novo</p></doc>')
        self.assertEqual(extract_passive_text(raw,'.docx')[0],'documento novo')

    def test_index_review_removes_unselected_source_and_refreshes_changed_text(self):
        a,b=self.root/'a.pdf',self.root/'b.pdf';dest=self.root/'set.linuxit-index.json'
        a.write_bytes(text_pdf(['old']));b.write_bytes(text_pdf(['excluded']))
        index.build_index(dest,{'paths':[str(a),str(b)]})
        _,identity=index.load_index(dest)
        a.write_bytes(text_pdf(['updated']))
        report=index.build_index(dest,{'paths':[str(a)],'expected_index_sha256':identity})
        self.assertEqual(report['documents'],1)
        self.assertEqual(len(index.search_index(dest,request('updated'))['hits']),1)
        self.assertEqual(index.search_index(dest,request('excluded'))['hits'],[])
        before=dest.read_bytes()
        with self.assertRaisesRegex(ValueError,'mudou desde'):
            index.build_index(dest,{'paths':[str(a)],'expected_index_sha256':identity})
        self.assertEqual(dest.read_bytes(),before)

    def test_competing_writer_is_refused_and_does_not_remove_someone_elses_lock(self):
        source=self.root/'a.pdf';source.write_bytes(text_pdf(['alpha']))
        dest=self.root/'set.linuxit-index.json'
        with index.index_writer_lock(dest):
            lock=dest.with_name(dest.name+'.lock');before=lock.read_bytes()
            with self.assertRaisesRegex(ValueError,'trava'):
                index.build_index(dest,{'paths':[str(source)]})
            self.assertEqual(lock.read_bytes(),before)
        self.assertFalse(lock.exists());self.assertFalse(dest.exists())

    def test_portuguese_and_english_stemming_match_words_and_preserve_actual_spans(self):
        for text,query,mode,expected in [('documentos documento mineral','documento','stem-pt',['documentos','documento']),
                                       ('running runs runner','run','stem-en',['running','runs'])]:
            spans=list(query_spans(text,query,mode=mode))
            self.assertEqual([text[a:b] for a,b in spans],expected)
        text='PRINTING documents printed document'
        spans=list(query_spans(text,'print document',mode='stem-en'))
        self.assertEqual([text[a:b] for a,b in spans],['PRINTING documents','printed document'])
        self.assertEqual(list(query_spans('abc','*',mode='literal')),[])
        with self.assertRaises(ValueError):list(query_spans('abc','a*',mode='stem-pt'))

    def test_stemming_is_available_in_attachment_worker_and_saved_index(self):
        host=self.root/'host.pdf';writer=PdfWriter();writer.add_blank_page(200,200)
        writer.add_attachment('readme.txt',b'running runs runner');writer.write(host)
        model=TextSearchIndex(host,1,page_sizes=[(200,200)])
        self.assertEqual(len(model.search('run',mode='stem-en',include_page_text=False,include_attachments=True)),2)
        source=self.root/'a.pdf';source.write_bytes(text_pdf(['documents document']))
        dest=self.root/'set.linuxit-index.json';index.build_index(dest,{'paths':[str(source)]})
        self.assertEqual(len(index.invoke_collection('index-search',dest,request('document',mode='stem-en'))['hits']),2)

    def test_vendored_snowball_files_match_the_pinned_distribution_and_include_license(self):
        root=Path(__file__).resolve().parents[1]
        provenance=json.loads((root/'docs/proveniencia-snowball.json').read_text())
        self.assertEqual(provenance['version'],'3.1.1')
        for name,digest in provenance['files'].items():
            self.assertEqual(hashlib.sha256((root/name).read_bytes()).hexdigest(),digest)
        self.assertIn('Redistribution and use',(root/'app/vendor/snowballstemmer/COPYING').read_text())


@unittest.skipUnless(os.environ.get('DISPLAY'),'Requires GTK and X display')
class SearchBatchGUITests(unittest.TestCase):
    def test_stemming_modes_are_exposed_in_reader_and_collection(self):
        from test_gui import wait_for
        from main import PDFWindow,Gtk
        from collection_window import CollectionWindow
        with tempfile.TemporaryDirectory() as directory,patch.object(Gtk,'main_quit'):
            path=Path(directory)/'gui.pdf';path.write_bytes(text_pdf(['running runs runner']))
            window=PDFWindow(str(path));collection=None
            try:
                wait_for(lambda:window.displayed_page==0)
                window.find_mode.set_active_id('stem-en');window.find_entry.set_text('run')
                wait_for(lambda:len(window.search_hits)==2 and not window.search_running)
                self.assertFalse(window.find_options['match_case'].get_sensitive())
                collection=CollectionWindow(window,lambda *_:None)
                collection.mode.set_active_id('stem-pt')
                self.assertFalse(collection.flags['match_case'].get_sensitive())
            finally:
                if collection:collection.destroy()
                window.destroy()
