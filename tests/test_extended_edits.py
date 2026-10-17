"""Real nested bookmark/note edits and persistent rotation, always into new copies."""
import hashlib
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
import pdf_changes as edits
from edit_tasks import invoke_edit_worker
from pypdf import PdfReader,PdfWriter
from pypdf.annotations import Text
from pypdf.generic import NameObject,NumberObject,RectangleObject,DictionaryObject,TextStringObject


class ExtendedEditTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='linuxit-extended-');self.root=Path(self.temp.name)
        self.source=self.root/'source.pdf';self.output=self.root/'out.pdf'
        self.writer=PdfWriter();page=self.writer.add_blank_page(200,300)
        page.cropbox=RectangleObject((10,20,190,280))
        parent=self.writer.add_outline_item('Parent',0);self.writer.add_outline_item('Child',0,parent=parent)
        self.writer.add_outline_item('Sibling',0)
        self.writer.add_annotation(0,Text(rect=(20,30,40,50),text='Old note',title_bar='Author'))
        self.writer.add_attachment('keep.txt',b'keep');self.writer.write(self.source)
        self.original=self.source.read_bytes();self.identity=hashlib.sha256(self.original).hexdigest()

    def tearDown(self):self.temp.cleanup()
    def save(self,operations):return edits.save_edited_copy(self.source,self.output,source_sha256=self.identity,operations=operations)

    def test_info_exposes_nested_paths_and_annotation_indices(self):
        info=edits.inspect_editable_document(self.source)
        self.assertEqual(info['bookmarks'],[{'path':[0],'title':'Parent'},{'path':[0,0],'title':'Child'},{'path':[1],'title':'Sibling'}])
        self.assertEqual(info['notes'],[{'page':0,'index':0,'text':'Old note','author':'Author'}])
        self.assertFalse(info['notes_truncated']);self.assertEqual(self.source.read_bytes(),self.original)

    def test_combined_edits_preserve_tree_destinations_geometry_and_source(self):
        self.save([{'kind':'rename-bookmark','path':[0,0],'title':'Renamed child'},
                   {'kind':'update-note','page':0,'index':0,'text':'Revised note','author':''},
                   {'kind':'rotate-page','page':0,'angle':90}])
        reader=PdfReader(self.output);page=reader.pages[0]
        self.assertEqual(reader.outline[0].title,'Parent');self.assertEqual(reader.outline[1][0].title,'Renamed child')
        self.assertEqual(reader.get_destination_page_number(reader.outline[1][0]),0)
        self.assertEqual(page.rotation,90);self.assertEqual(list(page.cropbox),[10,20,190,280])
        self.assertEqual(list(page.mediabox),[0,0,200,300])
        note=page['/Annots'][0].get_object();self.assertEqual(note['/Contents'],'Revised note');self.assertNotIn('/T',note)
        self.assertEqual(list(note['/Rect']),[20,30,40,50]);self.assertEqual(next(reader.attachment_list).content,b'keep')
        self.assertEqual(self.source.read_bytes(),self.original)

    def test_all_supported_rotations_persist(self):
        for angle in (-270,-180,-90,90,180,270):
            self.save([{'kind':'rotate-page','page':0,'angle':angle}])
            self.assertEqual(PdfReader(self.output).pages[0].rotation % 360,angle % 360);self.output.unlink()

    def test_invalid_paths_angles_and_note_indices_leave_no_output(self):
        cases=[{'kind':'rename-bookmark','path':[2],'title':'No'}, {'kind':'rename-bookmark','path':[True],'title':'No'},
               {'kind':'rename-bookmark','path':[],'title':'No'}, {'kind':'rotate-page','page':0,'angle':45},
               {'kind':'rotate-page','page':True,'angle':90}, {'kind':'update-note','page':0,'index':-1,'text':'No','author':''}]
        for operation in cases:
            with self.subTest(kind=operation['kind']),self.assertRaises(ValueError):self.save([operation])
            self.assertFalse(self.output.exists());self.assertEqual(list(self.root.glob('.linuxit-copy-*')),[])

    def test_locked_text_notes_cannot_be_edited(self):
        for flags in (64,128,512):
            note=self.writer.pages[0]['/Annots'][0].get_object();note[NameObject('/F')]=NumberObject(flags)
            self.writer.write(self.source);self.identity=hashlib.sha256(self.source.read_bytes()).hexdigest()
            self.assertEqual(edits.inspect_editable_document(self.source)['notes'],[])
            with self.assertRaises(ValueError):self.save([{'kind':'update-note','page':0,'index':0,'text':'No','author':''}])
            self.assertFalse(self.output.exists())

    def test_outline_cycles_and_depth_are_bounded(self):
        root=self.writer.root_object['/Outlines'];first=root['/First']
        first[NameObject('/Next')]=first.indirect_reference
        with self.assertRaisesRegex(ValueError,'Árvore'):edits._outline_nodes(self.writer)

    def test_late_failure_does_not_publish_earlier_valid_change(self):
        with self.assertRaises(ValueError):self.save([{'kind':'rotate-page','page':0,'angle':90},
            {'kind':'rename-bookmark','path':[100],'title':'Invalid'}])
        self.assertFalse(self.output.exists());self.assertEqual(self.source.read_bytes(),self.original)

    def test_real_edit_worker_exposes_and_applies_new_operations(self):
        info=invoke_edit_worker('edit-info',self.source)
        result=invoke_edit_worker('copy-edit',self.source,self.output,{'source_sha256':info['source_sha256'],
            'operations':[{'kind':'rename-bookmark','path':info['bookmarks'][1]['path'],'title':'Via worker'},
                          {'kind':'update-note','page':0,'index':info['notes'][0]['index'],'text':'Worker note','author':'Writer'}]})
        self.assertEqual(result['operations_applied'],2);self.assertEqual(PdfReader(self.output).outline[1][0].title,'Via worker')

    def test_note_inspection_total_budget_is_reported_as_truncated(self):
        for _ in range(40):self.writer.add_annotation(0,Text(rect=(20,30,40,50),text='x'*32768))
        self.writer.write(self.source)
        info=edits.inspect_editable_document(self.source)
        self.assertTrue(info['notes_truncated'])
        self.assertLessEqual(sum(len(n['text'].encode())+len(n['author'].encode()) for n in info['notes']),1024**2)
