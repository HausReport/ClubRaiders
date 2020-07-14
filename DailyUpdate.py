#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import tempfile
import traceback
from craid.eddb.loader import DataProducer
from craid.eddb.loader.MakeKeyFiles import loadKeys
from craid.eddb.loader.strategy.AWSLoader import LoadDataFromAWS
from craid.eddb.util.dataUpdate.CheckEddbFiles import eddbUpdateReadyForTemp
from craid.eddb.util.dataUpdate.MakeHistoryFile import appendTodaysData, cleanHistoryFile, copyIntoSource
from craid.eddb.util.dataUpdate.MakeSmolFiles import deleteOldFiles, munchFile, unDeleteOldFiles
from craid.eddb.util.dataUpdate.UploadToAmazon import uploadToAWSFromTemp
import logging
import os
from datetime import date, timedelta
from datetime import datetime
import pause
import requests
from craid.eddb.util.dataUpdate.CheckEddbFiles import oldestLocalEddbFile


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
            logging.basicConfig(
                format='DMN - %(asctime)s %(levelname)-8s %(message)s',
                level=logging.INFO,
                datefmt='%Y-%m-%d %H:%M:%S')
            logging.info("Creating dailyupdate singleton")
            # Put any initialization here.
        else:
            logging.info("Reusing dailyupdate singleton")
        return cls._instance

    def run(self):
        logging.info("Pausing 5 minutes for startup...")
        pause.minutes(5)  # FIXME: uncomment for production
        while True:
            today = date.today()
            lastnight = datetime.combine(today, datetime.min.time())
            tonight = lastnight + timedelta(days=1, hours=2)
            twoDaysAgo = lastnight + timedelta(days=-2, minutes=5)
            dt: datetime = oldestLocalEddbFile()

            retries = 0

            if dt < lastnight:
                force = False
                # case of one or more missing files
                if dt < twoDaysAgo:
                    force = True
                logging.info("Detected old or missing datafile.")
                returnValue = -1
                while returnValue != 0:
                    returnValue = dup.runUpdate(forceDownload=force)

                    if returnValue == DailyUpdate.OKEY_DOKEY:
                        logging.info("Successfully updated files.")
                    else:
                        if returnValue == DailyUpdate.NOT_ALL_UPDATES_READY:
                            logging.info("Not all updates are ready.")
                        elif returnValue == DailyUpdate.ERROR_UPLOADING_TO_AWS:
                            logging.error(f"Error {returnValue} uploading to AWS.")
                        elif returnValue == DailyUpdate.ERROR_UPDATING_HISTORY_FILE:
                            logging.error(f"Error {returnValue} updating history file.")
                        elif returnValue == DailyUpdate.ERROR_MAKING_KEY_FILES:
                            logging.error(f"Error {returnValue} making key files.")
                        elif returnValue == DailyUpdate.ERROR_GETTING_DATA_ARRAYS:
                            logging.error(f"Error {returnValue} getting data arrays.")
                        elif returnValue == DailyUpdate.ERROR_DELETING_FILES:
                            logging.error(f"Error {returnValue} deleting files.")
                        elif returnValue == DailyUpdate.ERROR_CHECKING_TIMES:
                            logging.error(f"Error {returnValue} checking times.")
                        else:
                            logging.error(f"Error with unknown return value {returnValue}")

                        retries = retries + 1
                        if retries > 12:
                            # give up for the day
                            logging.warning("12 retries - giving up for the day.")
                            retries = 0
                            force = True
                            pause.until(tonight)
                        else:
                            logging.info("Pausing 30 minutes before retrying.")
                            pause.minutes(30)

                logging.info("Restarting all dynos.")
                self.restartAllDynos()  # This should kill off this process when running in production
            else:
                logging.info("Detected no old or missing datafiles.")

            logging.info("Pausing until midnight.")
            pause.until(tonight)

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

    def restartAllDynos(self):
        app_name = os.getenv('HEROKU_APP_NAME')
        uname = os.getenv('HEROKU_CLI_USER')
        tok = os.getenv('HEROKU_CLI_TOKEN')

        # print(app_name)
        # print(uname)
        # print(tok)

        auth = (uname, tok)
        url = f"https://api.heroku.com/apps/{app_name}/dynos"
        logging.info(str(url))
        headers = {"Content-Type": "application/json",
                   "Accept"      : "application/vnd.heroku+json; version=3"}
        req = requests.delete(url=url, auth=auth, headers=headers)
        logging.info(str(req))
        logging.info(req.content)


if __name__ == '__main__':
    #
    # Fire up logger
    #
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.getLogger().level = logging.INFO

    dup = DailyUpdate()
    ret = dup.runUpdate()
    exit(ret)
