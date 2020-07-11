#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import os
from pprint import pprint
from typing import Dict, List

from craid.eddb.loader.CreateFactions import load_factions
from craid.eddb.loader.CreateSystems import load_systems
from craid.eddb.loader.DataProducer import getDataArrays
from craid.eddb.loader.strategy.DirectoryLoader import DirectoryLoader
import pandas as pd
import winsound

def beep():
    duration = 2000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)

loader = DirectoryLoader()

outfile = os.path.join('D:','systems','ann.jsonl')
print(f"Output file: {outfile}.")
#fName = loader.find_data_file("jul8.gz")
#print(fName)

prod = getDataArrays(loader= loader, clubSystemsOnly=False)

theDict = prod['sysIdFacIdToFactionInstance']

print("Reading bigfile")
#base: pd.DataFrame = pd.DataFrame()
base = pd.read_json(outfile)
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
base.to_json(outfile)
beep()

#print(df)
