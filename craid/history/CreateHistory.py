#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

#
# Load factions
#
import gzip
import logging
from datetime import datetime
from typing import Dict, Set, List

import ujson
import pandas as pd
from pandas import DataFrame

from craid.eddb.faction.Faction import Faction
from craid.eddb.faction.FactionNameFilter import FactionNameFilter
from craid.eddb.loader.strategy.DataLoader import DataLoader


# from memory_profiler import profile
from craid.eddb.loader.strategy.EDDBLoader import LoadDataFromEDDB


def create_history(loader: DataLoader) -> DataFrame:
    dataframe = None

    system: List[str] = []
    faction: List[str] = []
    updated: List[datetime] = []
    influence: List[float] =[]
    control: List[bool] =[]
    region: List[int] = []
    population: List[int] = []

    nLines: int = 0
    fName = loader.find_data_file('history.jsonl')
    # with gzip.open(fName, 'rb') as f:
    #     for line in f:
    #         facLine = ujson.loads(line)
    #         nLines += 1
    #
    #         lCurFactionId = int(facLine['id'])
    #         sys = facLine['system']
    #         fac = facLine['faction']
    #         tmp = facLine['updated']
    #         upd = datetime.datetime.fromtimestamp(tmp)
    #         inf = facLine['influence']
    #         ctrl= facLine['control']
    #         reg = facLine['region']
    #         pop = facLine['population']
    #
    #         system.append(sys)
    #         faction.append(fac)
    #         updated.append(upd)
    #         influence.append(inf)
    #         control.append(ctrl)
    #         region.append(reg)
    #         population.append(pop)
    #
    # data = {
    #     'system'          : system,
    #     'faction'         : faction,
    #     'updated'         : updated,
    #     'influence'       : influence,
    #     'control'         : control,
    #     'region'          : region,
    #     'population'      : population
    # }
    dataframe = pd.read_json(fName, lines=True, compression='infer')

    #dataframe = pd.DataFrame(data=data)
    logging.info("Read %s lines of history data", str(dataframe.count()))
    return dataframe

if __name__ == '__main__':
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.getLogger().level = logging.DEBUG
    myLoader = LoadDataFromEDDB()
    csa = create_history(myLoader)