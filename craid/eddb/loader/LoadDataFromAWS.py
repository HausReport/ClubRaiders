#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

# logic for caching at:
# https://stackoverflow.com/questions/29314287/python-requests-download-only-if-newer
from craid.eddb.loader.WebDataLoader import WebDataLoader


class LoadDataFromAWS(WebDataLoader):

    def __init__(self):
        super().__init__()

    def getWebFilePrefix(self) -> str:
        return "http://erlaed.s3.amazonaws.com/"

#if __name__ == '__main__':
    #LoadDataFromEDDB.load_data()
