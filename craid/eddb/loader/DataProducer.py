#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import gc
import logging
import multiprocessing
from typing import Dict, Set

import pandas as pd

import craid.eddb.util.Printmem as pm
from craid.eddb.base.Aware import Aware
from craid.eddb.faction.Faction import Faction
from craid.eddb.loader.CreateClubSystemKeys import getClubSystemKeys
from craid.eddb.loader.CreateDataFrame import getDataFrame
from craid.eddb.loader.CreateFactionInstances import getFactionInstances
from craid.eddb.loader.CreateFactions import load_factions
from craid.eddb.loader.CreateStationsInClubSystems import loadStationsInClubSystems
from craid.eddb.loader.CreateSystems import load_systems
from craid.eddb.loader.MakeKeyFiles import dumpKeys, loadKeys
from craid.eddb.loader.strategy.AWSLoader import LoadDataFromAWS
from craid.eddb.loader.strategy.EDDBLoader import LoadDataFromEDDB

lock = multiprocessing.Lock()


def getDataArrays(writeKeyFiles=False, useEddb=False, loader=None, clubSystemsOnly=True) -> Dict[str, object]:
    global lock
    #lock = multiprocessing.Lock()
    #lock.acquire()
    with lock:
        logging.info("Acquired lock.")
        if loader is not None:
            logging.info("Using supplied loader")
            myLoader = loader
        else:
            if useEddb:
                logging.info("Loading from EDDB")
                myLoader = LoadDataFromEDDB()
            else:
                logging.info("Loading from AWS")
                myLoader = LoadDataFromAWS()  # LoadDataFromGithub()

        playerFactionNameToSystemName: Dict[str, str] = {}

        pm.printmem('0')
        #
        # Load the basic factions and systems structures
        #
        all_factions_dict, player_faction_keys, club_faction_keys = load_factions(myLoader)
        pm.printmem('0.5')
        all_systems_dict = load_systems(myLoader)

        gc.collect()
        pm.printmem('1')

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
        clubSystemKeysExists = True
        club_system_keys = loadKeys('club-system-keys')
        if club_system_keys is None:
            club_system_keys = getClubSystemKeys(all_systems_dict, club_faction_keys)
            clubSystemKeysExists = False

        #
        # Make (2?) nifty list(s) of club faction presences
        #
        allClubSystemInstances, sysIdFacIdToFactionInstance, factions_of_interest_keys \
            = getFactionInstances(all_systems_dict, club_system_keys, all_factions_dict, club_faction_keys, clubSystemsOnly=clubSystemsOnly)

        gc.collect()
        pm.printmem('2')

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
        club_station_keys: Set[int] = \
            loadStationsInClubSystems(myLoader, all_systems_dict, club_faction_keys, club_system_keys)

        gc.collect()
        pm.printmem('3')
        #
        # And, finally return the big honking dict of things
        #

        df: pd.DataFrame = getDataFrame(allClubSystemInstances)

        #
        # Clean up some resources
        #

        if writeKeyFiles:
            dumpKeys("club-system-keys", club_system_keys)
            dumpKeys("factions-of-interest-keys", factions_of_interest_keys)
            dumpKeys("club-station-keys", club_station_keys)

        # FIXME - think about this
        # if not factions_of_interest_keys:
        # if not clubSystemKeysExists:

        allClubSystemInstances.clear()
        allClubSystemInstances = None
        club_faction_keys.clear()
        club_faction_keys = None
        gc.collect()

    #    lock.release() # FIXME: needs to be in a finally: block
    logging.info("Released lock.")

    # 'playerFactionIdToInfo': playerFactionIdToInfo,
    #
    #
    #  FIXME:playerFactionNameToSystemName  could be moved to dashboard
    return {'dataFrame'                    : df,
            # 'systemNameToXYZ'              : systemNameToXYZ,
            'sysIdFacIdToFactionInstance'  : sysIdFacIdToFactionInstance,
            'playerFactionNameToSystemName': playerFactionNameToSystemName,  # used in dashboard for 2nd dropdown
            }

# if __name__ == '__main__':
# csa = getDataArrays()
