import xml.etree.ElementTree as ET
from spacy.gold import biluo_tags_from_offsets
# import spacy
import json
import os

path_prefix = './'
corpus_path = 'data/kpwr-1.1/'
output_path = 'NER-wroc-analysis/'
output = 'analysis.json'


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


morphosyntax_xml = 'ann_morphosyntax.xml'
groups_xml = 'ann_groups.xml'
named_xml = 'ann_named.xml'
senses_xml = 'ann_senses.xml'
header_xml = 'header.xml'
segmentation_xml = 'ann_segmentation.xml'
words_xml = 'ann_words.xml'
text_xml = 'text.xml'


def print_children_recursively(n, i=0):
    if i > 10:
        return
    for c in n:
        print(' ' * (3 * i), c.attrib, c.tag)
        print_children_recursively(c, i + 1)


def get(node, k, v):
    if node is None:
        return
    for c in node:
        if c.attrib.get(k) == v:
            return c


def get_morph(seg):
    for c in seg:
        if c.attrib['type'] == 'morph':
            return c


def get_orth(seg):
    morph = get(seg, 'type', 'morph')
    orth = get(morph, 'name', 'orth')
    return orth[0].text if orth is not None else None


def get_named(seg):
    named = get(seg, 'type', 'named')
    orth = get(named, 'name', 'orth')
    return orth[0].text if orth is not None else None


def get_named_type(seg):
    named = get(seg, 'type', 'named')
    type = get(named, 'name', 'type')
    return type[0].attrib['value']


def get_ctag(seg):
    morph = get(seg, 'type', 'morph')
    interps = get(morph, 'name', 'interps')
    lex = get(interps, 'type', 'lex')
    ctag = get(lex, 'name', 'ctag')
    return ctag[0].attrib['value']


def get_corresp_morph(sent):
    return sent.attrib['corresp'].split('#')[1]


def get_entity_maps(root):
    result = {}
    for sent in root.iter('{http://www.tei-c.org/ns/1.0}s'):
        tmp = []
        for seg in sent:
            text = get_named(seg)
            type = get_named_type(seg)
            tmp += [(text, type)]

        result[get_corresp_morph(sent)] = dict(tmp)

    return result


def get_segmentation_text_maps(root):
    res = {}
    for paragraph in root.iter('{http://www.tei-c.org/ns/1.0}p'):
        key = paragraph.attrib['{http://www.w3.org/XML/1998/namespace}id']
        value = paragraph.attrib['corresp'].split('#')[1]
        res[key] = value

    return res


def get_text_maps(root):
    result = {}
    for paragraph in root.iter('{http://www.tei-c.org/ns/1.0}div'):
        key = paragraph.attrib['{http://www.w3.org/XML/1998/namespace}id']
        text = ''
        for child in paragraph:
            text += child.text

        result[key] = text

    return result


def get_sent_id(sent):
    return sent.attrib['{http://www.w3.org/XML/1998/namespace}id']


def get_paragraph_text(paragraph, segm_text_map, text_maps):
    paragraph_id = paragraph.attrib['corresp'].split('#')[1]
    return text_maps[segm_text_map[paragraph_id]]


def set_biluo_tags(sentences, tags):
    i = 0
    for sent in sentences:
        for token in sent:
            token['ner'] = tags[i]
            i += 1

    return sentences


def required_files_exist(dir):
    required_files = [segmentation_xml, text_xml, named_xml, morphosyntax_xml]
    for file in required_files:
        if not os.path.isfile(os.path.join(path_prefix, corpus_path, dir, file)):
            return False

    return True


# nlp = spacy.load('en_core_web_sm')
doc_id = 0
corpus = []

NE_njkp_to_spacy = {'persName': 'PERSON',
                    'placeName': 'LOC',
                    'orgName': 'ORG',
                    'date': 'DATE',
                    'time': 'TIME',
                    'geogName': 'LOC'}

