#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

import pprint
import time
from typing import Dict, Set

import requests
import ujson

import craid.edbgs.EdBgsSystemIds
import craid.eddb.loader.MakeKeyFiles as kf

newDict: Dict[int, str] = {}
keys: Set[int] = kf.loadKeys('club-system-keys')
keyLen = len(keys)

for sysId in keys: #BountyHuntingInfo.bhDict.keys():

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

    time.sleep(5)

pprint.pprint(str(newDict))
