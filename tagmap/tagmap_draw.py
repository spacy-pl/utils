fleksem_to_pos = {'ADJ': 'ADJ',
                  'ADJA': 'ADJ',
                  'ADJC': 'ADJ',
                  'ADJP': 'ADJ',
                  'ADV': 'ADV',
                  'AGLT': 'VERB',  # TO VERIFY
                  'BEDZIE': 'VERB',  # TO VERIFY 'BYĆ' IS AUX IN UD
                  'BREV': 'X',  # Consider assiging parts of speech of their full forms and adding attr "abbrev"
                  'BURK': 'PART',  # TODO: find better solution
                  'COMP': 'SCONJ',  # spójnik podrzędny
                  'CONJ': 'CCONJ',  # spójnik współrzędny
                  'DEPR': 'NOUN',
                  'FIN': 'VERB',
                  # NKJP DIFFERS FROM UD(IN UD GET IS NOUN)
                  # NEED TO CHECK AND CONSIDER CONSEQUENCES
                  'GER': 'VERB',
                  'IMPS': 'VERB',
                  'IMPT': 'VERB',
                  'INF': 'VERB',
                  'INTERJ': 'INTJ',
                  'INTERP': 'PUNCT',  # VERIFY: INTERP CAN BE SYMBOL(SYM)?
                  'NUM': 'NUM',
                  'NUMCOL': 'NUM',
                  'PACT': 'VERB',  # VERIFY POSSIBILITY TO BE ADJ
                  'PANT': 'VERB',
                  'PCON': 'VERB',
                  'PPAS': 'VERB',  # VERIFY POSSIBILITY TO BE ADJ
                  'PPRON12': 'PRON',
                  'PPRON3': 'PRON',
                  # can be AUX if we want so. Check class size and decide.
                  'PRAET': 'VERB',
                  'PRED': 'PART',  # meditate on this and check references
                  'PREP': 'ADP',  # Adposition = preposition OR postposition
                  'QUB': 'PART',  # maybe we dont neeet qub at all?
                  'SIEBIE': 'PRON',
                  'SUBST': 'NOUN',
                  'WINIEN': 'VERB',
                  'XXX'}

closed_pos = {'ADP', 'AUX', 'CCONJ', 'DET', 'NUM', 'PART', 'PRON', 'SCONJ'}
