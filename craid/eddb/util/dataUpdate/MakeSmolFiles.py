#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

import gzip
import logging
import os
import tempfile
from shutil import copyfile
from typing import Dict, List, Set

import ujson

from craid.eddb.loader import DataProducer
from craid.eddb.loader.MakeKeyFiles import loadKeys
from craid.eddb.loader.strategy.DataLoader import DataLoader
from craid.eddb.loader.strategy.EDDBLoader import LoadDataFromEDDB


#
# Note: For the Git part, see: https://gitpython.readthedocs.io/en/stable/reference.html#module-git.cmd
#
# Note: For the sleep part, see https://stackoverflow.com/questions/2031111/in-python-how-can-i-put-a-thread-to-sleep-until-a-specific-time
#
# Note: Heroku version of cron: https://devcenter.heroku.com/articles/clock-processes-python
#

def munchFile(keys: Set[int], xinName: str):
    tmp: List[Dict] = []

    myLoader: DataLoader = LoadDataFromEDDB()
    inFile = myLoader.find_data_file(xinName)
    with gzip.open(inFile, 'rb') as f:
        for line in f:
            facLine = ujson.loads(line)
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

    gitFile = os.path.join("..", "..", "..", "..", "data", outName)
    copyfile(outFile, gitFile)


def deleteOldFiles():
    keyFiles = ['keys-club-faction-keys.pkl', 'keys-club-station-keys.pkl', 'keys-club-system-keys.pkl',
                'keys-factions_of_interest_keys.pkl', 'keys-factions-of-interest-keys.pkl']
    eFiles = ['factions.jsonl', 'stations.jsonl', 'systems_populated.jsonl']

    tmpDir = tempfile.gettempdir()
    inFile = os.path.join(tmpDir, 'smol-systems_populated.jsonl.gz')
    if os.path.exists(inFile):
        outFile = os.path.join(tmpDir, 'smol-sys-old.jsonl.gz')
        copyfile(inFile,outFile)

    allFiles = keyFiles
    for fName in eFiles:
        allFiles.append(fName)
        allFiles.append(fName + ".gz")
        allFiles.append("smol-" + fName + ".gz")
        allFiles.append("smol-" + fName)

    for fName in allFiles:
        tmpDir = tempfile.gettempdir()
        outFile = os.path.join(tmpDir, fName)
        if os.path.exists(outFile):
            logging.info("removing: " + outFile)
            os.remove(outFile)


if __name__ == '__main__':
    #
    # Fire up logger
    #
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.getLogger().level = logging.DEBUG

    #
    # Get rid of old files
    #
    deleteOldFiles()

    # need to add exceptions to DataProducer.getDataArrays and handle here

    # download large files from eddb
    DataProducer.getDataArrays(writeKeyFiles=True, useEddb=True)

    # load key files & munch
    club_faction_keys = loadKeys("factions-of-interest-keys")
    munchFile(club_faction_keys, 'factions.jsonl')
    club_system_keys = loadKeys('club-system-keys')
    munchFile(club_system_keys, 'systems_populated.jsonl')
    club_station_keys = loadKeys("club-station-keys")
    munchFile(club_station_keys, 'stations.jsonl')

# inName = 'factions.jsonl'
