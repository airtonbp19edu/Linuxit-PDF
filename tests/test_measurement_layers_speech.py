"""Real own optional-content PDFs, calibrated geometry and offline voice."""
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_attachment_search import text_pdf
from pypdf import PdfReader,PdfWriter
from pypdf.generic import ArrayObject,DictionaryObject,NameObject,TextStringObject,DecodedStreamObject
from measurement import measure,calibrated_scale
from pdf_layers import inspect_layers,create_layer_view
from document_session import DocumentSession
from speech import export_speech


def layer_pdf(path,locked=False):
    writer=PdfWriter();page=writer.add_blank_page(200,200);groups=[]
    for name in ('Red','Blue'):
        groups.append(writer._add_object(DictionaryObject({NameObject('/Type'):NameObject('/OCG'),NameObject('/Name'):TextStringObject(name)})))
    config=DictionaryObject({NameObject('/BaseState'):NameObject('/ON'),NameObject('/Order'):ArrayObject(groups)})
    if locked:config[NameObject('/Locked')]=ArrayObject([groups[0]])
    writer.root_object[NameObject('/OCProperties')]=DictionaryObject({NameObject('/OCGs'):ArrayObject(groups),NameObject('/D'):config})
    page[NameObject('/Resources')]=DictionaryObject({NameObject('/Properties'):DictionaryObject({NameObject('/R'):groups[0],NameObject('/B'):groups[1]})})
    stream=DecodedStreamObject();stream.set_data(b'/OC /R BDC 1 0 0 rg 10 10 80 80 re f EMC\n/OC /B BDC 0 0 1 rg 110 10 80 80 re f EMC\n')
    page[NameObject('/Contents')]=writer._add_object(stream);writer.write(path)


class MeasurementLayersSpeechTests(unittest.TestCase):
    def test_measurement_text_uses_portuguese_decimal_comma(self):
        from measurement import decimal_text
        self.assertEqual([decimal_text(2.54,2),decimal_text(21.0,1),decimal_text(6.4516),decimal_text(100.0)],['2,54','21,0','6,4516','100'])
        for value in (float('nan'),float('inf'),'2.54'):
            with self.subTest(value=value),self.assertRaises(ValueError):decimal_text(value)

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)

    def tearDown(self):self.temp.cleanup()

    def test_distance_perimeter_area_units_and_calibration_have_known_geometric_results(self):
        square=[(0,0),(72,0),(72,72),(0,72)]
        self.assertAlmostEqual(measure(square[:2],unit='in'),1)
        self.assertAlmostEqual(measure(square,'perimeter','in'),4)
        self.assertAlmostEqual(measure(square,'area','in'),1)
        self.assertAlmostEqual(measure(square[::-1],'area','cm'),6.4516)
        scale=calibrated_scale(square[:2],10,'m')
        self.assertAlmostEqual(measure(square,'area','m',scale),100)
        shifted=[(x+1000000,y-1000000) for x,y in square]
        self.assertAlmostEqual(measure(shifted,'area','in'),1)

    def test_crossing_degenerate_nonfinite_and_excessive_measurements_are_refused(self):
        for vertices in ([(0,0),(10,10),(0,10),(10,0)],[(0,0),(1,1),(2,2)],[(0,0),(float('nan'),1),(3,4)],[(0,0)]*513):
            with self.subTest(length=len(vertices)),self.assertRaises(ValueError):measure(vertices,'area')
        with self.assertRaises(ValueError):calibrated_scale([(0,0),(1,1)],0)
        with self.assertRaises(ValueError):measure([(0,0),(1,1)],unit='unknown')

    def test_layer_view_changes_only_private_copy_configuration(self):
        source=self.root/'layers.pdf';layer_pdf(source);before=source.read_bytes();target=self.root/'view.pdf'
        create_layer_view(source,target,[False,True])
        self.assertEqual([r['visible'] for r in inspect_layers(PdfReader(target))],[False,True])
        self.assertEqual(source.read_bytes(),before)
        self.assertEqual([r['visible'] for r in inspect_layers(PdfReader(source))],[True,True])

    def test_locked_layer_and_existing_destination_are_preserved(self):
        source=self.root/'layers.pdf';layer_pdf(source,True);target=self.root/'view.pdf'
        with self.assertRaises(ValueError):create_layer_view(source,target,[False,True])
        self.assertFalse(target.exists());target.write_bytes(b'old')
        with self.assertRaises(ValueError):create_layer_view(source,target,[True,False])
        self.assertEqual(target.read_bytes(),b'old')

    def test_reading_path_replacement_keeps_active_lease_and_never_deletes_original(self):
        source=self.root/'plain.pdf';source.write_bytes(text_pdf(['original']))
        session=DocumentSession(source)
        try:
            session.prepare()
            first=session.root/'first.pdf';first.write_bytes(source.read_bytes());session.replace_read_path(first)
            with session.lease() as leased:
                second=session.root/'second.pdf';second.write_bytes(source.read_bytes());session.replace_read_path(second)
                self.assertEqual(Path(leased),first);self.assertTrue(first.exists())
            self.assertFalse(first.exists());self.assertTrue(second.exists());self.assertTrue(source.exists())
        finally:session.close()
        self.assertTrue(source.exists())

    def test_voice_budget_and_missing_backend_are_explicit_without_creating_destination(self):
        target=self.root/'voice.wav'
        with self.assertRaises(ValueError):export_speech(target,dict(text='x'*20001,voice='pt-br',rate=175))
        with patch('speech.shutil.which',return_value=None),self.assertRaises(RuntimeError):
            export_speech(target,dict(text='texto',voice='pt-br',rate=175))
        self.assertFalse(target.exists())


