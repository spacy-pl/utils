import numpy as np
import json
import click


class Split(object):
    def __init__(self, train_prob: float, validation_prob: float, test_prob: float, n_docs: int, random_seed: int=2137):
        assert(train_prob+validation_prob+test_prob == 1.0)
        np.random.seed(random_seed)
        indice_assignment = np.random.choice(3, n_docs, p=[train_prob, validation_prob, test_prob], replace=True)
        self.train = set(np.where(indice_assignment == 0)[0])
        self.validation = set(np.where(indice_assignment == 1)[0])
        self.test = set(np.where(indice_assignment == 2)[0])


@click.command(help="Split JSON converted for POS tagger (input-file) training into train, test and validation files (based on given probabilities).")
@click.option('--input-file', type=str)
@click.option('--train-output', type=str)
@click.option('--validation-output', type=str)
@click.option('--test-output', type=str)
@click.option('--train-prob', default=0.5)
@click.option('--validation-prob', default=0.25)
@click.option('--test-prob', default=0.25)
@click.option('--random-seed', default=2137)
def split_pos_data(
        input_file, 
        train_output, 
        validation_output, 
        test_output, 
        train_prob, 
        validation_prob, 
        test_prob, 
        random_seed
):
    print('Loading input...')
    js = json.load(open(input_file, 'r'))
    print('Splitting...')
    split = Split(train_prob, validation_prob, test_prob, n_docs=len(js), random_seed=random_seed)
    js_train = [doc for idx, doc in enumerate(js) if idx in split.train]
    js_valid = [doc for idx, doc in enumerate(js) if idx in split.validation]
    js_test = [doc for idx, doc in enumerate(js) if idx in split.test]
    print('Saving output...')
    with open(train_output, 'w') as f:
        json.dump(js_train, f)
    with open(validation_output, 'w') as f:
        json.dump(js_valid, f)
    with open(test_output, 'w') as f:
        json.dump(js_test, f)
    print('Done.')


if __name__ == '__main__':
    split_pos_data()
