"""Real appearance objects, comment preservation, refusals and draft history."""
import hashlib
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
import pdf_changes as edits
from pdf_annotations import create_annotation
from edit_history import EditSession
from edit_tasks import invoke_edit_worker
from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Text
from pypdf.generic import DictionaryObject, IndirectObject, NameObject, NumberObject, RectangleObject
from test_advanced_edits import make_controls

KINDS = [('add-underline','/Underline'),('add-strikeout','/StrikeOut'),
         ('add-squiggly','/Squiggly'),('add-ellipse','/Circle'),('add-line','/Line')]


class AnnotationExtensionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='linuxit-annotations-');self.root = Path(self.temp.name)
        self.source,self.output = self.root/'source.pdf',self.root/'output.pdf'
        self.writer,*_ = make_controls(self.source);self.record()
    def tearDown(self):self.temp.cleanup()
    def record(self):
        self.original = self.source.read_bytes();self.identity = hashlib.sha256(self.original).hexdigest()
    def operation(self,kind,page=1,geometry=None,text='Comentário çã漢字'):
        return {'kind':kind,'page':page,('points' if kind=='add-line' else 'rect'):
                geometry if geometry is not None else [20,30,120,60],'text':text}
    def save(self,*operations):
        edits.save_edited_copy(self.source,self.output,source_sha256=self.identity,operations=list(operations))
        self.assertEqual(self.source.read_bytes(),self.original)
        return PdfReader(self.output,strict=True)
    def reject(self,operation):
        with self.assertRaises((ValueError,NotImplementedError)):
            self.save({'kind':'add-bookmark','page':0,'title':'not published'},operation)
        self.assertFalse(self.output.exists());self.assertEqual(list(self.root.glob('.linuxit-copy-*')),[])
    def last(self,reader,page=1):return reader.pages[page]['/Annots'][-1].get_object()

    def test_all_five_types_roundtrip_with_printable_embedded_appearance(self):
        reader = self.save(*(self.operation(kind) for kind,_ in KINDS))
        self.assertEqual(len(reader.pages),2);self.assertEqual(len(reader.get_fields()),5)
        self.assertEqual(next(reader.attachment_list).content,b'unchanged attachment')
        self.assertEqual(reader.outline[0].title,'Parent')
        for ref,(_,subtype) in zip(reader.pages[1]['/Annots'],KINDS):
            note = ref.get_object();ap = note['/AP']['/N']
            self.assertEqual(note['/Subtype'],subtype);self.assertEqual(note['/F'],4)
            self.assertEqual(note['/Contents'],'Comentário çã漢字');self.assertEqual(list(note['/C']),[1,0,0])
            self.assertEqual((ap['/Type'],ap['/Subtype'],ap['/FormType']),('/XObject','/Form',1))
            self.assertIsInstance(note['/AP'].raw_get('/N'),IndirectObject)
            self.assertEqual(dict(ap['/Resources']),{});self.assertTrue(ap.get_data().endswith(b'S\nQ\n'))
            self.assertNotIn('/A',note);self.assertNotIn('/AA',note);self.assertNotIn('/Popup',note)

    def test_text_markup_quad_order_and_line_and_ellipse_metadata_are_distinct(self):
        reader = self.save(*(self.operation(kind) for kind,_ in KINDS))
        notes = [a.get_object() for a in reader.pages[1]['/Annots']]
        for note in notes[:3]:self.assertEqual(list(note['/QuadPoints']),[20,30,120,30,120,60,20,60])
        self.assertNotIn('/QuadPoints',notes[3]);self.assertEqual(notes[3]['/AP']['/N'].get_data().count(b' c\n'),4)
        self.assertEqual(list(notes[4]['/L']),[20,30,120,60]);self.assertEqual(list(notes[4]['/LE']),['/None','/None'])
        self.assertNotIn('/QuadPoints',notes[4])

    def test_offsets_and_page_rotations_do_not_double_transform_geometry(self):
        appearances = []
        for angle in (0,90,180,270):
            self.writer.pages[1].cropbox = RectangleObject([10,-30,190,250])
            self.writer.pages[1][NameObject('/Rotate')] = NumberObject(angle)
            self.writer.write(self.source);self.record()
            note = self.last(self.save(self.operation('add-strikeout',geometry=[20,-20,150,10])))
            self.assertEqual(list(note['/Rect']),[20,-20,150,10])
            self.assertEqual(list(note['/AP']['/N']['/BBox']),[0,0,130,30]);appearances.append(note['/AP']['/N'].get_data())
            self.output.unlink()
        self.assertTrue(all(value==appearances[0] for value in appearances))

    def test_horizontal_vertical_and_reversed_lines_keep_endpoint_direction(self):
        for points in ([20,30,120,30],[50,250,50,40],[180,240,20,30],[20,30,20,30.25]):
            note = self.last(self.save(self.operation('add-line',geometry=points)))
            self.assertEqual(list(note['/L']),points)
            x0,y0,x1,y1 = map(float,note['/Rect']);self.assertGreater(x1,x0);self.assertGreater(y1,y0)
            self.assertEqual(list(note['/AP']['/N']['/BBox']),[0,0,x1-x0,y1-y0]);self.output.unlink()

    def test_boundary_strokes_have_positive_clipped_boxes_and_small_areas_renderable_numbers(self):
        for points in ([0,0,200,300],[0,300,0,0],[0,0,200,0]):
            note = self.last(self.save(self.operation('add-line',geometry=points)))
            x0,y0,x1,y1 = note['/Rect'];self.assertTrue(0<=x0<x1<=200 and 0<=y0<y1<=300);self.output.unlink()
        note = create_annotation('add-ellipse',[0,0,.25,.25],[0,0,.25,.25],'')
        self.assertGreater(note['/BS']['/W'],0);self.assertNotIn(b'0.000000 w',note['/AP']['/N'].get_data())

    def test_squiggly_geometry_has_bounded_commands_even_on_extreme_page(self):
        note = create_annotation('add-squiggly',[-1e7,-1e7,1e7,1e7],[-1e7,-1e7,1e7,1e7],'')
        raw = note['/AP']['/N'].get_data()
        self.assertLess(len(raw),25000);self.assertLessEqual(raw.count(b' l\n'),512)
        self.assertNotIn(b'e+',raw);self.assertNotIn(b'e-',raw)

    def test_invalid_area_and_crop_coordinates_refuse_the_entire_batch(self):
        for rect in ([True,30,50,60],[0,0,float('nan'),20],[0,0,float('inf'),20],[-1,20,30,40],
                     [20,30,20,40],[20,30,19,40],[20,30,20.1,40],[20,30,30,301],[0,0,1e8,20]):
            with self.subTest(rect=rect):self.reject(self.operation('add-ellipse',geometry=rect))
        for box in ([0,0,.1,300],[0,0,200,0],[0,0,float('inf'),300]):
            with self.assertRaises(ValueError):create_annotation('add-underline',box,[1,1,10,10],'')

    def test_invalid_line_points_page_and_extra_fields_are_rejected(self):
        for points in ([20,30,20,30],[20,30,20.1,30.1],[20,30,201,40],[20,30,False,40],[20,30,40]):
            self.reject(self.operation('add-line',geometry=points))
        for page in (True,-1,2):self.reject(self.operation('add-line',page=page))
        for kind in (None,[],{}):self.reject(dict(self.operation('add-line'),kind=kind))
        extra = self.operation('add-line');extra['rect']=[20,30,120,60];self.reject(extra)

    def test_utf8_comment_and_author_limits_and_nonstring_values_are_enforced(self):
        for text in ('ç'*(32*1024+1),None,True):self.reject(self.operation('add-underline',text=text))
        update = {'kind':'update-annotation','page':0,'index':0,'text':'ok','author':''}
        for change in ({'text':'ç'*(32*1024+1)},{'author':'ç'*2049},{'author':None},{'text':[]}):self.reject(dict(update,**change))
        reader = self.save(self.operation('add-underline',text='ç'*(32*1024)))
        self.assertEqual(len(self.last(reader)['/Contents']),32*1024)

    def test_edit_and_clear_comment_author_preserve_geometry_appearance_and_other_content(self):
        self.save(*(self.operation(kind) for kind,_ in KINDS),
                  {'kind':'add-highlight','page':1,'rect':[20,100,120,130],'text':'highlight'},
                  {'kind':'add-rectangle','page':1,'rect':[20,140,120,180],'text':'square'})
        self.source.write_bytes(self.output.read_bytes());self.output.unlink();self.record()
        old = PdfReader(self.source)
        operations = [{'kind':'update-annotation','page':1,'index':i,'text':'Novo\nçã (S Q)','author':'Autora ç'} for i in range(7)]
        reader = self.save(*operations)
        for before,after in zip(old.pages[1]['/Annots'],reader.pages[1]['/Annots']):
            before,after = before.get_object(),after.get_object()
            self.assertEqual(list(before['/Rect']),list(after['/Rect']))
            self.assertEqual(after['/Contents'],'Novo\nçã (S Q)');self.assertEqual(after['/T'],'Autora ç')
            if '/AP' in before:self.assertEqual(before['/AP']['/N'].get_data(),after['/AP']['/N'].get_data())
        self.assertEqual(next(reader.attachment_list).content,b'unchanged attachment');self.assertEqual(len(reader.get_fields()),5)
        self.output.unlink()
        reader = self.save({'kind':'update-annotation','page':0,'index':0,'text':'','author':''})
        note = reader.pages[0]['/Annots'][0].get_object();self.assertEqual(note['/Contents'],'');self.assertNotIn('/T',note)

    def test_locked_related_and_unsupported_annotations_cannot_be_changed_or_deleted(self):
        # ISO 32000-1 12.5.3: ReadOnly blocks everything; Locked blocks deletion/geometry but not
        # contents; LockedContents blocks contents but not deletion.
        note = self.writer.pages[0]['/Annots'][0].get_object()
        update = {'kind':'update-annotation','page':0,'index':0,'text':'new','author':''}
        delete = {'kind':'delete-annotation','page':0,'index':0}
        for flag,update_ok,delete_ok in ((64,False,False),(128,True,False),(512,False,True)):
            note[NameObject('/F')] = NumberObject(flag);self.writer.write(self.source);self.record()
            for operation,allowed in ((update,update_ok),(delete,delete_ok)):
                with self.subTest(flag=flag,kind=operation['kind']):
                    if allowed:self.save(operation);self.output.unlink()
                    else:self.reject(operation)
        note[NameObject('/F')] = NumberObject(4)
        for key in ('/IRT','/Popup','/Parent'):
            note[NameObject(key)] = DictionaryObject();self.writer.write(self.source);self.record()
            self.reject(update);note.pop(key)
        reply = Text(rect=(5,5,20,20),text='reply');reply[NameObject('/IRT')]=note.indirect_reference
        self.writer.add_annotation(1,reply);self.writer.write(self.source);self.record()
        # A reply on another page keeps the text editable but blocks deletion and movement.
        self.assertEqual(self.save(update).pages[0]['/Annots'][0].get_object()['/Contents'],'new');self.output.unlink()
        self.reject(delete);self.reject({'kind':'move-annotation','page':0,'index':0,'dx':1,'dy':1})
        self.reject({'kind':'update-annotation','page':0,'index':1,'text':'widget','author':''})

    def test_deleting_new_types_uses_current_indices_and_preserves_forms_notes_and_other_page(self):
        operations = [self.operation(kind) for kind,_ in KINDS]
        operations += [{'kind':'delete-annotation','page':1,'index':i} for i in reversed(range(5))]
        reader = self.save(*operations)
        self.assertEqual(len(reader.pages[1]['/Annots']),0);self.assertEqual(len(reader.get_fields()),5)
        self.assertEqual(reader.pages[0]['/Annots'][0].get_object()['/Contents'],'Original note')
        self.assertEqual(next(reader.attachment_list).content,b'unchanged attachment')

    def test_real_worker_protocol_lists_new_types_and_author_and_refuses_source_and_destination_changes(self):
        operations = [self.operation(kind) for kind,_ in KINDS]
        operations.append({'kind':'update-annotation','page':1,'index':2,'text':'changed','author':'person'})
        result = invoke_edit_worker('copy-edit',self.source,self.output,{'source_sha256':self.identity,'operations':operations})
        self.assertEqual(result['operations_applied'],6)
        info = invoke_edit_worker('edit-info',self.output)
        self.assertEqual([r['subtype'] for r in info['annotations'][1:]],[subtype for _,subtype in KINDS])
        self.assertEqual(info['annotations'][3]['author'],'person');self.assertEqual(info['annotations'][3]['text'],'changed')
        saved = self.output.read_bytes()
        with self.assertRaises(RuntimeError):invoke_edit_worker('copy-edit',self.source,self.output,{'source_sha256':self.identity,'operations':operations})
        self.assertEqual(self.output.read_bytes(),saved)
        self.source.write_bytes(self.original+b'\n% changed\n')
        with self.assertRaises(RuntimeError):invoke_edit_worker('copy-edit',self.source,self.root/'changed.pdf',{'source_sha256':self.identity,'operations':operations})
        self.assertFalse((self.root/'changed.pdf').exists())

    def test_history_undo_redo_comment_delete_and_failed_branch_preserve_saved_copy(self):
        session = EditSession(self.source)
        try:
            session.add(self.operation('add-line'));session.add({'kind':'update-annotation','page':1,'index':0,'text':'history','author':'A'})
            session.save(self.output);saved = self.output.read_bytes()
            session.add({'kind':'delete-annotation','page':1,'index':0});self.assertEqual(len(session.info['annotations']),1)
            session.undo();self.assertEqual(session.info['annotations'][1]['text'],'history')
            session.undo();self.assertEqual(session.info['annotations'][1]['text'],'Comentário çã漢字')
            with self.assertRaises(RuntimeError):session.add(self.operation('add-line',geometry=[20,20,20,20]))
            self.assertTrue(session.can_redo);session.redo();self.assertEqual(session.info['annotations'][1]['author'],'A')
            session.add(self.operation('add-ellipse'));self.assertFalse(session.can_redo)
            self.assertEqual(self.output.read_bytes(),saved);self.assertEqual(self.source.read_bytes(),self.original)
        finally:session.close()


if __name__=='__main__':unittest.main()
