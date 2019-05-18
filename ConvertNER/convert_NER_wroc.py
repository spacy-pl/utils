import xml.etree.ElementTree as ET
import json
import os

path_prefix = './'
corpus_path = 'data/kpwr-1.1/'
output_path = 'data/NER/'
output = 'NER_wroc.json'

doc_id = 0
corpus = []

NE_njkp_to_spacy = {'persName': 'PERSON',
                    'placeName': 'LOC',
                    'orgName': 'ORG',
                    'date': 'DATE',
                    'time': 'TIME',
                    'geogName': 'LOC'}


class Token:
    def __init__(self, orth, attribs, id):
        self.orth = orth
        self.attribs = attribs
        self.id = id

    def is_NE(self):
        return len(self.attribs) != 0

    def get_NE(self):
        return self.attribs[0] if len(self.attribs) > 0 else ""

    def __str__(self):
        return (self.orth + ":" + str(self.attribs))


def get_subdirs(dir):
    return [name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name))]


def process_token(tok):
    attribs = []
    orth = tok.find("orth").text
    for ann in tok.iter("ann"):
        if ann.attrib['chan'].endswith("nam") and ann.text != "0":
            attribs += [ann.attrib['chan']]

    return Token(orth, attribs, -1)


def get_common_tag(t1, t2):
    set1 = set(t1.attribs)
    set2 = set(t2.attribs)
    common = list(set1 & set2)
    return common[0] if len(common) > 0 else None


def pick_tags(tokens):
    # first and last separately
    if len(tokens) == 0:
        return tokens
    if len(tokens) == 1:
        if tokens[0].is_NE():
            tokens[0].attribs = [tokens[0].attribs[0]]
        return tokens

    t0 = tokens[0]
    if len(t0.attribs) > 1:
        new_tag = get_common_tag(t0, tokens[1])
        if new_tag is None:
            t0.attribs = [t0.attribs[0]]
        else:
            t0.attribs = [new_tag]

    for i in range(1, len(tokens) - 1):
        if len(tokens[i].attribs) > 1:
            new_tag = get_common_tag(tokens[i - 1], tokens[i])
            if new_tag is None:
                new_tag = get_common_tag(tokens[i], tokens[i + 1])
                if new_tag is None:
                    tokens[i].attribs = [tokens[i].attribs[0]]
                else:
                    tokens[i].attribs = [new_tag]
            else:
                tokens[i].attribs = [new_tag]

    te = tokens[-1]
    if len(te.attribs) > 1:
        new_tag = get_common_tag(te, tokens[-2])
        if new_tag is None:
            te.attribs = [te.attribs[0]]
        else:
            te.attribs = [new_tag]

    assert (all(len(t.attribs) <= 1 for t in [t0] + tokens + [te]))
    return [t0] + tokens[1:-2] + [te]


def convert_to_biluo(tokens):
    out = []
    in_ne = False
    for i, token in enumerate(tokens[:-1]):
        if in_ne:
            if token.is_NE():
                if tokens[i + 1].is_NE() and token.get_NE() == tokens[i + 1].get_NE():
                    # inner NE
                    out += [Token(token.orth, ["I-" + token.get_NE()], token.id)]
                else:
                    # last NE
                    out += [Token(token.orth, ["L-" + token.get_NE()], token.id)]
                    in_ne = False
            else:
                # we shouldn't ever get here
                assert (False)

        else:
            if token.is_NE():
                # new NE
                if tokens[i + 1].is_NE() and token.get_NE() == tokens[i + 1].get_NE():
                    # beginning NE
                    out += [Token(token.orth, ["B-" + token.get_NE()], token.id)]
                    in_ne = True
                else:
                    # unit NE
                    out += [Token(token.orth, ["U-" + token.get_NE()], token.id)]
                    in_ne = False
            else:
                # outside of NE
                out += [Token(token.orth, ["O"], token.id)]

    # process last token
    token = tokens[-1]
    if in_ne:
        out += [Token(token.orth, ["L-" + token.get_NE()], token.id)]
    else:
        if token.is_NE():
            out += [Token(token.orth, ["U-" + token.get_NE()], token.id)]
        else:
            out += [Token(token.orth, ["O"], token.id)]

    return out


docs = []
doc_idx = 0
for subfolder in get_subdirs(os.path.join(path_prefix, corpus_path)):
    for file in os.listdir(os.path.join(path_prefix, corpus_path, subfolder)):
        if not file.endswith("rel.xml") and not file.endswith(".ini"):
            doc_json = {}
            sentences = []
            token_idx = 0
            raw = ""
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

                tokens = pick_tags(tokens)
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

with open(os.path.expanduser(os.path.join(path_prefix, output_path, output)), 'w+') as f:
    json.dump(corpus, f)
