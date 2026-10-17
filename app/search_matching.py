"""Bounded own Unicode query modes; no regular expression or original analyzer."""
import unicodedata


def normalized(text, match_case=False, ignore_accents=False):
    text = unicodedata.normalize('NFC', text)
    if not match_case:
        text = text.casefold()
    if ignore_accents:
        text = ''.join(c for c in unicodedata.normalize('NFD', text)
                       if unicodedata.category(c) != 'Mn')
    return text


def is_word(character):
    return character == '_' or unicodedata.category(character)[0] in 'LNM'


def tokens(text):
    start = None
    for position, char in enumerate(text):
        if is_word(char):
            if start is None:
                start = position
        elif start is not None:
            yield start, position, text[start:position]
            start = None
    if start is not None:
        yield start, len(text), text[start:]


def validate_query(query, mode='literal', proximity_distance=0, *, normalized_input=False):
    # NFC/casefold may expand one input character into up to three characters.
    # The original 256-character literal contract applies before normalization.
    maximum = 768 if normalized_input else 256
    if not isinstance(query, str) or len(query) > maximum:
        raise ValueError('A pesquisa deve ter no máximo 256 caracteres.')
    if not isinstance(mode, str) or mode not in {'literal', 'wildcard', 'proximity'}:
        raise ValueError('Modo de pesquisa não suportado.')
    if type(proximity_distance) is not int or not 0 <= proximity_distance <= 50:
        raise ValueError('A distância deve ser um inteiro de 0 a 50 palavras.')
    if not query.strip():
        return
    if mode == 'wildcard':
        if (len(query) > 64 or sum(c in '*?' for c in query) > 8
                or not any(is_word(c) for c in query)
                or any(not is_word(c) and c not in '*?' for c in query)):
            raise ValueError('Coringa: use uma palavra de até 64 caracteres, com até oito * ou ?, e ao menos uma letra ou número.')
    elif mode == 'proximity':
        words = list(tokens(query))
        if not 2 <= len(words) <= 8 or any(not is_word(c) and not c.isspace() for c in query):
            raise ValueError('Proximidade: informe de duas a oito palavras, na ordem desejada, separadas por espaços.')


def literal_spans(text, needle, whole_words=False):
    if not needle:
        return
    start = 0
    while True:
        pos = text.find(needle, start)
        if pos < 0:
            return
        end = pos + len(needle)
        bounded = ((pos == 0 or not is_word(text[pos - 1]))
                   and (end == len(text) or not is_word(text[end])))
        if not whole_words or bounded:
            yield pos, end
        start = end


def _glob(word, pattern):
    # One wildcard token, bounded pattern and token length; no regex backtracking.
    position = part = 0
    star = -1
    retry = 0
    while position < len(word):
        if part < len(pattern) and (pattern[part] == '?' or pattern[part] == word[position]):
            position += 1
            part += 1
        elif part < len(pattern) and pattern[part] == '*':
            star, retry = part, position
            part += 1
        elif star >= 0:
            retry += 1
            position, part = retry, star + 1
        else:
            return False
    return all(char == '*' for char in pattern[part:])


def query_spans(text, needle, whole_words=False, mode='literal', proximity_distance=0):
    """Positions on normalized text; proximity includes the intervening interval."""
    validate_query(needle, mode, proximity_distance, normalized_input=True)
    if mode == 'literal':
        yield from literal_spans(text, needle, whole_words)
        return
    words = list(tokens(text))
    if any(len(word) > 4096 for _, _, word in words):
        raise ValueError('Uma palavra excede o limite de 4096 caracteres dos modos avançados.')
    if mode == 'wildcard':
        for start, end, word in words:
            if _glob(word, needle):
                yield start, end
        return
    terms = [word for _, _, word in tokens(needle)]
    skip_before = 0
    for first, (start, _, word) in enumerate(words):
        if first < skip_before or not terms or word != terms[0]:
            continue
        previous = first
        for term_index, term in enumerate(terms[1:], 1):
            last = min(len(words) - 1, first + term_index + proximity_distance)
            match = next((i for i in range(previous + 1, last + 1) if words[i][2] == term), None)
            if match is None:
                break
            previous = match
        else:
            yield start, words[previous][1]
            skip_before = previous + 1
