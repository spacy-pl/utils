[{
    "id": int,                      # ID of the document within the corpus
    "paragraphs": [{                # list of paragraphs in the corpus
        "raw": str,              # raw text of the paragraph
        "sentences": [{             # list of sentences in the paragraph
            "tokens": [{            # list of tokens in the sentence
                "id": int,          # index of the token in the document
                #"dep": string,     # dependency label
                "head": int,        # offset of token head relative to token index
                "tag": str,      # part-of-speech tag
                "orth": str      # verbatim text of the token
                #"ner": string      # BILUO label, e.g. "O" or "B-ORG"
            }]
            #"brackets": [{          # phrase structure (NOT USED by current models)
            #    "first": int,       # index of first token
            #    "last": int,        # index of last token
            #   "label": string     # phrase label
            #}]
        }]
    }]
}]