"""Declarative Acrobat helper subset; never execute JavaScript from a PDF."""
import ast
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation, localcontext
import re

from pdf_form_controls import inherited, terminal

MAX_RULES = 128
MAX_SCRIPT = 16384
NUMBER = r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)'
# AFNumber sepStyle: (thousands separator, decimal separator). Own contract, not Foxit parity.
SEPARATORS = {0: (',', '.'), 1: ('', '.'), 2: ('.', ','), 3: ('', ','), 4: ("'", '.')}


def require(value, message):
    if not value:
        raise ValueError(message)


def _script(action):
    action = action.get_object()
    require(isinstance(action,dict) and action.get('/S') == '/JavaScript' and '/Next' not in action,
            'Ação composta ou diferente de JavaScript não suportada pelo contrato de formulário.')
    value = action.get('/JS')
    if hasattr(value,'get_object'):value=value.get_object()
    if hasattr(value,'get_data'):
        value=value.get_data()
        require(len(value)<=MAX_SCRIPT,'Script de formulário acima do limite.')
        value=value.decode('utf-8-sig')
    require(isinstance(value,str) and len(value.encode('utf-8'))<=MAX_SCRIPT,'Script de formulário inválido.')
    return value.strip()


def parse_calculation(script):
    match=re.fullmatch(r'AFSimple_Calculate\(\s*["\'](SUM|AVG|PRD|MIN|MAX)["\']\s*,\s*(.*?)\s*\)\s*;?',script,re.S)
    require(match is not None,'Cálculo fora do subconjunto AFSimple_Calculate suportado.')
    fields=match[2].strip()
    array=re.fullmatch(r'new\s+Array\s*\((.*)\)',fields,re.S)
    if array:fields='['+array[1]+']'
    require(len(fields)<=MAX_SCRIPT and fields.startswith('[') and fields.endswith(']'),'Lista de cálculo inválida.')
    try:values=ast.literal_eval(fields)
    except (ValueError,SyntaxError,RecursionError) as exc:raise ValueError('Lista de campos do cálculo inválida.') from exc
    require(isinstance(values,list) and 1<=len(values)<=128 and all(isinstance(v,str) and 0<len(v.encode('utf-8'))<=4096 for v in values),'Campos do cálculo inválidos.')
    return dict(function=match[1],fields=values)


def parse_validation(script):
    match=re.fullmatch(r'AFRange_Validate\(\s*(true|false)\s*,\s*('+NUMBER+r')\s*,\s*(true|false)\s*,\s*('+NUMBER+r')\s*\)\s*;?',script)
    require(match is not None,'Validação fora do subconjunto AFRange_Validate suportado.')
    return dict(minimum=match[2] if match[1]=='true' else None,maximum=match[4] if match[3]=='true' else None)


def _number_arguments(helper, script):
    match=re.fullmatch(helper+r'\(\s*(\d{1,2})\s*,\s*(\d)\s*,\s*(\d)\s*,\s*(\d)\s*,\s*'
                       r'(?:"([^"\\\n]{0,16})"|\'([^\'\\\n]{0,16})\')\s*,\s*(true|false)\s*\)\s*;?',script)
    require(match is not None,helper+' fora do subconjunto suportado.')
    decimals,separator,negative,style=(int(match[i]) for i in range(1,5))
    require(decimals<=10 and separator in SEPARATORS and style==0,helper+' com parâmetros não suportados.')
    require(negative in (0,2),'Negativos em vermelho ainda não são suportados; use sinal ou parênteses.')
    currency=match[5] if match[5] is not None else match[6]
    return dict(decimals=decimals,separator=separator,negative=negative,currency=currency,prepend=match[7]=='true')


def parse_number_format(script):
    return _number_arguments('AFNumber_Format',script)


def parse_number_keystroke(script):
    return _number_arguments('AFNumber_Keystroke',script)


def format_number(number, rule):
    """Own AFNumber_Format display: half-up rounding, grouping, currency, sign or parentheses."""
    require(isinstance(number,Decimal) and number.is_finite(),'Número de formulário inválido.')
    with localcontext() as context:
        context.prec=40
        rounded=number.quantize(Decimal(1).scaleb(-rule['decimals']),rounding=ROUND_HALF_UP)
    integer,_,fraction=format(abs(rounded),'f').partition('.')
    group,decimal=SEPARATORS[rule['separator']]
    if group:
        integer=group.join(integer[max(0,i-3):i] for i in range(len(integer),0,-3)[::-1])
    text=integer+(decimal+fraction if rule['decimals'] else '')
    if rule['currency']:
        text=rule['currency']+text if rule['prepend'] else text+rule['currency']
    if rounded<0:
        text='('+text+')' if rule['negative']==2 else '-'+text
    return text


def _input_number(value, keystroke):
    """Canonical dot-decimal text for a field whose keystroke rule allows a comma decimal."""
    text=value.strip()
    if keystroke is None or SEPARATORS[keystroke['separator']][1]!=',' or ',' not in text:
        return value
    require('.' not in text and text.count(',')==1,'Use vírgula decimal, sem separador de milhar.')
    return text.replace(',','.')


