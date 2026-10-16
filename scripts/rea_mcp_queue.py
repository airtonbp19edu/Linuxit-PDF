"""Owned local MCP driver; reuse a single REA/Ghidra session across queries."""
import argparse,json,subprocess,time,threading
from pathlib import Path
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--session-dir',type=Path,required=True,help='Directory containing queue/*.json; results must be empty')
parser.add_argument('--rea',default='/workspace/.rea-cli/bin/rea')
args=parser.parse_args()
ROOT=args.session_dir.resolve()
if (ROOT/'STOP').exists():parser.error('Remove STOP only when deliberately creating a fresh session')
for subdir in ('queue','results','logs'):(ROOT/subdir).mkdir(parents=True,exist_ok=True)
if any((ROOT/'results').iterdir()):parser.error('Use a fresh results directory; previous results cannot represent this new live session')
def save_json(path,value):
    temporary=path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(value,indent=2))
    temporary.replace(path)

proc=subprocess.Popen([args.rea,'mcp'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                      stderr=(ROOT/'logs/rea-stderr.log').open('wb'),text=True,bufsize=1)
save_json(ROOT/'server-pid.json',{'pid':proc.pid,'owner':'foxit-rea-session','started':time.time()})
def emit(message):
    # A reconnect can close the launching tool's stdout; keep the owned session usable.
    with (ROOT/'logs/driver.log').open('a') as log:log.write(message+'\n')
    try:print(message,flush=True)
    except BrokenPipeError:pass
seq=0
pending={}
lock=threading.Lock()
def reader():
    for line in proc.stdout:
        try: msg=json.loads(line)
        except ValueError: continue
        with lock:
            if 'id' in msg:pending[msg['id']]=msg
            else:
                with (ROOT/'logs/notifications.jsonl').open('a') as out:out.write(json.dumps(msg)+'\n')
threading.Thread(target=reader,daemon=True).start()
def rpc(method,params,timeout=1900):
    global seq
    seq+=1;ident=seq
    proc.stdin.write(json.dumps({'jsonrpc':'2.0','id':ident,'method':method,'params':params})+'\n');proc.stdin.flush()
    until=time.monotonic()+timeout
    while time.monotonic()<until:
        with lock:msg=pending.pop(ident,None)
        if msg is not None:return msg
        if proc.poll() is not None:raise RuntimeError('REA server exited '+str(proc.returncode))
        time.sleep(.1)
    raise TimeoutError('REA request '+method)
try:
    init=rpc('initialize',{'protocolVersion':'2025-03-26','capabilities':{},'clientInfo':{'name':'foxit-rea-analysis','version':'1.0'}},30)
    save_json(ROOT/'results/initialize.json',init)
    proc.stdin.write(json.dumps({'jsonrpc':'2.0','method':'notifications/initialized'})+'\n');proc.stdin.flush()
    catalog=rpc('tools/list',{},30)
    save_json(ROOT/'results/tool-catalog.json',catalog)
    emit('MCP initialized; catalog retained')
    while not (ROOT/'STOP').exists():
        if (ROOT/'PAUSE').exists():time.sleep(.3);continue
        requests=sorted((ROOT/'queue').glob('*.json'))
        if not requests:time.sleep(.3);continue
        for path in requests:
            if (ROOT/'STOP').exists():break
            target=ROOT/'results'/path.name
            if target.exists():continue
            req=json.loads(path.read_text())
            started=time.monotonic()
            save_json(ROOT/'current.json',{'request':path.name,'tool':req['name'],'started':time.time()})
            emit('START '+path.name+' '+req['name'])
            try:
                result=rpc('tools/call',req)
                save_json(target,{'elapsed_sec':time.monotonic()-started,'response':result})
                emit('DONE '+path.name+' bytes='+str(target.stat().st_size)+' elapsed='+str(round(time.monotonic()-started,1)))
                if result.get('error') or result.get('result',{}).get('isError'):
                    (ROOT/'PAUSE').touch()
                    emit('PAUSED after tool error; inspect the result before removing PAUSE.')
                    break
            except Exception as exc:
                save_json(target,{'elapsed_sec':time.monotonic()-started,'error':type(exc).__name__+': '+str(exc)})
                emit('ERROR '+path.name+' '+str(exc))
                (ROOT/'PAUSE').touch()
                break
        time.sleep(.1)
finally:
    try:
        rpc('tools/call',{'name':'close_binary','arguments':{}},30)
    except Exception:pass
    proc.stdin.close()
    try:proc.wait(timeout=20)
    except subprocess.TimeoutExpired:proc.terminate();proc.wait(timeout=10)
