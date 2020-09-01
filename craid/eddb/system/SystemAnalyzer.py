#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
#
#   SPDX-License-Identifier: BSD-3-Clause
from typing import List

import craid.eddb.base.GameConstants as gconst
from craid.eddb.Station import Station
from craid.eddb.faction.FactionInstance import FactionInstance
from craid.eddb.system.InhabitedSystem import InhabitedSystem
from craid.eddb.util.MessageList import MessageList


class SystemAnalyzer(object):

    def __init__(self, theSystem: InhabitedSystem, theFaction: FactionInstance):
        self.theSystem = theSystem
        self.theFaction = theFaction
        self.messages = MessageList()

        diff: float = theFaction.getDifficulty()
        homeSys: bool = theFaction.isHomeSystem()

        nFacs = theSystem.getNumberOfFactionsInSystem()

        if not homeSys:
            if nFacs< 4:
                msg = f'It is impossible to retreat a faction when there are fewer than 4 factions in the system\n'
                self.messages.add(110.0, msg)
                return
            elif diff == 999999:
                msg = f'It is impossible to force the faction out of this system for reasons that are not understood.\n'
                self.messages.add(110.0, msg)
                return
        elif homeSys:
            msg = f"This is the faction's home system, so it cannot be forced out.  Effort may be better spent elsewhere.\n"
            self.messages.add(110.0, msg)
        else:
            adj: str = theFaction.getDifficultyString()
            msg = f"I estimate that forcing a retreat from this system would {adj}."
            self.messages.add(110.0, msg)

        daysSinceScouted: int = theSystem.getDaysSinceScouted()
        if daysSinceScouted > 3:
            msg = f"The system was last scouted {daysSinceScouted} days ago.  The situation may have changed."
            if daysSinceScouted > 10:
                msg = "~~" + msg + "~~"

            self.messages.add(105.0, msg)

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
            self.mining()
            self.piracyMurder()
            self.tradeExploration()

        self.smuggling()
        self.bountyHunting()

    def bountyHunting(self):
        bhSco, msg = self.theFaction.bountyHuntingScore()
        if bhSco <= 0.0:
            msg = f'Bounty hunting is not recommended because {msg}.'
        elif bhSco <= 50.0:
            msg = f'Bounty hunting is effective.'
        else:
            msg = f'Bounty hunting is particularly effective for the following reasons: {msg}.'
        self.messages.add(bhSco, msg)

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
        smSco, msg = self.theFaction.missionScore()
        if smSco <= 0.0:
            msg = f'Running missions is not recommended because {msg}.'
        elif smSco <= 50.0:
            msg = f'Running missions is effective.'
        else:
            msg = f'Running missions is particularly effective for the following reasons: {msg}.'

        self.messages.add(smSco, msg)

    def smuggling(self):
        smSco, msg = self.theFaction.smugglingScore()
        if smSco <= 0.0:
            msg = f'Smuggling is not recommended because {msg}.'
        elif smSco <= 50.0:
            msg = f'Smuggling is effective.'
        else:
            msg = f'Smuggling is particularly effective for the following reasons: {msg}.'

        self.messages.add(smSco, msg)

    def piracyMurder(self):
        sta: Station = self.theSystem.getBestCrimeStation()
        if sta is None:
            return

        staName = sta.get_name()
        msg = f'Piracy and murder at the nav beacon and station {staName}.'
        self.messages.add(50, msg)

    def mining(self):
        sco: int = self.theSystem.mineralSalesScore()
        if sco < 2:
            return
        elif sco == 2:
            adj = "good"
        elif sco == 3:
            adj = "very good"
        elif sco == 4:
            adj = "extremely good"
        else:
            adj = "phenomenal"

        msg = f'Conditions are right for mineral prices to be {adj} in the system at non-club controlled stations.'
        self.messages.add(70, msg)

    def tradeExploration(self):
        sta: Station = self.theSystem.getBestTradeStation()
        if sta is None:
            return

        staName = sta.get_name()
        staDist = sta.getDistanceToStar()

        ## TODO: Boom, Investment
        msg = f'Trade or sell exploration data to opposing faction at {staName}.'

        msg2 = ""
        infra: bool = sta.hasState(gconst.STATE_INFRASTRUCTURE_FAILURE)
        if infra:
            msg2 = "Delivery of food and machinery will aid controlling faction's infrastructure failure"
        else:
            boom: bool = sta.hasState(gconst.STATE_BOOM)
            inv: bool = sta.hasState(gconst.STATE_INVESTMENT)
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
        elif mineral >= 5:
            msg3 = "Selling mined minerals may be extremely profitable."

        msg += msg3

        if staDist > 25000:
            msg += "  Note the distance to the station."
        self.messages.add(10, msg)

    def toString(self) -> str:
        return self.messages.toString()
