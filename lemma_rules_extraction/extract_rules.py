import argparse
import json
from collections import defaultdict, namedtuple

import settings

# aktualne dane pochodzą z sjp-ispell-pl-20181128-src

SKIP_FIRST_N = 34


def extract_comment(line):
    if line[0] == '#':
        comment = line[1:]
        line = ''
    else:
        splitted = line.split("#")
        line = splitted[0]
        if len(splitted) > 1:
            comment = splitted[1]
        else:
            comment = ''
    return line.strip(), comment.strip()


def main(args):

    with open(args.ispell_rules, "rb") as f:
            lines = f.readlines()

    lines = [l.decode('iso-8859-2').strip() for l in lines]
    lines = lines[SKIP_FIRST_N:]  # pominięcie pierwszych linii
    lines = [l.replace('\t', '') for l in lines]
    lines = [l for l in lines if l.replace(' ', '') != '']
    lines = [(l.replace(' ', ''), c) for l, c in [extract_comment(line) for line in lines]]
    lines = [l for l in lines if l[0] != '' or l[1] != '']

    rule_groups = defaultdict(list)
    comments = defaultdict(list)
    flag = ''
    for l in lines:
        line = l[0]
        if line.startswith('flag*'):
            flag = line[5]
        elif line == '' and l[1] != '':
            comments[flag].append(l[1])
        elif line != '':
            suf, ends = line.split('>')
            if ',' in ends:
                lemma_end, word_end = ends.split(',')
                lemma_end = lemma_end.strip()[1:]
                word_end = word_end.strip()
                word_suf = suf[:-len(lemma_end)] + word_end
            else:
                lemma_end = ''
                word_end = ends
                word_suf = suf + word_end
            rule_groups[flag].append({'word_suf': word_suf, "lemma_suf": suf})
        else:
            raise Exception("Unexpected empty line! ({})".format(l))

    with open(args.output, 'w') as f:
        json.dump(rule_groups, f)

    if args.verbose:
        for f, r in rule_groups.items():
            print(f, len(r))

    if args.flags:
        with open(args.description_file, "w") as f:
            for flag, c in comments.items():
                f.write("\n===== " + flag + " =====\n")
                f.write('\n'.join(c) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract rules from ispell aff file to more convenient form")
    parser.add_argument('-r', '--ispell_rules', type=str, help="Ispell aff file path",
                        default=settings.ISPELL_RULES)
    parser.add_argument('-o', '--output', type=str, help="Output file path",
                        default=settings.LEMMA_RULES)
    parser.add_argument('-v', '--verbose', help="Display additional info",
                        action='store_true')
    parser.add_argument('-f', '--flags', help="Generate flags description file",
                        action='store_true')
    parser.add_argument('--description_file', type=str, help="Descrition file path",
                        default=settings.FLAGS_DESC)
    args = parser.parse_args()
    main(args)