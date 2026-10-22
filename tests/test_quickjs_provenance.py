import importlib.util,io,json,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('linuxit_prepare_js',ROOT/'scripts/prepare_js_runtime.py')
runtime=importlib.util.module_from_spec(spec);spec.loader.exec_module(runtime)

class QuickJSProvenanceTests(unittest.TestCase):
    def test_known_version_source_and_wheel_are_statically_pinned(self):
        pins=json.loads(runtime.PINS.read_text(encoding='utf-8'))
        self.assertEqual(pins['version'],runtime.VERSION)
        self.assertEqual(pins['source']['sha256'],'fab189fb7c46d6d33561f27af8bc128a309833db48cca76ffbf311bf0ebcb542')
        self.assertEqual(pins['linux_x86_64_wheel']['sha256'],'697576e6fb769070dc5955da84c3512f891d269c582fbe0ebe86c174ab130e8d')
    def test_tampered_download_fails_before_install(self):
        with patch.object(runtime.urllib.request,'urlopen',return_value=io.BytesIO(b'bad')):
            with self.assertRaisesRegex(ValueError,'digest'):runtime.download_verified(dict(url='https://files.pythonhosted.org/a',bytes=3,sha256='0'*64))
    def test_unapproved_host_is_never_contacted(self):
        with patch.object(runtime.urllib.request,'urlopen') as request:
            with self.assertRaises(ValueError):runtime.download_verified(dict(url='https://example.com/a',bytes=3,sha256='0'*64))
            request.assert_not_called()
