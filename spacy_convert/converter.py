import os
import nltk
import random
import json

def make_document(index: int, paragraphs: list):
    converted_paras=[]
    starting_id=0
    for sentences in paragraphs:
        paragraph, tokens_number = make_paragraph(sentences, starting_id)
        converted_paras.append(paragraph)
        starting_id+=tokens_number
    
        
    document={
        "id": index,
        "paragraphs": converted_paras
    }
    
    return document    

def make_paragraph(sentences: list, starting_id: int):
    converted_sents=[]
    tokens_num=0
    
    for tokens in sentences:
        converted_sentence=make_sentence(tokens, starting_id)#TODO
        converted_sents.append(converted_sentence)
        
        sentence_size=len(converted_sentence)
        starting_id+=sentence_size
        tokens_num+=sentence_size
        
    paragraph={
        #"raw": '',#TODO
        "sentences": converted_sents
    }
    
    return paragraph, tokens_num

def make_sentence(tokens: list, starting_id:int):#, tags: list):
    converted_tokens=[]
    id=starting_id
    for token in tokens:
        converted_token=make_token(id, token[0], token[1])
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

corpus_path=os.path.abspath("./data/NKJP_1.2_nltk/")
corpus=nltk.corpus.reader.TaggedCorpusReader(root=corpus_path, fileids=".*")


files=corpus.fileids()
output=[]

for i, f in enumerate(files):
    document=make_document(i, corpus.tagged_paras(f))
    output.append(document)

with open("./data/spacy_convert/pos.json", "w") as result_file:
    json.dump(output, result_file, indent=4, ensure_ascii=False)
