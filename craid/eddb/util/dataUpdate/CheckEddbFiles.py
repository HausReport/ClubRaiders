#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import logging
import os
import tempfile
import time
from datetime import datetime

import urllib3


def eddbUpdateReadyForTemp():
    tmpDir = tempfile.gettempdir()
    return eddbUpdateReady(tmpDir)


def eddbUpdateReady(localDirectory: str) -> bool:
    frags = ["stations.jsonl", "systems_populated.jsonl", "factions.jsonl"]
    for frag in frags:
        staFile = os.path.join(localDirectory, frag + ".gz")
        if not localFileIsOutOfDate(staFile, frag):
            return False

    return True  # False = all are current


# # NOTE: This is important - this does not tell us that all files are ready on the server
# def tempFilesAreOutOfDate():
#     tmpDir = tempfile.gettempdir()
#     return localFilesAreOutOfDate(tmpDir)
#
# # NOTE: This is important - this does not tell us that all files are ready on the server
# def localFilesAreOutOfDate(localDirectory: str) -> bool:
#     frags = [ "stations.jsonl", "systems_populated.jsonl", "factions.jsonl"]
#     for frag in frags:
#         staFile = os.path.join(localDirectory, frag + ".gz")
#         if localFileIsOutOfDate(staFile, frag):
#             return True  # True = at lease one is out of date
#
#     return False  # False = all are current


def localFileIsOutOfDate(fullLocalFilename: str, shortUrlFragment: str) -> bool:
    http = urllib3.PoolManager()
    url = "https://eddb.io/archive/v6/" + shortUrlFragment  # factions.jsonl"

    u = http.request('HEAD', url)
    meta = u.info()
    # print(meta)
    logging.info("Server Last Modified: " + str(meta.getheaders("Last-Modified")))

    gmTime = datetime.strptime(''.join(meta.getheaders("Last-Modified")),
                               "%a, %d %b %Y %X GMT").timetuple()
    # meta_modified = time.mktime(gmTime)

    # file = fullLocalFilename

    if not os.path.exists(fullLocalFilename):
        logging.info(f"Local file {fullLocalFilename} doesn't exist. ")
        return True

    localMod = time.gmtime(os.path.getmtime(fullLocalFilename))
    localStr = time.asctime(localMod)
    logging.info("Local Last Modified: " + localStr)
    # foo = meta_modified

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
    print(eddbUpdateReadyForTemp())
