import os
import re
import sys
import nltk
import json
import spacy
from numpy import log

from spacy.lang.pl import Polish


LATIN_UPPERCASE_REGEX = 'A-Z'
POLISH_SPECIAL_UPPERCASE_REGEX = 'ĄĆĘŁŃÓŚŹŻ'

LATIN_LOWERCASE_REGEX = LATIN_UPPERCASE_REGEX.lower()
POLISH_SPECIAL_LOWERCASE_REGEX = POLISH_SPECIAL_UPPERCASE_REGEX.lower()

POLISH_UPPERCASE_REGEX = f'[{LATIN_UPPERCASE_REGEX}|{POLISH_SPECIAL_UPPERCASE_REGEX}]'
POLISH_LOWERCASE_REGEX = f'[{LATIN_LOWERCASE_REGEX}|{POLISH_SPECIAL_LOWERCASE_REGEX}]'

PUNCT = set('… …… , : ; \! \? ¿ ؟ ¡ \( \) \[ \] \{ \} < > _ # \* & 。 ？ ！ ， 、 ； ： ～ · । ، ؛ ٪'.split(' '))
QUOTE = set('\' \'\' " ” “ `` ` ‘ ´ ‘‘ ’’ ‚ , „ » « 「 」 『 』 （ ） 〔 〕 【 】 《 》 〈 〉'.split(' '))


def get_orth(word):
    return word


def get_lower(word):
    return word.lower()


def get_upper(word):
    return word.upper()


def get_norm(word):
    return word.lower()


def get_length(word):
    return len(word)


def get_cluster(token):
    return str(token.cluster)  # it's a string according to spaCy docs - why?


def get_prob(count):
    return log(count/fd.N())


def get_shape(word):
    t1 = re.sub(POLISH_UPPERCASE_REGEX, 'X', word)
    t2 = re.sub(POLISH_LOWERCASE_REGEX, 'x', t1)
    return re.sub('[0-9]', 'd', t2)


def is_upper(word):
    return word.isupper()


def is_lower(word):
    return word.islower()


def is_ascii(word):
    return all(ord(c) < 128 for c in word)


def is_alpha(word):
    return word.isalpha()


def is_digit(word):
    return word.isdigit()


def is_punct(word):
    return all(c in PUNCT for c in word)


def is_quote(word):
    return all(c in QUOTE for c in word)


def is_space(word):
    return bool(re.match(r'^\s+$', word))


vocab = []
nlp = Polish()

corpus_path = os.path.abspath("./data/NKJP_1.2_nltk/")
corpus = nltk.corpus.reader.TaggedCorpusReader(root=corpus_path, fileids=".*")
fd = nltk.FreqDist(corpus.words())
fd.most_common()
samples = fd.most_common()

for i, t in enumerate(samples):
    word, count = t
    token = nlp(word)[0]
    word_entry = {
        "orth": str(get_orth(word)),
        "id": int(i),
        "lower": str(get_lower(word)),
        "norm": str(get_norm(word)),
        "shape": str(get_shape(word)),
        "prefix": str(token.prefix_),
        "suffix": str(token.suffix_),
        "length": int(get_length(word)),
        "cluster": str(get_cluster(token)),
        "prob": float(get_prob(count)),
        "is_alpha": bool(is_alpha(word)),
        "is_ascii": bool(is_ascii(word)),
        "is_digit": bool(is_digit(word)),
        "is_lower": bool(is_lower(word)),
        "is_punct": bool(is_punct(word)),
        "is_space": bool(is_space(word)),
        "is_title": bool(token.is_title),
        "is_upper": bool(is_upper(word)),
        "like_url": bool(token.like_url),
        "like_num": bool(token.like_num),
        "like_email": bool(token.like_email),
        "is_stop": bool(token.is_stop),
        "is_oov": bool(token.is_oov),
        "is_quote": bool(is_quote(word)),
        "is_left_punct": bool(token.is_left_punct),
        "is_right_punct": bool(token.is_right_punct)
    }
    vocab += [word_entry]

first_line = {"lang": "pl", "oov_prob": -20}

with open('./data/vocab.jsonl', 'w+') as f:
    json.dump(first_line, f)
    f.write('\n')
    for entry in vocab:
        json.dump(entry, f)
        f.write('\n')
