import datetime
import gzip
import logging
import os
import tempfile
import time
import traceback
from pathlib import Path

import requests
# logic for caching at:
# https://stackoverflow.com/questions/29314287/python-requests-download-only-if-newer
import urllib3


class LoadDataFromEDDB:

    def __init__(self):
        pass

    # Hint: To enable compression, add the
    # Accept-Encoding: gzip, deflate, sdch entry to your request header.
    @staticmethod
    def download_file(shortName: str, targetDirectory: str) -> str:

        headers = {
            "User-Agent"     : "ClubRaiders Application",
            "Accept-Encoding": "gzip, deflate, sdch",
        }

        assert os.path.exists(targetDirectory), "data dir doesn't exist: [" + targetDirectory + "]"
        url = 'https://eddb.io/archive/v6/' + shortName
        fName = os.path.join(targetDirectory, shortName + ".gz")
        logging.info("2 - downloading [%s] to [%s] data file.", url, fName)
        r = requests.get(url, allow_redirects=True, headers=headers)
        gzip.open(fName, 'wb').write(r.content)
        return fName

    # @staticmethod
    # def load_data():
    #     if not os.path.exists('../data'):
    #         os.makedirs('data')
    #     if True is True:
    #         #
    #         # Gets the most recent data dumps from eddb.io
    #         #
    #         url = 'https://eddb.io/archive/v6/systems_populated.jsonl'
    #         r = requests.get(url, allow_redirects=True)
    #         open('../data/systems_populated.jsonl', 'wb').write(r.content)
    #
    #         # url = 'https://eddb.io/archive/v6/stations.jsonl'
    #         # r = requests.get(url, allow_redirects=True)
    #         # open('data/stations.jsonl', 'wb').write(r.content)
    #
    #         url = 'https://eddb.io/archive/v6/factions.jsonl'
    #         r = requests.get(url, allow_redirects=True)
    #         open('../data/factions.jsonl', 'wb').write(r.content)

    @staticmethod
    def find_data_file(_shortName: str):
        shortName = _shortName
        #
        # If data dir exists, use that one
        #
        #cur = Path("../data")
        #fName: str = os.path.join(cur.parent, "data", shortName)
        #fName: str = os.path.join(cur, shortName ) + ".gz"
        #logging.info("1- Checking for: " + fName)
        #traceback.print_stack()

        #
        # If not, check the temp dir
        #
        tmpDir = tempfile.gettempdir()
        #if not os.path.exists(fName):
        fName = os.path.join(tmpDir, shortName)  + ".gz"
        #logging.info("1- Checking for: " + fName)

        fileIsOutOfDate: bool = False

       # TODO: Need some extra logic here.  Like, if the day of the file is less than today, don't even check headers
       # fileIsOutOfDate = LoadDataFromEDDB.fileIsOutOfDate(fName, shortName)


        #
        # If neither exist, download the file to the temp dir
        #
        if fileIsOutOfDate or not os.path.exists(fName):
            logging.info("1- downloading to: " + fName)
            fName = LoadDataFromEDDB.download_file(shortName, tmpDir)
            #fName +=".gz"  added in download_file


        if not os.path.exists(fName):
            logging.error("No data file: " + fName)
            assert False, "Couldn't get data file" + fName
            return None
        else:
            logging.info("Found data file: %s", fName)
            #with open(fName, 'r') as handle:
            return fName



    @staticmethod
    def fileIsOutOfDate(fName: str, _shortName: str):
        http = urllib3.PoolManager()
        url = "https://eddb.io/archive/v6/" + _shortName #factions.jsonl"

        u = http.request('HEAD', url)
        meta = u.info()
        print(meta)
        print("Server Last Modified: " + str(meta.getheaders("Last-Modified")))

        meta_modifiedtime = time.mktime(datetime.datetime.strptime(
            ''.join(meta.getheaders("Last-Modified")), "%a, %d %b %Y %X GMT").timetuple())

        file = fName
        if os.path.getmtime(file) < meta_modifiedtime:  # change > to <
            print("CPU file is older than server file.")
            return True
        else:
            print("CPU file is NOT older than server file.")
            return False



if __name__ == '__main__':
    LoadDataFromEDDB.load_data()
