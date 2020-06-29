#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import logging
import tempfile
import traceback

from craid.eddb.loader import DataProducer
from craid.eddb.loader.MakeKeyFiles import loadKeys
from craid.eddb.loader.strategy.AWSLoader import LoadDataFromAWS
from craid.eddb.util.dataUpdate.CheckEddbFiles import tempFilesAreOutOfDate
from craid.eddb.util.dataUpdate.MakeHistoryFile import appendTodaysData, cleanHistoryFile, copyIntoSource
from craid.eddb.util.dataUpdate.MakeSmolFiles import deleteOldFiles, munchFile
from craid.eddb.util.dataUpdate.UploadToAmazon import uploadToAWSFromTemp

if __name__ == '__main__':
    #
    # Fire up logger
    #
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.getLogger().level = logging.DEBUG

    try:
        filesAreOutOfDate = tempFilesAreOutOfDate()
        if not filesAreOutOfDate:
            exit(1)
    except:
        exit(2)

    try:
        deleteOldFiles()
    except:
        exit(3)

    try:
        DataProducer.getDataArrays(writeKeyFiles=True, useEddb=True)
    except:
        exit(4)

    try:
        club_faction_keys = loadKeys("factions-of-interest-keys")
        munchFile(club_faction_keys, 'factions.jsonl')
        club_system_keys = loadKeys('club-system-keys')
        munchFile(club_system_keys, 'systems_populated.jsonl')
        club_station_keys = loadKeys("club-station-keys")
        munchFile(club_station_keys, 'stations.jsonl')
    except:
        exit(5)

    try:
        loader: LoadDataFromAWS = LoadDataFromAWS(forceWebDownload=True, useSmol=False)
        tmpDir = tempfile.gettempdir()
        fName = loader.download_file("history.jsonl",tmpDir) #.gz is added in the function
        appendTodaysData(fName)
        cleanHistoryFile(fName)
        copyIntoSource(fName)
    except Exception as e:
        traceback.print_exc()
        logging.error( str(e))
        exit(6)

    #
    # TODO: Test files for validity here
    #

    try:
        sNames = [ 'smol-factions.jsonl.gz', 'smol-systems_populated.jsonl.gz', 'smol-stations.jsonl.gz', 'history.jsonl.gz']
        shortName: str
        for shortName in sNames:
            ret = uploadToAWSFromTemp(shortName)
            logging.info( f"Uploading {shortName} to AWS status is {ret}")
    except Exception as e:
        traceback.print_exc()
        logging.error(str(e))
        exit(7)

    #
    # TODO: no copy of history exists in temp
    # NOTE: check in te
    #

    exit(0)