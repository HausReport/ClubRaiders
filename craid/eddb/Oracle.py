#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

import string

import pandas as pd

from PassThroughDict import PassThroughDict


class Oracle:

    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self.myDict: PassThroughDict[str, str] = PassThroughDict()
        self.myDict['test'] = "test string"

        if df is None:
            return

        frame: pd.DataFrame = df
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

        #
        #
        #

        #
        #
        #

    def template(self, msg: str) -> str:
        template = string.Template(msg)
        output = template.substitute(self.myDict)
        return output


#         #boo: Dict[str, str] = {'buffy': 'travesty!'}
#         #boo = dict({'buffy': 'trade', 'angel': 'los angeles'})
#         temp = Template(str)
#         temp.
#         #return temp.render(lo )
#         return temp.render(locals())


if __name__ == '__main__':
    # myDict = dict({'girl': 'buffy', 'town': 'sunnydale'})
    msg = "[$test]: $girl lives in $town"
    seer: Oracle = Oracle(None)
    output = seer.template(msg)

    print(output)
