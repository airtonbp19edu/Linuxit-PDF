"""E19: accessible text and OCR follow two-column pages column by column (own bounded heuristic)."""
import hashlib,os,shutil,sys,tempfile,unittest
from io import BytesIO
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];APP=Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'));sys.path.insert(0,str(APP))
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject,DictionaryObject,NameObject
from reading_order import order_lines

TITLE='Titulo do documento ocupa a largura toda'
LEFT=['esquerda um alfa','esquerda dois beta','esquerda tres gama','esquerda quatro delta']
RIGHT=['direita um epsilon','direita dois zeta','direita tres eta','direita quatro teta']
FOOTER='Rodape tambem ocupa a largura toda da pagina'
EXPECTED=[TITLE,*LEFT,*RIGHT,FOOTER]


def two_columns(size=12):
    writer=PdfWriter();page=writer.add_blank_page(420,400)
    font=writer._add_object(DictionaryObject({NameObject('/Type'):NameObject('/Font'),NameObject('/Subtype'):NameObject('/Type1'),NameObject('/BaseFont'):NameObject('/Helvetica')}))
    page[NameObject('/Resources')]=DictionaryObject({NameObject('/Font'):DictionaryObject({NameObject('/F1'):font})})
    parts=[(30,360,TITLE)]
    # Right column written first in the content stream: stream order must not decide the reading order.
    parts+=[(230,320-30*i,t) for i,t in enumerate(RIGHT)]+[(30,320-30*i,t) for i,t in enumerate(LEFT)]
    parts.append((30,60,FOOTER))
    body=b''.join(b'BT /F1 %d Tf %d %d Td (%s) Tj ET\n'%(size,x,y,t.encode()) for x,y,t in parts)
    stream=DecodedStreamObject();stream.set_data(body);page[NameObject('/Contents')]=writer._add_object(stream)
    output=BytesIO();writer.write(output);return output.getvalue()


def box(x,y,w,text,h=10):return (x,y,x+w,y+h,text)


class ReadingOrderUnitTests(unittest.TestCase):
    def test_two_columns_with_full_width_title_and_footer(self):
        lines=[box(30,20,340,TITLE)]+[box(220,60+30*i,150,t) for i,t in enumerate(RIGHT)]+[box(30,60+30*i,150,t) for i,t in enumerate(LEFT)]+[box(30,330,340,FOOTER)]
        self.assertEqual(order_lines(lines,400),EXPECTED)

    def test_three_columns_and_bands_separated_by_wide_lines(self):
        cols=[[box(20+130*c,50+20*r,100,f'c{c}r{r}') for r in range(3)] for c in range(3)]
        lines=[l for col in cols for l in col]+[box(20,140,360,'meio')]+[box(20,170+20*r,150,f'b{r}') for r in range(2)]+[box(220,170+20*r,150,f'd{r}') for r in range(2)]
        self.assertEqual(order_lines(lines,400),[f'c{c}r{r}' for c in range(3) for r in range(3)]+['meio','b0','b1','d0','d1'])

    def test_single_column_and_unclear_gutter_keep_top_to_bottom(self):
        single=[box(30,20+15*i,300 if i%2 else 120,f'l{i}') for i in range(6)]
        self.assertEqual(order_lines(single,400),[f'l{i}' for i in range(6)])
        # Only one line on the right: not enough evidence of a second column.
        lines=[box(30,20,150,'a'),box(30,40,150,'b'),box(220,20,150,'c')]
        self.assertEqual(order_lines(lines,400),['a','c','b'])
        self.assertEqual(order_lines([],400),[])


class ReadingOrderPdfTests(unittest.TestCase):
    def setUp(self):
        if not shutil.which('pdftotext'):self.skipTest('Poppler pdftotext required')
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        self.source=self.root/'duas-colunas.pdf';self.source.write_bytes(two_columns())

    def test_accessible_text_reads_column_by_column(self):
        from rendering import extract_page_text
        self.assertEqual(extract_page_text(str(self.source),0).splitlines(),EXPECTED)
        from pdf_security import invoke_accessible_text
        self.assertEqual(invoke_accessible_text(str(self.source),0).splitlines(),EXPECTED)

    def test_ocr_copy_text_layer_is_read_column_by_column(self):
        if not shutil.which('tesseract') or not shutil.which('pdftocairo'):self.skipTest('Tesseract and Poppler required')
        from pdf_ocr import create_searchable_copy
        from rendering import extract_page_text
        source=self.root/'grande.pdf';source.write_bytes(two_columns(size=14))
        target=self.root/'ocr.pdf'
        create_searchable_copy(source,target,{'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'language':'por','dpi':300,'psm':3})
        lines=[l.lower() for l in extract_page_text(str(target),0).splitlines() if l.strip()]
        self.assertTrue(ordered_like_expected(lines),lines)

    def test_fuzzy_order_check_accepts_misread_words_and_rejects_interleaving(self):
        # Words as the Flatpak Tesseract read them in CI 39524293929 (order right, spelling not).
        sandbox=['tal do docum ento ocupa a armguia toda','esquerda um alfa','esquerda dois beta','esquerda tes gama',
                 'esquerda quatro delta','direta um epsibn','direta dois zeta','dieta tes eta','dieta quato teta',
                 'rodape tam bem ocupa a argura toda da pagha']
        self.assertTrue(ordered_like_expected(sandbox))
        interleaved=[TITLE,LEFT[0],RIGHT[0],LEFT[1],RIGHT[1],LEFT[2],RIGHT[2],LEFT[3],RIGHT[3],FOOTER]
        self.assertFalse(ordered_like_expected([l.lower() for l in interleaved]))


def ordered_like_expected(lines):
    """OCR quality varies with the Tesseract build (source vs sandbox), so each recognised line is
    matched to the closest expected line; the check is the order, not the spelling."""
    from difflib import SequenceMatcher
    expected=[e.lower() for e in EXPECTED];found=[]
    for line in lines:
        score,index=max((SequenceMatcher(None,line,e).ratio(),i) for i,e in enumerate(expected))
        if score>=0.6:found.append(index)
    return len(set(found))>=8 and found==sorted(found) and len(found)==len(set(found))

if __name__=='__main__':unittest.main()
