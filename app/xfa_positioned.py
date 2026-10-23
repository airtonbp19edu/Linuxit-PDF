"""Own single-page positioned XFA subset: top-left x/y/w/h in explicit units."""
import math
import re

from pdf_xfa import _require


def measure(value):
    match = re.fullmatch(r'([+]?(?:\d+(?:\.\d*)?|\.\d+))(pt|in|mm|cm)?', str(value))
    _require(match is not None, 'Medida XFA deve ser não negativa em pt/in/mm/cm.')
    result = float(match[1])*{None:1, 'pt':1, 'in':72, 'mm':72/25.4, 'cm':72/2.54}[match[2]]
    _require(math.isfinite(result) and 0 <= result <= 14400, 'Medida XFA acima do limite.')
    return result


def geometry(node, origin, container):
    x = measure(node.get('x', '0'));y = measure(node.get('y', '0'))
    width = measure(node.get('w', str(container[0]-x)))
    height = measure(node.get('h', str(container[1]-y)))
    _require(width > 0 and height > 0 and x+width <= container[0]+.01 and y+height <= container[1]+.01,
             'Objeto XFA fora dos limites do contêiner.')
    return (origin[0]+x, origin[1]+y, width, height)


def render(model):
    from pdf_xfa_flow import _latin
    from pdf_xfa import _new_stream
    from pypdf import PdfWriter
    from pypdf.generic import (ArrayObject, BooleanObject, DictionaryObject, DecodedStreamObject,
                               FloatObject, NameObject, NumberObject, TextStringObject)
    writer = PdfWriter();width, height = model['page_size']
    page = writer.add_blank_page(width, height)
    font = writer._add_object(DictionaryObject({NameObject('/Type'):NameObject('/Font'), NameObject('/Subtype'):NameObject('/Type1'),
              NameObject('/BaseFont'):NameObject('/Helvetica'),NameObject('/Encoding'):NameObject('/WinAnsiEncoding')}))
    resources = DictionaryObject({NameObject('/Font'):DictionaryObject({NameObject('/Helv'):font})})
    page[NameObject('/Resources')] = resources;page[NameObject('/Annots')] = ArrayObject()
    fields, commands = ArrayObject(), []
    for row in model['rows']:
        x, top, w, h = row['rect'];bottom = height-top-h
        text = row['value'] if row['kind'] == 'field' else row['text']
        _latin(text)
        columns = int((w-8)//11)
        _require(columns >= 1 and h >= 20, 'Objeto XFA pequeno demais para a fonte portátil de 11 pt.')
        lines = []
        for line in text.replace('\r\n','\n').replace('\r','\n').split('\n'):
            lines.extend(line[i:i+columns] for i in range(0,len(line),columns)) if line else lines.append('')
        _require(len(lines)*14+6 <= h, 'Texto não cabe no retângulo XFA; aumente w/h.')
        content = [f'q 0 0 {w} {h} re W n'.encode()]
        if row['kind'] == 'field':content.append(f'0.7 G 0.5 0.5 {w-1} {h-1} re S'.encode())
        for i, line in enumerate(lines):
            content.append(f'BT /Helv 11 Tf 0 g 4 {h-14-i*14} Td <'.encode()+_latin(line).hex().encode()+b'> Tj ET')
        content.append(b'Q');raw = b'\n'.join(content)
        if row['kind'] == 'field':
            ap = DecodedStreamObject();ap.set_data(raw)
            ap.update({NameObject('/Type'):NameObject('/XObject'),NameObject('/Subtype'):NameObject('/Form'),
                       NameObject('/BBox'):ArrayObject(FloatObject(v) for v in (0,0,w,h)),NameObject('/Resources'):resources})
            widget = DictionaryObject({NameObject('/Type'):NameObject('/Annot'),NameObject('/Subtype'):NameObject('/Widget'),
                       NameObject('/FT'):NameObject('/Tx'),NameObject('/T'):TextStringObject(row['path']),NameObject('/V'):TextStringObject(text),
                       NameObject('/DA'):TextStringObject('/Helv 11 Tf 0 g'),NameObject('/Ff'):NumberObject(4096 | bool(row.get('calculate'))),
                       NameObject('/F'):NumberObject(4),NameObject('/Rect'):ArrayObject(FloatObject(v) for v in (x,bottom,x+w,bottom+h)),
                       NameObject('/P'):page.indirect_reference,NameObject('/AP'):DictionaryObject({NameObject('/N'):writer._add_object(ap)})})
            ref = writer._add_object(widget);fields.append(ref);page['/Annots'].append(ref)
        else:
            commands.append(f'q 1 0 0 1 {x} {bottom} cm\n'.encode()+raw+b'\nQ')
    page[NameObject('/Contents')] = _new_stream(writer,b'\n'.join(commands))
    form = DictionaryObject({NameObject('/Fields'):fields,NameObject('/DR'):resources,NameObject('/DA'):TextStringObject('/Helv 11 Tf 0 g'),
           NameObject('/XFA'):ArrayObject([TextStringObject('template'),_new_stream(writer,model['template']),TextStringObject('datasets'),_new_stream(writer,model['datasets'])])})
    writer.root_object[NameObject('/AcroForm')] = writer._add_object(form)
    if model['calculations']:form[NameObject('/LinuxitFormCalc')] = BooleanObject(True)
    writer.root_object[NameObject('/NeedsRendering')] = BooleanObject(False)
    writer.add_metadata({'/Producer':'Linuxit PDF — own positioned XFA subset','/Subject':'Posições suportadas; fontes/estilos originais não preservados'})
    return writer
