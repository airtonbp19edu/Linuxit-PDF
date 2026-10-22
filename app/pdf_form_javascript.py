"""Opt-in field JavaScript in a separate, resource-limited QuickJS process.

No Python callable, module loader, filesystem, network, timers or GUI object is
installed in the JS runtime. Only field values and /K /V /C /F scripts cross the
JSON boundary. Document/open/page actions are deliberately never executed.
This isolates capabilities; it is not a claim to contain a native engine CVE.
"""
import importlib.util
import json
import math
import os
from pathlib import Path
import subprocess
import sys

MAX_REQUEST = 4 * 1024**2
MAX_VALUE = 65536
MAX_SCRIPTS = 128
ENGINE_VERSION = '0.15.1.1'


def available():
    return importlib.util.find_spec('_quickjs') is not None


def _require(value, message):
    if not value:
        raise ValueError(message)


def _request(document, changes):
    from pdf_form_controls import inherited, terminal
    from pdf_form_events import _script
    fields = document.get_fields() or {}
    _require(isinstance(changes, dict) and 1 <= len(changes) <= 256, 'Informe de 1 a 256 campos para JavaScript.')
    _require(len(fields) <= 2048, 'Formulário acima de 2048 campos.')
    rows, scripts = {}, 0
    for name, field in fields.items():
        if not terminal(field):
            continue
        if inherited(field, '/FT') != '/Tx':
            # Mixing unsupported controls with script calculations must not use
            # invented string values or silently skip their actions.
            _require(inherited(field, '/AA') is None, 'JavaScript em controles não textuais ainda não é suportado.')
            continue
        value = inherited(field, '/V', '')
        _require(isinstance(value, str) and len(value.encode('utf-8')) <= MAX_VALUE, 'Valor de campo acima do limite.')
        row = dict(value=str(value), readonly=bool(int(inherited(field, '/Ff', 0)) & 1), actions={})
        actions = inherited(field, '/AA')
        if actions is not None:
            actions = actions.get_object()
            _require(isinstance(actions, dict), 'Ações de campo inválidas.')
            for event, action in actions.items():
                _require(event in ('/K', '/V', '/C', '/F'), 'Evento de campo fora de K/V/C/F; execução recusada.')
                row['actions'][str(event)] = _script(action)
                scripts += 1
        rows[str(name)] = row
    _require(scripts <= MAX_SCRIPTS, 'Formulário acima de 128 scripts.')
    for name, value in changes.items():
        _require(name in rows and isinstance(value, str) and len(value.encode('utf-8')) <= MAX_VALUE, 'Campo ou valor JavaScript inválido.')
        _require(not rows[name]['readonly'] and '/C' not in rows[name]['actions'], 'Preencha os dados de entrada, não o campo calculado ou somente leitura.')
    order = []
    form = document.root_object.get('/AcroForm')
    raw_order = form.get_object().get('/CO', []) if form else []
    _require(len(raw_order) <= 2048, 'Ordem de cálculo acima do limite.')
    refs = {id(field.indirect_reference.get_object()): name for name, field in fields.items()
            if getattr(field, 'indirect_reference', None) is not None}
    for ref in raw_order:
        name = refs.get(id(ref.get_object()))
        if name in rows and name not in order:
            order.append(name)
    order.extend(name for name, row in rows.items() if '/C' in row['actions'] and name not in order)
    return dict(fields=rows, changes=changes, order=order)


