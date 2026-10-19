"""Offline WAV export through eSpeak NG, without network or generative models."""
from pathlib import Path
import shutil, subprocess, tempfile, wave
from local_files import publish_copy
from platform_runtime import subprocess_options
from search_tasks import run_search_worker


def export_speech(destination,request):
    if (not isinstance(request,dict) or set(request)!={'text','voice','rate'}
            or not isinstance(request['text'],str) or not request['text'].strip()
            or len(request['text'])>20000 or len(request['text'].encode('utf-8'))>128*1024
            or request['voice'] not in {'pt-br','en'} or type(request['rate']) is not int
            or not 80<=request['rate']<=300):
        raise ValueError('Voz: até20000 caracteres, português/inglês e80–300 palavras por minuto.')
    executable=shutil.which('espeak-ng')
    if not executable:raise RuntimeError('eSpeak NG indisponível neste ambiente.')
    destination=Path(destination)
    if destination.suffix.lower()!='.wav' or destination.exists() or destination.is_symlink():
        raise ValueError('Escolha um novo arquivo .wav.')
    with tempfile.TemporaryDirectory(prefix='linuxit-speech-') as folder:
        output=Path(folder)/'speech.wav'
        proc=subprocess.run([executable,'--stdin','-v',request['voice'],'-s',str(request['rate']),'-w',str(output)],
            input=request['text'].encode('utf-8'),stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,timeout=120,**subprocess_options())
        if proc.returncode or not output.is_file() or output.stat().st_size>64*1024**2:
            raise RuntimeError('Falha na síntese ou áudio acima de64MiB.')
        with wave.open(str(output),'rb') as audio:
            if audio.getnframes()<=0 or audio.getnchannels()!=1 or audio.getsampwidth()!=2:raise RuntimeError('Áudio PCM mono inválido.')
            seconds=audio.getnframes()/audio.getframerate()
        publish_copy(output,destination)
    return dict(schema='linuxit-speech-wav-v1',path=str(destination),seconds=seconds,offline=True)


def invoke_speech(destination,text,voice='pt-br',rate=175,cancel=None):
    return run_search_worker('speech-export',destination,dict(text=text,voice=voice,rate=rate),cancel,timeout=150)