def get_sorted_pair(p):
    p = sorted(p)
    return (p[0], p[1])

class Token:
    # def __init__(self, orth, attribs):
    #     self.orth = orth
    #     self.attribs = attribs
    #     self.id = None #this is fugly

    def __init__(self, orth, attribs, id):
        self.orth = orth
        self.attribs = attribs
        self.id = id

    def is_NE(self):
        return len(self.attribs) != 0

    def get_NE(self):
        return self.attribs[0] if len(self.attribs) > 0 else ""

    def get_cooccurences(self):
        res = setCounter()
        for i in range(0, len(self.attribs)):
            for j in range(i+1, len(self.attribs)):
                res.count(get_sorted_pair((self.attribs[i], self.attribs[j])))

        return res

    def __str__(self):
        return (self.orth + ":" + str(self.attribs))


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

def  tag1_implies_tag2(tokens, tag1, tag2):
    for token in tokens:
        if tag1 in token.attribs and (not (tag2 in token.attribs)):
            print(token.attribs)
            return False

    return True


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


def get_text(tokens):
    raw = ""
    for token in tokens:
        raw += token.orth + " "

    _punct = r'… …… , : ; \! \? ¿ ؟ ¡ \( \) \[ \] \{ \} < > _ # \* & 。 ？ ！ ， 、 ； ： ～ · । ، ؛ ٪ . ! ?'
    _quotes = r'\' \'\' " ” “ `` ` ‘ ´ ‘‘ ’’ ‚ , „ » « 「 」 『 』 （ ） 〔 〕 【 】 《 》 〈 〉'
    _hyphens = '- – — -- --- —— ~'
    _brackets_pref = ") ] }"
    _brackets_post = "( [ {"

    interp_pref = _punct.split(" ") + _quotes.split(" ") + _hyphens.split(" ") + _brackets_pref.split(" ")
    interp_post = _brackets_post.split(" ")
    raw = raw[:-1]
    for char in interp_pref:
        raw = raw.replace(" " + char, char)

    for char in interp_post:
        raw = raw.replace(char + " ", char)

    return raw


all_labels = setCounter()
cooccurences = setCounter()
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
                    # if token.is_NE(): print(token)
                    tokens += [token]

                # all_labels |= get_all_labels(tokens)
                all_labels.merge(get_all_labels_with_cardinalities(tokens))
                for tok in tokens:
                    cooccurences.merge(tok.get_cooccurences())
                if not tag1_implies_tag2(tokens, "person_first_nam", "person_nam"):
                    print("person_first_nam isn't always a person_nam" + " " + subfolder + " " + file)
                if not tag1_implies_tag2(tokens, "person_last_nam", "person_nam"):
                    print("person_last_nam isn't always a person_nam" + " " + subfolder + " " + file)

                tokens = pick_tags(tokens)
                tokens = convert_to_biluo(tokens)

                sent = {'tokens': [{
                    'orth': t.orth,
                    'id': t.id,
                    'ner': t.get_NE()}
                    for t in tokens
                ], 'brackets': []
                }
                # print(sent)
                # print(get_text(tokens))

                text = get_text(tokens)
                sentences += [sent]
                raw += "\n" + text

            doc_json = {
                'id': doc_idx,
                'paragraphs': [{'sentences': sentences}]
            }
            corpus += [doc_json]
            doc_idx += 1

# with open(os.path.expanduser(os.path.join(path_prefix, output_path, output)), 'w+') as f:
#     json.dump(corpus, f)

# print(cooccurences.contents)

with open(os.path.expanduser(os.path.join(path_prefix, output_path, "analysis.json")), 'w+') as f:
    json.dump(all_labels.contents, f)


cooccur = [(k,v) for k,v in cooccurences.contents.items()]
with open(os.path.expanduser(os.path.join(path_prefix, output_path, "cooccurences.json")), 'w+') as f:
    json.dump(cooccur, f)
