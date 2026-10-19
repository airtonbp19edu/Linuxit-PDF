import hashlib,json,os,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
from tool_preferences import DEFAULTS,read_tool_preferences,save_tool_preferences
from reading_preferences import preferences_path
from pdf_ocr import validate_request,invoke_ocr
from test_attachment_search import text_pdf
from pypdf import PdfReader


class ToolPreferenceTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        self.environment=patch.dict(os.environ,{'XDG_CONFIG_HOME':str(self.root/'config')});self.environment.start();self.addCleanup(self.environment.stop)

    def test_tool_preferences_roundtrip_and_invalid_file_fall_back_without_paths(self):
        values=dict(DEFAULTS,speech_rate=220,ocr_psm=6,ocr_language='por+eng')
        save_tool_preferences(values);self.assertEqual(read_tool_preferences(),values)
        path=preferences_path().with_name('tools.json');self.assertEqual(set(json.loads(path.read_text())),set(DEFAULTS))
        path.write_text('{');self.assertEqual(read_tool_preferences(),DEFAULTS)
        with self.assertRaises(ValueError):save_tool_preferences(dict(DEFAULTS,speech_rate=True))

    def test_failed_settings_publication_preserves_previous_and_cleans_staging(self):
        save_tool_preferences(DEFAULTS);path=preferences_path().with_name('tools.json');before=path.read_bytes()
        with patch('tool_preferences.os.replace',side_effect=OSError('disk full')),self.assertRaises(OSError):save_tool_preferences(dict(DEFAULTS,ocr_dpi=150))
        self.assertEqual(path.read_bytes(),before);self.assertEqual(list(path.parent.glob('.tools-*')),[])

    def test_selected_ocr_pages_and_layout_refuse_duplicate_or_invalid_values(self):
        good=dict(source_sha256='a'*64,language='por',dpi=150,pages=[1,3],psm=6)
        self.assertEqual(validate_request(good),('a'*64,'por',150))
        for kwargs in [dict(pages=[]),dict(pages=[1,1]),dict(pages=[True]),dict(pages=[21]),dict(psm=13),dict(psm=True)]:
            with self.subTest(kwargs=kwargs),self.assertRaises(ValueError):validate_request(dict(good,**kwargs))

    @unittest.skipIf(os.name=='nt','Native Linux Poppler/Tesseract')
    def test_selected_page_ocr_keeps_other_page_text_and_original_intact(self):
        source=self.root/'source.pdf';source.write_bytes(text_pdf(['ALPHA EXAMPLE','PRESERVE VECTOR TEXT']))
        before=source.read_bytes();target=self.root/'ocr.pdf'
        report=invoke_ocr(source,target,dict(source_sha256=hashlib.sha256(before).hexdigest(),language='eng',dpi=150,pages=[1],psm=6))
        self.assertEqual(report['rasterized_pages'],[1]);self.assertTrue(report['pages_info'][0]['ocr_applied']);self.assertFalse(report['pages_info'][1]['ocr_applied'])
        self.assertIn('PRESERVE VECTOR TEXT',PdfReader(target).pages[1].extract_text());self.assertEqual(source.read_bytes(),before)
