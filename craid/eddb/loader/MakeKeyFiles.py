#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import os
import tempfile
from typing import Dict, Set

import ujson
import pickle

def dumpKeys(shortName: str, what: Set[int]):
    shortName = "keys-" + shortName + ".pkl"
    #
    # Get a good path
    #
    tmpDir = tempfile.gettempdir()
    # if not os.path.exists(fName):
    fName = os.path.join(tmpDir, shortName)

    #
    # dump away
    #
    with open(fName, 'wb') as fileOut:
        pickle.dump(what, fileOut)

def loadKeys(shortName: str):
    shortName = "keys-" + shortName + ".pkl"
    #
    # Get a good path
    #
    tmpDir = tempfile.gettempdir()
    # if not os.path.exists(fName):
    fName = os.path.join(tmpDir, shortName)

    if not os.path.exists(fName):
        return None

    #
    # dump away
    #
    with open(fName, 'rb') as fileOut:
        return pickle.load(fileOut)

if __name__ == '__main__':
    pass
