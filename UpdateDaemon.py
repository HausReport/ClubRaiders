#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import logging
import os
from datetime import date, timedelta
from datetime import datetime

import pause
import requests

from DailyUpdate import DailyUpdate
from craid.eddb.util.dataUpdate.CheckEddbFiles import oldestLocalEddbFile


def restartAllDynos():
    app_name = os.getenv('HEROKU_APP_NAME')
    uname = os.getenv('HEROKU_CLI_USER')
    tok = os.getenv('HEROKU_CLI_TOKEN')

    # print(app_name)
    # print(uname)
    # print(tok)

    auth = (uname, tok)
    url = f"https://api.heroku.com/apps/{app_name}/dynos"
    print(str(url))
    headers = {"Content-Type": "application/json",
               "Accept"      : "application/vnd.heroku+json; version=3"}
    req = requests.delete(url=url, auth=auth, headers=headers)
    print(str(req))
    print(req.content)


# 0. WAIT 5 MINUTES (LET WEB SERVER STARTUP & GET FILES.  AVOID RACE CONDITION.)
# 1. GET TIME OF OLDEST DATA FILE
# 2. IF FILE IS MISSING
#    OR OLDER THAN MIDNIGHT
#       -- LOOP UNTIL DATA AVAILABLE
#       -- RELOAD
#       -- CONSIDER RETURN VALUE
#       -- RESTART SERVER IF GOOD
# 3. SLEEP UNTIL MIDNIGHT
# 4. GOTO 1.

if __name__ == '__main__':
    #
    # Fire up logger
    #
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.getLogger().level = logging.INFO

    logging.info("Pausing 5 minutes for startup...")
    # pause.minutes(5)   FIXME: uncomment for production

    dup = DailyUpdate()

    while True:
        today = date.today()
        lastnight = datetime.combine(today, datetime.min.time())
        tonight = lastnight + timedelta(days=1,hours=2)
        twoDaysAgo = lastnight + timedelta(days=-2,minutes=5)
        dt: datetime = oldestLocalEddbFile()

        retries = 0

        if dt < lastnight:
            force = False
            # case of one or more missing files
            if dt < twoDaysAgo:
                force = True
            logging.info("Detected old or missing datafile.")
            ret = -1
            while ret != 0:
                ret = dup.runUpdate(forceDownload=force)

                if ret == DailyUpdate.OKEY_DOKEY:
                    logging.info("Successfully updated files.")
                else:
                    if ret  == DailyUpdate.NOT_ALL_UPDATES_READY:
                        logging.info("Not all updates are ready.")
                    elif ret == DailyUpdate.ERROR_UPLOADING_TO_AWS:
                        logging.error(f"Error {ret} uploading to AWS.")
                    elif ret == DailyUpdate.ERROR_UPDATING_HISTORY_FILE:
                        logging.error(f"Error {ret} updating history file.")
                    elif ret == DailyUpdate.ERROR_MAKING_KEY_FILES:
                        logging.error(f"Error {ret} making key files.")
                    elif ret == DailyUpdate.ERROR_GETTING_DATA_ARRAYS:
                        logging.error(f"Error {ret} getting data arrays.")
                    elif ret == DailyUpdate.ERROR_DELETING_FILES:
                        logging.error(f"Error {ret} deleting files.")
                    elif ret == DailyUpdate.ERROR_CHECKING_TIMES:
                        logging.error(f"Error {ret} checking times.")
                    else:
                        logging.error(f"Error with unknown return value {ret}")

                    retries = retries + 1
                    if retries > 12:
                        #give up for the day
                        logging.warning("12 retries - giving up for the day.")
                        retries=0
                        force = True
                        pause.until(tonight)
                    else:
                        logging.info("Pausing 30 minutes before retrying.")
                        pause.minutes(30)

            logging.info("Restarting all dynos.")
            restartAllDynos()   # This should kill off this process when running in production
        else:
            logging.info("Detected no old or missing datafiles.")

        logging.info("Pausing until midnight.")
        pause.until(tonight)
