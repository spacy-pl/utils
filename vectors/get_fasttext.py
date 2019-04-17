import click
import os
import numpy as np
from spacy.vectors import Vectors


class MyVec:

    def __init__(self, filepath):
        self.filepath = filepath
        with open(self.filepath, 'rb') as file_:
            header = file_.readline()
            nr_row, nr_dim = header.split()
        self.nr_row = int(nr_row)
        self.nr_dim = int(nr_dim)

    @property
    def size(self):
        return get_file_size(self.filepath)

    def _get_key(self, line):
        line = line.rstrip().decode('utf8')
        pieces = line.rsplit(' ', self.nr_dim)
        return pieces[0]

    def _get_vector(self, line):
        line = line.rstrip().decode('utf8')
        pieces = line.rsplit(' ', self.nr_dim)
        vec = np.asarray(list(map(float, pieces[1:])), dtype='f')
        return vec

    def keys(self, size=None):
        with open(self.filepath, 'rb') as file_:
            file_.readline()  # first line
            words = [self._get_key(line) for count, line in enumerate(file_, 1)
                     if size is None or count <= size]
        return words

    def vectors(self, size=None):
        with open(self.filepath, 'rb') as file_:
            file_.readline()  # first line
            vectors = [self._get_vector(line) for count, line in enumerate(file_, 1)
                       if size is None or count <= size]
        vectors = np.array(vectors)
        return vectors

    def get_first_n(self, n):
        lines = [""] * n
        with open(self.filepath, 'rb') as file_:
            file_.readline()
            for count, line in enumerate(file_):
                if count >= n:
                    break
                lines[count] = line
        return lines


def get_file_size(filepath):
    statinfo = os.stat(filepath)
    size_mb = statinfo.st_size / 1024 / 1024
    return size_mb


def get_ints_sizes(for_cutting, ref, n=100):
    ref_s = set(ref)
    sizes = np.linspace(len(ref), len(for_cutting), n)
    sizes = list(map(int, sizes))
    ints_s = [len(set(for_cutting[:s]) & ref_s) for s in sizes]
    ints_s = [s/len(ref) for s in ints_s]
    sizes = [s/1000 for s in sizes]
    return ints_s, sizes


@click.command(help="Write chosen amount of fasttext vectors to specified files")
@click.option('--bin-file', type=str, default="data/vectors/fasttext_spacy")
@click.option('--txt-file', type=str, default="data/vectors/fasttext.txt")
@click.option('--fasttext-file', type=str, default="data/vectors/cc.pl.300.vec")
@click.option('--size', type=int, default=700000)
def get_fasttext(
    bin_file,
    txt_file,
    fasttext_file,
    size,
):
    print("Reading data...")
    fst = MyVec(fasttext_file)
    fst_short_k = fst.keys(size)
    fst_short_v = fst.vectors(size)

    # save bin vectors
    print("Saving bin version...")
    fst_spacy = Vectors(data=fst_short_v, keys=fst_short_k)
    fst_spacy.to_disk(bin_file)
    s = get_file_size(os.path.join(bin_file, 'vectors'))
    print("Chosen fasttexts in binary format weight {} MB".format(round(s)))

    # save txt vectors
    print("Saving txt version...")
    chosen_lines = fst.get_first_n(size)
    with open(txt_file, 'wb') as f:
        f.write(bytes("{} {}\n".format(size, fst.nr_dim), 'utf-8'))
        f.writelines(chosen_lines)
    s = get_file_size(txt_file)
    print("Chosen fasttexts in txt format weight {} MB".format(round(s)))


if __name__ == "__main__":
    get_fasttext()
