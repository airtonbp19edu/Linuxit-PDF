"""Inventory Foxit's UI resources and candidate MFC routes, without execution."""
import argparse,collections,hashlib,json,re,struct,sys
from pathlib import Path
# Install pefile in the caller's Python environment; no executable is launched.
import pefile
from foxit_pe_resources import dialog
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('target',type=Path)
parser.add_argument('--output',type=Path,required=True,help='New directory outside the application')
parser.add_argument('--module-root',type=Path,help='Also inventory PE files below the supplied Foxit directory')
args=parser.parse_args()
TARGET=args.target.resolve()
ROOT=args.output.resolve()
ROOT.mkdir(parents=True,exist_ok=False)
raw=TARGET.read_bytes();pe=pefile.PE(data=raw,fast_load=True);pe.parse_data_directories(directories=[1,2,13])
base=pe.OPTIONAL_HEADER.ImageBase

def menu(data):
    version,offset=struct.unpack_from('<HH',data)
    cursor=4+offset
    out=[]
    def utf16():
        nonlocal cursor
        start=cursor
        while struct.unpack_from('<H',data,cursor)[0]:cursor+=2
        value=data[start:cursor].decode('utf-16-le');cursor+=2;return value
    def level(parents):
        nonlocal cursor
        while cursor<len(data):
            if version==0:
                flags=struct.unpack_from('<H',data,cursor)[0];cursor+=2
                popup=bool(flags&0x10)
                item_id=None if popup else struct.unpack_from('<H',data,cursor)[0]
                if not popup:cursor+=2
                label=utf16();end=bool(flags&0x80)
            elif version==1:
                cursor=(cursor+3)&~3
                kind,state,item_id,flags=struct.unpack_from('<IIIH',data,cursor);cursor+=14
                label=utf16();popup=bool(flags&1);end=bool(flags&0x80)
                if popup:cursor=(cursor+3)&~3;cursor+=4
            else:raise ValueError('Unsupported MENU version')
            path=parents+[label] if label else parents
            out.append({'id':item_id,'label':label,'path':path,'popup':popup})
            if popup:level(path)
            if end:return
    level([])
    return out

strings=[];dialogs=[];menus=[];errors=[];resources=[]
for typ in pe.DIRECTORY_ENTRY_RESOURCE.entries:
    for item in typ.directory.entries:
        for lang in item.directory.entries:
            entry=lang.data.struct;data=pe.get_data(entry.OffsetToData,entry.Size)
            rid=item.id if item.id is not None else str(item.name)
            resources.append({'type':typ.id if typ.id is not None else str(typ.name),'id':rid,'language':lang.id,'bytes':len(data),'rva':hex(entry.OffsetToData),'sha256':hashlib.sha256(data).hexdigest()})
            try:
                if typ.id==5:dialogs.append({'id':rid,'language':lang.id,**dialog(data)})
                elif typ.id==4:menus.append({'id':rid,'language':lang.id,'items':menu(data)})
                elif typ.id==6:
                    cursor=0
                    for i in range(16):
                        size=struct.unpack_from('<H',data,cursor)[0];cursor+=2
                        text=data[cursor:cursor+size*2].decode('utf-16-le');cursor+=size*2
                        if text:strings.append({'id':(int(rid)-1)*16+i,'language':lang.id,'text':text})
            except (ValueError,struct.error,IndexError,UnicodeDecodeError) as exc:errors.append({'resource':rid,'type':typ.id,'error':str(exc)})
# Structural candidates only. Matching numeric IDs is not proof of a unique UI route.
handlers=[]
for m in re.finditer(re.escape(struct.pack('<I',0x111)),raw):
    if m.start()+24>len(raw):continue
    message,code,first,last,signature,address=struct.unpack_from('<6I',raw,m.start())
    if not(0<first<=last<=0xffff and signature<256):continue
    section=pe.get_section_by_rva(address-base)
    if section is None or not section.Characteristics&0x20000000:continue
    handlers.append({'message':'WM_COMMAND','notification':hex(code),'id_first':first,'id_last':last,'signature_enum':signature,'handler_va':hex(address),'map_file_offset':hex(m.start()),'status':'structural_candidate'})
byid=collections.defaultdict(list)
for h in handlers:
    if h['id_first']==h['id_last']:byid[h['id_first']].append(h)
