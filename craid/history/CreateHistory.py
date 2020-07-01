#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

#
# Load factions
#
import logging

import pandas as pd
from pandas import DataFrame

from craid.eddb.loader.strategy.DataLoader import DataLoader
# from memory_profiler import profile
from craid.eddb.loader.strategy.GithubLoader import LoadDataFromGithub


def create_history(loader: DataLoader) -> DataFrame:
    fName = loader.find_data_file('history.jsonl')
    dataframe = pd.read_json(fName, lines=True, compression='infer')
    dataframe.updated = pd.to_datetime(dataframe.updated, unit="ms")
    dataframe['updated'] = dataframe.updated.dt.round("D")  # truncate to day

    logging.info("Read %s lines of history data", str(dataframe.count()))
    return dataframe


if __name__ == '__main__':
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.getLogger().level = logging.DEBUG
    myLoader = LoadDataFromGithub(_forceWebDownload=False, useSmol=False)
    csa = create_history(myLoader)
