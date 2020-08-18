#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import gzip
import logging
from pprint import pprint
from typing import List, Dict, Set

import ujson

from craid.club.regions.RegionFactory import RegionFactory
from craid.eddb.base.Aware import Aware
from craid.eddb.faction.FactionInstance import FactionInstance
from craid.eddb.loader.CreateFactionInstances import getFactionInstances
from craid.eddb.loader.CreateFactions import load_factions
from craid.eddb.loader.CreateSystems import load_systems
from craid.eddb.loader.MakeKeyFiles import loadKeys
from craid.eddb.loader.strategy.AWSLoader import LoadDataFromAWS
from craid.eddb.loader.strategy.EDDBLoader import LoadDataFromEDDB
from craid.eddb.loader.strategy.GithubLoader import LoadDataFromGithub
from craid.eddb.system.BountyHuntingInfo import BountyHuntingInfo
from craid.eddb.system.InhabitedSystem import InhabitedSystem

counts: Dict[str,int] = {}
pleiades = RegionFactory.getRegionByNumber(1)

logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().level = logging.DEBUG

sysNames: Dict[int, str] = {}
facNames: Dict[int, str] = {}

loader = LoadDataFromAWS()
loaderFac = LoadDataFromEDDB()
nLines = 0
fName = loaderFac.find_data_file('factions.jsonl')
with gzip.open(fName, 'rb') as f:
    for line in f:
        facLine = ujson.loads(line)
        nLines += 1
        tid = int(facLine['id'])
        nam = facLine['name']
        facNames[tid] = nam
logging.info("Read %s lines of faction data", str(nLines))

nLines = 0
#fName = loader.find_data_file('systems_populated.jsonl')
fName = loaderFac.find_data_file('systems_populated.jsonl')
with gzip.open(fName, 'rb') as f:
    for line in f:
        sysLine = ujson.loads(line)
        nLines += 1
        #tid = int(sysLine['id'])

        x = int(sysLine['x'])
        y = int(sysLine['y'])
        z = int(sysLine['z'])

        if pleiades.contains(x,y,z):

            mfp = sysLine['minor_faction_presences']
            for item in mfp:
                fid = item['minor_faction_id']
                facName = facNames[fid]

                if facName in counts:
                    counts[facName] = counts[facName] + 1
                else:
                    counts[facName] = 1

logging.info("Read %s lines of systems data", str(nLines))

theKeys = sorted(counts.keys())
for key in theKeys:
    name = key
    val = counts[name]
    print(f"{name} - ({val})")

