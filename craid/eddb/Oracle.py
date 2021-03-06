#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

import string

import humanize
import pandas as pd

from craid.eddb.util.PassThroughDict import PassThroughDict


def formatLargeNumber(num: int) -> str:
    return humanize.intword(num)


def formatLargeDiff(num: int) -> str:
    prefix: str
    if num < 0:
        # &uarr;
        prefix = "&darr; "
        num = abs(num)
    elif num == 0:
        return "-"
    else:
        prefix = "&uarr; "

    return prefix + humanize.intword(num)


def formatFloatDiff(num: float) -> str:
    prefix: str
    if num < 0.0:
        # &uarr;
        prefix = "&darr; "
        num = abs(num)
    elif num == 0.0:
        return "-"
    else:
        prefix = "&uarr; "

    return prefix + "{0:,.2f}".format(num)


class Oracle:

    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self.myDict: PassThroughDict[str, str] = PassThroughDict()
        self.myDict['test'] = "test string"
        self.df = df

        if df is None:
            return

        frame: pd.DataFrame = df
        numUniqueSystems = int(frame['systemName'].nunique())

        #
        # This was a little nuanced - was double-counting population of systems with two
        # club faction instances
        #
        self.myDict['number_of_factions'] = "{:,}".format(numUniqueSystems)
        n_by_sys = df.groupby("systemName")[["systemName", "population"]].agg(
            {'systemName': 'first', 'population': 'first'})
        total_pop = n_by_sys["population"].sum()
        total_systems = n_by_sys["systemName"].count()

        if total_systems==0:
            self.myDict['systems_active'] = 0
            self.myDict['systems_active_pop'] = 0
            self.myDict['systems_control'] = 0
            self.myDict['systems_control_perc'] = 0.0
            self.myDict['west_fac_name'] = ""
            self.myDict['west_sys_name'] = ""
            self.myDict['west_sys_x'] = 0
            self.myDict['east_fac_name'] = ""
            self.myDict['east_sys_name'] = ""
            self.myDict['east_sys_x'] = 0
            self.myDict['north_fac_name'] = ""
            self.myDict['north_sys_name'] = ""
            self.myDict['north_sys_z'] = 0
            self.myDict['south_fac_name'] = ""
            self.myDict['south_sys_name'] = ""
            self.myDict['south_sys_z'] = 0
            self.myDict['zenith_fac_name'] = ""
            self.myDict['zenith_sys_name'] = ""
            self.myDict['zenith_sys_y'] = 0
            self.myDict['nadir_fac_name'] = ""
            self.myDict['nadir_sys_name'] = ""
            self.myDict['nadir_sys_y'] = 0
            self.myDict['population_min'] = 0
            self.myDict['population_max'] = 0
            self.myDict['population_avg'] = 0
            self.myDict['population_sum'] = 0
            self.myDict['population_50p'] = 0
            self.myDict['population_25p'] = 0
            self.myDict['influence_min'] = 0
            self.myDict['influence_max'] = 0
            self.myDict['influence_avg'] = 0
            self.myDict['influence_sum'] = 0
            self.myDict['influence_50p'] = 0
            self.myDict['influence_25p'] = 0
            self.myDict['uncontrol_influence_min'] = 0
            self.myDict['uncontrol_influence_max'] = 0
            self.myDict['uncontrol_influence_avg'] = 0
            self.myDict['uncontrol_influence_sum'] = 0
            self.myDict['uncontrol_influence_50p'] = 0
            self.myDict['uncontrol_influence_25p'] = 0
            self.myDict['n_wars'] = 0
            self.myDict['n_elections'] = 0
            self.myDict['n_expansions'] = 0
            self.myDict['n_retreats'] = 0
            self.myDict['n_very_easy'] = 0
            self.myDict['diff_active_systems'] = 0 # formatLargeDiff(diff_active_systems)
            self.myDict['diff_population'] = 0 # formatLargeDiff(diff_population)
            self.myDict['diff_control_systems'] = 0 #formatLargeDiff(diff_control_systems)
            self.myDict['diff_avg_influence'] = 0 #formatFloatDiff(diff_avg_influence)
            self.myDict['diff_total_influence'] = 0 #formatFloatDiff(diff_total_influence)
            return

        #
        # General statistics
        #
        cur_active_systems = int(total_systems)
        cur_population = int(total_pop)
        cur_control_systems = int(frame['control'].sum())
        cur_avg_influence = float(frame['influence'].mean())
        cur_total_influence = float(frame['influence'].sum(axis=0))

        self.myDict['systems_active'] = "{:,}".format(cur_active_systems)
        self.myDict['systems_active_pop'] = formatLargeNumber(cur_population)
        self.myDict['systems_control'] = "{:,}".format(cur_control_systems)
        if cur_active_systems == 0.0:
            self.myDict['systems_control_perc'] = 0.0
        else:
            self.myDict['systems_control_perc'] = "{:,}".format((1.0 * cur_control_systems) / (1.0 * cur_active_systems))

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
        self.myDict['population_min'] = formatLargeNumber(frame['population'].min())
        self.myDict['population_max'] = formatLargeNumber(frame['population'].max())
        self.myDict['population_avg'] = formatLargeNumber(frame['population'].mean())
        self.myDict['population_sum'] = formatLargeNumber(frame['population'].sum(axis=0))

        self.caxx = frame['population'].describe()
        self.myDict['population_50p'] = formatLargeNumber(self.caxx[5])
        self.myDict['population_25p'] = formatLargeNumber(self.caxx[4])

        #
        # Influence stats
        #
        self.myDict['influence_min'] = "{0:,.2f}".format(frame['influence'].min())
        self.myDict['influence_max'] = "{0:,.2f}".format(frame['influence'].max())
        self.myDict['influence_avg'] = "{0:,.2f}".format(cur_avg_influence)
        self.myDict['influence_sum'] = "{0:,.2f}".format(cur_total_influence)

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
        self.myDict['n_expansions'] = df[df["vulnerable"].str.contains("xpans")]["factionName"].nunique()
        self.myDict['n_retreats'] = df[df["vulnerable"].str.contains("etre")]["systemName"].nunique()

        self.myDict['n_very_easy'] = df[df["difficulty"] <= 1.0]["systemName"].nunique()

        #
        #
        #
        # base_date = "2020-06-02 09:00"
        # base_active_systems = 172
        # base_population = 80566632766
        # base_control_systems = 40
        # base_avg_influence = 21.29
        # base_total_influence = 3960.53

        # adjusted for addition of Pleiades Resource Enterprise
        base_date = "2020-06-02 09:00"
        base_active_systems = 184
        base_population = 80566632766 + 6920000
        base_control_systems = 40 + 2
        base_total_influence = 3960.53 + 320
        base_avg_influence = base_total_influence/base_active_systems

        diff_active_systems = cur_active_systems - base_active_systems
        diff_population = cur_population - base_population
        diff_control_systems = cur_control_systems - base_control_systems
        diff_avg_influence = cur_avg_influence - base_avg_influence
        diff_total_influence = cur_total_influence - base_total_influence

        self.myDict['diff_active_systems'] = formatLargeDiff(diff_active_systems)
        self.myDict['diff_population'] = formatLargeDiff(diff_population)
        self.myDict['diff_control_systems'] = formatLargeDiff(diff_control_systems)
        self.myDict['diff_avg_influence'] = formatFloatDiff(diff_avg_influence)
        self.myDict['diff_total_influence'] = formatFloatDiff(diff_total_influence)

        #
        #
        #

    def getFactionTable(self):
        n_by_sys = self.df.groupby("factionName")[["factionName", "systemName", "population", "influence"]].agg(
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
