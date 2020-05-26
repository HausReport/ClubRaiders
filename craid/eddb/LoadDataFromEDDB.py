import logging
import os
import tempfile
from pathlib import Path

import requests


# logic for caching at:
# https://stackoverflow.com/questions/29314287/python-requests-download-only-if-newer

class LoadDataFromEDDB:

    def __init__(self):
        pass

    @staticmethod
    def download_file(shortName: str, targetDirectory: str) -> str:
        assert os.path.exists(targetDirectory), "data dir doesn't exist: [" + targetDirectory + "]"
        url = 'https://eddb.io/archive/v6/' + shortName
        logging.info("downloading data file: %s", url)
        r = requests.get(url, allow_redirects=True)
        # tmpDir = tempfile.gettempdir()
        fName = os.path.join(targetDirectory, shortName)
        open(fName, 'wb').write(r.content)
        return fName

    @staticmethod
    def load_data():
        if not os.path.exists('../data'):
            os.makedirs('data')
        if True is True:
            #
            # Gets the most recent data dumps from eddb.io
            #
            url = 'https://eddb.io/archive/v6/systems_populated.jsonl'
            r = requests.get(url, allow_redirects=True)
            open('../data/systems_populated.jsonl', 'wb').write(r.content)

            # url = 'https://eddb.io/archive/v6/stations.jsonl'
            # r = requests.get(url, allow_redirects=True)
            # open('data/stations.jsonl', 'wb').write(r.content)

            url = 'https://eddb.io/archive/v6/factions.jsonl'
            r = requests.get(url, allow_redirects=True)
            open('../data/factions.jsonl', 'wb').write(r.content)

    @staticmethod
    def find_data_file(shortName: str):
        #
        # If data dir exists, use that one
        #
        cur = Path("../data")
        fName: str = os.path.join(cur.parent, "data", shortName)
        logging.info("Checking for: " + fName)


        #
        # If not, check the temp dir
        #
        if not os.path.exists(fName):
            tmpDir = tempfile.gettempdir()
            fName = os.path.join(tmpDir, shortName)
            logging.info("Checking for: " + fName)

        #
        # If neither exist, download the file to the temp dir
        #
        if not os.path.exists(fName):
            fName = LoadDataFromEDDB.download_file(shortName, tmpDir)
            logging.info("Checking for: " + fName)

        if not os.path.exists(fName):
            logging.error("No data file: " + fName)
            assert False, "Couldn't get data file" + fName
        else:
            logging.info("found data file: %s", fName)
            with open(fName, 'r') as handle:
                yield handle



if __name__ == '__main__':
    LoadDataFromEDDB.load_data()
