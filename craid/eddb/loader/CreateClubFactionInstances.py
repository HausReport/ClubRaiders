#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
import logging
from typing import Dict, List, Set, Tuple

from craid.eddb.Faction import Faction
from craid.eddb.FactionInstance import FactionInstance
from craid.eddb.InhabitedSystem import InhabitedSystem
from craid.eddb.States import States


#   SPDX-License-Identifier: BSD-3-Clause

#
# Make nifty list of club faction presences.
# Note: This does have to go through _all_ populated systems
#
def getFactionInstances(all_systems_dict: Dict[int, InhabitedSystem], club_system_keys: Set[int],
                        all_factions_dict: Dict[int, Faction], club_faction_keys: Set[int]  ):

    allClubSystemInstances: List[FactionInstance] = []  # make this one avaiable
    sysIdFacIdToFactionInstance: Dict[Tuple[int, int], FactionInstance] = {}

    currentSystem: InhabitedSystem
    for currentSystem in all_systems_dict.values():

        sys_id = currentSystem.get_id()     # this is the big time-saver
        if sys_id not in club_system_keys:
            continue

        mfp = currentSystem._getMinorFactionPresencesDict()
        for faction_ptr in mfp:
            if faction_ptr is None:
                continue
            faction_id: int = int(faction_ptr['minor_faction_id'])
            if faction_id is None:
                continue

            fac = all_factions_dict[faction_id]
            #factionName: str = fac.get_name2()

            #
            # Scan for interesting faction states
            #
            govt = currentSystem.getGovernment()
            inf = faction_ptr['influence']
            vulnerabilities: States = States(govt, inf, faction_ptr['active_states'])

            #
            # Create the faction instance and pop it in the appropriate bins
            #
            factionInstance = FactionInstance(fac, currentSystem, inf, vulnerabilities)
            # seems redundant, but
            if fac.isClub():
                factionInstance.setClub(True)

            system_id: int = currentSystem.get_id()
            sysIdFacIdToFactionInstance[(system_id, faction_id)] = factionInstance

            currentSystem._addMinorFactionPresence(factionInstance)

            #
            # Special handling for club factions
            #
            if faction_id in club_faction_keys:
                #
                # Keep player factions out of club factions.
                # Cheap trick to see if it's a player faction that
                # was identified by the filter as a club faction
                #
                #if factionName.startswith("*"):
                if factionInstance.is_player():
                    continue  # filters player factions

                allClubSystemInstances.append(factionInstance)


    logging.info("Populated club faction presences")
    logging.debug("Club system lookup set has {%d} items", len(club_system_keys))
    return allClubSystemInstances, sysIdFacIdToFactionInstance
