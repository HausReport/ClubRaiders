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

from craid.eddb.InhabitedSystem import InhabitedSystem
from craid.eddb.loader.LoadDataFromEDDB import LoadDataFromEDDB


#
# Load all inhabited systems
#
def load_systems() -> Dict[int, InhabitedSystem]:
    all_systems_dict: Dict[int, InhabitedSystem] = {}  # private
    nLines = 0
    fName = LoadDataFromEDDB.find_data_file('systems_populated.jsonl')
    with json_lines.open(fName, broken=True) as handle:
        for sysLine in handle:
            nLines += 1
            tid = int(sysLine['id'])
            foo = InhabitedSystem(sysLine)
            all_systems_dict[tid] = foo

    logging.info("Read %s lines of systems data", str(nLines))
    return all_systems_dict
