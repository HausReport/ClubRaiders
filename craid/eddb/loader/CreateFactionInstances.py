#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
import logging
from typing import Dict, List, Set, Tuple

from craid.eddb.States import States
from craid.eddb.faction.Faction import Faction
from craid.eddb.faction.FactionInstance import FactionInstance
from craid.eddb.system.InhabitedSystem import InhabitedSystem


#   SPDX-License-Identifier: BSD-3-Clause

#
# Make nifty list of club faction presences.
# Note: This does have to go through _all_ populated systems
#
def getFactionInstances(all_systems_dict: Dict[int, InhabitedSystem], club_system_keys: Set[int],
                        all_factions_dict: Dict[int, Faction], club_faction_keys: Set[int], clubSystemsOnly=True):
    allClubSystemInstances: List[FactionInstance] = []  # make this one avaiable
    sysIdFacIdToFactionInstance: Dict[Tuple[int, int], FactionInstance] = {}
    factions_of_interest_keys: Set[int] = set()

    nFacInst = 0
    currentSystem: InhabitedSystem
    for currentSystem in all_systems_dict.values():

        sys_id = currentSystem.get_id()  # this is the big time-saver
        if clubSystemsOnly and (sys_id not in club_system_keys):
            continue

        mfp = currentSystem._getMinorFactionPresencesDict()
        for faction_ptr in mfp:
            if faction_ptr is None:
                continue
            faction_id: int = int(faction_ptr['minor_faction_id'])
            if faction_id is None:
                continue

            fac = all_factions_dict.get(faction_id)
            if fac is None:
                logging.warning("Unknown faction ID: " + str(faction_id))
                continue
            # factionName: str = fac.get_name2()

            #
            # Scan for interesting faction states
            #
            govt = currentSystem.getGovernment()
            inf = faction_ptr['influence']
            active_states: States = States(govt, inf, faction_ptr['active_states'])
            recovering_states: States = States(govt, inf, faction_ptr['recovering_states'])
            pending_states: States = States(govt, inf, faction_ptr['pending_states'])

            #
            # Create the faction instance and pop it in the appropriate bins
            #
            nFacInst += 1
            factionInstance = FactionInstance(fac, currentSystem, inf, active_states, recovering_states, pending_states)
            factions_of_interest_keys.add(faction_id)

            happ_id = faction_ptr['happiness_id']
            factionInstance.set_happiness_id(happ_id)

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
                # if factionName.startswith("*"):
                if factionInstance.is_player():
                    continue  # filters player factions

                allClubSystemInstances.append(factionInstance)

    logging.info("Populated faction instances: {%d} items.", nFacInst)
    return allClubSystemInstances, sysIdFacIdToFactionInstance, factions_of_interest_keys
