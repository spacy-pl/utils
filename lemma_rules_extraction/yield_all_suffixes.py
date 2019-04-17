# coding: utf-8
import sre_yield
import string
import json
import sys
import os

sys.path.append(".")
from data.lemmatizer_data.lemma_sources._adjective_rules import ADJECTIVE_RULES
from data.lemmatizer_data.lemma_sources._adverb_rules import ADVERB_RULES
from data.lemmatizer_data.lemma_sources._noun_rules import NOUN_RULES
from data.lemmatizer_data.lemma_sources._participle_rules import PARTICIPLE_RULES
from data.lemmatizer_data.lemma_sources._verb_rules import VERB_RULES
from data.lemmatizer_data.lemma_sources._other_rules import OTHER_RULES

charset = string.ascii_lowercase + "ąężźćńółęąś"

def generate_rules(rules):
    # rules are expected to be in format:
    # [(suffix, (regex, replacement))]
    expanded_rules = []
    for rule in rules:
        replacement = rule[1]
        regex = rule[0]
        suffixes = list(sre_yield.AllStrings(rule[0], charset=charset))
        expanded_rules += [(suf, regex, replacement) for suf in suffixes]

    return expanded_rules

if __name__ == "__main__":
    output = os.path.expanduser("./_expanded_rules.py")
    prefix = os.path.expanduser("./data/lemmatizer_data/lemma_sources_exp/")
    os.makedirs(prefix, exist_ok=True)
    HEADER = "# coding: utf-8\nfrom __future__ import unicode_literals\n\n"
    INDENT = 4*" "

    LEMMA_RULES = {'adj': ADJECTIVE_RULES, 'adv': ADVERB_RULES, 'noun': NOUN_RULES,
                    'part': PARTICIPLE_RULES, 'verb': VERB_RULES, 'other': OTHER_RULES}

    NAMES = {'adj': {'rules': 'ADJECTIVE_RULES', 'filename': "_adjective_rules.py"},
             'adv': {'rules': 'ADVERB_RULES', 'filename': "_adverb_rules.py" },
             'noun': {'rules': 'NOUN_RULES', 'filename': "_noun_rules.py"},
             'part': {'rules': 'PARTICIPLE_RULES', 'filename': "_participle_rules.py"},
             'verb': {'rules': 'VERB_RULES', 'filename': '_verb_rules.py'},
             'other': {'rules': 'OTHER_RULES', 'filename': None}}

    exp_rules = {}
    for univ_pos in ['noun', 'verb', 'adj', 'adv', 'part']:
        exp_rules = generate_rules(LEMMA_RULES.get(univ_pos, []) + LEMMA_RULES.get('other', {}))

        with open(os.path.join(prefix, os.path.expanduser(NAMES[univ_pos]['filename'])), 'w+') as f:
            text = HEADER + NAMES[univ_pos]['rules'] + " = [\n"
            for rule in exp_rules:
                text += INDENT + json.dumps(rule) + ",\n"
            text = text[:-2] + "\n]\n"
            f.write(text)

