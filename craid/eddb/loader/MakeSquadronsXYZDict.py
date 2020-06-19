#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import gzip
import os
import pprint
import tempfile
from typing import Dict, List, Set
from typing import Tuple

import ujson

from craid.eddb.GameConstants import MINOR_FACTION_PRESENCES
from craid.eddb.SystemXYZ import SystemXYZ
from craid.eddb.loader.CreateFactions import load_factions
from craid.eddb.loader.LoadDataFromAWS import LoadDataFromAWS
from craid.eddb.loader.LoadDataFromEDDB import LoadDataFromEDDB

#
# First, get player faction keys
#
myLoader = LoadDataFromEDDB()  # LoadDataFromGithub()

#
# Load the basic factions and systems structures
#
player_faction_keys: Set[int] = set()
all_factions_dict, player_faction_keys, club_faction_keys = load_factions(myLoader)

#
# Now, read through big systems file
#
shortName = "systems_populated.jsonl"
tmpDir = tempfile.gettempdir()
fName = os.path.join(tmpDir, shortName) + ".gz"

workingDictionary: Dict[int, Set[str]] = {}
outputDictionary: Dict[str, Dict[str,Tuple[int,int,int]]] = {}

nLines: int = 0
with gzip.open(fName, 'rb') as f:
    for line in f:
        sysLine = ujson.loads(line)
        nLines += 1

        mfp = sysLine[MINOR_FACTION_PRESENCES]
        for facLine in mfp:
            facKey = facLine['minor_faction_id']
            #print( str(facKey))
            if facKey in player_faction_keys:
                mySystems = workingDictionary.get(facKey)
                if mySystems is None:
                    mySystems = {} #set()
                tName = sysLine['name']
                #print("+")
                point = SystemXYZ.myDict.get(tName)
                mySystems[tName] = point #.add(tName)
                workingDictionary[facKey]  = mySystems


count = 0
for key in workingDictionary.keys():
    count = count+1
    tKey = all_factions_dict[key].get_name()
    #str(key)
    #print('\'' + tKey + '\' :'),
    #pprint.pprint(workingDictionary[key])
    outputDictionary[tKey] = workingDictionary[key]  # switch from int to string keys

print(str(count))
pprint.pprint(outputDictionary)
#for key, value in sorted(outputDictionary.items(), key=lambda x: x[1]):
    #print("{} : {}".format(key, value))