import spacy
import click
from tqdm import tqdm
import pandas as pd
from conll_df import conll_df
from spacy.lang.pl import Polish


def load_data(path, sample_size):
    '''Load conllu file to dataframe'''
    df = conll_df(path, skip_meta=True)
    if sample_size != 0:
        df=df.iloc[:sample_size]
    df = df[['w', 'l', 'x']].reset_index(drop=True)
    df.columns = ['orth', 'lemma', 'UD_POS']
    return df


def predict_lemmas(data):
    '''Generates lemmatizer predictions, using golden POS'''
    lemmatizer = Polish.Defaults.create_lemmatizer()
    tqdm.pandas() #registring pandas in tqdm
    data['predictions'] = data.progress_apply(lambda row: lemmatizer(row.orth, row.UD_POS), axis = 1)
    return data

def load_and_predict_lemmas(data_path, output_path, sample_size):
    data = load_data(data_path, sample_size)
    results = predict_lemmas(data)
    return results

@click.command(help='Iterate lemmatizer over annotated conllu corpus and saves predictions')
@click.option("--data-path", type=str, default='./data/dependency_trees/UD_Polish-LFG-master/pl_lfg-ud-dev.conllu')
@click.option("--output-path", type=str, default='./analysis/lemmatizer_predictions_lfg_dev.json')
@click.option("--sample-size", type=int, default=0)
def generate_lemmatizer_predictions(data_path, output_path, sample_size):
    predictions = load_and_predict_lemmas(data_path, output_path, sample_size)
    predictions.to_json(output_path)


if __name__ == '__main__':
    generate_lemmatizer_predictions()