#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
from typing import List

import craid.eddb.GameConstants as gconst

from craid.eddb.InhabitedSystem import InhabitedSystem
from craid.eddb.Station import Station
from craid.eddb.util.MessageList import MessageList
from craid.eddb.FactionInstance import FactionInstance


def isProbablyAGoodBountyHuntingSystem(theSys: InhabitedSystem):
    if not theSys.hasAnarchyFaction():
        return False
    econ = theSys.jsonLine['primary_economy']
    if not econ:
        return False
    if (not econ.startswith('Extract')) and (
            not econ.startswith('Refine')):
        return False
    return True


class SystemAnalyzer(object):

    def __init__(self, theSystem: InhabitedSystem, theFaction: FactionInstance):
        self.theSystem = theSystem
        self.theFaction = theFaction
        self.messages = MessageList()

        diff: float = theFaction.getDifficulty()
        homeSys: bool = theFaction.isHomeSystem()

        if not homeSys and diff == 999999:
            msg = f'It is impossible to force the faction out of this system for reasons that are not understood.\n'
            self.messages.add(100.0, msg)
            return
        elif homeSys:
            msg = f"This is the faction's home system, so it cannot be forced out.  Effort may be better spent elsewhere.\n"
            self.messages.add(100.0, msg)
        else:
            adj: str = theFaction.getDifficultyString()
            msg = f"I estimate that forcing a retreat from this system would {adj}."
            self.messages.add(100.0, msg)

        if theFaction.hasState(gconst.STATE_ELECTION):
            msg = "The faction is in a state of election, losing the election will have significant effects on its influence."
            self.messages.add(99.0, msg)
        if theFaction.hasState(gconst.STATE_INFRASTRUCTURE_FAILURE):
            msg = "The faction is in a state of infrastructure failure, influence losses are magnified."
            self.messages.add(99.0, msg)

        if theFaction.hasState(gconst.STATE_WAR) or theFaction.hasState(gconst.STATE_CIVIL_WAR):
            self.warZones()
            self.piracyMurder()
        else:
            self.missions()
            self.smuggling()
            self.piracyMurder()
            self.tradeExploration()

    def warZones(self):
        wars: List[str] = self.theSystem.getClubInState(gconst.STATE_WAR)
        for warFac in wars:
            msg = f'Fight in war zones against {warFac}.\n'
            self.messages.add(99.0, msg)
        wars: List[str] = self.theSystem.getClubInState(gconst.STATE_CIVIL_WAR)
        for warFac in wars:
            msg = f'Fight in civil war zones against {warFac}.\n'
            self.messages.add(99.0, msg)

    def missions(self):
        sta: Station = self.theSystem.getBestMissionStation()
        if sta is None:
            return

        staName = sta.get_name()
        staDist = sta.getDistanceToStar()

        ## TODO: Boom, Investment
        msg = f'Run missions for competing factions at station {staName}.'

        if (staDist>25000):
            msg += "  Note the distance to the station."
        self.messages.add(10,msg)

    def smuggling(self):
        sta: Station = self.theSystem.getBestSmugglingStation()
        if sta is None:
            return

        staName = sta.get_name()
        msg = f'Smuggling to station {staName}.'
        self.messages.add(50, msg)

    def piracyMurder(self):
        sta: Station = self.theSystem.getBestCrimeStation()
        if sta is None:
            return

        staName = sta.get_name()
        msg = f'Piracy and murder at the nav beacon and station {staName}.'
        self.messages.add(50, msg)

    def tradeExploration(self):
        sta: Station = self.theSystem.getBestTradeStation()
        if sta is None:
            return

        staName = sta.get_name()
        staDist = sta.getDistanceToStar()

        ## TODO: Boom, Investment
        msg = f'Trade or sell exploration data to opposing faction at {staName}.'

        boom: bool = sta.hasState(gconst.STATE_BOOM)
        inv: bool = sta.hasState(gconst.STATE_INVESTMENT)

        msg2 = ""
        if boom and inv:
            msg2 = "  Effects are significantly increased by the controlling faction being in boom and investment states."
        elif boom:
            msg2 = "  Effects are increased by the controlling faction being in a boom state."
        elif inv:
            msg2 = "  Effects are increased by the controlling faction being in an investment state."

        msg += msg2

        msg3 = ""
        mineral = sta.getMineralSalesScore()
        if mineral == 3:
            msg3 = "Selling mined minerals may be profitable."
        elif mineral == 4:
            msg3 = "Selling mined minerals may be very profitable."
        elif mineral == 5:
            msg3 = "Selling mined minerals may be extremely profitable."

        msg += msg3

        if (staDist > 25000):
            msg += "  Note the distance to the station."
        self.messages.add(10, msg)

    def toString(self) -> str:
        return self.messages.toString()
