#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

#
# Load factions
#
import logging
from datetime import date, timedelta
import datetime as dt

import pandas as pd
from dateutil.relativedelta import relativedelta
from pandas import DataFrame

from craid.eddb.loader.strategy.AWSLoader import LoadDataFromAWS
from craid.eddb.loader.strategy.DataLoader import DataLoader


# from memory_profiler import profile


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

        # renamed systems
        dataframe.drop(dataframe[dataframe.system == "Pleiades Sector IR-W d1-55"].index, inplace=True)

        logging.info("Read %s lines of history data", str(dataframe.count()))
        return dataframe

    def getNormalizedDataFrame(self) -> DataFrame:
        return self._normalizedFrame

    def _getNormalizedDataFrame(self) -> DataFrame:
        target = pd.DataFrame()
        start_date = date(2018, 5, 15)
        daily_date = date(2020, 6, 1)
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

    def getHistoryForFacationAndSystem(self, fac: str, sys: str):
        # hist = History()
        tmp = self.getRawDataFrame()
        return tmp[(tmp['faction'] == fac) & (tmp['system'] == sys)]

    def getHistoryForFacation(self, fac: str):
        # hist = History()
        tmp = self.getRawDataFrame()
        return tmp[(tmp['faction'] == fac)]

    def getHistoryForSystem(self, sys: str):
        # hist = History()
        tmp = self.getRawDataFrame()
        return tmp[tmp['system'] == sys]

    def getHistoryForRegion(self, reg: int):
        # hist = History()
        tmp = self.getRawDataFrame()
        return tmp[tmp['region'] == reg]

    def getLatestInfluences(self):
        # hist = History()
        csa = self.getRawDataFrame()
        stage1 = csa.loc[csa.groupby(['faction', 'system']).updated.idxmax()]
        return stage1.sort_values(['faction', 'system'])

    def getLatestInfluenceBefore(self, dateStr: str):
        # hist = History()
        csa = self.getRawDataFrame()
        csa = csa[csa['updated'] <= dateStr]
        # csa = csa[ csa['updated'<dateStr]]
        stage1 = csa.loc[csa.groupby(['faction', 'system']).updated.idxmax()]
        return stage1.sort_values(['faction', 'system'])

    def getClubInfluenceOnDate(self, dateStr: str):
        # reg = csa[ csa['region']== 1]
        # hist = History()
        csa = self.getLatestInfluenceBefore(dateStr)
        stage1 = csa.loc[csa.groupby(['faction', 'system']).updated.idxmax()]
        stage3 = stage1[['system', 'faction', 'influence']].groupby('faction').influence.sum().reset_index()
        return stage3.influence.sum()

    def getHistoryByWeek(self):
        # hist = History()
        tmp = self.getRawDataFrame().copy()
        tmp['week'] = pd.to_datetime(tmp.updated).dt.to_period('W').dt.to_timestamp()
        tmp = tmp.loc[tmp.groupby(['faction', 'system', 'week']).updated.idxmax()]
        tmp.updated = tmp.week
        return tmp.sort_values(['faction', 'system'])

    def getHistoryByMonth(self):
        # hist = History()
        tmp = self.getRawDataFrame().copy()
        tmp['month'] = pd.to_datetime(tmp.updated).dt.to_period('M').dt.to_timestamp()
        tmp = tmp.loc[tmp.groupby(['faction', 'system', 'month']).updated.idxmax()]
        return tmp.sort_values(['faction', 'system'])

    def getSmallFrame(self, dateStr: str, faction, system):
        date_time_str = dateStr + " 00:00:00"  # '2020-10-05 00:00:00'
        date_time_obj = dt.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

        hist = History()
        df2 = self.getHistoryForFacationAndSystem(faction, system).copy()

        #
        # Convert to daily and clean
        #
        df2['updated'] = pd.to_datetime(df2.updated, unit='ms')
        df2['updated'] = pd.to_datetime(df2.updated).dt.to_period('D').dt.to_timestamp()
        df2 = df2[df2['updated'] >= date_time_obj]
        df2 = df2.drop_duplicates(subset=['system', 'faction', 'updated'])
        return df2.sort_values(['updated'])


if __name__ == '__main__':
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.getLogger().level = logging.DEBUG
    # myLoader = LoadDataFromGithub(_forceWebDownload=False, useSmol=False)
    hist = History()
    csa = hist.getRawDataFrame()
    print(csa)
