#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

#
# Load factions
#
import gzip
import logging
from typing import Dict, Set

import ujson

from craid.eddb.Faction import Faction
from craid.eddb.FactionNameFilter import FactionNameFilter
from craid.eddb.loader.DataLoader import DataLoader


# from memory_profiler import profile


def load_factions(loader: DataLoader) -> [Dict[int, Faction], Dict[int, Faction], Dict[int, Faction]]:
    all_factions_dict: Dict[int, Faction] = {}  # private
    player_faction_keys: Set[int] = set()
    club_keys: Set[int] = set()

    nLines: int = 0
    fName = loader.find_data_file('factions.jsonl')
#    with jsonlines.open(fName) as handle:
#        for facLine in handle:
    with gzip.open(fName, 'rb') as f:
        for line in f:
            facLine = ujson.loads(line)
            nLines += 1
            lCurFactionId = int(facLine['id'])
            curFaction = Faction(facLine)
            if FactionNameFilter.proClubFaction(curFaction):
                curFaction.setClub(True)

            all_factions_dict[lCurFactionId] = curFaction

            if curFaction.is_player():
                player_faction_keys.add(lCurFactionId)
            if curFaction.isClub():
               club_keys.add(lCurFactionId)
               # clubFactionIdToInfo[lCurFactionId] = curFaction

    logging.info("Read %s lines of faction data", str(nLines))
    return all_factions_dict, player_faction_keys, club_keys
