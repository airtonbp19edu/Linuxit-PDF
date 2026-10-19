"""Own reading defaults. No document paths, passwords or private keys stored."""
import json,os,tempfile
from pathlib import Path

DEFAULTS=dict(zoom_mode='fit-width',zoom_percent=100,sidebar=True,highlight_all=True)


def preferences_path():
    return Path(os.environ.get('XDG_CONFIG_HOME') or Path.home()/'.config')/'linuxit-pdf/reading.json'


def validate(values):
    if (not isinstance(values,dict) or set(values)!=set(DEFAULTS)
            or values['zoom_mode'] not in ('fit-page','fit-width','percent')
            or type(values['zoom_percent']) is not int or not 1<=values['zoom_percent']<=6400
            or type(values['sidebar']) is not bool or type(values['highlight_all']) is not bool):
        raise ValueError('Preferências de leitura inválidas.')
    return dict(values)


def read_preferences():
    try:
        path=preferences_path()
        if path.stat().st_size>8192:return dict(DEFAULTS)
        return validate(json.loads(path.read_text(encoding='utf-8')))
    except (OSError,ValueError,TypeError):return dict(DEFAULTS)


def save_preferences(values):
    values=validate(values);path=preferences_path();path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    descriptor,name=tempfile.mkstemp(prefix='.reading-',dir=path.parent)
    try:
        with os.fdopen(descriptor,'w',encoding='utf-8') as output:
            json.dump(values,output);output.write('\n');output.flush();os.fsync(output.fileno())
        os.replace(name,path)
    finally:Path(name).unlink(missing_ok=True)