def run_form_javascript(document, changes):
    """Return (raw changed values, display values); nothing is committed here."""
    request = _request(document, changes)
    raw = json.dumps(request, ensure_ascii=True).encode('ascii')
    _require(len(raw) <= MAX_REQUEST, 'Pedido JavaScript acima de 4 MiB.')
    spec = importlib.util.find_spec('_quickjs')
    if spec is None or not spec.origin:
        raise RuntimeError('JavaScript isolado requer python-quickjs-ng ' + ENGINE_VERSION + '.')
    # -I ignores PYTHONPATH/user-site/current-directory imports. Only the known
    # binary-extension directory is explicitly appended inside the child.
    command = [sys.executable, '-I', str(Path(__file__).resolve()), '--worker', str(Path(spec.origin).parent)]
    environment = {key: value for key, value in os.environ.items()
                   if key.upper() in ('SYSTEMROOT', 'WINDIR', 'PATH', 'TEMP', 'TMP', 'LD_LIBRARY_PATH')}
    with subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=environment, cwd=str(Path(__file__).parent),
                          creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)) as process:
        try:
            output, error = process.communicate(raw, timeout=6)
        except subprocess.TimeoutExpired:
            process.kill(); process.communicate()
            raise ValueError('JavaScript excedeu o limite de tempo; nenhuma alteração foi aplicada.') from None
    _require(process.returncode == 0 and len(output) <= MAX_REQUEST, 'JavaScript falhou; nenhuma alteração foi aplicada.')
    try:
        reply = json.loads(output)
    except (ValueError, UnicodeError):
        raise ValueError('Resposta JavaScript inválida; nenhuma alteração foi aplicada.') from None
    _require(reply.get('ok') is True, 'JavaScript recusado: ' + str(reply.get('error', 'erro desconhecido'))[:300])
    _require(set(reply) == {'ok', 'values', 'display'}, 'Resposta JavaScript fora do contrato.')
    result, display = reply.get('values'), reply.get('display')
    for values in (result, display):
        _require(isinstance(values, dict) and len(values) <= 256 and all(name in request['fields'] and isinstance(value, str)
                 and len(value.encode('utf-8')) <= MAX_VALUE for name, value in values.items()), 'Resultado JavaScript fora do contrato.')
    _require(set(display) <= set(result), 'Aparência JavaScript sem valor correspondente.')
    for name in result:
        row = request['fields'][name]
        _require(not row['readonly'] or '/C' in row['actions'] and name in request['order'],
                 'JavaScript tentou alterar campo somente leitura fora do cálculo autorizado.')
    return result, display