@unittest.skipUnless(os.environ.get('DISPLAY'),'Requires GTK, Poppler and X display')
class MeasurementLayersVoiceLinuxTests(unittest.TestCase):
    def test_poppler_pixels_actually_hide_selected_layer(self):
        from rendering import render_page
        from PIL import Image
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);source=root/'source.pdf';target=root/'view.pdf';layer_pdf(source)
            create_layer_view(source,target,[False,True])
            with Image.open(render_page(str(source),0,200,str(root),'layer-before')) as image:
                self.assertGreater(image.convert('RGB').getpixel((50,150))[0],240)
                self.assertLess(image.convert('RGB').getpixel((50,150))[1],20)
            with Image.open(render_page(str(target),0,200,str(root),'layer-after')) as image:
                self.assertTrue(all(v>240 for v in image.convert('RGB').getpixel((50,150))))
                self.assertLess(image.convert('RGB').getpixel((150,150))[0],20)

    def test_measurement_window_and_reader_layer_checkbox_use_implemented_backends(self):
        from main import PDFWindow,Gtk
        from test_gui import wait_for
        from measurement_window import MeasurementWindow
        with tempfile.TemporaryDirectory() as directory,patch.object(Gtk,'main_quit'):
            source=Path(directory)/'layers.pdf';layer_pdf(source);window=PDFWindow(str(source));measurement=None
            try:
                wait_for(lambda:window.displayed_page==0 and len(getattr(window,'layer_checks',[]))==2)
                window.layer_checks[0].set_active(False)
                wait_for(lambda:window.document_session.info.get('layer_override') and not window._render_pending
                         and len(window.layer_checks)==2 and window.layer_checks[0].get_sensitive())
                self.assertFalse(window.layer_checks[0].get_active())
                self.assertNotEqual(window.document_session.read_path,str(source.resolve()))
                measurement=MeasurementWindow(window,window.current_pixbuf,(72,72),'synthetic')
                measurement.points=[(0,0),(72,0),(72,72),(0,72)];measurement.kind.set_active_id('area')
                measurement._measure();self.assertIn('6,4516',measurement.status.get_text())
                measurement.known.set_value(10);measurement._calibrate();measurement._measure()
                self.assertEqual(measurement.status.get_text(),'100 cm²')
            finally:
                if measurement:measurement.destroy()
                window.destroy()

    def test_real_offline_voice_wav_export_in_both_languages(self):
        from speech import invoke_speech
        import wave
        with tempfile.TemporaryDirectory() as directory:
            for voice,text in [('pt-br','Texto de teste local.'),('en','Local test text.')]:
                path=Path(directory)/(voice+'.wav');result=invoke_speech(path,text,voice)
                self.assertTrue(result['offline']);self.assertGreater(result['seconds'],0)
                with wave.open(str(path),'rb') as audio:self.assertGreater(audio.getnframes(),0)
