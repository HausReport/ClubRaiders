import string
from typing import Dict

import pandas as pd

class PassThroughDict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
    def __missing__(self, key):
        return key

class Oracle:

    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self.dict: PassThroughDict[str,str] = PassThroughDict()
        self.dict['test'] = "test string"

        if df is None:
            return

        self.frame: pd.DataFrame = df
        frame = self.frame
        #
        #
        #
        dict['systems_active']          = "{:,}".format(frame['systemName'].count())
        dict['systems_active_pop']      = "{:,}".format(frame['population'].sum(axis=0))
        dict['systems_control']         = "{:,}".format(frame['control'].sum())
        dict['systems_control_perc']    = 1.0 * self.systems_control / self.systems_active

        #
        # Westernmost presence
        #
        idx = frame['x'].idxmin()  # westerly
        dict['west_fac_name']   = frame.at[idx, 'factionName']
        dict['west_sys_name']   = frame.at[idx, 'systemName']
        dict['west_sys_x']      = "{:,}".format(abs(int(frame.at[idx, 'x'])))

        #
        # Easternmost presence
        #
        idx = frame['x'].idxmax()  # westerly
        dict['east_fac_name']   = frame.at[idx, 'factionName']
        dict['east_sys_name']   = frame.at[idx, 'systemName']
        dict['east_sys_x']      = "{:,}".format(abs(int(frame.at[idx, 'x'])))

        #
        # Northernmost presence (z because E:D)
        #
        idx = frame['z'].idxmax()  # s'ly
        dict['north_fac_name']  = frame.at[idx, 'factionName']
        dict['north_sys_name']  = frame.at[idx, 'systemName']
        dict['north_sys_z']     = "{:,}".format(abs(int(frame.at[idx, 'z'])))

        #
        # Southernmost presence
        #
        idx = frame['z'].idxmin()  # n'ly
        dict['south_fac_name']  = frame.at[idx, 'factionName']
        dict['south_sys_name']  = frame.at[idx, 'systemName']
        dict['south_sys_z']     = "{:,}".format(abs(int(frame.at[idx, 'z'])))

        #
        # Zenithnmost presence (y because E:D)
        #
        idx = frame['y'].idxmax()  # u'ly
        dict['zenith_fac_name'] = frame.at[idx, 'factionName']
        dict['zenith_sys_name'] = frame.at[idx, 'systemName']
        dict['zenith_sys_y']    = "{:,}".format(abs(int(frame.at[idx, 'y'])))

        #
        # Nadirmost presence
        #
        idx = frame['z'].idxmin()  # d'ly
        dict['nadir_fac_name']  = frame.at[idx, 'factionName']
        dict['nadir_sys_name']  = frame.at[idx, 'systemName']
        dict['nadir_sys_y']     = "{:,}".format(abs(int(frame.at[idx, 'y'])))

        #
        # Population stats
        #
        dict['population_min'] = "{:,}".format(frame['population'].min())
        dict['population_max'] = "{:,}".format(frame['population'].max())
        dict['population_avg'] = "{:,}".format(frame['population'].mean())
        dict['population_sum'] = "{:,}".format(frame['population'].sum(axis=0))

        self.caxx = frame['population'].describe()
        dict['population_50p'] = "{:,}".format(self.caxx[5])
        dict['population_25p'] = "{:,}".format(self.caxx[4])

        #
        # Influence stats
        #
        dict['influence_min'] = "{0:,.2f}".format(frame['influence'].min())
        dict['influence_max'] = "{0:,.2f}".format(frame['influence'].max())
        dict['influence_avg'] = "{0:,.2f}".format(frame['influence'].mean())
        dict['influence_sum'] = "{0:,.2f}".format(frame['influence'].sum(axis=0))

        self.caxx = frame['influence'].describe()
        dict['influence_50p'] = "{0:,.2f}".format(self.caxx[5])
        dict['influence_25p'] = "{0:,.2f}".format(self.caxx[4])

        #
        #
        #
        uncontrolled = frame[~frame['control']]
        dict['uncontrol_influence_min'] = "{0:,.2f}".format(uncontrolled['influence'].min())
        dict['uncontrol_influence_max'] = "{0:,.2f}".format(uncontrolled['influence'].max())
        dict['uncontrol_influence_avg'] = "{0:,.2f}".format(uncontrolled['influence'].mean())
        dict['uncontrol_influence_sum'] = "{0:,.2f}".format(uncontrolled['influence'].sum(axis=0))

        gaxx = uncontrolled['influence'].describe()
        dict['uncontrol_influence_50p'] = "{0:,.2f}".format(gaxx[5])
        dict['uncontrol_influence_25p'] = "{0:,.2f}".format(gaxx[4])

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
        output = template.substitute(self.dict)
        return output


#         #boo: Dict[str, str] = {'buffy': 'travesty!'}
#         #boo = dict({'buffy': 'trade', 'angel': 'los angeles'})
#         temp = Template(str)
#         temp.
#         #return temp.render(lo )
#         return temp.render(locals())


if __name__ == '__main__':
    #myDict = dict({'girl': 'buffy', 'town': 'sunnydale'})
    msg = "[$test]: $girl lives in $town"
    seer: Oracle = Oracle(None)
    output = seer.template(msg)

    print(output)
