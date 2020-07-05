#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

#
# Load factions
#
import logging
from datetime import date, timedelta

import pandas as pd
from dateutil.relativedelta import relativedelta
from pandas import DataFrame

from craid.eddb.loader.strategy.AWSLoader import LoadDataFromAWS
from craid.eddb.loader.strategy.DataLoader import DataLoader
# from memory_profiler import profile
from craid.eddb.loader.strategy.GithubLoader import LoadDataFromGithub


class History(object):
    _instance = None
    _rawFrame = None
    _normalizedFrame = None

    def __new__(cls):
        if cls._instance is None:
             print('Creating the object')
             cls._instance = super(History, cls).__new__(cls)
             myLoader = LoadDataFromAWS(forceWebDownload=False, useSmol=False)
             cls._rawFrame = cls._getRawDataFrame(cls, myLoader)
             cls._normalizedFrame = cls._getNormalizedDataFrame(cls)

             # Put any initialization here.
        return cls._instance

    def getRawDataFrame(self) -> DataFrame:
        return self._rawFrame

    def _getRawDataFrame(self, loader: DataLoader) -> DataFrame:
        fName = loader.find_data_file('history.jsonl')
        dataframe = pd.read_json(fName, lines=True, compression='infer')
        dataframe.updated = pd.to_datetime(dataframe.updated, unit="ms")
        dataframe['updated'] = dataframe.updated.dt.round("D")  # truncate to day

        logging.info("Read %s lines of history data", str(dataframe.count()))
        return dataframe

    def getNormalizedDataFrame(self) -> DataFrame:
        return self._normalizedFrame

    def _getNormalizedDataFrame(self) -> DataFrame:
        target = pd.DataFrame()
        start_date = date(2018, 5, 15)
        daily_date = date(2020, 5, 30)
        end_date = date.today() + timedelta(days=1)  # date(2020, 6, 28)

        csa = self._rawFrame
        single_date = start_date
        while single_date <= end_date:
            theDate = single_date.strftime("%Y-%m-%d")
            dated = csa[csa['updated'] <= theDate]

            mostRecentDataOnDate = dated.loc[dated.groupby(['faction', 'system']).updated.idxmax()]
            target = target.append(mostRecentDataOnDate)
            if single_date < daily_date:
                single_date = single_date + relativedelta(months=1)
            else:
                single_date = single_date + relativedelta(days=1)

        return target

if __name__ == '__main__':
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.getLogger().level = logging.DEBUG
    #myLoader = LoadDataFromGithub(_forceWebDownload=False, useSmol=False)
    hist = History()
    csa = hist.getRawDataFrame()
    print(csa)
