#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
#
#   SPDX-License-Identifier: BSD-3-Clause

import gzip
import logging
import os
import tempfile

import requests

from craid.eddb.loader.strategy.DataLoader import DataLoader


# logic for caching at:
# https://stackoverflow.com/questions/29314287/python-requests-download-only-if-newer


class LoadDataFromEDDB(DataLoader):

    def __init__(self):
        super().__init__()

    def getPrefix(self) -> str:
        return ""

    # Hint: To enable compression, add the
    # Accept-Encoding: gzip, deflate, sdch entry to your request header.
    def download_file(self, shortName: str, targetDirectory: str) -> str:

        headers = {
            "User-Agent"     : "ClubRaiders Application",
            "Accept-Encoding": "gzip, deflate, sdch",
        }

        assert os.path.exists(targetDirectory), "data dir doesn't exist: [" + targetDirectory + "]"
        url = 'https://eddb.io/archive/v6/' + shortName
        fName = os.path.join(targetDirectory, shortName + ".gz")
        logging.info("2 - downloading [%s] to [%s] data file.", url, fName)
        r = requests.get(url, allow_redirects=True, headers=headers)
        f = gzip.open(fName, 'wb')
        f.write(r.content)
        f.close()

        return fName

    def find_data_file(self, _shortName: str, forceDownload=False):
        shortName = _shortName
        #
        # If data dir exists, use that one
        #
        # cur = Path("../data")
        # fName: str = os.path.join(cur.parent, "data", shortName)
        # fName: str = os.path.join(cur, shortName ) + ".gz"
        # logging.info("1- Checking for: " + fName)
        # traceback.print_stack()

        #
        # If not, check the temp dir
        #
        tmpDir = tempfile.gettempdir()
        # if not os.path.exists(fName):
        fName = os.path.join(tmpDir, shortName) + ".gz"
        # logging.info("1- Checking for: " + fName)

        fileIsOutOfDate: bool = False
        if not forceDownload:
            pass
            # TODO: Need some extra logic here.  Like, if the day of the file is less than today, don't even check headers
            # localFileIsOutOfDate = LoadDataFromEDDB.localFileIsOutOfDate(fName, shortName)

        #
        # If neither exist, download the file to the temp dir
        #
        if forceDownload or fileIsOutOfDate or not os.path.exists(fName):
            #logging.info("1- downloading to: " + fName)
            fName = self.download_file(shortName, tmpDir)
            # fName +=".gz"  added in download_file

        if not os.path.exists(fName):
            logging.error("No data file: " + fName)
            assert False, "Couldn't get data file" + fName
            # return None
        else:
            logging.info("Found data file: %s", fName)
            # with open(fName, 'r') as handle:
            return fName

# if __name__ == '__main__':
# LoadDataFromEDDB.load_data()
