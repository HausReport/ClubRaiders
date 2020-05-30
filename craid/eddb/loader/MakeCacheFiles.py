#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import os
import tempfile
from typing import Dict

import ujson

from craid.eddb.loader.DataProducer import getDataArrays


def dump(shortName: str, what):
    #
    # Get a good path
    #
    tmpDir = tempfile.gettempdir()
    # if not os.path.exists(fName):
    fName = os.path.join(tmpDir, shortName) # + ".gz"

    #
    # dump away
    #
    with open(fName, 'w') as fileOut:
        ujson.dump(what, fileOut)


if __name__ == '__main__':
    # clubFactionIdToInfo,
    # 'all_systems_dict': all_systems_dict,
    # 'allClubSystemInstances': allClubSystemInstances,
    # 'systemNameToXYZ': systemNameToXYZ,
    # 'sysIdFacIdToFactionInstance': sysIdFacIdToFactionInstance,
    # 'playerFactionNameToSystemName': playerFactionNameToSystemName,  # used in dashboard for 2nd dropdown
    # }

    ## TODO: it would be great to serialize these dicts but not as easy as I'd hoped
    ## https://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
    out : Dict = getDataArrays()
    allClubSystemInstances = out.get('allClubSystemInstances')
    dump('allClubSystemInstances',allClubSystemInstances)
