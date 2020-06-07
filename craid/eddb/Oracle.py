#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

import string

import pandas as pd

from craid.eddb.PassThroughDict import PassThroughDict


class Oracle:

    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self.myDict: PassThroughDict[str, str] = PassThroughDict()
        self.myDict['test'] = "test string"
        self.df = df
        # &uarr; &darr;

        if df is None:
            return

        base_date = "02/06/2020 09:00"
        base_active_systems = 186
        base_population = 95479284266
        base_control_systems = 40
        base_avg_influence = 21.29
        base_total_influence = 3960.53

        frame: pd.DataFrame = df

        #
        #
        #
        self.myDict['number_of_factions'] = "{:,}".format(int(frame['systemName'].nunique()))

        #
        # General statistics
        #
        self.myDict['systems_active'] = "{:,}".format(int(frame['systemName'].count()))
        self.myDict['systems_active_pop'] = "{:,}".format(frame['population'].sum(axis=0))
        self.myDict['systems_control'] = "{:,}".format(frame['control'].sum())
        self.myDict['systems_control_perc'] = "{:,}".format(
            1.0 * frame['control'].sum() / int(frame['systemName'].count()))

        #
        # Westernmost presence
        #
        idx = frame['x'].idxmin()  # westerly
        self.myDict['west_fac_name'] = frame.at[idx, 'factionName']
        self.myDict['west_sys_name'] = frame.at[idx, 'systemName']
        self.myDict['west_sys_x'] = "{:,}".format(abs(int(frame.at[idx, 'x'])))

        #
        # Easternmost presence
        #
        idx = frame['x'].idxmax()  # westerly
        self.myDict['east_fac_name'] = frame.at[idx, 'factionName']
        self.myDict['east_sys_name'] = frame.at[idx, 'systemName']
        self.myDict['east_sys_x'] = "{:,}".format(abs(int(frame.at[idx, 'x'])))

        #
        # Northernmost presence (z because E:D)
        #
        idx = frame['z'].idxmax()  # s'ly
        self.myDict['north_fac_name'] = frame.at[idx, 'factionName']
        self.myDict['north_sys_name'] = frame.at[idx, 'systemName']
        self.myDict['north_sys_z'] = "{:,}".format(abs(int(frame.at[idx, 'z'])))

        #
        # Southernmost presence
        #
        idx = frame['z'].idxmin()  # n'ly
        self.myDict['south_fac_name'] = frame.at[idx, 'factionName']
        self.myDict['south_sys_name'] = frame.at[idx, 'systemName']
        self.myDict['south_sys_z'] = "{:,}".format(abs(int(frame.at[idx, 'z'])))

        #
        # Zenithnmost presence (y because E:D)
        #
        idx = frame['y'].idxmax()  # u'ly
        self.myDict['zenith_fac_name'] = frame.at[idx, 'factionName']
        self.myDict['zenith_sys_name'] = frame.at[idx, 'systemName']
        self.myDict['zenith_sys_y'] = "{:,}".format(abs(int(frame.at[idx, 'y'])))

        #
        # Nadirmost presence
        #
        idx = frame['z'].idxmin()  # d'ly
        self.myDict['nadir_fac_name'] = frame.at[idx, 'factionName']
        self.myDict['nadir_sys_name'] = frame.at[idx, 'systemName']
        self.myDict['nadir_sys_y'] = "{:,}".format(abs(int(frame.at[idx, 'y'])))

        #
        # Population stats
        #
        self.myDict['population_min'] = "{:,}".format(frame['population'].min())
        self.myDict['population_max'] = "{:,}".format(frame['population'].max())
        self.myDict['population_avg'] = "{:,}".format(frame['population'].mean())
        self.myDict['population_sum'] = "{:,}".format(frame['population'].sum(axis=0))

        self.caxx = frame['population'].describe()
        self.myDict['population_50p'] = "{:,}".format(self.caxx[5])
        self.myDict['population_25p'] = "{:,}".format(self.caxx[4])

        #
        # Influence stats
        #
        self.myDict['influence_min'] = "{0:,.2f}".format(frame['influence'].min())
        self.myDict['influence_max'] = "{0:,.2f}".format(frame['influence'].max())
        self.myDict['influence_avg'] = "{0:,.2f}".format(frame['influence'].mean())
        self.myDict['influence_sum'] = "{0:,.2f}".format(frame['influence'].sum(axis=0))

        self.caxx = frame['influence'].describe()
        self.myDict['influence_50p'] = "{0:,.2f}".format(self.caxx[5])
        self.myDict['influence_25p'] = "{0:,.2f}".format(self.caxx[4])

        #
        #
        #
        uncontrolled = frame[~frame['control']]
        self.myDict['uncontrol_influence_min'] = "{0:,.2f}".format(uncontrolled['influence'].min())
        self.myDict['uncontrol_influence_max'] = "{0:,.2f}".format(uncontrolled['influence'].max())
        self.myDict['uncontrol_influence_avg'] = "{0:,.2f}".format(uncontrolled['influence'].mean())
        self.myDict['uncontrol_influence_sum'] = "{0:,.2f}".format(uncontrolled['influence'].sum(axis=0))

        gaxx = uncontrolled['influence'].describe()
        self.myDict['uncontrol_influence_50p'] = "{0:,.2f}".format(gaxx[5])
        self.myDict['uncontrol_influence_25p'] = "{0:,.2f}".format(gaxx[4])

        #
        #
        #
        self.myDict['n_wars'] = df[df["vulnerable"].str.contains("War")]["systemName"].nunique()
        self.myDict['n_elections'] = df[df["vulnerable"].str.contains("lect")]["systemName"].nunique()
        self.myDict['n_expansions'] = df[df["vulnerable"].str.contains("xpans")]["systemName"].nunique()
        self.myDict['n_retreats'] = df[df["vulnerable"].str.contains("etre")]["systemName"].nunique()

        self.myDict['n_very_easy'] =  df[df["difficulty"] <= 1.0]["systemName"].nunique()

        #
        #
        #

        #
        #
        #

    def getFactionTable(self):
        n_by_sys = self.df.groupby("factionName")["factionName", "systemName", "population", "influence"].agg(
            {'factionName': 'first', 'systemName': 'count', 'population': 'sum', 'influence': 'sum'})
        n_by_sys.columns = ['Faction Name', 'Systems', 'Population', 'Total Influence']
        import dash_table
        return dash_table.DataTable(
            id='faction_table',
            columns=[{"name": i, "id": i} for i in n_by_sys.columns],
            data=n_by_sys.to_dict('records'),
        )

    def template(self, theMsg: str) -> str:
        template = string.Template(theMsg)
        ret = template.substitute(self.myDict)
        return ret
