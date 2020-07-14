#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause






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
import logging

from DailyUpdate import DailyUpdate

if __name__ == '__main__':
    #
    # Fire up logger
    #
    logging.basicConfig(
        format='DMN - %(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    dup = DailyUpdate()
    dup.run()


