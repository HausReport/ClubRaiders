#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import gzip
import logging
from typing import Set, Tuple, Dict

import ujson

from craid.eddb.loader.LoadDataFromAWS import LoadDataFromAWS


# NOTE: To get the May 31 file: $ curl "https://github.com/HausReport/ClubRaiders/blob/d5ff5b1741467618df70a75c7078fb6b6fc32fe3/data/smol-systems_populated.jsonl.gz?raw=true" -L -o smol-sys-old.jsonl.gz
logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().level = logging.DEBUG

newSet: Dict[int,Set[int]] = {}
oldSet: Dict[int,Set[int]] = {}

sysNames: Dict[int, str] = {}
facNames: Dict[int, str] = {}

loader = LoadDataFromAWS()

nLines = 0
fName = loader.find_data_file('factions.jsonl')
with gzip.open(fName, 'rb') as f:
    for line in f:
        facLine = ujson.loads(line)
        nLines += 1
        tid = int(facLine['id'])
        nam = facLine['name']
        facNames[tid]=nam
logging.info("Read %s lines of faction data", str(nLines))



nLines = 0
fName = loader.find_data_file('systems_populated.jsonl')
with gzip.open(fName, 'rb') as f:
    for line in f:
        sysLine = ujson.loads(line)
        nLines += 1
        tid = int(sysLine['id'])
        mfp = sysLine['minor_faction_presences']
        mfps: Set[int] = set()
        for item in mfp:
           mfps.add(item['minor_faction_id'])
        newSet[tid] = mfps

        #foo = InhabitedSystem(sysLine)
        #all_systems_dict[tid] = foo

logging.info("Read %s lines of systems data", str(nLines))

nLines = 0
fName = loader.find_data_file('sys-old.jsonl')
with gzip.open(fName, 'rb') as f:
    for line in f:
        sysLine = ujson.loads(line)
        nLines += 1
        tid = int(sysLine['id'])
        mfp = sysLine['minor_faction_presences']
        mfps: Set[int] = set()
        for item in mfp:
           mfps.add(item['minor_faction_id'])
        oldSet[tid] = mfps
        sysNames[tid] = sysLine['name']

logging.info("Read %s lines of systems data", str(nLines))

for key in newSet.keys():
    oldFacs = oldSet.get(key)
    if oldFacs is None:
        print("New club activity in system: " + str(key))
    else:
        newFacs = newSet.get(key)
        news = newFacs-oldFacs
        olds = oldFacs-newFacs
        if len(news)>0 or len(olds)>0:
            sName = sysNames.get(key)
            if sName is None:
                sName = "Unknown"
            print("Change in system: " + sName)
        if len(news)>0:
            for tid in news:
                theFac = facNames.get(tid)
                if theFac is None:
                    theFac = "Unknown"
                print("\t\t" + theFac + " expanded here")
        if len(olds)>0:
            for tid in olds:
                theFac = facNames.get(tid)
                if theFac is None:
                    theFac = "Unknown"
                print("\t\t" + theFac + " retreated")

for key in oldSet.keys():
    newFacs = newSet.get(key)
    if newFacs is None:
        print("Club removed from in system: " + str(key))
    else:
        oldFacs =oldSet.get(key)
        news = newFacs-oldFacs
        olds = oldFacs-newFacs
        if len(news)>0 or len(olds)>0:
            sName = sysNames.get(key)
            if sName is None:
                sName = "Unknown"
            print("Change in system: " + sName)
        if len(news)>0:
            for tid in news:
                theFac = facNames.get(tid)
                if theFac is None:
                    theFac = "Unknown"
                print("\t\t" + theFac + " expanded here")
        if len(olds)>0:
            for tid in olds:
                theFac = facNames.get(tid)
                if theFac is None:
                    theFac = "Unknown"
                print("\t\t" + theFac + " retreated")

#print("Retreats: " + str(oldSet-newSet))
#print("Expansions: " + str(newSet-oldSet))
