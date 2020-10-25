#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
from pandas import DataFrame

from craid.eddb.faction.FactionInstance import FactionInstance
from craid.eddb.faction.Simulation import Simulation
from craid.eddb.faction.Strategy import Strategy
from craid.eddb.system.InhabitedSystem import InhabitedSystem


#
# Need:
#    start date
#    ally name
#    ally initial influence
#    target name
#

#
# Form
#    a simulation
#

#
#  Return
#    campaign graph
#    campaign strategy text
#    estimated days
#

class Campaign:
    sys: InhabitedSystem
    ally: FactionInstance
    target: FactionInstance
    strategy: Strategy
    sim: Simulation
    frame: DataFrame

    def __init__(self, aStrategy: Strategy, ally_inf: float, targ_inf: float, pop: int):
        self.pop = pop
        self.targ_inf = targ_inf
        self.ally_inf = ally_inf
        self.strategy = aStrategy
        self.sim = Simulation(aStrategy)
        self.frame = self.sim.getSimulationFrame(self.ally_inf, self.targ_inf, self.pop)

