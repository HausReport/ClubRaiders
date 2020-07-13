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
from craid.eddb.util.dataUpdate.CheckEddbFiles import eddbUpdateReadyForTemp
from craid.eddb.util.dataUpdate.MakeHistoryFile import appendTodaysData, cleanHistoryFile, copyIntoSource
from craid.eddb.util.dataUpdate.MakeSmolFiles import deleteOldFiles, munchFile, unDeleteOldFiles
from craid.eddb.util.dataUpdate.UploadToAmazon import uploadToAWSFromTemp


class DailyUpdate(object):
    _instance = None
    OKEY_DOKEY = 0
    ERROR_UPLOADING_TO_AWS = 7
    ERROR_UPDATING_HISTORY_FILE = 6
    ERROR_MAKING_KEY_FILES = 5
    ERROR_GETTING_DATA_ARRAYS = 4
    ERROR_DELETING_FILES = 3
    ERROR_CHECKING_TIMES = 2
    NOT_ALL_UPDATES_READY = 1

    def __new__(cls):
        if cls._instance is None:
            #print('Creating the object')
            cls._instance = super(DailyUpdate, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance

    def runUpdate(self, forceDownload=False) -> int:
        #
        # Check if EDDB's data is newer than ours
        #
        if forceDownload:
            logging.info("Forcing download - old or missing files.")
        else:
            try:
                allUpdatesReady = eddbUpdateReadyForTemp()
                if not allUpdatesReady:
                    return DailyUpdate.NOT_ALL_UPDATES_READY
            except Exception as e:
                traceback.print_exc()
                logging.error(str(e))
                return DailyUpdate.ERROR_CHECKING_TIMES

        #
        # Get rid of old files
        # NOTE: make copies and fall back to them in case of error?
        #
        try:
            deleteOldFiles()
        except Exception as e:
            traceback.print_exc()
            logging.error(str(e))
            unDeleteOldFiles()
            return DailyUpdate.ERROR_DELETING_FILES

        #
        # Make key files from new large data files
        #
        try:
            DataProducer.getDataArrays(writeKeyFiles=True, useEddb=True)
        except Exception as e:
            traceback.print_exc()
            logging.error(str(e))
            unDeleteOldFiles()  # NOTE: new
            return DailyUpdate.ERROR_GETTING_DATA_ARRAYS

        #
        # Make smol-.gz files from keys+large data files
        #
        try:
            club_faction_keys = loadKeys("factions-of-interest-keys")
            munchFile(club_faction_keys, 'factions.jsonl')
            club_system_keys = loadKeys('club-system-keys')
            munchFile(club_system_keys, 'systems_populated.jsonl')
            club_station_keys = loadKeys("club-station-keys")
            munchFile(club_station_keys, 'stations.jsonl')
        except Exception as e:
            traceback.print_exc()
            logging.error(str(e))
            unDeleteOldFiles()  # NOTE: new
            return DailyUpdate.ERROR_MAKING_KEY_FILES

        #
        # Get history from AWS, update & clean it
        #
        try:
            loader: LoadDataFromAWS = LoadDataFromAWS(forceWebDownload=True, useSmol=False)
            tmpDir = tempfile.gettempdir()
            fName = loader.download_file("history.jsonl", tmpDir)  # .gz is added in the function
            appendTodaysData(fName)
            cleanHistoryFile(fName)
            copyIntoSource(fName)  # FIXME: Not sure about this on production server
        except Exception as e:
            traceback.print_exc()
            logging.error(str(e))
            # ?????????????? unDeleteOldFiles() # NOTE: not sure about this
            return DailyUpdate.ERROR_UPDATING_HISTORY_FILE

        #
        # TODO: Test files for validity here
        #

        # factions should be more than 30 rows long
        # factioninstances should be more than 30 rows long
        # club factions should be more than 30 rows long
        # systems should be more than 30 rows long

        # if necessary
        # unDeleteOldFiles() #NOTE: new

        #
        # Upload to AWS
        #
        try:
            sNames = ['smol-factions.jsonl.gz',
                      'smol-systems_populated.jsonl.gz',
                      'smol-stations.jsonl.gz',
                      'history.jsonl.gz']
            shortName: str
            for shortName in sNames:
                retVal = uploadToAWSFromTemp(shortName)
                logging.info(f"Uploading {shortName} to AWS status is {retVal}")
        except Exception as e:
            traceback.print_exc()
            logging.error(str(e))
            return DailyUpdate.ERROR_UPLOADING_TO_AWS

        #
        # FIXME: check new files into github
        #

        return DailyUpdate.OKEY_DOKEY


if __name__ == '__main__':
    #
    # Fire up logger
    #
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.getLogger().level = logging.INFO

    dup = DailyUpdate()
    ret = dup.runUpdate()
    exit(ret)
