import os
import tarfile
import datetime
import argparse
from shutil import copyfile, rmtree

import settings

SJP_ISPELL_ZIP = os.path.join(settings.LEMMATIZER_DATA_DIR, 'sjp_ispell.tar.bz2')


def main(args):
    td = datetime.date.today()
    result = 1
    while result != 0:
        date = '{}{:02d}{:02d}'.format(td.year, td.month, td.day)
        url = 'https://sjp.pl/slownik/ort/sjp-ispell-pl-{}-src.tar.bz2'.format(date)
        result = os.system('wget {} -O {} -q'.format(url, SJP_ISPELL_ZIP))
        td = td - datetime.timedelta(days=1)
    print('Downloaded from date {}'.format(date))

    tar = tarfile.open(SJP_ISPELL_ZIP, "r:bz2")
    tar.extractall(settings.LEMMATIZER_DATA_DIR)
    tar.close()

    ispell_dir = os.path.join(settings.LEMMATIZER_DATA_DIR, 'sjp-ispell-pl-{}'.format(date))
    copyfile(os.path.join(ispell_dir, 'polish.aff'), settings.ISPELL_RULES)
    copyfile(os.path.join(ispell_dir, 'polish.all'), settings.ISPELL_DICT)

    rmtree(ispell_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Download and unpack the newest sjp rules')
    args = parser.parse_args()
    main(args)
