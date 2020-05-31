#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import gzip
import os
import tempfile
from typing import Dict, List, Set

import json_lines
import ujson

from craid.eddb.loader.MakeKeyFiles import loadKeys
from craid.eddb.loader.LoadDataFromGithub import LoadDataFromGithub


def munchFile(keys: Set[int], inName: str):
    tmp: List[Dict] = []
    inFile = LoadDataFromGithub.find_data_file(inName)
    with json_lines.open(inFile, broken=True) as handle:
        for facLine in handle:
            if facLine['id'] in keys:
                tmp.append(facLine)

    outName = "smol-" + inName + ".gz"
    tmpDir = tempfile.gettempdir()
    outFile = os.path.join(tmpDir, outName)

    with gzip.open(outFile, 'wt', encoding='utf-8') as file:
        foo: Dict
        for foo in tmp:
            ujson.dump(foo, file)
            file.write('\n')


if __name__ == '__main__':
    club_faction_keys = loadKeys("factions-of-interest-keys")
    munchFile( club_faction_keys, 'factions.jsonl')
    club_system_keys    = loadKeys('club-system-keys')
    munchFile( club_system_keys, 'systems_populated.jsonl')
    club_station_keys   = loadKeys("club-station-keys")
    munchFile( club_station_keys,'stations.jsonl' )

# NOTE: if any don't load, abort

inName = 'factions.jsonl'


