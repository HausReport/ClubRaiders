#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import os
import shutil
from typing import Dict, List

import pandas as pd
import winsound

from craid.eddb.loader.DataProducer import getDataArrays
from craid.eddb.loader.strategy.DirectoryLoader import DirectoryLoader


def beep():
    duration = 2000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)

loader = DirectoryLoader()

outfile = os.path.join('D:','systems','ann.jsonl')
print(f"Output file: {outfile}.")
#fName = loader.find_data_file("jul8.gz")
#print(fName)

datafiles = [ 'jul4.gz','jul5.gz','jul6.gz','jul7.gz','jul8.gz','jul9.gz','jul10.gz', 'jul11.gz']

for short in datafiles:
    fromFile = os.path.join('D:','systems',short)
    toFile = os.path.join('D:','systems','systems_populated.jsonl.gz')
    shutil.copyfile(fromFile,toFile)

    prod = getDataArrays(loader= loader, clubSystemsOnly=False)

    theDict = prod['sysIdFacIdToFactionInstance']

    if os.path.exists(outfile):
        print("Reading bigfile")
        base = pd.read_json(outfile)
    else:
        print("No bigfile - creating a new one")
        base: pd.DataFrame = pd.DataFrame()

    foo: List[Dict] = []

    siz = len(theDict)
    print(f"Total size: {siz}")
    i = 0
    for facInst in theDict.values():
        i += 1
        if i%50 == 0:
            print(".", end='')
        if i%(50*100)==0:
            print(f"\nRow:{i}",end='')
        # if i>250:
        #     break
        new_row = facInst.getANNRow()
        #df = df.append(new_row, ignore_index=True)
        foo.append(new_row)
        #pprint(facInst.getANNRow())

    base = base.append(foo, ignore_index=True)
    # can't fix the dates yet
    #base['updated'] = pd.to_datetime(base['updated'])
    #base['updated'] = base.updated.dt.round("D")
    base = base.drop_duplicates()
    base.to_json(outfile)

beep()
#print(df)
