"""Own preference persistence and explicit conversion of animation frames."""
import json,os,tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
from test_pdf_creation import creation,Image,PdfReader
from reading_preferences import read_preferences,save_preferences,preferences_path,DEFAULTS


class PreferencesAnimationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.environment=patch.dict(os.environ,{'XDG_CONFIG_HOME':str(self.root/'config')});self.environment.start()

    def tearDown(self):self.environment.stop();self.temp.cleanup()

    def test_preferences_roundtrip_and_invalid_or_truncated_file_falls_back(self):
        self.assertEqual(read_preferences(),DEFAULTS)
        values=dict(zoom_mode='percent',zoom_percent=175,sidebar=False,highlight_all=False)
        save_preferences(values);self.assertEqual(read_preferences(),values)
        self.assertEqual(set(json.loads(preferences_path().read_text())),set(DEFAULTS))
        for raw in ('{','{"zoom_percent":true}','x'*8193):
            preferences_path().write_text(raw);self.assertEqual(read_preferences(),DEFAULTS)

    def test_failed_preference_write_preserves_old_values_and_cleans_staging(self):
        save_preferences(DEFAULTS);before=preferences_path().read_bytes()
        with patch('reading_preferences.os.replace',side_effect=OSError('disk full')),self.assertRaises(OSError):
            save_preferences(dict(DEFAULTS,zoom_percent=200))
        self.assertEqual(preferences_path().read_bytes(),before)
        self.assertEqual(list(preferences_path().parent.glob('.reading-*')),[])
        with self.assertRaises(ValueError):save_preferences(dict(DEFAULTS,zoom_percent=True))

    def test_gif_apng_webp_frames_expand_only_when_explicitly_requested(self):
        for suffix,format_ in [('gif','GIF'),('png','PNG'),('webp','WEBP')]:
            with self.subTest(format=format_):
                source=self.root/('animation.'+suffix);target=self.root/(suffix+'.pdf')
                with Image.new('RGB',(8,6),'red') as first,Image.new('RGB',(8,6),'blue') as second:
                    first.save(source,format=format_,save_all=True,append_images=[second],duration=100,**({'lossless':True} if format_=='WEBP' else {}))
                before=source.read_bytes()
                with self.assertRaises(ValueError):creation.create_pdf_from_images(target,dict(paths=[str(source)],dpi=72))
                result=creation.invoke_image_creation(target,dict(paths=[str(source)],dpi=72,frames='all'))
                self.assertEqual(result['pages'],2)
                self.assertEqual([row['frame'] for row in result['sources']],[1,2])
                self.assertEqual(source.read_bytes(),before)
                pages=PdfReader(target).pages
                self.assertEqual(pages[0]['/Resources']['/XObject']['/Im1'].get_data(),bytes((255,0,0))*48)
                self.assertEqual(pages[1]['/Resources']['/XObject']['/Im1'].get_data(),bytes((0,0,255))*48)

    def test_frame_limit_refuses_whole_import_without_partial_pdf(self):
        source=self.root/'many.gif';target=self.root/'out.pdf'
        frames=[Image.new('RGB',(3,3),color) for color in ('red','green','blue')]
        try:frames[0].save(source,save_all=True,append_images=frames[1:],duration=100)
        finally:
            for frame in frames:frame.close()
        with patch.object(creation,'MAX_PAGES',2),self.assertRaises(ValueError):
            creation.create_pdf_from_images(target,dict(paths=[str(source)],dpi=72,frames='all'))
        self.assertFalse(target.exists())

    def test_portable_pixmap_and_icon_are_decoded_as_static_images(self):
        for suffix,format_ in [('ppm','PPM'),('ico','ICO')]:
            source=self.root/('image.'+suffix);target=self.root/(suffix+'.pdf')
            with Image.new('RGB',(32,32),'red') as image:image.save(source,format=format_,**({'sizes':[(32,32)]} if suffix=='ico' else {}))
            result=creation.create_pdf_from_images(target,dict(paths=[str(source)],dpi=72))
            self.assertEqual(result['pages'],1);self.assertEqual(result['sources'][0]['format'],format_)


@unittest.skipUnless(os.environ.get('DISPLAY'),'Requires GTK and X display')
class ReadingPreferencesGUITests(unittest.TestCase):
    def test_saved_preferences_are_applied_when_opening_next_pdf(self):
        from main import PDFWindow,Gtk
        from test_gui import wait_for
        from test_attachment_search import text_pdf
        with tempfile.TemporaryDirectory() as directory,patch.dict(os.environ,{'XDG_CONFIG_HOME':directory}),patch.object(Gtk,'main_quit'):
            source=Path(directory)/'source.pdf';source.write_bytes(text_pdf(['alpha']))
            save_preferences(dict(zoom_mode='percent',zoom_percent=175,sidebar=False,highlight_all=False))
            window=PDFWindow(str(source))
            try:
                wait_for(lambda:window.displayed_page==0)
                self.assertEqual((window.zoom_mode,window.zoom_percent),('percent',175))
                self.assertFalse(window.sidebar_visible);self.assertFalse(window.find_highlight_all.get_active())
            finally:window.destroy()
