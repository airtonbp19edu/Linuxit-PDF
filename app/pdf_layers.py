"""Own reading visibility for default PDF optional-content configuration."""
from pathlib import Path
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader,PdfWriter
from pypdf.generic import ArrayObject,DictionaryObject,NameObject


def _key(ref):
    indirect=ref if hasattr(ref,'idnum') else getattr(ref,'indirect_reference',None)
    return (indirect.idnum,indirect.generation) if indirect is not None else id(ref)


def _array(obj,name):
    value=obj.get(name)
    if value is None:return []
    value=value.get_object()
    if not isinstance(value,ArrayObject):raise ValueError('Lista de camadas inválida.')
    return value


def inspect_layers(reader):
    props=reader.root_object.get('/OCProperties')
    if props is None:return []
    props=props.get_object();groups=_array(props,'/OCGs')
    if len(groups)>256:raise ValueError('PDF acima de256 camadas.')
    if len({_key(ref) for ref in groups})!=len(groups):raise ValueError('Camadas repetidas.')
    config=props.get('/D',DictionaryObject()).get_object()
    base_state=config.get('/BaseState','/ON')
    if base_state not in ('/ON','/OFF'):raise ValueError('BaseState não suportado nesta configuração.')
    base=base_state=='/ON'
    on={_key(ref) for ref in _array(config,'/ON')};off={_key(ref) for ref in _array(config,'/OFF')}
    locked={_key(ref) for ref in _array(config,'/Locked')}
    return [dict(index=i,name=str(ref.get_object().get('/Name','Camada'))[:1024],
                 visible=False if _key(ref) in off else True if _key(ref) in on else base,
                 locked=_key(ref) in locked) for i,ref in enumerate(groups)]


def create_layer_view(path,destination,visible):
    source,target=Path(path),Path(destination)
    if source.stat().st_size>64*1024**2:raise ValueError('Visibilidade temporária limitada a PDFs de64MiB.')
    if target.exists() or target.is_symlink() or target.resolve()==source.resolve():raise ValueError('Use destino privado novo.')
    reader=PdfReader(source,strict=True)
    if reader.is_encrypted:raise ValueError('Abra a sessão autenticada antes de alterar a visibilidade.')
    rows=inspect_layers(reader)
    if not rows or not isinstance(visible,list) or len(visible)!=len(rows) or not all(type(v) is bool for v in visible):
        raise ValueError('Seleção de camadas inválida.')
    if any(row['locked'] and row['visible']!=visible[row['index']] for row in rows):raise ValueError('Camada bloqueada nesta configuração.')
    writer=PdfWriter(clone_from=reader);props=writer.root_object['/OCProperties']
    groups=props['/OCGs'];config=props.get('/D',DictionaryObject()).get_object()
    lookup={_key(ref):i for i,ref in enumerate(groups)}
    for group in _array(config,'/RBGroups'):
        if sum(visible[lookup[_key(ref)]] for ref in group.get_object() if _key(ref) in lookup)>1:
            raise ValueError('Grupo exclusivo: desmarque a camada anterior antes de selecionar outra.')
    config[NameObject('/BaseState')]=NameObject('/OFF')
    config[NameObject('/ON')]=ArrayObject(ref for i,ref in enumerate(groups) if visible[i])
    config[NameObject('/OFF')]=ArrayObject(ref for i,ref in enumerate(groups) if not visible[i])
    config.pop('/AS',None)  # Explicit reading override, not automatic usage selection.
    props[NameObject('/D')]=config
    try:
        with target.open('xb') as stream:writer.write(stream)
        if target.stat().st_size>64*1024**2:raise ValueError('Representação de camadas acima de64MiB.')
        check=PdfReader(target,strict=True)
        if len(check.pages)!=len(reader.pages) or [r['visible'] for r in inspect_layers(check)]!=visible:
            raise ValueError('Visibilidade de leitura não confirmada.')
        return str(target)
    except BaseException:
        target.unlink(missing_ok=True);raise
