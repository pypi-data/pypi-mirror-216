#!/usr/bin/env python3.10

from pprint import pprint
from ndbioimage import Imread


if __name__ == '__main__':
    file = '/DATA/lenstra_lab/w.pomp/data/20220525/LG_1A2_2022_05_25__15_25_49.czi'

    with Imread(file) as im:
        pprint(im)
