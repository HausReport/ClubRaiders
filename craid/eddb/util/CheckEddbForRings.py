#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
from pprint import pprint
from typing import Dict, List, Tuple

from craid.eddb.Aware import Aware
from craid.eddb.Faction import Faction
from craid.eddb.FactionInstance import FactionInstance
from craid.eddb.InhabitedSystem import InhabitedSystem
from craid.eddb.loader.CreateFactionInstances import getFactionInstances
from craid.eddb.loader.CreateFactions import load_factions
from craid.eddb.loader.CreateSystems import load_systems
from craid.eddb.loader.LoadDataFromGithub import LoadDataFromGithub
from craid.eddb.loader.MakeKeyFiles import loadKeys

myLoader = LoadDataFromGithub()

all_factions_dict, player_faction_keys, club_faction_keys = load_factions(myLoader)
club_system_keys = loadKeys('club-system-keys')
all_systems_dict = load_systems(myLoader)

allClubSystemInstances, sysIdFacIdToFactionInstance, factions_of_interest_keys \
    = getFactionInstances(all_systems_dict, club_system_keys, all_factions_dict, club_faction_keys)

Aware.setFactionsDict(all_factions_dict)

bhArr: List[ List] = [] #[int, str, str, str]]
sysId : int
for sysId in all_systems_dict.keys():
    tSys: InhabitedSystem = all_systems_dict.get(sysId)
    cf: FactionInstance = tSys.getControllingFactionInstance()

    if cf.isHomeSystem():
        continue

    url = "https://eddb.io/system/bodies/" + str(sysId)
    sysName = tSys.get_name()
    item = [ sysId, sysName, "unknown", "unknown", url]
    bhArr.append(item)
    print(tSys.get_name()    )

pprint(bhArr)
