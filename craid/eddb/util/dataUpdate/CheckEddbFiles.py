#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import logging
import os
import tempfile
from datetime import datetime
import time
import urllib3

def tempFilesAreOutOfDate():
    tmpDir = tempfile.gettempdir()
    return localFilesAreOutOfDate(tmpDir)

def localFilesAreOutOfDate(localDirectory: str) -> bool:
    sysFrag = "systems_populated.jsonl"
    sysFile = os.path.join(localDirectory, sysFrag + ".gz")
    if localFileIsOutOfDate(sysFile, sysFrag):
        return True

    facFrag = "factions.jsonl"
    facFile = os.path.join(localDirectory, facFrag + ".gz")
    if localFileIsOutOfDate(facFile, facFrag):
        return True

    staFrag = "stations.jsonl"
    staFile = os.path.join(localDirectory, staFrag + ".gz")
    if localFileIsOutOfDate(staFile, staFrag):
        return True

    return False


def localFileIsOutOfDate(fullLocalFilename: str, shortUrlFragment: str) -> bool:
    http = urllib3.PoolManager()
    url = "https://eddb.io/archive/v6/" + shortUrlFragment  # factions.jsonl"

    u = http.request('HEAD', url)
    meta = u.info()
    # print(meta)
    print("Server Last Modified: " + str(meta.getheaders("Last-Modified")))

    gmTime =datetime.strptime( ''.join(meta.getheaders("Last-Modified")),
                           "%a, %d %b %Y %X GMT").timetuple()
    meta_modified = time.mktime( gmTime )

    #file = fullLocalFilename

    if not os.path.exists(fullLocalFilename):
        return True

    localMod = time.gmtime(os.path.getmtime(fullLocalFilename))
    localStr = time.asctime(localMod)
    print("Local Last Modified: " + localStr)
    foo = meta_modified

    if localMod < gmTime:  # change > to <
        print("Local file is older than EDDB server file.")
        return True
    else:
        print("Local file is NOT older than EDDB server file.")
        return False

if __name__ == '__main__':
    #
    # Fire up logger
    #
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.getLogger().level = logging.DEBUG
    print(tempFilesAreOutOfDate())