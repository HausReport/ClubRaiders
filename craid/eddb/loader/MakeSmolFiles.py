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

from craid.eddb.loader import DataProducer
from craid.eddb.loader.DataLoader import DataLoader
from craid.eddb.loader.LoadDataFromGithub import LoadDataFromGithub
from craid.eddb.loader.MakeKeyFiles import loadKeys


def munchFile(keys: Set[int], xinName: str):
    tmp: List[Dict] = []

    myLoader: DataLoader = LoadDataFromGithub()
    inFile = myLoader.find_data_file(xinName)
    with json_lines.open(inFile, broken=True) as handle:
        for facLine in handle:
            if facLine['id'] in keys:
                tmp.append(facLine)

    outName = "smol-" + xinName + ".gz"
    tmpDir = tempfile.gettempdir()
    outFile = os.path.join(tmpDir, outName)

    with gzip.open(outFile, 'wt', encoding='utf-8') as file:
        foo: Dict
        for foo in tmp:
            ujson.dump(foo, file)
            file.write('\n')


if __name__ == '__main__':

    # TODO: Delete large files from temp directory


    # download large files from eddb
    DataProducer.getDataArrays(writeKeyFiles=True, useEddb=True)
    # delete smol

    #load key files & munch
    club_faction_keys = loadKeys("factions-of-interest-keys")
    munchFile( club_faction_keys, 'factions.jsonl')
    club_system_keys    = loadKeys('club-system-keys')
    munchFile( club_system_keys, 'systems_populated.jsonl')
    club_station_keys   = loadKeys("club-station-keys")
    munchFile( club_station_keys,'stations.jsonl' )

# NOTE: if any don't load, abort

inName = 'factions.jsonl'


