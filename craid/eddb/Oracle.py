from typing import Dict

import pandas as pd

class Oracle:

    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self.test = "fantastic test!"

        if df == None:
            return
        self.frame: pd.DataFrame = df
        frame = self.frame
        #
        #
        #
        self.systems_active = "{:,}".format(frame['systemName'].count())
        self.systems_active_pop = "{:,}".format(frame['population'].sum(axis=0))
        self.systems_control = "{:,}".format(frame['control'].sum())
        self.systems_control_perc = 1.0 * self.systems_control / self.systems_active

        #
        # Westernmost presence
        #
        idx = frame['x'].idxmin()  # westerly
        self.west_fac_name = frame.at[idx, 'factionName']
        self.west_sys_name = frame.at[idx, 'systemName']
        self.west_sys_x = "{:,}".format(abs(int(frame.at[idx, 'x'])))

        #
        # Easternmost presence
        #
        idx = frame['x'].idxmax()  # westerly
        self.east_fac_name = frame.at[idx, 'factionName']
        self.east_sys_name = frame.at[idx, 'systemName']
        self.east_sys_x = "{:,}".format(abs(int(frame.at[idx, 'x'])))

        #
        # Northernmost presence (z because E:D)
        #
        idx = frame['z'].idxmax()  # s'ly
        self.north_fac_name = frame.at[idx, 'factionName']
        self.north_sys_name = frame.at[idx, 'systemName']
        self.north_sys_z = "{:,}".format(abs(int(frame.at[idx, 'z'])))

        #
        # Southernmost presence
        #
        idx = frame['z'].idxmin()  # n'ly
        self.south_fac_name = frame.at[idx, 'factionName']
        self.south_sys_name = frame.at[idx, 'systemName']
        self.south_sys_z = "{:,}".format(abs(int(frame.at[idx, 'z'])))

        #
        # Zenithnmost presence (y because E:D)
        #
        idx = frame['y'].idxmax()  # u'ly
        self.zenith_fac_name = frame.at[idx, 'factionName']
        self.zenith_sys_name = frame.at[idx, 'systemName']
        self.zenith_sys_y = "{:,}".format(abs(int(frame.at[idx, 'y'])))

        #
        # Nadirmost presence
        #
        idx = frame['z'].idxmin()  # d'ly
        self.nadir_fac_name = frame.at[idx, 'factionName']
        self.nadir_sys_name = frame.at[idx, 'systemName']
        self.nadir_sys_y = "{:,}".format(abs(int(frame.at[idx, 'y'])))

        #
        # Population stats
        #
        self.population_min = "{:,}".format(frame['population'].min())
        self.population_max = "{:,}".format(frame['population'].max())
        self.population_avg = "{:,}".format(frame['population'].mean())
        self.population_sum = "{:,}".format(frame['population'].sum(axis=0))

        self.caxx = frame['population'].describe()
        self.population_50p = "{:,}".format(self.caxx[5])
        self.population_25p = "{:,}".format(self.caxx[4])

        #
        # Influence stats
        #
        self.influence_min = frame['influence'].min()
        self.influence_max = frame['influence'].max()
        self.influence_avg = frame['influence'].mean()
        self.influence_sum = frame['influence'].sum(axis=0)

        self.caxx = frame['influence'].describe()
        self.influence_50p = self.caxx[5]
        self.influence_25p = self.caxx[4]

        #
        #
        #
        uncontrolled = frame[~frame['control']]
        self.uncontrol_influence_min = uncontrolled['influence'].min()
        self.uncontrol_influence_max = uncontrolled['influence'].max()
        self.uncontrol_influence_avg = uncontrolled['influence'].mean()
        self.uncontrol_influence_sum = uncontrolled['influence'].sum(axis=0)

        gaxx = uncontrolled['influence'].describe()
        self.uncontrol_influence_50p = gaxx[5]
        self.uncontrol_influence_25p = gaxx[4]

        #
        #
        #

        #
        #
        #

        #
        #
        #
    boo = dict({'buffy': 'trade', 'angel': 'los angeles'})

    def template(self, template: str) -> str:
        pass
#         #boo: Dict[str, str] = {'buffy': 'travesty!'}
#         #boo = dict({'buffy': 'trade', 'angel': 'los angeles'})
#         temp = Template(str)
#         temp.
#         #return temp.render(lo )
#         return temp.render(locals())
#
#
# if __name__ == '__main__':
#     boo = dict({'buffy': 'trade', 'angel': 'los angeles'})
#     #boo: Dict[str, str] = {'buffy':'travesty!'}
#     seer: Oracle = Oracle(None)
#     print(seer.template("This is a @boo.buffy"))
