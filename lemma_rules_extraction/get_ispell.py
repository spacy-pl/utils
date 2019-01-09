import os
import tarfile
import datetime
from shutil import copyfile, rmtree

import settings

SJP_ISPELL_ZIP = os.path.join(settings.LEMMATIZER_DATA_DIR, 'tmp_sjp_ispell.tar.bz2')


def main():
    td = datetime.date.today()
    date = '{}{:02d}{:02d}'.format(td.year, td.month, td.day)
    print(date)
    url = 'https://sjp.pl/slownik/ort/sjp-ispell-pl-{}-src.tar.bz2'.format(date)
    os.system('wget {} -O {} -q'.format(url, SJP_ISPELL_ZIP))

    tar = tarfile.open(SJP_ISPELL_ZIP, "r:bz2")
    tar.extractall(settings.LEMMATIZER_DATA_DIR)
    tar.close()

    ispell_dir = os.path.join(settings.LEMMATIZER_DATA_DIR, 'sjp-ispell-pl-{}'.format(date))
    copyfile(os.path.join(ispell_dir, 'polish.aff'), settings.ISPELL_RULES)
    copyfile(os.path.join(ispell_dir, 'polish.all'), settings.ISPELL_DICT)

    rmtree(ispell_dir)
    os.remove(SJP_ISPELL_ZIP)


if __name__ == '__main__':
    main()