import json
import argparse
import re

def main(args):
    with open("rules.json", "r") as f:
        rule_groups = json.load(f)
    with open("words.json", "r") as f:
        word_groups = json.load(f)

    lemmas = set()
    for f, r in rule_groups.items():
        for rule in r:
            # print(rule['word_suf']+'$', rule['lemma_suf'])
            if re.search(r'{}$'.format(rule['word_suf']), args.word.upper()):
                new_word_suf = rule['word_suf'].replace('[', '([').replace(']', '])')
                new_lemma_suf = re.sub(r'\[.*\]', r'\\1', rule['lemma_suf'])
                # print(rule['word_suf'], new_word_suf, rule['lemma_suf'], new_lemma_suf)
                m = re.search(r'{}$'.format(new_word_suf), args.word.upper())
                print(args.word, rule['word_suf'], rule['lemma_suf'])
                if m:
                    print('OK', m.groups())
                lemma = re.sub(r'{}$'.format(new_word_suf), r'{}'.format(new_lemma_suf), args.word.upper())
                print(args.word, rule['word_suf'], rule['lemma_suf'], lemma)
                lemmas.add(lemma)
    result = set()
    lemmas = {l.lower() for l in lemmas}
    print(lemmas)
    for f, w in word_groups.items():
        for word in w:
            if word in lemmas:
                result.add(word)
    print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Lemmatize word')
    parser.add_argument('word', type=str, help='word to lemmatize')
    parser.add_argument('--pos', type=str, help='pos tag of word')
    args = parser.parse_args()
    main(args)
