import os
import nltk
import random
import json
import click

def make_document(index: int, paragraphs: list, conversion_map: dict):
    converted_paras=[]
    starting_id=0
    for sentences in paragraphs:
        paragraph, tokens_number = make_paragraph(sentences, starting_id, conversion_map)
        converted_paras.append(paragraph)
        starting_id+=tokens_number


    document={
        "id": index,
        "paragraphs": converted_paras
    }

    return document

def make_paragraph(sentences: list, starting_id: int, conversion_map: dict):
    converted_sents=[]
    tokens_num=0

    for tokens in sentences:
        converted_sentence=make_sentence(tokens, starting_id, conversion_map)#TODO
        converted_sents.append(converted_sentence)

        sentence_size=len(converted_sentence)
        starting_id+=sentence_size
        tokens_num+=sentence_size

    paragraph={
        #"raw": '',#TODO
        "sentences": converted_sents
    }

    return paragraph, tokens_num

def make_sentence(tokens: list, starting_id:int, conversion_map: dict):#, tags: list):
    converted_tokens=[]
    id=starting_id
    for token in tokens:
        tag = token[1]
        if conversion_map:
            tag = conversion_map[tag]
        converted_token=make_token(id, token[0], tag)
        converted_tokens.append(converted_token)
        id+=1

    sentence={
        "tokens": converted_tokens
    }

    return sentence

def make_token(id: int, orth: str, tag: str):
    token={
        "id": id,
        "head": 0, #TODO
        "tag": tag,
        "orth": orth
    }

    return token

@click.command(help="Convert nkjp to spacy format")
@click.option('--output-path', type=str, default="./data/spacy_convert/pos.json")
@click.option('--conversion_map_filepath')
def convert(
        output_path,
        conversion_map_filepath,
):
    corpus_path=os.path.abspath("./data/NKJP_1.2_nltk/")
    corpus=nltk.corpus.reader.TaggedCorpusReader(root=corpus_path, fileids=".*")

    if conversion_map_filepath is not None:
        with open(conversion_map_filepath, "r") as f:
            conversion_map = json.load(f)
    else:
        conversion_map = None

    files=corpus.fileids()
    output=[]

    for i, f in enumerate(files):
        document=make_document(i, corpus.tagged_paras(f), conversion_map)
        output.append(document)

    with open(output_path, "w") as result_file:
        json.dump(output, result_file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    convert()
