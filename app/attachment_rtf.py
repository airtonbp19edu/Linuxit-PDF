"""Bounded passive RTF text; objects, pictures and optional destinations skipped."""
import re

MAX_BYTES=2*1024**2
SKIP={'fonttbl','colortbl','stylesheet','info','pict','object','objdata','filetbl','datastore','themedata','xmlnstbl','listtable','listoverridetable','fldinst','nonshppict','shppict'}
SPECIAL={'par':'\n','line':'\n','tab':'\t','emdash':'—','endash':'–','bullet':'•','lquote':'‘','rquote':'’','ldblquote':'“','rdblquote':'”'}


def extract_rtf(payload):
    if not isinstance(payload,bytes) or len(payload)>MAX_BYTES or not payload.startswith(b'{\\rtf1'):
        raise ValueError('RTF inválido ou acima de 2MiB.')
    text=payload.decode('latin1');stack=[];state=dict(hidden=False,skip=False,uc=1,codepage='cp1252')
    parts=[];fallback=0;position=0
    def append(value):
        nonlocal fallback
        if fallback:fallback-=1;return
        if not state['skip'] and not state['hidden']:parts.append(value)
    while position<len(text):
        char=text[position];position+=1
        if char=='{':
            if len(stack)>=128:raise ValueError('RTF acima de 128 níveis.')
            stack.append(state.copy());state=state.copy()
        elif char=='}':
            if not stack:raise ValueError('Grupo RTF inválido.')
            state=stack.pop()
            if not stack:
                if text[position:].strip():raise ValueError('Dados após o grupo raiz RTF.')
                break
        elif char=='\\':
            if position>=len(text):raise ValueError('Escape RTF incompleto.')
            char=text[position];position+=1
            if char in '{}\\':append(char)
            elif char=="'":
                try:value=bytes([int(text[position:position+2],16)]).decode(state['codepage'])
                except (ValueError,UnicodeError) as exc:raise ValueError('Escape de caracteres RTF inválido.') from exc
                if len(text[position:position+2])!=2:raise ValueError('Escape RTF incompleto.')
                position+=2;append(value)
            elif char=='*':state['skip']=True
            elif char in '~_-':append({'~':'\u00a0','_':'\u2011','-':'\u00ad'}[char])
            elif char.isalpha() and char.isascii():
                start=position-1
                while position<len(text) and text[position].isalpha() and text[position].isascii():position+=1
                word=text[start:position];number_start=position
                if position<len(text) and text[position]=='-':position+=1
                while position<len(text) and text[position].isdigit() and text[position].isascii():position+=1
                raw=text[number_start:position];number=int(raw) if raw and raw!='-' and len(raw)<=10 else None
                if raw and number is None:raise ValueError('Parâmetro numérico RTF inválido.')
                if position<len(text) and text[position]==' ':position+=1
                if word in SKIP:state['skip']=True
                elif word=='v':state['hidden']=number!=0
                elif word=='uc':
                    if number is None or not 0<=number<=16:raise ValueError('Fallback Unicode RTF inválido.')
                    state['uc']=number
                elif word=='u':
                    if number is None or not -32768<=number<=65535:raise ValueError('Unidade Unicode RTF inválida.')
                    fallback=0;append(chr(number&65535));fallback=state['uc']
                elif word=='ansicpg':
                    if number not in range(1250,1259):raise ValueError('Codepage RTF não suportado; use Unicode ou Windows1250–1258.')
                    state['codepage']='cp'+str(number)
                elif word=='bin':
                    if number is None or not 0<=number<=len(text)-position:raise ValueError('Bloco binário RTF inválido.')
                    position+=number
                elif word in SPECIAL:append(SPECIAL[word])
            elif char in '\r\n':pass
        elif char not in '\r\n':append(bytes([ord(char)]).decode(state['codepage']))
    if stack:raise ValueError('Grupos RTF não encerrados.')
    try:result=''.join(parts).encode('utf-16-le','surrogatepass').decode('utf-16-le')
    except UnicodeError as exc:raise ValueError('Pares Unicode RTF inválidos.') from exc
    if len(result.encode('utf-8'))>MAX_BYTES:raise ValueError('Texto RTF acima de 2MiB.')
    return result.strip(),'RTF: texto passivo; objetos, imagens, instruções de campos e destinos opcionais omitidos.'
