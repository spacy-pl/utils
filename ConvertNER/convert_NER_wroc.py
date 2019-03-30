import xml.etree.ElementTree as ET
from spacy.gold import biluo_tags_from_offsets
# import spacy
import json
import os

path_prefix = './'
corpus_path = 'data/kpwr-1.1/'
output_path = 'data/NER/'
output = 'NER_wroc.json'

def get_subdirs(dir):
    return [name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir,name))]

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
        print(' '*(3*i), c.attrib, c.tag)
        print_children_recursively(c, i+1)

def get(node, k, v):
    if node is None:
        return
    for c in node:
        if c.attrib.get(k)==v:
            return c

def get_morph(seg):
    for c in seg:
        if c.attrib['type']=='morph':
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
        res[key]=value

    return res

def get_text_maps(root):
    result = {}
    for paragraph in root.iter('{http://www.tei-c.org/ns/1.0}div'):
        key = paragraph.attrib['{http://www.w3.org/XML/1998/namespace}id']
        text = ''
        for child in paragraph:
            text += child.text

        result[key]=text

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
        if not os.path.isfile(os.path.join(path_prefix,corpus_path,dir,file)):
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

    def __str__(self):
        return (self.orth + ":" + str(self.attribs))


def process_token(tok):
    attribs = []
    orth = tok.find("orth").text
    for ann in tok.iter("ann"):
        if ann.attrib['chan'].endswith("nam") and ann.text=="1":
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

    for i in range(1, len(tokens)-1):
        if len(tokens[i].attribs) > 1:
            new_tag = get_common_tag(tokens[i-1], tokens[i])
            if new_tag is None:
                new_tag = get_common_tag(tokens[i], tokens[i+1])
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

    assert(all(len(t.attribs)<=1 for t in [t0] + tokens+ [te]))
    return [t0] + tokens[1:-2] + [te]

def convert_to_biluo(tokens):
    out = []
    in_ne = False
    for i, token in enumerate(tokens[:-1]):
        if in_ne:
            if token.is_NE():
                if tokens[i+1].is_NE() and token.get_NE() == tokens[i+1].get_NE():
                    # inner NE
                    out += [Token(token.orth, ["I-"+token.get_NE()], token.id)]
                else:
                    # last NE
                    out += [Token(token.orth, ["L-"+token.get_NE()], token.id)]
                    in_ne = False
            else:
                # we shouldn't ever get here
                assert(False)

        else:
            if token.is_NE():
                # new NE
                if tokens[i+1].is_NE() and token.get_NE() == tokens[i+1].get_NE():
                    # beginning NE
                    out += [Token(token.orth, ["B-"+token.get_NE()], token.id)]
                    in_ne = True
                else:
                    # unit NE
                    out += [Token(token.orth, ["U-"+token.get_NE()], token.id)]
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
    _brackets_pref =  ") ] }"
    _brackets_post = "( [ {"

    interp_pref = _punct.split(" ") + _quotes.split(" ") + _hyphens.split(" ") + _brackets_pref.split(" ")
    interp_post = _brackets_post.split(" ")
    raw = raw[:-1]
    for char in interp_pref:
        raw = raw.replace(" "+char, char)

    for char in interp_post:
        raw = raw.replace(char+" ", char)

    return raw



all_labels = set()
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

                all_labels |= get_all_labels(tokens)
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
                raw += "\n"+text

            doc_json = {
                'id': doc_idx,
                'paragraphs': [{'sentences': sentences}]
            }
            corpus += [doc_json]
            doc_idx +=1

# print(corpus)
with open(os.path.expanduser(os.path.join(path_prefix, output_path, output)), 'w+') as f:
    json.dump(corpus, f)
# for f in os.listdir(os.path.join(path_prefix, corpus_path)):
#     doc_json = {}
#     current_folder = f
#
#     if not os.path.isdir((os.path.join(path_prefix,corpus_path,current_folder))):
#         continue
#
#     if not required_files_exist(current_folder):
#         # doc_id +=1 ?
#         continue
#
#     tree_morphosyntax = ET.parse(os.path.join(path_prefix,corpus_path,current_folder,morphosyntax_xml))
#     root_morphosyntax = tree_morphosyntax.getroot()
#
#     tree_named = ET.parse(os.path.join(path_prefix,corpus_path,current_folder,named_xml))
#     root_named = tree_named.getroot()
#
#     tree_text = ET.parse(os.path.join(path_prefix,corpus_path,current_folder,text_xml))
#     root_text = tree_text.getroot()
#
#     tree_segmentation = ET.parse(os.path.join(path_prefix,corpus_path,current_folder,segmentation_xml))
#     root_segmentation = tree_segmentation.getroot()
#
#     segmentation_text_map = get_segmentation_text_maps(root_segmentation)
#     entity_maps = get_entity_maps(root_named)
#     text_maps = get_text_maps(root_text)
#
#     token_idx = 0
#     paragraphs = []
#     for paragraph in root_morphosyntax.iter('{http://www.tei-c.org/ns/1.0}p'):
#         paragraph_json = {}
#         pg_text = get_paragraph_text(paragraph, segmentation_text_map, text_maps)
#
#         text = ''
#         nes = []
#         sentences = []
#         for sentence in paragraph:
#             sent_id = get_sent_id(sentence)
#             sentence_entity_map = entity_maps[sent_id]
#             sentence_json = []
#             for seg in sentence:
#                 token = {}
#                 ctag = get_ctag(seg)
#                 orth = get_orth(seg)
#                 ne = sentence_entity_map.get(orth)
#
#                 text += orth + ' '
#
#                 if ne is not None:
#                     ne = NE_njkp_to_spacy[ne]
#                     nes += [(len(text)-1-len(orth), len(text)-1, ne)]
#
#                 token['ctag'] = ctag
#                 token['orth'] = orth
#                 token['head'] = 0  # @TODO
#                 token['dep'] = 'NA'  # @TODO
#                 token['id'] = token_idx
#                 token['ner'] = ne
#                 token_idx += 1
#                 sentence_json += [token]
#             sentences += [sentence_json]
#
#         doc = nlp(text)
#         entities = nes
#         biluo_tags = biluo_tags_from_offsets(doc, entities)
#
#         sentences = set_biluo_tags(sentences, biluo_tags)
#         paragraph_json['sentences'] = [{'tokens': tok, 'brackets': []} for tok in sentences]
#         paragraph_json['raw'] = pg_text
#         paragraphs += [paragraph_json]
#
#     doc_json['id'] = doc_id
#     doc_json['paragraphs'] = paragraphs
#
#     doc_id += 1
#     corpus += [doc_json]
#