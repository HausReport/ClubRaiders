#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import time
from typing import Set

import requests
import ujson

import craid.eddb.loader.MakeKeyFiles as kf
from craid.edbgs.EdBgsFactionIds import EdBgsFactionIds

keys: Set[int] = kf.loadKeys('factions-of-interest-keys')

wait = 5

counter = 0
for facId in keys:
    # print( str(sysId))
    counter += 1

    if EdBgsFactionIds.hasId(facId):
        continue

    url = 'https://elitebgs.app/api/ebgs/v4/factions?eddbId=' + str(facId)
    r = requests.get(url, allow_redirects=True)  # , headers=headers)
    myDict = ujson.loads(r.content)
    docs = myDict['docs']
    if len(docs) < 1:
        time.sleep(wait)
        continue
    docZero = docs[0]
    # print( str( docZero))

    sName = docZero['name']
    bgsId = docZero['_id']
    edId = docZero['eddb_id']

    # newDict[edId] = bgsId

    print(f"\t{edId}:'{bgsId}',")
    # f = gzip.open(fName, 'wb')
    # f.write(r.content)
    # f.close()

    time.sleep(wait)

print(str(counter))
