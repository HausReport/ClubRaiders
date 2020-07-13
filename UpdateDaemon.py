#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import os
import requests
import pause

# 0. WAIT 5 MINUTES (LET WEB SERVER STARTUP & GET FILES.  AVOID RACE CONDITION.)
# 1. DO ALL FILES EXIST?
#    -- IF NOT, RELOAD
#       -- CONSIDER RETURN VALUE
#       -- RESTART SERVER IF GOOD
# 2. GET TIME OF OLDEST DATA FILE
# 3. IF IT'S TODAY
#    -- SLEEP UNTIL MIDNIGHT
#    -- GOTO 1.
# 4. IF IT'S NOT TODAY
#    -- 4A CHECK IF UPDATE IS READY
#       -- YES - RELOAD
#          -- CONSIDER RETURN VALUE
#          -- RESTART SERVER IF GOOD
#       -- NO
#          -- SLEEP 30 MIN
#          -- GO TO 4A
# 5. SLEEP UNTIL MIDNIGHT
#    -- GOTO 1.


def restartAllDynos():
    app_name = os.getenv('HEROKU_APP_NAME')
    uname = os.getenv('HEROKU_CLI_USER')
    tok = os.getenv('HEROKU_CLI_TOKEN')

    #print(app_name)
    #print(uname)
    #print(tok)

    auth = (uname,tok)
    url = f"https://api.heroku.com/apps/{app_name}/dynos"
    print( str(url))
    headers = { "Content-Type" : "application/json",
                "Accept"       : "application/vnd.heroku+json; version=3"}
    req = requests.delete(url=url, auth=auth, headers=headers)
    print( str(req))
    print( req.content)