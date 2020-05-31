#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import logging
from typing import Dict
import pandas as pd

from craid.eddb.Aware import Aware
from craid.eddb.loader.CreateClubFactionInstances import getFactionInstances
from craid.eddb.loader.CreateFactions import load_factions
from craid.eddb.loader.CreateStationsInClubSystems import loadStationsInClubSystems
from craid.eddb.loader.CreateSystemNameToPositionMap import loadSystemNameToPositionMap
from craid.eddb.loader.CreateSystems import load_systems
import craid.eddb.Printmem as pm

import gc

#
# Expensive function - run once, use result many times
#
from craid.eddb.loader.CreateDataFrame import getDataFrame
from eddb.Faction import Faction
from eddb.loader.CreateClubSystemKeys import getClubSystemKeys


def getDataArrays() -> Dict[str, object]:
    playerFactionNameToSystemName: Dict[str, str] = {}

    pm.printmem('0')
    #
    # Load the basic factions and systems structures
    #
    all_factions_dict, player_faction_keys, club_faction_keys = load_factions()
    pm.printmem('0.5')
    all_systems_dict = load_systems()

    gc.collect()
    pm.printmem('1')

    #
    # Populate dict of system name & x,y,zs
    # Used by dropdowns in dashboard
    #
    systemNameToXYZ = loadSystemNameToPositionMap(all_systems_dict)

    #
    # Populate dict of player faction name -> system name
    # Used by dropdowns in dashboard
    #
    k: int
    for k in player_faction_keys:
        fac: Faction = all_factions_dict[k]
        fac_name: str = fac.get_name()
        sys_id: int = all_factions_dict[k].homesystem_id
        sys = all_systems_dict.get(sys_id)
        if sys is not None:
            sys_name: str = sys.get_name()
            playerFactionNameToSystemName[fac_name] = sys_name

    #
    # Identify systems with club faction presence
    #
    club_system_keys = getClubSystemKeys(all_systems_dict, club_faction_keys)

    #
    # Make (2?) nifty list(s) of club faction presences
    #
    allClubSystemInstances, sysIdFacIdToFactionInstance \
            = getFactionInstances(all_systems_dict, club_system_keys, all_factions_dict, club_faction_keys )


    gc.collect()
    pm.printmem('2')

    # Had almost no impact on memory usage
    # Prune down all_systems_dict to systems we're interested in
    #
    # key: int
    # for key in list(all_systems_dict.keys()):
    #     if key in club_system_keys:
    #         continue
    #     else:
    #         all_systems_dict.pop(key)
    #
    # logging.info("Pruned systems dict down to " + str(len(all_systems_dict)))
    # key: int
    # for key in list(all_factions_dict.keys()):
    #     if key in club_system_keys:
    #         continue
    #     else:
    #         all_systems_dict.pop(key)

    #
    # Give global faction info to systems and
    # give global system info to factions
    #
    Aware.setSystemsDict(all_systems_dict)
    Aware.setFactionsDict(all_factions_dict)

    #
    # Only now, can we populate lists of stations in **club** systems
    # No return value - stations are stored in their respective system objects
    #
    loadStationsInClubSystems(all_systems_dict, club_faction_keys, club_system_keys )

    gc.collect()
    pm.printmem('3')
    #
    # And, finally return the big honking dict of things
    #

    df: pd.DataFrame = getDataFrame(allClubSystemInstances)

    #
    # Clean up some resources
    #
    allClubSystemInstances.clear()
    allClubSystemInstances = None
    club_faction_keys.clear()
    club_faction_keys = None
    gc.collect()

    # 'playerFactionIdToInfo': playerFactionIdToInfo,
    #
    #  FIXME: the roles of allClubSystemInstances and sysIdFacIdToFactionInstance
    #          could be combined.  only really need the latter
    #
    #  FIXME:playerFactionNameToSystemName  could be moved to dashboard
    return {#'clubFactionIdToInfo'          : clubFactionIdToInfo,
            'dataFrame'                     : df,
            #'all_systems_dict'             : all_systems_dict,
            #'allClubSystemInstances'       : allClubSystemInstances,
            'systemNameToXYZ'              : systemNameToXYZ,
            'sysIdFacIdToFactionInstance'  : sysIdFacIdToFactionInstance,
            'playerFactionNameToSystemName': playerFactionNameToSystemName,  # used in dashboard for 2nd dropdown
            }

# if __name__ == '__main__':
# csa = getDataArrays()
