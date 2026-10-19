import math,os,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];APP=Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'));sys.path[:0]=[str(APP),str(ROOT/'tests')]
from character_selection import boundaries,nearest_caret,select_range,move_caret,validate_layout,carets


def layout(text):
    return dict(width=300,height=200,text=text,boxes=[[i*10,0,(i+1)*10,12] for i in range(len(text))])


class CharacterSelectionTests(unittest.TestCase):
    def test_exact_substring_and_reverse_drag_keep_logical_unicode_order(self):
        data=layout('ação שלום 123')
        self.assertEqual(select_range(data,1,4)['text'],'ção')
        self.assertEqual(select_range(data,9,5)['text'],'שלום')
        self.assertEqual(select_range(data,5,9)['rects'],data['boxes'][5:9])

    def test_combining_joiner_skin_tone_and_flag_are_not_split(self):
        for text in ('e\u0301','👩\u200d💻','👍🏽','🇧🇷','\r\n'):
            self.assertEqual(boundaries(text),[0,len(text)])
            self.assertEqual(select_range(layout(text),0,1)['text'],text)

    def test_actual_unequal_glyph_widths_determine_cursor(self):
        data=layout('Wi');data['boxes']=[[0,0,30,12],[30,0,33,12]]
        self.assertEqual(nearest_caret(data,(29,5)),1)
        self.assertEqual(nearest_caret(data,(33,5)),2)
        self.assertEqual(select_range(data,1,2)['rects'],[[30,0,33,12]])

    def test_rtl_visual_arrows_follow_positions_without_reversing_copied_text(self):
        data=layout('שלום');data['boxes']=[[30-i*10,0,40-i*10,12] for i in range(4)]
        self.assertEqual(nearest_caret(data,(40,6)),0)
        self.assertEqual(move_caret(data,0,'Left'),1)
        self.assertEqual(select_range(data,0,4)['text'],'שלום')
        self.assertEqual(move_caret(data,2,'Home'),4)
        self.assertEqual(move_caret(data,2,'End'),0)

    def test_vertical_movement_and_document_edges(self):
        data=layout('ABCD');data['boxes'][2:]=[[0,20,10,32],[10,20,20,32]]
        self.assertEqual(move_caret(data,1,'Down'),3)
        self.assertEqual(move_caret(data,1,'End',True),4)
        self.assertEqual(move_caret(data,3,'Home',True),0)
        self.assertEqual(nearest_caret(layout(''),(3,4)),0)

    def test_malformed_layout_and_oversized_text_fail_without_fake_geometry(self):
        for data in (dict(text='ab',boxes=[]),layout('x'*100001)):
            with self.assertRaises(ValueError):validate_layout(data)
        data=layout('x');data['boxes'][0][0]=math.nan
        with self.assertRaises(ValueError):validate_layout(data)


@unittest.skipUnless(os.environ.get('DISPLAY'),'Requires Poppler/GTK and X display')
class CharacterSelectionLinuxTests(unittest.TestCase):
    def test_native_pango_graphemes_cover_hangul_combining_emoji_and_regional_pairs(self):
        from character_extraction import unicode_cursor_stops
        for text in ('e\u0301','👩\u200d💻','👍🏽','🇧🇷','각'):
            self.assertEqual(unicode_cursor_stops(text),[0,len(text)])
    def test_poppler_worker_returns_real_character_positions_and_rotated_crop_size(self):
        from test_regressions import make_pdf
        from character_extraction import page_characters
        from pypdf import PdfReader,PdfWriter
        from pypdf.generic import RectangleObject
        with tempfile.TemporaryDirectory() as d:
            source=Path(d)/'text.pdf';make_pdf(source,['Wi ação'])
            data=page_characters(source,0)
            self.assertIn('Wi ação',data['text']);self.assertEqual(len(data['boxes']),len(data['text']))
            wi=data['text'].index('Wi');self.assertGreater(data['boxes'][wi][2]-data['boxes'][wi][0],data['boxes'][wi+1][2]-data['boxes'][wi+1][0])
            reader=PdfReader(source);writer=PdfWriter(clone_from=reader)
            writer.pages[0].cropbox=RectangleObject([10,20,300,400]);writer.pages[0].rotate(90)
            changed=Path(d)/'rotated.pdf';writer.write(changed)
            rotated=page_characters(changed,0);self.assertEqual((rotated['width'],rotated['height']),(380,290))

    def test_gtk_partial_character_copy_keyboard_extension_and_stale_page_guard(self):
        from main import PDFWindow,Gtk
        from test_gui import wait_for
        from test_regressions import make_pdf
        from character_extraction import page_characters
        with tempfile.TemporaryDirectory() as d,patch.object(Gtk,'main_quit'):
            path=Path(d)/'text.pdf';make_pdf(path,['ABCDE','second'])
            data=page_characters(path,0);window=PDFWindow(str(path))
            try:
                wait_for(lambda:window.displayed_page==0)
                boxes=data['boxes'];start=window._pdf_rect_to_display([boxes[1][0],boxes[1][1],boxes[1][0],boxes[1][3]],data)
                end=window._pdf_rect_to_display([boxes[3][0],boxes[3][1],boxes[3][0],boxes[3][3]],data)
                window.active_tool='caret';window._finish_character_selection(start[:2],end[:2])
                wait_for(lambda:window.character_state is not None)
                state=window.character_state
                self.assertEqual(select_range(data,state['anchor'],state['focus'])['text'],'BC')
                self.assertTrue(window._character_key('Right',False,True))
                self.assertEqual(select_range(data,state['anchor'],state['focus'])['text'],'BCD')
                window.goto_page(1);self.assertFalse(window._character_key('Right',False,True))
            finally:window.destroy()
