import xml.etree.ElementTree as ET
from NER_pwr_to_spacy import NER_pwr_to_spacy
import json
import os
import click

path_prefix = './'
corpus_path = 'data/kpwr-1.1/'


class setCounter:
    def __init__(self):
        self.contents = {}

    def count(self, k, times=1):
        if k in self.contents:
            self.contents[k] += times
        else:
            self.contents[k] = times

    def merge(self, other):
        for k in other.contents:
            self.count(k, other.contents[k])


def get_subdirs(dir):
    return [name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name))]


class Token:
    def __init__(self, orth, attribs, id):
        self.orth = orth
        self.attribs = attribs
        self.id = id

    def is_NE(self):
        return self.get_NE() is not None

    def get_NE(self):
        for attrib in self.attribs:
            for k in attrib:
                if attrib[k] != "0":
                    return k

        return None

    def __str__(self):
        return (self.orth + ":" + str(self.attribs))


def process_token(tok):
    attribs = []
    orth = tok.find("orth").text
    for ann in tok.iter("ann"):
        if ann.attrib['chan'].endswith("nam"):  # and ann.text != "0":
            attribs += [{ann.attrib['chan']: ann.text}]

    return Token(orth, attribs, -1)


def get_common_tag(t1, t2):
    set1 = set(t1.attribs)
    set2 = set(t2.attribs)
    common = list(set1 & set2)
    return common[0] if len(common) > 0 else None


def get_all_labels(tokens):
    labels = set()
    for tok in tokens:
        for attr in tok.attribs:
            labels.add(attr)

    return labels


def get_all_labels_with_cardinalities(tokens):
    labels = setCounter()
    for tok in tokens:
        for attr in tok.attribs:
            labels.count(attr)

    return labels


def map_labels(tokens, map):
    for tok in tokens:
        tok.attribs = [{map[k]: v} for attrib in tok.attribs for k, v in attrib.items()]

    return tokens


def still_in_sequence(v1, v2):
    return any(v1e == v2e != "0" for v1e in v1 for v2e in v2)


def get_last_label(v):
    for i, e in enumerate(v):
        if e != "0":
            return i
    return None


def get_longest_sequences(tokens):
    res = []
    b = 0
    e = 0
    attribs = [k for d in tokens[0].attribs for k in d]
    last_set = None

    while e != len(tokens) - 1:
        current_token = tokens[e]

        if last_set == None:
            last_set = [v for d in current_token.attribs for k, v in d.items()]
            b = e
        else:
            new_set = [v for d in current_token.attribs for k, v in d.items()]
            if not still_in_sequence(last_set, new_set):
                label_id = get_last_label(last_set)
                if (label_id != None):
                    label = attribs[label_id]
                    res.append((b, e, label))
                b = e

            last_set = new_set
        e += 1

    return res


emptyset = set()


def pick_tags(tokens):
    longest_sequences = get_longest_sequences(tokens)
    for b, e, label in longest_sequences:
        seq = tokens[b:e]
        for tok in seq:
            tok.attribs = [{label: '1'}]
        tokens[b:e] = seq
    return tokens


def convert_to_biluo(tokens):
    out = []
    in_ne = False
    for i, token in enumerate(tokens[:-1]):
        if in_ne:
            if token.is_NE():
                if tokens[i + 1].is_NE() and token.get_NE() == tokens[i + 1].get_NE():
                    # inner NE
                    out += [Token(token.orth, [{"I-" + token.get_NE(): '1'}], token.id)]
                else:
                    # last NE
                    out += [Token(token.orth, [{"L-" + token.get_NE(): '1'}], token.id)]
                    in_ne = False
            else:
                # we shouldn't ever get here
                assert (False)

        else:
            if token.is_NE():
                # new NE
                if tokens[i + 1].is_NE() and token.get_NE() == tokens[i + 1].get_NE():
                    # beginning NE
                    out += [Token(token.orth, [{"B-" + token.get_NE(): '1'}], token.id)]
                    in_ne = True
                else:
                    # unit NE
                    out += [Token(token.orth, [{"U-" + token.get_NE(): '1'}], token.id)]
                    in_ne = False
            else:
                # outside of NE
                out += [Token(token.orth, [{"O": '1'}], token.id)]

    # process last token
    token = tokens[-1]
    if in_ne:
        out += [Token(token.orth, [{"L-" + token.get_NE(): '1'}], token.id)]
    else:
        if token.is_NE():
            out += [Token(token.orth, [{"U-" + token.get_NE(): '1'}], token.id)]
        else:
            out += [Token(token.orth, [{"O": '1'}], token.id)]

    return out


@click.command()
@click.option("-m", "--use-label-map", type=bool, default=False)
@click.argument("output_path", type=str)
def main(
        use_label_map,
        output_path,
):
    corpus = []
    doc_idx = 0
    for subfolder in get_subdirs(os.path.join(path_prefix, corpus_path)):
        for file in os.listdir(os.path.join(path_prefix, corpus_path, subfolder)):
            if not file.endswith("rel.xml") and not file.endswith(".ini"):
                sentences = []
                token_idx = 0
                tree = ET.parse(os.path.join(path_prefix, corpus_path, subfolder, file))
                root = tree.getroot()
                sents = root.iter("sentence")
                for sent in sents:
                    tokens = []
                    for tok in sent.iter("tok"):
                        token = process_token(tok)
                        token.id = token_idx
                        token_idx += 1
                        tokens += [token]

                    # all_labels.merge(get_all_labels_with_cardinalities(tokens))  # for debug and analysis
                    tokens = pick_tags(tokens)
                    # tokens = flatten_token_attrib_dicts(tokens)

                    if use_label_map:
                        tokens = map_labels(tokens, NER_pwr_to_spacy)
                    tokens = convert_to_biluo(tokens)

                    sent = {'tokens': [{
                        'orth': t.orth,
                        'id': t.id,
                        'ner': t.get_NE()}
                        for t in tokens
                    ], 'brackets': []
                    }

                    sentences += [sent]

                doc_json = {
                    'id': doc_idx,
                    'paragraphs': [{'sentences': sentences}]
                }
                corpus += [doc_json]
                doc_idx += 1

    with open(os.path.expanduser(output_path), 'w+') as f:
        json.dump(corpus, f)


if __name__ == "__main__":
    main()
