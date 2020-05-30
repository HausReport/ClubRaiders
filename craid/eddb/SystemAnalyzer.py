#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
from typing import List

import craid.eddb.GameConstants
import GameConstants
from craid.eddb.Station import Station
from craid.eddb.InhabitedSystem import InhabitedSystem
from craid.eddb.util.MessageList import MessageList


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

    def __init__(self, theSystem: InhabitedSystem):
        self.theSystem = theSystem
        self.messages = MessageList()
        self.warZones()
        self.missions()
        self.smuggling()
        self.piracyMurder()

    def warZones(self):
        wars: List[str] = self.theSystem.getClubInState(GameConstants.STATE_WAR)
        for warFac in wars:
            msg = f'Fight in war zones against {warFac}.\n'
            self.messages.add(100.0, msg)
        wars: List[str] = self.theSystem.getClubInState(GameConstants.STATE_CIVIL_WAR)
        for warFac in wars:
            msg = f'Fight in civil war zones against {warFac}.\n'
            self.messages.add(100.0, msg)

    def missions(self):
        sta: Station = self.theSystem.getBestMissionStation()
        if sta is None:
            return

        staName = sta.get_name()
        staDist = sta.getDistanceToStar()

        ## TODO: Boom, Investment
        msg = f'Missions at station {staName}.'

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

    def toString(self) -> str:
        return self.messages.toString()
