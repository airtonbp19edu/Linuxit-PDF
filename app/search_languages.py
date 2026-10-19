"""Explicit language choices for the unchanged pinned Snowball Python package."""
from importlib import import_module
from pathlib import Path
import sys

LANGUAGES = {
    'pt':('portuguese','português'),'en':('english','inglês'),
    'es':('spanish','espanhol'),'fr':('french','francês'),'de':('german','alemão'),
    'it':('italian','italiano'),'nl':('dutch','neerlandês'),'ar':('arabic','árabe'),
    'hy':('armenian','armênio'),'eu':('basque','basco'),'ca':('catalan','catalão'),
    'cs':('czech','tcheco'),'da':('danish','dinamarquês'),'eo':('esperanto','esperanto'),
    'et':('estonian','estoniano'),'fi':('finnish','finlandês'),'el':('greek','grego'),
    'hi':('hindi','híndi'),'hu':('hungarian','húngaro'),'id':('indonesian','indonésio'),
    'ga':('irish','irlandês'),'lt':('lithuanian','lituano'),'ne':('nepali','nepalês'),
    'no':('norwegian','norueguês'),'fa':('persian','persa'),'pl':('polish','polonês'),
    'ro':('romanian','romeno'),'ru':('russian','russo'),'sr':('serbian','sérvio'),
    'st':('sesotho','sesoto'),'sv':('swedish','sueco'),'ta':('tamil','tâmil'),
    'tr':('turkish','turco'),'yi':('yiddish','iídiche'),
    'en-porter':('porter','inglês (Porter)'),'nl-porter':('dutch_porter','neerlandês (Porter)'),
}
LANGUAGE_MODES=[('stem-'+code,'Radicais: '+name) for code,(_,name) in LANGUAGES.items()]


def python_stemmer(mode):
    if not isinstance(mode,str) or mode not in {'stem-'+code for code in LANGUAGES}:
        raise ValueError('Idioma de radicais não suportado.')
    algorithm=LANGUAGES[mode[5:]][0]
    vendor=str(Path(__file__).resolve().parent/'vendor')
    if vendor not in sys.path:sys.path.insert(0,vendor)
    module=import_module('snowballstemmer.'+algorithm+'_stemmer')
    name=''.join(word.capitalize() for word in algorithm.split('_'))+'Stemmer'
    return getattr(module,name)()
