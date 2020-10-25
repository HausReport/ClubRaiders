#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

import gzip
import logging
import os
import shutil
import tempfile
import traceback
from shutil import copyfile
from typing import Dict, List, Set

import ujson

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

    #gitFile = os.path.join("..", "..", "..", "..", "data", outName)
    gitFile = os.path.join("data", outName)
    copyfile(outFile, gitFile)


def deleteOldFiles():
    keyFiles = ['keys-club-faction-keys.pkl', 'keys-club-station-keys.pkl', 'keys-club-system-keys.pkl',
                'keys-factions_of_interest_keys.pkl', 'keys-factions-of-interest-keys.pkl']
    eFiles = ['factions.jsonl', 'stations.jsonl', 'systems_populated.jsonl']

    #
    # Step 0: Clean recovery directory
    #
    tmpDir = tempfile.gettempdir()
    recoverDir = os.path.join(tmpDir, "crec")
    if not os.path.exists(recoverDir):
        os.makedirs(recoverDir)
    else:
        clearRecoveryFolder()

    #
    # Step 1: copy old systems file to new old-systems file
    #
    inFile = os.path.join(tmpDir, 'smol-systems_populated.jsonl.gz')
    outFile = os.path.join(tmpDir, 'smol-sys-old.jsonl.gz')
    recFile = os.path.join(recoverDir, 'smol-sys-old.jsonl.gz')
    if os.path.exists(outFile):
        copyfile(outFile, recFile)
    if os.path.exists(inFile):
        copyfile(inFile, outFile)

    #
    # Step 2: generate all filename permutations
    #
    allFiles = keyFiles
    for fName in eFiles:
        allFiles.append(fName)
        allFiles.append(fName + ".gz")
        allFiles.append("smol-" + fName + ".gz")
        allFiles.append("smol-" + fName)

    #
    # Step 3: delete the files (move to recovery dir)
    #
    for fName in allFiles:
        tmpDir = tempfile.gettempdir()
        outFile = os.path.join(tmpDir, fName)
        recFile = os.path.join(recoverDir, fName)
        if os.path.exists(outFile):
            logging.info("removing: " + outFile)
            try:
                shutil.copy2(outFile, recFile)  # NOTE: copy2 to preserve file modification time
                os.remove(outFile)
            except Exception as e:
                # FIXME: not really sure how missing file problem can happen here
                # but according to the logs it can happen
                traceback.print_exc()
                logging.error(str(e))


def unDeleteOldFiles():
    tmpDir = tempfile.gettempdir()
    recoveryDir = os.path.join(tmpDir, "crec")
    for filename in os.listdir(recoveryDir):
        fromFile = os.path.join(recoveryDir, filename)
        toFile = os.path.join(tmpDir, filename)
        shutil.copy2(fromFile, toFile)  # NOTE: copy2 to preserve file modification time


def clearRecoveryFolder():
    tmpDir = tempfile.gettempdir()
    folder = os.path.join(tmpDir, "crec")
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


# if __name__ == '__main__':
#     #
#     # Fire up logger
#     #
#     logging.getLogger().addHandler(logging.StreamHandler())
#     logging.getLogger().level = logging.DEBUG
#
#     #
#     # Get rid of old files
#     #
#     deleteOldFiles()
#
#     # need to add exceptions to DataProducer.getDataArrays and handle here
#
#     # download large files from eddb
#     DataProducer.getDataArrays(writeKeyFiles=True, useEddb=True)
#
#     # load key files & munch
#     club_faction_keys = loadKeys("factions-of-interest-keys")
#     munchFile(club_faction_keys, 'factions.jsonl')
#     club_system_keys = loadKeys('club-system-keys')
#     munchFile(club_system_keys, 'systems_populated.jsonl')
#     club_station_keys = loadKeys("club-station-keys")
#     munchFile(club_station_keys, 'stations.jsonl')

# inName = 'factions.jsonl'
