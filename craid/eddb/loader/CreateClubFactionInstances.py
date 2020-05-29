#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
import logging
from typing import Dict, List, Set, Tuple

from Faction import Faction
from FactionInstance import FactionInstance
from InhabitedSystem import InhabitedSystem
from Vulnerability import Vulnerability
#   SPDX-License-Identifier: BSD-3-Clause

#
# Make nifty list of club faction presences
#
def getFactionInstances(all_systems_dict: Dict[int, InhabitedSystem], clubFactionIdToInfo: Dict[int, Faction] ):
    cSystem: InhabitedSystem

    allClubSystemInstances: List[FactionInstance] = []  # make this one avaiable
    clubSystemLookup: Set[int] = set()
    sysIdFacIdToFactionInstance: Dict[Tuple[int, int], FactionInstance] = {}

    for cSystem in all_systems_dict.values():
        mfp = cSystem.getMinorFactionPresences()
        for faction_ptr in mfp:
            if faction_ptr is None:
                continue
            faction_id: int = int(faction_ptr['minor_faction_id'])
            if faction_id is None:
                continue
            if faction_id in clubFactionIdToInfo:
                fac = clubFactionIdToInfo[faction_id]  ## FIXME: double lookup
                factionName: str = fac.get_name2()

                #
                # Cheap trick to see if it's a player faction that
                # was identified by the filter as a club faction
                #
                if factionName.startswith("*"):
                    continue  # filters player factions

                #
                # Scan for interesting faction states
                #
                govt = cSystem.getGovernment()
                inf = faction_ptr['influence']
                vulnerabilities: Vulnerability = Vulnerability(govt, inf, faction_ptr['active_states'])

                #
                # Create the faction instance and pop it in the appropriate bins
                #
                factionInstance = FactionInstance(fac, cSystem, inf, vulnerabilities)
                allClubSystemInstances.append(factionInstance)

                system_id: int = cSystem.get_id()
                sysIdFacIdToFactionInstance[(system_id, faction_id)] = factionInstance

                #
                # We use this set later to quickly match systems that have
                # a club presence
                clubSystemLookup.add(system_id)  # it's a set

    logging.info("Populated club faction presences")
    logging.debug("Club system lookup set has {%d} items", len(clubSystemLookup))
    return allClubSystemInstances, clubSystemLookup, sysIdFacIdToFactionInstance
