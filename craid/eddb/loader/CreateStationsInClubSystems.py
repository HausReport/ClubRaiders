#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

#
# Only now, can we populate lists of stations in **club** systems
#
import gzip
import logging
from typing import Dict
from typing import Set

import ujson

from craid.eddb.system.InhabitedSystem import InhabitedSystem
from craid.eddb.Station import Station
from craid.eddb.loader.DataLoader import DataLoader


def loadStationsInClubSystems(loader: DataLoader,
                              all_systems_dict: Dict[int, InhabitedSystem],
                              club_faction_keys: Set[int],
                              club_system_keys: Set[int]) -> Set[int]:
    station_keys = set()
    nLines: int = 0
    nAdded: int = 0
    fName = loader.find_data_file('stations.jsonl')
    # with jsonlines.open(fName) as handle:
    #    staLine: Dict
    # for staLine in handle:
    with gzip.open(fName, 'rb') as f:
        for line in f:
            staLine = ujson.loads(line)
            nLines += 1
            #
            # Weeds out stations with no controlling faction
            #
            controlFacId = staLine.get('controlling_minor_faction_id')
            if controlFacId is not None:
                #
                # Only load stations in systems with club presence
                #
                lCurSystemId = int(staLine['system_id'])
                if lCurSystemId in club_system_keys:
                    #
                    # Only load stations in systems with valid ids
                    #
                    curSys: InhabitedSystem = all_systems_dict[lCurSystemId]
                    if curSys is not None:

                        # Note: playing with reducing mem requirements
                        staLine.pop("selling_ships")
                        staLine.pop("selling_modules")
                        #
                        # Create the station object
                        #
                        sta: Station = Station(staLine)
                        sid: int = sta.get_id()
                        station_keys.add(sid)
                        nAdded += 1
                        #
                        # If the club controls the station, set that here
                        #
                        if controlFacId in club_faction_keys:  # clubSystemLookup:
                            sta.setClub(True)

                        #
                        # Add the station
                        #
                        curSys.addStation(sta)

    logging.info("Read %d lines of station data, adding %d\n", nLines, nAdded)
    return station_keys