def inspect_form_events(document):
    rules=[];unsupported=[]
    fields=document.get_fields() or {}
    require(len(fields)<=2048,'Formulário acima de 2048 campos para eventos.')
    for name,field in fields.items():
        if not terminal(field):continue
        actions=inherited(field,'/AA')
        if actions is None:continue
        actions=actions.get_object()
        require(isinstance(actions,dict),'Ações de campo inválidas.')
        for event,action in actions.items():
            require(len(rules)+len(unsupported)<MAX_RULES,'Formulário acima de 128 regras de evento.')
            try:
                script=_script(action)
                if event=='/C':rule=parse_calculation(script)
                elif event=='/V':rule=parse_validation(script)
                elif event=='/F':rule=parse_number_format(script)
                elif event=='/K':rule=parse_number_keystroke(script)
                else:raise ValueError('Evento ainda não suportado pelo motor declarativo.')
                rules.append(dict(field=name,event=event,rule=rule))
            except (ValueError,UnicodeError) as exc:unsupported.append(dict(field=name,event=event,reason=str(exc)))
    return dict(rules=rules,unsupported=unsupported,javascript_executed=False)


def _number(value):
    require(isinstance(value,str) and len(value)<=128 and (not value.strip() or re.fullmatch(NUMBER,value.strip())),
            'Use número decimal com ponto, sem separador de milhar.')
    try:number=Decimal(value.strip() or '0')
    except InvalidOperation as exc:raise ValueError('Número de formulário inválido.') from exc
    require(number.is_finite() and abs(number)<=Decimal('1e18'),'Número de formulário fora do intervalo permitido.')
    return number


def calculate_form_values(document,values):
    require(isinstance(values,dict) and 0<len(values)<=256 and all(isinstance(k,str) and isinstance(v,str) and len(v.encode('utf-8'))<=65536 for k,v in values.items()),'Informe de 1 a 256 valores textuais válidos.')
    fields=document.get_fields() or {};configuration=inspect_form_events(document)
    require(not configuration['unsupported'],'Há eventos não suportados; nenhum script será executado. Use o preenchimento simples ou um leitor compatível com esses eventos.')
    for name in values:
        require(name in fields and terminal(fields[name]) and inherited(fields[name],'/FT')=='/Tx','Campo de texto não encontrado.')
        require(not int(inherited(fields[name],'/Ff',0)) & 1,'Campo somente leitura não pode ser preenchido diretamente.')
    calculations={r['field']:r['rule'] for r in configuration['rules'] if r['event']=='/C'}
    require(not set(values)&calculations.keys(),'Preencha os dados de entrada; os campos calculados são produzidos pelo cálculo.')
    keystrokes={r['field']:r['rule'] for r in configuration['rules'] if r['event']=='/K'}
    result={name:_input_number(text,keystrokes.get(name)) for name,text in values.items()}
    for name in keystrokes.keys()&result.keys():
        _number(result[name])
    visiting=set();completed=set()
    def value(name):
        require(name in fields and terminal(fields[name]),'Campo dependente do cálculo não encontrado.')
        if name in calculations and name not in completed:
            require(name not in visiting and len(visiting)<64,'Cálculo circular ou acima de 64 dependências.')
            visiting.add(name);rule=calculations[name];numbers=[value(n) for n in rule['fields']]
            with localcontext() as context:
                context.prec=28;kind=rule['function']
                if kind in ('SUM','AVG'):number=sum(numbers,Decimal(0));number=number/len(numbers) if kind=='AVG' else number
                elif kind=='MIN':number=min(numbers)
                elif kind=='MAX':number=max(numbers)
                else:
                    number=Decimal(1)
                    for n in numbers:number*=n
            require(number.is_finite() and abs(number)<=Decimal('1e18'),'Resultado do cálculo acima do limite.')
            result[name]=format(number.normalize(),'f');completed.add(name);visiting.remove(name)
        return _number(result[name] if name in result else str(inherited(fields[name],'/V','')))
    for name in calculations:value(name)
    for entry in configuration['rules']:
        if entry['event']!='/V':continue
        number=value(entry['field']);rule=entry['rule']
        require((rule['minimum'] is None or number>=_number(rule['minimum'])) and
                (rule['maximum'] is None or number<=_number(rule['maximum'])),
                'Valor fora do intervalo permitido por uma regra de formulário.')
    require(len(result)<=256,'Resultado acima de 256 campos por alteração.')
    return result


def format_form_values(document,values):
    """Display text for fields with AFNumber_Format; field values stay unformatted."""
    formats={r['field']:r['rule'] for r in inspect_form_events(document)['rules'] if r['event']=='/F'}
    return {name:format_number(_number(value),formats[name]) for name,value in values.items()
            if name in formats and value.strip()}
