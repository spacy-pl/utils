import argparse
import json
import os
import re

import settings

HEADER = '''# coding: utf-8
from __future__ import unicode_literals


'''

MAPPING = {"nouns": set("K Q R M O T V S C X D N W U L Z P j d s l f e i m z o w".split()),
           "verbs": set("I B H J F p u h k".split()),
           "adjectives": set("Y".split()),
           "other": set("G E x g y".split() + [settings.NO_FLAG_SGN]),
           }


def create_rule_file(args, rules, key):
    pos = key[:-1] if key.endswith('s') else key  # bez s na końcu
    filename = "_{}_rules.py".format(pos)
    filepath = os.path.join(args.output_dir, filename)

    row_pattern = "    [\"{}\", \"{}\"],\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(HEADER)
        f.write("{}_RULES = [\n".format(pos.upper()))
        for rule in rules:
            re_word_suf = rule["word_suf"].replace('[', '([').replace(']', '])') + '$'
            re_lemma_suf = re.sub(r'\[.*\]', r'\\\\1', rule["lemma_suf"])
            rule_row = row_pattern.format(re_word_suf, re_lemma_suf)
            rule_row = rule_row.lower()
            f.write(rule_row)
        f.write("]\n")


def create_rule_files(args, rules, mapping):
    for key, flag_set in mapping.items():
        key_rules = [rule for flag, rule_list in rules.items() for rule in rule_list if flag in flag_set]
        create_rule_file(args, key_rules, key)


def create_word_file(args, words, key):
    filename = "_{}.py".format(key)
    filepath = os.path.join(args.output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(HEADER)
        f.write("{} = set(\"\"\"\n".format(key.upper()))
        f.write('\n'.join(words) + '\n')
        f.write("\"\"\".split())\n")


def create_word_files(args, words, mapping):
    for key, flag_set in mapping.items():
        key_words = [word for flag, word_list in words.items() for word in word_list if flag in flag_set]
        create_word_file(args, key_words, key)


def main(args):
    with open(args.rules, "r") as f:
        rules = json.load(f)
    create_rule_files(args, rules, MAPPING)

    with open(args.words, "r") as f:
        words = json.load(f)
    create_word_files(args, words, MAPPING)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Assigns lemmas to lemmatization rule flags')
    parser.add_argument('-r', '--rules', type=str, help='Rules extracted from ispell',
                        default=settings.LEMMA_RULES)
    parser.add_argument('-o', '--output_dir', type=str, help='Output file path',
                        default=settings.LEMMATIZER_DATA_DIR)
    parser.add_argument('-v', '--verbose', help='Display additional info',
                        action='store_true')
    parser.add_argument('-w', '--words', type=str, help='Words from ispell dict',
                        default=settings.LEMMA_WORDS)
    args = parser.parse_args()
    main(args)