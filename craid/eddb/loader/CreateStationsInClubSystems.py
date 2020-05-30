#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

#
# Only now, can we populate lists of stations in **club** systems
#
import logging
from typing import Dict
from typing import Set

import json_lines

from Faction import Faction
from InhabitedSystem import InhabitedSystem
from Station import Station
from loader.LoadDataFromEDDB import LoadDataFromEDDB


def loadStationsInClubSystems(all_systems_dict : Dict[int, InhabitedSystem] , clubFactionIdToInfo: Dict[int, Faction], clubSystemLookup : Set[int] ) -> None:
    nLines: int = 0
    nAdded: int = 0
    fName = LoadDataFromEDDB.find_data_file('stations.jsonl')
    with json_lines.open(fName, broken=True) as handle:
        for staLine in handle:
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
                if lCurSystemId in clubSystemLookup:
                    #
                    # Only load stations in systems with valid ids
                    #
                    curSys: InhabitedSystem = all_systems_dict[lCurSystemId]
                    if curSys is not None:
                        #
                        # Create the station object
                        #
                        sta: Station = Station(staLine)
                        nAdded += 1
                        #
                        # If the club controls the station, set that here
                        #
                        if controlFacId in clubFactionIdToInfo:  # clubSystemLookup:
                            sta.setClub(True)

                        #
                        # Add the station
                        #
                        curSys.addStation(sta)

    logging.info("Read %d lines of station data, adding %d\n", nLines, nAdded)
    return None
