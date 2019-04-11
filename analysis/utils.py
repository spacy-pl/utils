import json
import pandas as pd
from tqdm import tqdm


def load_spacy_to_pandas(filepath):
    with open(filepath) as f:
        data = json.load(f)

    rows = [pd.DataFrame(s["tokens"]) for f in tqdm(data)
            for p in f["paragraphs"]
            for s in p["sentences"]]

    d = pd.concat(rows, ignore_index=None)
    return d
