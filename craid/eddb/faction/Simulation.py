#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
from typing import List

import pandas as pd
import plotly.graph_objects as go
import humanize
import datetime as dt

from craid.eddb.faction.Strategy import Strategy


class Simulation:

    def __init__(self, strat: Strategy):
        self.strat = strat

    def getSimulationFrame(self, ally_inf: float, targ_inf: float, pop: int):
        # nDays = daysToRetreat(inf, pop)

        dayNum = []
        ally_infs = []
        targ_infs = []
        ally_note = []
        targ_note = []

        day = 0

        dayNum.append(day)
        targ_infs.append(targ_inf)
        ally_infs.append(ally_inf)
        targ_note.append("")
        ally_note.append("")

        targetInf  = targ_inf
        allyInf = ally_inf

        expansion_day = 0
        retreat_day = 0

        while retreat_day <= 7:
            day += 1
            # Save current day's numbers
            prevAllyInf = allyInf
            prevTargInf = targetInf

            # Get next day's numbers
            allyInf = self.strat.expandOneDay(allyInf, pop)
            targetInf = self.strat.retreatOneDay(targetInf , pop)

            # detect crossing
            if ((prevAllyInf <= prevTargInf) and (allyInf >= targetInf )):
                minf = (allyInf + targetInf ) / 2.0
                for i in range(5):
                    dayNum.append(day)
                    targ_infs.append(minf)
                    ally_infs.append(minf)
                    note = ""
                    if i == 0:
                        note = "Pending Conflict"
                    else:
                        note = "Conflict day " + str(i)
                    targ_note.append(note)
                    ally_note.append(note)
                    day += 1
            else:
                dayNum.append(day)
                note = ""
                if targetInf  < 2.5:
                    if retreat_day == 0:
                        note = "Pending Retreat"
                    else:
                        note = "Retreat day " + str(retreat_day)
                    retreat_day += 1

                targ_infs.append(targetInf )
                targ_note.append(note)

                note: str = ""
                if allyInf > 75.0:
                    if expansion_day < 5:
                        note = "Pending Expansion day " + str(expansion_day + 1)
                    elif expansion_day < 12:
                        note = "Expansion day " + str(expansion_day - 5 + 1)
                        if expansion_day >= 10:
                            note = note + " *"
                    elif expansion_day == 12:
                        note = "Expansion *"
                        allyInf = allyInf - 10.0  # expansion tax
                    else:
                        note = ""
                    expansion_day += 1
                ally_infs.append(allyInf)
                ally_note.append(note)

        # df = pd.DataFrame( list(zip(dayNum, ally_infs, targ_infs)), columns=["dayNum","ally_inf","target_inf"])
        df = pd.DataFrame(list(zip(dayNum, ally_infs, ally_note, targ_infs, targ_note)),
                          columns=["dayNum", "ally_inf", "ally_note", "target_inf", "targ_note"])
        return df

    def getDatedSimulationFrame(self, startDate: dt.datetime, ally_inf: float, targ_inf: float, pop: int):
        df = self.getSimulationFrame(ally_inf, targ_inf, pop)
        dates = []
        for i in range(df.dayNum.size):
            theDate: dt.date = (startDate + dt.timedelta(days=i)).date()
            dates.append(theDate)

        df['date'] = dates
        return df

    def daysToPendingExpansion(self, inf: float, pop: int):
        currentInf = inf
        day = 0
        while currentInf < 75.0:
            day += 1
            currentInf = self.strat.expandOneDay(currentInf, pop)
        return day

    def daysToPendingRetreat(self, inf: float, pop: int):
        currentInf = inf
        day = 0
        while currentInf > 2.5:
            day += 1
            currentInf = self.strat.retreatOneDay(currentInf, pop)
        return day

    def daysToExpansion(self, inf: float, pop: int):
        ret = self.daysToPendingExpansion(inf, pop)
        ret += 5  # pending days
        ret += 7  # active expansion https://discordapp.com/channels/483005833853009950/483005833853009952/759126832750002186
        return ret

    def daysToRetreat(self, inf: float, pop: int):
        ret = self.daysToPendingRetreat(inf, pop)
        ret += 1  # pending day
        ret += 6  # active retreat
        ret += 1
        return ret

    # noinspection PyTypeChecker
    def getSimulationFigure(self, sim: pd.DataFrame, title="Retreat Simulation", ally="Ally", target="Target"):
        ally_color = "pink"
        target_color = "red"
        conflict_color = "yellow"
        expansion_color = "magenta"
        retreat_color = "deeppink"

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=sim.date, y=sim.ally_inf,
                                 mode='lines',
                                 name=ally,
                                 marker_color='blue'))
        fig.add_trace(go.Scatter(x=sim.date, y=sim.target_inf,
                                 mode='lines',
                                 name=target,
                                 marker_color='red'))
        retLine: List[float] = list(2.5 for i in range(sim.dayNum.size))
        expLine: List[float] = list(75.0 for i in range(sim.dayNum.size))
        fig.add_trace(go.Scatter(x=sim.date, y=retLine,
                                 mode='lines',
                                 name='Retreat',
                                 marker_color='#ff0000',
                                 line_dash='dot'))
        fig.add_trace(go.Scatter(x=sim.date, y=expLine,
                                 mode='lines',
                                 name='Expand',
                                 marker_color='#00ff00',
                                 line_dash='dot'))

        fig.update_layout( title=title)
        # fig.update_yaxes(type="log")
        return fig
