#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
#
#   SPDX-License-Identifier: BSD-3-Clause
import logging
import os
import tempfile

import requests

from craid.eddb.loader.strategy.DataLoader import DataLoader


class DirectoryLoader(DataLoader):

    def __init__(self, directory='foobar', useSmol=False):
        super().__init__()
        self.dir = os.path.join('D:','systems')
        self.useSmol = useSmol

    def getPrefix(self) -> str:
        if self.useSmol:
            return "smol-"
        return ""

    def getSuffix(self) -> str:
        return ".gz"

    def find_data_file(self, _shortName: str):
        shortName = self.getPrefix() + _shortName + self.getSuffix()
        fName = os.path.join(self.dir, shortName)
        if not os.path.exists(fName):
            logging.error("No data file: " + fName)
            assert False, "Couldn't get data file" + fName
            # return None
        else:
            logging.info("Found data file: %s", fName)
            # with open(fName, 'r') as handle:
            return fName