commands=[]
for resource in menus:
    if resource['language'] not in (0,1033):continue
    for item in resource['items']:
        if item['id'] and item['label'] and not item['popup']:
            commands.append({'source':'menu','resource_id':resource['id'],'language':resource['language'],**item,'candidates':byid.get(item['id'],[])})
for resource in dialogs:
    if resource['language'] not in (0,1033):continue
    for control in resource['controls']:
        if control['text'] and control['id'] not in (0,0xffff,0xffffffff):
            commands.append({'source':'dialog','resource_id':resource['id'],'language':resource['language'],'dialog_title':resource['title'],'id':control['id'],'label':control['text'],'class':control['class'],'candidates':byid.get(control['id'],[])})
imports={}
for directory in ('DIRECTORY_ENTRY_IMPORT','DIRECTORY_ENTRY_DELAY_IMPORT'):
    for dll in getattr(pe,directory,[]):
        imports.setdefault(dll.dll.decode(errors='replace'),[]).extend(x.name.decode(errors='replace') if x.name else f'ordinal:{x.ordinal}' for x in dll.imports)
result={'target_sha256':hashlib.sha256(raw).hexdigest(),'image_base':hex(base),'resources':resources,'dialogs':dialogs,'menus':menus,'string_table':strings,'message_map_candidates':handlers,'ui_items':commands,'imports':imports,'errors':errors,'limitations':['Read-only PE parsing, supplemental to REA/Ghidra analysis.','Structural message-map candidates require confirmation by code/reference analysis.','IDs may be reused across dialogs/classes; labels do not establish behavior or feature availability.','Only English/neutral UI items are joined to routes; the raw resource inventory retains other languages.']}
(ROOT/'ui-catalog.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
summary={'resources':len(resources),'dialogs':len(dialogs),'menus':len(menus),'string_table_items':len(strings),'mfc_route_candidates':len(handlers),'distinct_candidate_functions':len({h['handler_va'] for h in handlers}),'english_ui_items':len(commands),'parse_errors':errors}
(ROOT/'ui-catalog-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))

if args.module_root:
    module_root=args.module_root.resolve()
    rows=[];module_errors=[]
    for file in sorted(module_root.rglob('*')):
        if not file.is_file() or file.suffix.lower() not in ('.exe','.dll','.fpi'):continue
        try:
            content=file.read_bytes()
            module=pefile.PE(data=content,fast_load=True)
            module.parse_data_directories(directories=[0,1,13])
            dependencies={}
            for directory in ('DIRECTORY_ENTRY_IMPORT','DIRECTORY_ENTRY_DELAY_IMPORT'):
                for dll in getattr(module,directory,[]):
                    dependencies.setdefault(dll.dll.decode(errors='replace'),[]).extend(i.name.decode(errors='replace') if i.name else f'ordinal:{i.ordinal}' for i in dll.imports)
            exports=[{'name':s.name.decode(errors='replace') if s.name else None,'ordinal':s.ordinal,'va':hex(module.OPTIONAL_HEADER.ImageBase+s.address),'forwarder':s.forwarder.decode(errors='replace') if s.forwarder else None} for s in getattr(getattr(module,'DIRECTORY_ENTRY_EXPORT',None),'symbols',[])]
            rows.append({'path':str(file.relative_to(module_root)),'bytes':len(content),'sha256':hashlib.sha256(content).hexdigest(),'machine':hex(module.FILE_HEADER.Machine),'image_base':hex(module.OPTIONAL_HEADER.ImageBase),'entry_point_va':hex(module.OPTIONAL_HEADER.ImageBase+module.OPTIONAL_HEADER.AddressOfEntryPoint),'imports':dependencies,'exports':exports})
            module.close()
        except (pefile.PEFormatError,OSError,ValueError) as exc:
            module_errors.append({'path':str(file.relative_to(module_root)),'error':str(exc)})
    modules={'root_sha256':hashlib.sha256(raw).hexdigest(),'modules':rows,'errors':module_errors,'limitations':['Static PE inventory only; availability does not establish runtime loading, licensed functionality, or behavior.','No module was executed. Exports include internal names and third-party runtime functions.']}
    (ROOT/'module-catalog.json').write_text(json.dumps(modules,indent=2)+'\n')
    print(json.dumps({'modules':len(rows),'plugins':sum(r['path'].endswith('.fpi') for r in rows),'errors':module_errors},indent=2))
