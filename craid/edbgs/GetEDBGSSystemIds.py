#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
#
#   SPDX-License-Identifier: BSD-3-Clause

import time
from typing import Dict
import pprint

import requests
import ujson

from craid.eddb.BountyHuntingInfo import BountyHuntingInfo
import craid.edbgs.EdBgsSystemIds

newDict: Dict[int, str] = {}


for sysId in BountyHuntingInfo.bhDict.keys():

    if sysId in craid.edbgs.EdBgsSystemIds.EdBgsSystemIds.myDict:
        continue

    # assert os.path.exists(targetDirectory), "data dir doesn't exist: [" + targetDirectory + "]"
    # fName = os.path.join(targetDirectory, shortName + ".gz")
    # logging.info("2 - downloading [%s] to [%s] data file.", url, fName)

    url = 'https://elitebgs.app/api/ebgs/v4/systems?eddbId=' + str(sysId)
    r = requests.get(url, allow_redirects=True)  # , headers=headers)
    myDict = ujson.loads(r.content)
    docs = myDict['docs']
    if len(docs) < 1:
        continue
    docZero = docs[0]
    # print( str( docZero))

    sName = docZero['name']
    bgsId = docZero['_id']
    edId = docZero['eddb_id']

    newDict[edId] = bgsId

    print(f"\t{edId}:'{bgsId}',")
    # f = gzip.open(fName, 'wb')
    # f.write(r.content)
    # f.close()

    time.sleep(10)

pprint.pprint(str(newDict))

