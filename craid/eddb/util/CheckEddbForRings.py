#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
from typing import List

from craid.eddb.base.Aware import Aware
from craid.eddb.faction.FactionInstance import FactionInstance
from craid.eddb.loader.CreateFactionInstances import getFactionInstances
from craid.eddb.loader.CreateFactions import load_factions
from craid.eddb.loader.CreateSystems import load_systems
from craid.eddb.loader.MakeKeyFiles import loadKeys
from craid.eddb.loader.strategy.GithubLoader import LoadDataFromGithub
from craid.eddb.system.BountyHuntingInfo import BountyHuntingInfo
from craid.eddb.system.InhabitedSystem import InhabitedSystem

bhDict = BountyHuntingInfo.bhDict

myLoader = LoadDataFromGithub()

all_factions_dict, player_faction_keys, club_faction_keys = load_factions(myLoader)
club_system_keys = loadKeys('club-system-keys')
all_systems_dict = load_systems(myLoader)

allClubSystemInstances, sysIdFacIdToFactionInstance, factions_of_interest_keys \
    = getFactionInstances(all_systems_dict, club_system_keys, all_factions_dict, club_faction_keys)

Aware.setFactionsDict(all_factions_dict)

bhArr: List[List] = []  # [int, str, str, str]]
sysId: int
sorted_systems = sorted(club_system_keys)

for sysId in sorted_systems: #club_system_keys: #all_systems_dict.keys():
    tSys: InhabitedSystem = all_systems_dict.get(sysId)
    if sysId in bhDict:
        continue

    cf: FactionInstance = tSys.getControllingFactionInstance()

    if cf is None:
        print(f"System {tSys.get_name()} controlling faction is none")
        continue

    #if cf.isHomeSystem():
        #continue

    url = "https://eddb.io/system/bodies/" + str(sysId)
    sysName = tSys.get_name()
    item = [sysId, sysName, "unknown", "unknown", url]
    bhArr.append(item)
    print(f"\t\t{sysId} : False, # {sysName} {url}")

#pprint(bhArr)
