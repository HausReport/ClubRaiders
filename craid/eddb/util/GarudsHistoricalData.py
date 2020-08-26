#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import logging
import os
import tempfile
from datetime import datetime
from typing import Tuple
from urllib import parse

import numpy as np
import pandas as pd
import ujson
from dateutil.relativedelta import relativedelta

from craid.club.regions.RegionFactory import RegionFactory
from craid.eddb.system.SystemXYZ import SystemXYZ

epoch = datetime.utcfromtimestamp(0)
endTime = datetime(2020, 5, 15)
startTime = datetime(2018, 5, 15)


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


def createShellScript(facOrig):
    facName = parse.quote(facOrig)
    curDate = startTime
    while curDate <= endTime:
        millis: int = unix_time_millis(curDate)
        curl: str = f' curl "https://elitebgs.app/api/ebgs/v4/factions?name={facName}&timemin={millis:.0f}" '
        process: str = '| jq ".docs" | grep -v "^\[" | grep -v "^\]" | jq ".history"  | grep -v "^\[" | grep -v "^\]" | sed "s/^  \}\,/  }/g" | jq -c "{system: .system, updated: .updated_at, influence: .influence}" >> '
        process += f'data/{facName}.jsonl'
        print(curl + process)
        print("sleep 10")
        curDate = curDate + relativedelta(months=1)


def fixRegions():
    tmpDir = tempfile.gettempdir()
    # if not os.path.exists(fName):
    fName = os.path.join(tmpDir, 'data', "foo" + ".jsonl")
    print(os.path.exists(fName))
    dataframe = pd.read_json(fName, lines=True, compression='infer')
    dataframe['region'] = dataframe['system'].apply(lambda x: getRegionNumber(x))
    # pd.set_option("display.max_rows", None, "display.max_columns", None)
    # print(dataframe)
    # for index, row in dataframe.iterrows():
    #    print(row.to_dict())
    with open(fName, 'w') as out_file:
        for index, row in dataframe.iterrows():
            print(row.to_dict())
            out_file.write(ujson.dumps(row.to_dict()))


def getRegionNumber(sysName):
    xyz: Tuple[int, int, int] = SystemXYZ.myDict.get(sysName)
    if xyz is None:
        return 0
    reg = RegionFactory.getRegion(xyz[0], xyz[1], xyz[2])
    if reg is None:
        return 0
    return reg.getNumber()


def massageJsonFile(facName):
    facEncoded = parse.quote(facName)

    tmpDir = tempfile.gettempdir()
    # if not os.path.exists(fName):
    fName = os.path.join(tmpDir, 'data', facEncoded + ".jsonl")
    print(os.path.exists(fName))
    dataframe = pd.read_json(fName, lines=True, compression='infer')
    # dataframe['faction'] = facName
    dataframe['updated'] = pd.to_datetime(dataframe['updated'], infer_datetime_format=True)
    dataframe['updated'] = dataframe.updated.dt.to_period('M').dt.to_timestamp()
    dataframe['influence'] = dataframe['influence'] * 100.0

    # foo = dataframe.loc[dataframe.groupby([['system', 'updated']]).influence.mean()]

    stage3 = dataframe[['system', 'updated', 'influence']].groupby(['system', 'updated']).influence.mean().reset_index()
    foo = stage3
    foo.insert(1, 'faction', facName)
    foo['control'] = False
    foo['region'] = 0
    foo['population'] = 0
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    foo['updated'] = foo['updated'].astype(np.int64) / int(1e6)
    print(foo)
    # foo.to_json(fName)
    with open(fName, 'w') as out_file:
        for index, row in foo.iterrows():
            # print(row.to_dict())
            out_file.write(ujson.dumps(row.to_dict()))


def convertPandasJsonToNormal(facName):
    facEncoded = parse.quote(facName)

    tmpDir = tempfile.gettempdir()
    # if not os.path.exists(fName):
    fName = os.path.join(tmpDir, 'data', facEncoded + ".jsonl")
    print(os.path.exists(fName))
    dataframe = pd.read_json(fName, compression='infer')

    for index, row in dataframe.iterrows():
        print(row.to_dict())

    with open(fName, 'w') as out_file:
        for index, row in dataframe.iterrows():
            # print(row.to_dict())
            out_file.write(ujson.dumps(row.to_dict()))


if __name__ == '__main__':
    # 'Sirius Corporation',
    # 'Bill Turner'
    # "Emperor's Dawn"
    # 'Aegis Defense',
    allFacs = ['Sirius Drives',
               #'Worster Insurance',
               'Abroin Universal PLC',
               'Hodack Prison Colony', 'Turner Research Group',
               'Sirius Luxury Transports', 'Aegis Core',
               'Aegis Research', 'Sirius Mining Merope',
               'Wiggins Development Trust', 'CQC Holdings', 'Sirius Hot2Cold',
               #"Benton's Gang",
               'Janus Incorporated', 'The Rockforth Corporation',
               'Sirius Mining', 'Sirius Atmospherics', 'Sirius Hyperspace',
               'Wreaken Construction', 'Gallant Investment Brokers',
               #'Bentonian Party',
               'Sirius Industrial',
               'The Greenventure Group', 'Sirius Power', 'Reynhardt IntelliSys',
               'Reyan BPS', "Namarii Emperor's Dawn", 'The Peterson Group',
               'Sirius Catering', 'Pleaides Resource Enterprise']
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.getLogger().level = logging.DEBUG
    fixRegions()
    # for fac in allFacs:
    #     massageJsonFile(fac)

    # createShellScript(fac)
    # doThirdThing("Sirius Corporation")
