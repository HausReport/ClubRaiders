#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

#
# Load factions
#
import logging
from typing import Dict

import json_lines

from craid.eddb.Faction import Faction
from craid.eddb.FactionNameFilter import FactionNameFilter
from craid.eddb.loader.LoadDataFromEDDB import LoadDataFromEDDB


def load_factions() -> [Dict[int, Faction], Dict[int, Faction], Dict[int, Faction]]:
    all_factions_dict: Dict[int, Faction] = {}  # private
    playerFactionIdToInfo: Dict[int, Faction] = {}  # private
    clubFactionIdToInfo: Dict[int, Faction] = {}  # private

    nLines: int = 0
    fName = LoadDataFromEDDB.find_data_file('factions.jsonl')
    with json_lines.open(fName, broken=True) as handle:
        for facLine in handle:
            nLines += 1
            lCurFactionId = int(facLine['id'])
            curFaction = Faction(facLine)
            if FactionNameFilter.proClubFaction(curFaction):
                curFaction.setClub(True)

            all_factions_dict[lCurFactionId] = curFaction

            if curFaction.is_player():
                playerFactionIdToInfo[lCurFactionId] = curFaction
            if curFaction.isClub():
                clubFactionIdToInfo[lCurFactionId] = curFaction

    logging.info("Read %s lines of faction data", str(nLines))
    return all_factions_dict, playerFactionIdToInfo, clubFactionIdToInfo
