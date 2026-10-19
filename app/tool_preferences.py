"""Small validated tool defaults, separate from existing reading preferences."""
import json,os,tempfile
from pathlib import Path
from reading_preferences import preferences_path

DEFAULTS=dict(speech_voice='pt-br',speech_rate=175,ocr_language='por',ocr_psm=3,ocr_dpi=300)


def validate(values):
    if not isinstance(values,dict) or set(values)!=set(DEFAULTS) or values['speech_voice'] not in ('pt-br','en') or type(values['speech_rate']) is not int or not 80<=values['speech_rate']<=300 or values['ocr_language'] not in ('por','eng','por+eng') or type(values['ocr_psm']) is not int or values['ocr_psm'] not in (3,6,11) or type(values['ocr_dpi']) is not int or values['ocr_dpi'] not in (150,300):
        raise ValueError('Padrões de voz/OCR inválidos.')
    return dict(values)


def read_tool_preferences():
    try:
        path=preferences_path().with_name('tools.json')
        if path.stat().st_size>8192:return dict(DEFAULTS)
        return validate(json.loads(path.read_text(encoding='utf-8')))
    except (OSError,ValueError,TypeError):return dict(DEFAULTS)


def save_tool_preferences(values):
    values=validate(values);path=preferences_path().with_name('tools.json');path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    descriptor,name=tempfile.mkstemp(prefix='.tools-',dir=path.parent)
    try:
        with os.fdopen(descriptor,'w',encoding='utf-8') as stream:json.dump(values,stream);stream.write('\n');stream.flush();os.fsync(stream.fileno())
        os.replace(name,path)
    finally:Path(name).unlink(missing_ok=True)
