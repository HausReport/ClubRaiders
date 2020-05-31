#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import logging
from typing import Dict, List, Set, Tuple

from craid.eddb.InhabitedSystem import InhabitedSystem

#
# Make nifty list of club faction presences.
# Note: This does have to go through _all_ populated systems
#
def getClubSystemKeys(all_systems_dict: Dict[int, InhabitedSystem], club_faction_keys: Set[int]):
    currentSystem: InhabitedSystem
    club_system_keys: Set[int] = set()

    for currentSystem in all_systems_dict.values():
        mfp = currentSystem._getMinorFactionPresencesDict()
        for faction_ptr in mfp:
            if faction_ptr is None:
                continue
            faction_id: int = int(faction_ptr['minor_faction_id'])
            if faction_id is None:
                continue

            if faction_id in club_faction_keys:
                system_id: int = currentSystem.get_id()
                club_system_keys.add(system_id)  # it's a set

    logging.info("Populated club system keys")
    logging.debug("Club system lookup set has {%d} items", len(club_system_keys))
    return club_system_keys
