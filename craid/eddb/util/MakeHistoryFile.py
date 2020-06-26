#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

#Read big factions file
#Read small systems file
#Construct factioninstances
#output to jsonl
import gzip
import logging
from typing import List, Dict

import ujson

from craid.eddb.faction.Faction import Faction
from craid.eddb.loader.CreateClubSystemKeys import getClubSystemKeys
from craid.eddb.loader.CreateFactionInstances import getFactionInstances
from craid.eddb.loader.CreateFactions import load_factions
from craid.eddb.loader.CreateSystems import load_systems
from craid.eddb.loader.strategy.DataLoader import DataLoader
from craid.eddb.loader.strategy.LoadDataFromEDDB import LoadDataFromEDDB


# 6/25
# https://github.com/HausReport/ClubRaiders/raw/7cd6abc33aafab80cace0c13c2beb6e1d8f1779b/data/smol-systems_populated.jsonl.gz
# 6/24
# https://github.com/HausReport/ClubRaiders/raw/ebbdc4e809cc446bbe35b1a540b3480006be4e67/data/smol-systems_populated.jsonl.gz
# 6/23
# https://github.com/HausReport/ClubRaiders/raw/50eb68e359a444de0cec194a603a3a9a339855fa/data/smol-systems_populated.jsonl.gz
# 6/22
# 6/21
# https://github.com/HausReport/ClubRaiders/raw/43f0480c50e9b69c0506a30e366c9f34d4fa60f8/data/smol-systems_populated.jsonl.gz
# 6/20
# https://github.com/HausReport/ClubRaiders/raw/4b7ead2c26999e9736ff179a38f38c5677c2423c/data/smol-systems_populated.jsonl.gz
# 6/19
# https://github.com/HausReport/ClubRaiders/raw/c337e9261161bbfc1be99e1a9e1a31d9b01159f0/data/smol-systems_populated.jsonl.gz
# 6/18
# 6/17
# 6/16
# 6/15
# 6/14
# 6/13
# 6/12
# 6/11
# 6/10
# 6/09
# 6/08
# 6/07
# 6/06
# 6/05
# 6/04
# 6/03
# 6/02
# 6/01
# 5/31
# ht0ps://github.com/HausReport/ClubRaiders/raw/066c92ef24354305b1dd94ae0e12596afc3a6fd6/data/smol-systems_populated.jsonl.gz

# xinName = 'factions.jsonl'
# allFactions: List[Dict] = []
#
# myLoader: DataLoader = LoadDataFromEDDB()
# inFile = myLoader.find_data_file(xinName)
# with gzip.open(inFile, 'rb') as f:
#     for line in f:
#         facLine = ujson.loads(line)
#         if facLine['id'] in keys:
#             allFactions.append(facLine)
#             curFaction = Faction(facLine)
#             if FactionNameFilter.proClubFaction(curFaction):
#                 curFaction.setClub(True)
#
#             all_factions_dict[lCurFactionId] = curFaction

#
# Fire up logger
#
logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().level = logging.DEBUG

myLoader = LoadDataFromEDDB()
playerFactionNameToSystemName: Dict[str, str] = {}
all_factions_dict, player_faction_keys, club_faction_keys = load_factions(myLoader)
all_systems_dict = load_systems(myLoader)

club_system_keys = getClubSystemKeys(all_systems_dict, club_faction_keys)

allClubSystemInstances, sysIdFacIdToFactionInstance, factions_of_interest_keys \
    = getFactionInstances(all_systems_dict, club_system_keys, all_factions_dict, club_faction_keys)

for val in sysIdFacIdToFactionInstance.values():
    if val.isClub():
        print(val.getHistoryLine())