BRIDGE = r'''
(function (input) {
  "use strict";
  // PDF code runs in a global Function scope but shares this engine's builtins.
  // Protect the bridge's collection, validation and serialization intrinsics:
  // e.g. Object.prototype.toJSON must not forge an apparently valid transaction.
  for (const name of ['Object','Array','Function','String','Number','Boolean','Set','Map','JSON','Math','RegExp']) {
    const item = globalThis[name];
    if (item.prototype) Object.freeze(item.prototype);
    Object.freeze(item);
    Object.defineProperty(globalThis,name,{value:item,writable:false,configurable:false});
  }
  const stringify = JSON.stringify.bind(JSON), own = Function.call.bind(Object.prototype.hasOwnProperty);
  const fields = input.fields, values = Object.create(null), api = Object.create(null), changed = new Set();
  const display = Object.create(null); let active = null;
  function text(v) {
    if (!['string','number','boolean'].includes(typeof v) || (typeof v === 'number' && !Number.isFinite(v)))
      throw Error('Valor de campo precisa ser texto, número finito ou booleano.');
    v = String(v); if (v.length > 65536) throw Error('Valor de campo acima do limite.'); return v;
  }
  for (const name of Object.keys(fields)) {
    values[name] = fields[name].value;
    const item = Object.create(null);
    Object.defineProperties(item, {
      name: {value:name}, readonly:{value:fields[name].readonly},
      value: {get:()=>values[name], set:v=>{
        if (fields[name].readonly && !(active && active.name === name && active.event === '/C'))
          throw Error('Campo somente leitura.');
        values[name]=text(v);changed.add(name);
      }},
      valueAsString: {get:()=>values[name]}
    });
    api[name]=Object.freeze(item);
  }
  function getField(name) {return own(api,String(name)) ? api[String(name)] : null;}
  const doc = Object.freeze({getField, numFields:Object.keys(fields).length,
    getNthFieldName:index=>Object.keys(fields)[index] ?? null});
  Object.defineProperty(globalThis,'getField',{value:getField,writable:false,configurable:false});
  let event;
  function number(v) {let n=Number(v);if(!Number.isFinite(n))throw Error('Número inválido.');return n;}
  Object.defineProperties(globalThis, {
    AFSimple_Calculate:{value:function(op,names){
      if(!Array.isArray(names)||!names.length||names.length>128)throw Error('Lista de cálculo inválida.');
      let n=names.map(name=>{let f=getField(name);if(!f)throw Error('Campo ausente.');return number(f.value);});
      event.value=op==='SUM'?n.reduce((a,b)=>a+b,0):op==='AVG'?n.reduce((a,b)=>a+b,0)/n.length:
        op==='PRD'?n.reduce((a,b)=>a*b,1):op==='MIN'?Math.min(...n):op==='MAX'?Math.max(...n):NaN;
    }},
    AFRange_Validate:{value:function(low,min,high,max){let n=number(event.value);event.rc=(!low||n>=min)&&(!high||n<=max);}},
    AFNumber_Format:{value:function(dec,sep,neg,style,currency,prepend){
      if(!Number.isInteger(dec)||dec<0||dec>10||![0,1,2,3,4].includes(sep)||![0,2].includes(neg)||style!==0)
        throw Error('Formato numérico fora do contrato.');
      let n=number(event.value),v=Math.abs(n).toFixed(dec).split('.'),group=[',','','.','',"'"][sep],dot=[ '.', '.', ',', ',', '.' ][sep];
      if(group)v[0]=v[0].replace(/\B(?=(\d{3})+(?!\d))/g,group);
      let s=v.join(dot);s=prepend?currency+s:s+currency;event.value=n<0?(neg===2?'('+s+')':'-'+s):s;
    }},
    AFNumber_Keystroke:{value:function(_dec,sep){let t=String(event.value);if(sep===2||sep===3)t=t.replace(',','.');
      event.rc=/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$/.test(t)||t==='';event.value=t;}}
  });
  const run = Function('event','script','return Function("event", "\\\"use strict\\\";\\n"+script).call(this,event);');
  function invoke(name,key,value) {
    let code=fields[name].actions[key];if(code===undefined)return value;
    active={name,event:key};event={value,rc:true,target:api[name],willCommit:true,change:'',name:key.slice(1)};
    // The Function constructor gives document code a global scope, not access
    // to the closure carrying the parent input, serialization or transaction.
    run.call(doc,event,code);
    if(event.rc!==true)throw Error('Validação do formulário recusou o valor.');
    const result=text(event.value);active=null;return result;
  }
  for(const name of Object.keys(input.changes)) {
    let value=text(input.changes[name]);value=invoke(name,'/K',value);value=invoke(name,'/V',value);
    values[name]=value;changed.add(name);
  }
  for(const name of input.order) if(own(fields[name].actions,'/C')) {
    values[name]=invoke(name,'/C',values[name]);changed.add(name);
    values[name]=invoke(name,'/V',values[name]);
  }
  for(const name of changed) if(own(fields[name].actions,'/F')) display[name]=invoke(name,'/F',values[name]);
  let result=Object.create(null);for(const name of changed)result[name]=values[name];
  return stringify({ok:true,values:result,display});
})
'''


def _worker(dependency):
    sys.path.append(dependency)
    import _quickjs
    try:
        import resource
        resource.setrlimit(resource.RLIMIT_CPU, (3, 3))
        resource.setrlimit(resource.RLIMIT_AS, (256 * 1024**2, 256 * 1024**2))
    except (ImportError, OSError, ValueError):
        pass
    raw = sys.stdin.buffer.read(MAX_REQUEST + 1)
    _require(len(raw) <= MAX_REQUEST, 'Pedido acima do limite.')
    context = _quickjs.Context()
    context.set_memory_limit(32 * 1024**2)
    context.set_max_stack_size(512 * 1024)
    context.set_time_limit(1.0)
    try:
        # JSON is inserted as a quoted string, never as executable input.
        expression = '(' + BRIDGE + ')(JSON.parse(' + json.dumps(raw.decode('ascii')) + '))'
        output = context.eval(expression)
        _require(isinstance(output, str) and len(output.encode('utf-8')) <= MAX_REQUEST, 'Resultado acima do limite.')
        print(output)
    except Exception as exc:
        print(json.dumps(dict(ok=False, error=str(exc)[:300])))


if __name__ == '__main__' and len(sys.argv) == 3 and sys.argv[1] == '--worker':
    _worker(sys.argv[2])
