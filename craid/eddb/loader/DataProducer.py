#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

from typing import Dict

from Aware import Aware
from loader.CreateClubFactionInstances import getFactionInstances
from loader.CreateFactions import load_factions
from loader.CreateStationsInClubSystems import loadStationsInClubSystems
from loader.CreateSystemNameToPositionMap import loadSystemNameToPositionMap
from loader.CreateSystems import load_systems


#
# Expensive function - run once, use result many times
#
def getDataArrays() -> Dict[str, object]:
    playerFactionNameToSystemName: Dict[str, str] = {}


    #
    # Load the basic factions and systems structures
    #
    all_factions_dict, playerFactionIdToInfo, clubFactionIdToInfo = load_factions()
    all_systems_dict = load_systems()

    #
    # Give global faction info to systems and
    # give global system info to factions
    #
    Aware.setSystemsDict(all_systems_dict)
    Aware.setFactionsDict(all_factions_dict)

    #
    # Populate dict of system name & x,y,zs
    # Used by dropdowns in dashboard
    #
    systemNameToXYZ = loadSystemNameToPositionMap(all_systems_dict)

    #
    # Make (2?) nifty list(s) of club faction presences
    #
    allClubSystemInstances, clubSystemLookup, sysIdFacIdToFactionInstance \
            = getFactionInstances(all_systems_dict, clubFactionIdToInfo, all_factions_dict)

    #
    # Only now, can we populate lists of stations in **club** systems
    # No return value - stations are stored in their respective system objects
    #
    loadStationsInClubSystems(all_systems_dict, clubFactionIdToInfo, clubSystemLookup )

    #
    # And, finally return the big honking dict of things
    #


    # 'playerFactionIdToInfo': playerFactionIdToInfo,
    #
    #  FIXME: the roles of allClubSystemInstances and sysIdFacIdToFactionInstance
    #          could be combined.  only really need the latter
    #
    #  FIXME:playerFactionNameToSystemName  could be moved to dashboard
    return {'clubFactionIdToInfo'          : clubFactionIdToInfo,
            'all_systems_dict'             : all_systems_dict,
            'allClubSystemInstances'       : allClubSystemInstances,
            'systemNameToXYZ'              : systemNameToXYZ,
            'sysIdFacIdToFactionInstance'  : sysIdFacIdToFactionInstance,
            'playerFactionNameToSystemName': playerFactionNameToSystemName,  # used in dashboard for 2nd dropdown
            }

# if __name__ == '__main__':
# csa = getDataArrays()
