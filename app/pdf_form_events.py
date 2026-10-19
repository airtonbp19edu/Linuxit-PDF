"""Declarative Acrobat helper subset; never execute JavaScript from a PDF."""
import ast
from decimal import Decimal, InvalidOperation, localcontext
import re

from pdf_form_controls import inherited, terminal

MAX_RULES = 128
MAX_SCRIPT = 16384
NUMBER = r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)'


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
    result=dict(values);visiting=set();completed=set()
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
