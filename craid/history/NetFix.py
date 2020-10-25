#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import os
from typing import List, Dict

import pandas as pd
import winsound


def beep():
    duration = 2000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)

def printShape(df):
    print(str(df.shape))


infile = os.path.join('D:', 'systems', 'ann.jsonl')
print(f"Input file: {infile}.")

base = pd.read_json(infile)
printShape(base)

base = base.drop_duplicates()
printShape(base)

#
# Condition data
#
# prepare data
df = base

df['updated'] = pd.to_datetime(df['updated'])
df['updated'] = df.updated.dt.round("D")
df = df.drop_duplicates()
df = df.sort_values(by=['sysid', 'facid', 'updated'])

# this drops out all data that doesn't have at least 2 days in a row
systems = df['sysid'].unique().tolist()

# try with holder as a List[Dict]
# holder = pd.DataFrame()
foo: List[Dict] = []

sysLen = len(systems)
i = 0
for sys in systems:
    i = i + 1
    percentDone = (i * 100.0) / sysLen
    print(f"{sys} - {percentDone}")
    sysSlice = df[df['sysid'] == sys]
    factions = sysSlice['facid'].unique().tolist()
    for fac in factions:
        #print(f"\t {fac}")
        facSlice = sysSlice[sysSlice['facid'] == fac].reset_index()
        facSlice['diff1'] = facSlice.updated.diff(periods=1).dt.days.abs()
        facSlice['diff2'] = facSlice.updated.diff(periods=-1).dt.days.abs()
        facSlice = facSlice.fillna(999.0)
        facSlice['diffz'] = facSlice[['diff1', 'diff2']].min(axis=1)
        facSlice = facSlice[facSlice['diffz'] <= 1.0]
        facSlice = facSlice.drop(['diff1', 'diff2', 'diffz'], axis=1)

        aDict = facSlice.to_dict('records')
        # holder = holder.append(facSlice.copy(), ignore_index=True)
        foo.append(aDict)

print("Converting from list of dict to dataframe")
holder = pd.DataFrame()
holder = holder.append(foo, ignore_index=True)

printShape(holder)

#
#
#
outfile = os.path.join('D:', 'systems', 'holder2.jsonl')
print(f"Output file: {outfile}.")
holder.to_json(outfile)
print("Save complete.")
beep()
print("Run complete.")
