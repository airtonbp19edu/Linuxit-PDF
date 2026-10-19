import hashlib,os,sys,tempfile,unittest,wave
from io import BytesIO
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
from pypdf import PdfReader,PdfWriter
from pypdf.generic import DictionaryObject,NameObject,ArrayObject,DecodedStreamObject,NumberObject
from pdf_media import inspect_media,extract_media
from pdf_changes import save_edited_copy
from pdf_layers import inspect_layers
from test_measurement_layers_speech import layer_pdf


class MediaLayerPersistenceTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name);self.source=self.root/'source.pdf'

    def fixture(self):
        output=BytesIO()
        with wave.open(output,'wb') as audio:
            audio.setnchannels(1);audio.setsampwidth(1);audio.setframerate(8000);audio.writeframes(b'\x80'*800)
        self.wav=output.getvalue();writer=PdfWriter();page=writer.add_blank_page(200,200)
        entry=writer.add_attachment('track.wav',self.wav)
        movie=DictionaryObject({NameObject('/Subtype'):NameObject('/Movie'),NameObject('/Movie'):DictionaryObject({NameObject('/F'):entry.pdf_object})})
        sound=DecodedStreamObject();sound.set_data(b'\x00\x01\xff\xfe'*20)
        sound.update({NameObject('/R'):NumberObject(8000),NameObject('/C'):NumberObject(1),NameObject('/B'):NumberObject(16),NameObject('/E'):NameObject('/Signed')})
        sound_annotation=DictionaryObject({NameObject('/Subtype'):NameObject('/Sound'),NameObject('/Sound'):writer._add_object(sound)})
        model=DecodedStreamObject();model.set_data(b'SYNTHETIC U3D fixture, not a renderable model');model[NameObject('/Subtype')]=NameObject('/U3D')
        three_d=DictionaryObject({NameObject('/Subtype'):NameObject('/3D'),NameObject('/3DD'):writer._add_object(model)})
        # External URLs never become a source for the media player.
        external=DictionaryObject({NameObject('/Subtype'):NameObject('/Movie'),NameObject('/Movie'):DictionaryObject({NameObject('/F'):DictionaryObject({NameObject('/F'):NameObject('/https://example.invalid/')})})})
        page[NameObject('/Annots')]=ArrayObject(writer._add_object(a) for a in (movie,sound_annotation,three_d,external));writer.write(self.source)

    def test_embedded_movie_sound_and_3d_are_passive_and_external_urls_ignored(self):
        self.fixture();before=self.source.read_bytes();report=inspect_media(self.source,{})
        self.assertEqual([row['kind'] for row in report['assets']],['file','sound','3d'])
        self.assertFalse(report['three_d_renderer_available']);self.assertFalse(report['actions_executed']);self.assertFalse(report['network_used'])
        self.assertEqual(before,self.source.read_bytes())
        target=self.root/'movie.wav';extract_media(self.source,dict(index=0,destination=str(target),source_sha256=report['source_sha256']))
        self.assertEqual(target.read_bytes(),self.wav)

    def test_pdf_sound_big_endian_pcm_is_converted_to_little_endian_wave(self):
        self.fixture();report=inspect_media(self.source,{});target=self.root/'sound.wav'
        extract_media(self.source,dict(index=1,destination=str(target),source_sha256=report['source_sha256']))
        with wave.open(str(target),'rb') as sound:
            self.assertEqual(sound.getframerate(),8000);self.assertEqual(sound.getsampwidth(),2);self.assertEqual(sound.readframes(2),b'\x01\x00\xfe\xff')

    def test_changed_source_existing_target_wrong_extension_and_copy_denial_preserve_outputs(self):
        self.fixture();report=inspect_media(self.source,{});target=self.root/'movie.wav';target.write_bytes(b'preserve')
        with self.assertRaises(FileExistsError):extract_media(self.source,dict(index=0,destination=str(target),source_sha256=report['source_sha256']))
        self.assertEqual(target.read_bytes(),b'preserve')
        with self.assertRaises(ValueError):extract_media(self.source,dict(index=0,destination=str(self.root/'bad.exe'),source_sha256=report['source_sha256']))
        with self.assertRaises(ValueError):extract_media(self.source,dict(index=0,destination=str(self.root/'new.wav'),source_sha256='0'*64))

    def test_layer_configuration_saved_reopened_without_changing_original(self):
        layer_pdf(self.source);before=self.source.read_bytes();target=self.root/'layers.pdf'
        save_edited_copy(self.source,target,source_sha256=hashlib.sha256(before).hexdigest(),operations=[dict(kind='set-layer-visibility',visible=[False,True])])
        self.assertEqual([row['visible'] for row in inspect_layers(PdfReader(target))],[False,True]);self.assertEqual(before,self.source.read_bytes())

    def test_layer_configuration_save_preserves_encryption_and_locked_guard(self):
        layer_pdf(self.source);writer=PdfWriter(clone_from=self.source);writer.encrypt('user','owner',algorithm='AES-256');writer.write(self.root/'encrypted.pdf')
        source=self.root/'encrypted.pdf';target=self.root/'layers.pdf'
        save_edited_copy(source,target,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),operations=[dict(kind='set-layer-visibility',visible=[False,True])],auth=dict(password='owner',recover=False))
        reader=PdfReader(target);self.assertTrue(reader.is_encrypted);self.assertTrue(reader.decrypt('user'));self.assertEqual([r['visible'] for r in inspect_layers(reader)],[False,True])
        layer_pdf(self.source,locked=True)
        with self.assertRaises(ValueError):save_edited_copy(self.source,self.root/'locked.pdf',source_sha256=hashlib.sha256(self.source.read_bytes()).hexdigest(),operations=[dict(kind='set-layer-visibility',visible=[False,True])])
