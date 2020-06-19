#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

#
# Load factions
#
import gzip
import logging
from typing import Dict

# from memory_profiler import profile
import ujson

from craid.eddb.InhabitedSystem import InhabitedSystem
#
# Load all inhabited systems
#
# @profile
from craid.eddb.loader.DataLoader import DataLoader


def load_systems(loader: DataLoader) -> Dict[int, InhabitedSystem]:
    all_systems_dict: Dict[int, InhabitedSystem] = {}  # private
    nLines = 0
    fName = loader.find_data_file('systems_populated.jsonl')
    with gzip.open(fName, 'rb') as f:
        for line in f:
            sysLine = ujson.loads(line)
            nLines += 1
            tid = int(sysLine['id'])
            foo = InhabitedSystem(sysLine)
            all_systems_dict[tid] = foo

    logging.info("Read %s lines of systems data", str(nLines))
    return all_systems_dict
