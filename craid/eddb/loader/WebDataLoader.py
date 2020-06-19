#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import logging
import os
import tempfile

import requests

from craid.eddb.loader.DataLoader import DataLoader


class WebDataLoader(DataLoader):

    def __init__(self):
        super().__init__()

    def getPrefix(self) -> str:
        return "smol-"

    def find_data_file(self, _shortName: str, forceDownload=False):
        shortName = self.getPrefix() + _shortName
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
            # fileIsOutOfDate = LoadDataFromEDDB.fileIsOutOfDate(fName, shortName)

        #
        # If neither exist, download the file to the temp dir
        #
        if fileIsOutOfDate or not os.path.exists(fName):
            logging.info("1- downloading to: " + fName)
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

    def fileIsOutOfDate(self, fName: str, _shortName: str):
        return False
        # TODO: THINK THIS THROUGH
        # http = urllib3.PoolManager()
        # url = "https://eddb.io/archive/v6/" + _shortName  # factions.jsonl"
        #
        # u = http.request('HEAD', url)
        # meta = u.info()
        # print(meta)
        # print("Server Last Modified: " + str(meta.getheaders("Last-Modified")))
        #
        # meta_modifiedtime = time.mktime(datetime.datetime.strptime(
        #     ''.join(meta.getheaders("Last-Modified")), "%a, %d %b %Y %X GMT").timetuple())
        #
        # file = fName
        # if os.path.getmtime(file) < meta_modifiedtime:  # change > to <
        #     print("CPU file is older than server file.")
        #     return True
        # else:
        #     print("CPU file is NOT older than server file.")
        #     return False

    def download_file(self, shortName: str, targetDirectory: str) -> str:

        headers = {
            "User-Agent"     : "ClubRaiders Application",
            "Accept-Encoding": "gzip, deflate, sdch",
        }

        assert os.path.exists(targetDirectory), "data dir doesn't exist: [" + targetDirectory + "]"

        prefix = self.getWebFilePrefix()
        url = prefix + shortName + ".gz"

        fName = os.path.join(targetDirectory, shortName + ".gz")
        logging.info("2 - downloading [%s] to [%s] data file.", url, fName)
        r = requests.get(url, allow_redirects=True, headers=headers)
        f = open(fName, 'wb')
        f.write(r.content)
        f.close()

        return fName
