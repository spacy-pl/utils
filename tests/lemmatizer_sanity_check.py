import pandas as pd
import sys
sys.path.append(".")
from evaluation.lemmatizer_predict import load_and_predict_lemmas

reference_results = pd.read_json('./tests/data/lemmatizer-results.json')
new_results = load_and_predict_lemmas('./data/dependency_trees/UD_Polish-LFG-master/pl_lfg-ud-dev.conllu', './analysis/lemmatizer_predictions_lfg_dev.json', 150)
all_passed = True
for reference_lemmas, new_lemmas in zip(reference_results.predictions.sort_index(), new_results.predictions.sort_index()):
    if not sorted(reference_lemmas) == sorted(new_lemmas):
        print(f'Failed, previously: {sorted(reference_lemmas)}, now: {sorted(new_lemmas)}')
        all_passed = False

if all_passed:
    print('Fine! Lemmatization looks like previously!')