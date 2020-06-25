#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
#
#   SPDX-License-Identifier: BSD-3-Clause

import datetime
import string
from typing import List

from craid.eddb.base import GameConstants as gconst
from craid.eddb.faction.Faction import Faction
from craid.eddb.system.InhabitedSystem import InhabitedSystem
from craid.eddb.util.PassThroughDict import PassThroughDict
from craid.eddb.States import States


class FactionInstance(Faction):

    # getters/setters for id & name in superclass
    def __init__(self, par: Faction, _mySystem: InhabitedSystem, inf: float, _states: States):
        super().__init__(par, True)
        self.mySystem: InhabitedSystem = _mySystem
        self.influence: float = inf
        self.states: States = _states

    def getSystem(self):
        return self.mySystem

    def getFactionID(self):
        return self.get_id()

    def getPopulation(self):
        return self.mySystem.getPopulation()

    def getSystemID(self):
        return self.mySystem.get_id()

    def getSystemName(self):
        return self.mySystem.get_name()

    def getSystemNameById(self, _id):
        return super().getSystemNameById(_id)

    # def getUpdated(self):
    #    return self.mySystem.getUpdated()

    # <1, A single player can easily retreat
    # 1-100, A single player can retreatA
    # >50, Recommended for small groups
    # >100, requires significant team
    # excel formula = (D10/15000)*(E10^2)/ 1000
    # d=pop, e = inf
    def getDifficulty(self) -> float:
        theMax = 999999.0
        if not self.canRetreat():
            return theMax
        e10 = self.getInfluence()
        if e10 == 0.0:
            return theMax
        e10 = max(0.0, e10 - 2.5)  # only need to get them to 2.5% to trigger retreat
        d10 = self.getPopulation()
        ret = (d10 / 15000.0) * (e10 ** 2.0) / 1000.0

        if ret < 0.0:
            ret = 0.0
        if ret > theMax:
            ret = theMax
        return round(ret, 1)  # TODO: trimmed to 3 decimals since no format support

    def getDifficultyString(self) -> str:
        val = self.getDifficulty()
        # "Forcing a retreat from this system would "
        if val < .5: return "be extremely easy for one commander"
        if val < 1: return "be very easy for one commander"
        if val < 10: return "be easy for one commander"
        if val < 25: return "be easy"
        if val < 50: return "take some work for one commander"
        if val < 100: return "be possible for one commander"
        if val < 1000: return "require group effort"
        if val < 10000: return "require a gargantuan effort"
        if val < 100000: return "be well-nigh impossible"
        return "seem an impossibility"

    def canRetreat(self) -> bool:
        if self.isHomeSystem(): return False

        # FIXME: can't call getDifficulty here
        # if self.getDifficulty() == 999999: return False
        return True

    def getUpdatedDateTime(self) -> datetime:
        return self.mySystem.getUpdatedDateTime()

    def getX(self):
        return self.mySystem.getX()

    def getY(self):
        return self.mySystem.getY()

    def getZ(self):
        return self.mySystem.getZ()

    def getInfluence(self):
        return self.influence

    def getPowerState(self):
        return self.mySystem.getPowerState()

    def getPower(self):
        return self.mySystem.getPower()

    #
    # Vulnerability is a Frankenstein's Monster atm,
    # but it will take some thought to work out.
    #
    # At the moment, it's determined on data load.
    #
    # def isVulnerable(self):
    #    return self.vulnerable is not 0

    def getVulnerableString(self):
        assert self.states is not None, 'null vulnerable'
        retval: str = self.states.getShortString()
        assert retval is not None, 'null vulnerable 2'
        return retval

    def getUpdatedString(self):
        date = self.mySystem.getUpdatedDateTime()
        ds = date.strftime("%d-%b-%Y %H:%M")
        return ds

    def printCSV(self):
        facName = self.get_name2()
        war = self.getVulnerableString()
        sysName = self.getSystemName()
        x = '{:04.2f}'.format(self.getX())
        y = '{:04.2f}'.format(self.getY)
        z = '{:04.2f}'.format(self.getZ)
        sinf = '{:04.2f}'.format(self.getInfluence)
        allg = self.get_allegiance()
        ds = self.getUpdatedString()
        print(f"{facName},{sysName},{x},{y},{z},{allg},{sinf},{war},{ds}")
        #    facName + "," + sysName + "," + x + "," + y + "," + z + "," + allg +
        #    "," + sinf + "," + war + "," + ds)  # + "," + allg)

    def isHomeSystem(self) -> bool:
        factionHomeSystemId: int = self.get_homesystem_id()
        systemId = self.getSystemID()
        return systemId == factionHomeSystemId

    def controlsSystem(self) -> bool:
        cid = self.mySystem.getControllingFactionId()
        mid: int = int(self.get_id())
        return cid == mid

    def template(self, msg: str) -> str:
        myDict: PassThroughDict[str, str] = PassThroughDict()

        myDict['home_system'] = self.get_homesystem_name()
        myDict['allegiance'] = str(self.get_allegiance())
        myDict['government'] = str(self.get_government())
        # myDict['inara_link'] = self.getInaraFactionUrl()
        myDict['faction_name'] = self.get_name2()

        template = string.Template(msg)
        output = template.substitute(myDict)
        return output

    def hasState(self, state: int):
        return self.states.hasState(state)

    # shared code for trade/exploration
    def _ss(self) -> [float, List[str]]:

        sco: float = 10.0
        bonuses: List[str] = []

        #
        # Stage 1: Is the _system_ good for smuggling
        #
        from craid.eddb.Station import Station
        sta: Station = self.mySystem.getBestTradeStation()
        if sta is None:
            return 0, ["no suitable station"]

        if sta.isOrbital():
            bonuses.append("station is orbital")
            sco = sco * 2

        if sta.hasLargePads():
            bonuses.append("station has large pads")
            sco = sco * 2

        #
        # Stage 2: Can the opposing faction benefit from smuggling
        #
        if sta.hasState(gconst.STATE_WAR) or sta.hasState(gconst.STATE_CIVIL_WAR):
            return 0.0, "station's controlling faction is at war"

        if sta.hasState(gconst.STATE_ELECTION):
            bonuses.append("station is in an election state")
            sco = sco * 2

        if sta.hasState(gconst.STATE_INVESTMENT):
            bonuses.append("station is in investment state")
            sco = sco * 2

        if sta.hasState(gconst.STATE_EXPANSION):
            bonuses.append("station is in expansion state")
            sco = sco * 2

        #
        # Stage 3: Can the club faction be damaged by bounty hunting
        #
        if self.hasState(gconst.STATE_LOCKDOWN):
            return 0.0, "the Club faction is in lockdown"

        if self.hasState(gconst.STATE_WAR) or self.hasState(gconst.STATE_CIVIL_WAR):
            return 0.0, "the club faction is at war"

        if self.hasState(gconst.STATE_ELECTION):
            sco = sco * 2.0
            bonuses.append("the Club faction being in elections")

        return sco, bonuses

    def salesScore(self) -> [float, str]:
        sco: float
        bonuses: List[str]
        sco, bonuses = self._ss()

        if sco <= 0.0:
            my_string = ','.join(bonuses)
            return sco, my_string

        from craid.eddb.Station import Station
        sta: Station = self.mySystem.getBestTradeStation()

        if sta.hasState(gconst.STATE_FAMINE):
            bonuses.append("food trade will help end the famine")
            sco = sco * 2

        if sta.hasState(gconst.STATE_OUTBREAK):
            bonuses.append("medicine trade will help end the outbreak")
            sco = sco * 2

        my_string = ','.join(bonuses)
        return sco, my_string

    def explorationScore(self):
        sco: float
        bonuses: List[str]
        sco, bonuses = self._ss()
        # sco: float, bonuses: List[str] = self._ss()
        # sco, bonuses = self._ss()
        my_string = ','.join(bonuses)
        return sco, my_string

    # def explorationScore(self):
    #     return self.mySystem.explorationScore()
    #
    # def salesScore(self):
    #     return self.mySystem.salesScore()

    # def bountyHuntingScore(self) -> float:
    #     return self.mySystem.bountyHuntingScore()

    def smugglingScore(self) -> [float, str]:
        score: float = 50.0
        bonuses: List[str] = []

        #
        # Stage 1: Is the _system_ good for smuggling
        #
        from craid.eddb.Station import Station
        sta: Station = self.mySystem.getBestSmugglingStation()
        if sta is None:
            return 0.0, "there is no suitable station"

        #
        # Stage 2: Can the opposing faction benefit from smuggling
        #
        # in this case, the opposer is either the system's controlling faction or the non-club faction with the highest influence

        opposer = self.mySystem.getControllingFactionInstance()
        if opposer is None:
            return 0.0, "opposing faction is unknown"

        if opposer.isClub():
            opposer = self.mySystem.getHighestInfluenceNonClubFactionInstance()

        if not opposer:
            return 0.0, "there is no suitable opposition"

        oppName = opposer.get_name2()
        if opposer.hasState(gconst.STATE_WAR) or opposer.hasState(gconst.STATE_CIVIL_WAR):
            return 0.0, f"the opposing faction {oppName} is at war"
        if opposer.hasState(gconst.STATE_LOCKDOWN):
            return 0.0, "the opposing faction is in lockdown"
        if opposer.hasState(gconst.STATE_BOOM):
            score = score * 2
            bonuses.append(f"the opposing faction, {oppName}, being in a boom state")
        if opposer.hasState(gconst.STATE_ELECTION):
            score = score * 2.0
            bonuses.append("the opposing faction being in elections")

        #
        # Stage 3: Can the club faction be damaged by smuggling
        #
        if self.hasState(gconst.STATE_LOCKDOWN):
            return 0.0, "the Club faction is in lockdown"

        if self.hasState(gconst.STATE_WAR) or self.hasState(gconst.STATE_CIVIL_WAR):
            return 0.0, "the club faction is at war"

        if self.hasState(gconst.STATE_ELECTION):
            score = score * 2.0
            bonuses.append("the Club faction being in elections")

        my_string = ','.join(bonuses)
        return round(score, 0), my_string

    def getSystemEdbgsLink(self):
        return self.mySystem.getEdbgsLink(self, self.get_name2())

    # much taken from https://forums.frontier.co.uk/threads/dev-update-07-01-2016.221826/
    def bountyHuntingScore(self) -> [float, str]:
        score: float = 50.0
        bonuses: List[str] = []

        #
        # Doing bounty hunting is to _benefit_ a non-club faction in control of a system
        # and a non-club faction in control of a station.  They may not be the same.
        # If one of those factions is in lockdown, that part of the effect is lost.
        #

        #
        # Stage 1: Is the _system_ good for bounty hunting
        #
        hasRings = self.mySystem.hasRings()
        if not hasRings:
            return 0.0, "the system has no ringed bodies"

        bonuses.append("having ringed planets")

        if self.mySystem.hasAnarchyFaction():
            score = score * 1.1
            bonuses.append("having a local pirate faction")

        econ = self.mySystem.getPrimaryEconomy()
        if econ.startswith('Extract') or econ.startswith('Refine'):
            score = score * 1.1
            bonuses.append("having a mining economy")

        from craid.eddb.Station import Station
        sta: Station = self.mySystem.getBestTradeStation()
        if sta is None:
            return 0.0, "the system doesn't have a suitable station to turn in bounties"

        #
        # Stage 2: Can the opposing faction benefit from bounty hunting
        #
        opposer = sta.getControllingFactionInstance()
        if opposer is None:
            return 0.0, "opposing faction is unknown"

        if opposer.hasState(gconst.STATE_LOCKDOWN):
            return 0.0, "the opposing faction is in lockdown"

        if opposer.hasState(gconst.STATE_ELECTION):
            return 0.0, "the opposing faction is in an election"

        if opposer.hasState(gconst.STATE_OUTBREAK):
            return 0.0, "the opposing faction is in an outbreak"

        if opposer.hasState(gconst.STATE_FAMINE):
            return 0.0, "the opposing faction is in a famine"

        if opposer.hasState(gconst.STATE_WAR) or opposer.hasState(gconst.STATE_CIVIL_WAR):
            score = score * 2.0
            bonuses.append("the opposing faction being at war")

        if opposer.hasState(gconst.STATE_CIVIL_UNREST):
            score = score * 2.0
            bonuses.append("the opposing faction being in civil unrest")

        #
        # Stage 3: Can the club faction be damaged by bounty hunting
        #

        if self.hasState(gconst.STATE_LOCKDOWN):
            return 0.0, "the Club faction is in lockdown"

        if self.hasState(gconst.STATE_ELECTION):
            return 0.0, "the Club faction is in an election"

        if self.hasState(gconst.STATE_OUTBREAK):
            return 0.0, "the Club faction is in outbreak"

        if self.hasState(gconst.STATE_FAMINE):
            return 0.0, "the Club faction is in famine"

        if self.hasState(gconst.STATE_WAR) or self.hasState(gconst.STATE_CIVIL_WAR):
            score = score * 2.0
            bonuses.append("the club faction being at war")

        # NOTE: would be nice to use pirateattack state
        my_string = ','.join(bonuses)
        return round(score, 0), my_string

    def getRegionNumber(self):
        return self.mySystem.getRegionNumber()

    def missionScore(self) -> [float, str]:
        sco: float = 50.0
        bonuses: List[str] = []
        after = ""

        #
        # Stage 1: Is the _system_ good for running mission
        #
        from craid.eddb.Station import Station
        sta: Station = self.mySystem.getBestMissionStation()
        if sta is None:
            return 0, ["no suitable station"]

        if sta.isOrbital():
            bonuses.append("station is orbital")
            sco = sco * 2

        if sta.hasLargePads():
            bonuses.append("station has large pads")
            sco = sco * 2

        staName = sta.get_name()
        staDist = sta.getDistanceToStar()

        #
        # Stage 2: Can the opposing faction benefit from missions
        #
        opposer = sta.getControllingFactionInstance()
        if opposer is None:
            return 0.0, "opposing faction is unknown"

        if opposer.hasState(gconst.STATE_WAR) or opposer.hasState(gconst.STATE_CIVIL_WAR):
            return 0.0, "opposition faction is at war"

        if opposer.hasState(gconst.STATE_WAR) or opposer.hasState(gconst.STATE_CIVIL_WAR):
            return 0.0, "opposition faction is in lockdown"

        if opposer.hasState(gconst.STATE_ELECTION):
            bonuses.append("opposition is in an election state")
            sco = sco * 2

        if opposer.hasState(gconst.STATE_BOOM):
            bonuses.append("opposition is in boom state")
            sco = sco * 2

        if opposer.hasState(gconst.STATE_INVESTMENT):
            bonuses.append("opposition is in investment state")
            sco = sco * 2

        if opposer.hasState(gconst.STATE_EXPANSION):
            bonuses.append("opposition is in expansion state")
            sco = sco * 1.5

        #
        # Penalty for really far stations
        #
        if staDist > 100000:
            sco = sco * .5
        elif staDist > 75000:
            sco = sco * .75
        elif staDist > 50000:
            sco = sco * .9
        elif staDist > 25000:
            sco = sco * .95

        #
        # Stage 3: Can the club faction be damaged by bounty hunting
        #
        if self.hasState(gconst.STATE_LOCKDOWN):
            return 0.0, "the Club faction is in lockdown"

        if self.hasState(gconst.STATE_WAR) or self.hasState(gconst.STATE_CIVIL_WAR):
            return 0.0, "the Club faction is at war"

        if self.hasState(gconst.STATE_ELECTION):
            sco = sco * 2.0
            bonuses.append("the Club faction being in elections")

        my_string = ','.join(bonuses)
        return round(sco, 0), my_string

        ## TODO: Check self vs Investment/Lockdown
        # msg = f'Run missions for competing factions at station {staName}.'
        # if staDist>25000:
        #    after += "  Note the distance to the station."

    def piracyMurderScore(self) -> float:
        return self.mySystem.piracyMurderScore()

    def mineralSalesScore(self):
        return self.mySystem.mineralSalesScore()
