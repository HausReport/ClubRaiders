#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

import string
from collections import deque
from typing import List, Deque

from craid.eddb.Faction import Faction
from craid.eddb.GameConstants import *
from craid.eddb.PassThroughDict import PassThroughDict
from craid.eddb.Station import Station
from craid.eddb.System import System
from craid.eddb.util.TextDecoration import boolToTorBlank, boolToYesOrNo


#
# INFO: Tap-dancing right on the edge of a cyclic import catastrophe with FactionInstance
#
class InhabitedSystem(System):
    FLAG_CLUB_ONLY: int = 0
    FLAG_NON_CLUB_ONLY: int = 1
    FLAG_EITHER: int = 2

    # FIXME: expand constructor and remove jsonLine references as possible
    def __init__(self, jsonString: str):
        super().__init__(jsonString)
        self.jsonLine = jsonString
        self.hasAnarchy: bool = False
        self.powerState: str = jsonString[POWER_STATE]
        self.stations: List[Station] = []
        self.minorFactionPresences: List[object] = []

    # ================================================================================
    # General statistics
    #
    def getAllegiance(self) -> str:
        return self.jsonLine['allegiance']

    def getGovernment(self) -> str:
        return self.jsonLine['government']

    def getPowerState(self):
        return self.jsonLine[POWER_STATE]

    def getPower(self):
        return self.jsonLine['power']

    def getEconomy(self):
        return self.jsonLine['primary_economy']

    def getPowerLabel(self):
        power = self.getPower()
        powerState = self.getPowerState()
        return f'{power}-{powerState}'

    def getPopulation(self) -> int:
        return int(self.jsonLine['population'])

    # ================================================================================
    # Factions Methods
    #

    def getControllingFactionInstance(self):
        theId = self.getControllingFactionId()
        return self.getFactionInstanceById(theId)

    def getFactionInstanceById(self, theId: int):
        from craid.eddb.FactionInstance import FactionInstance
        fac: FactionInstance
        for fac in self.minorFactionPresences:
            if fac.get_id() == theId:
                return fac

    def getControllingFactionId(self):
        return int(self.jsonLine['controlling_minor_faction_id'])

    def getControllingFactionName(self):
        cf: int = self.getControllingFactionId()
        return super().getFactionNameById(cf)

    def getControllingFactionName2(self):
        cf: int = self.getControllingFactionId()
        f: Faction = super().getFactionById(cf)
        return f.get_name2()

    def getMinorFactionsAsMarkdown(self):
        from craid.eddb.FactionInstance import FactionInstance

        ret: str = "\n\n"
        ret += "|Name | Inf. | States | \n"  # " LPad | Club | Yard | BM | Controlling | \n"
        ret += "| --- | --- |--- | \n"  # "--- | --- | --- | --- | --- |\n"
        f: FactionInstance
        for f in self.minorFactionPresences:
            ret += "| "
            ret += f.get_name2()  # decorates name for md
            ret += " | "
            ret += "{:,}".format(f.getInfluence())
            ret += " | "
            ret += f.getVulnerableString()
            ret += " | "
            # ret += boolToTorBlank(sta.hasLargePads())
            # ret += " | "
            # ret += boolToTorBlank(sta.isClub())
            # ret += " | "
            # ret += boolToTorBlank(sta.hasShipyard())
            # ret += "  | "
            # ret += boolToTorBlank(sta.hasBlackMarket())
            # ret += "  | "
            # ret += sta.getControllingFactionName2()
            # ret += "  | "
            ret += "\n"

        theret = ret + "\n\n\n"
        # print(theret)
        return theret

    def hasAnarchyFaction(self):
        from craid.eddb.FactionInstance import FactionInstance
        fi: FactionInstance
        for fi in self.minorFactionPresences:
            if fi.is_anarchy():
                return True

        return False

    def _addMinorFactionPresence(self, what: object):
        self.minorFactionPresences.append(what)

    def _getMinorFactionPresencesDict(self):
        return self.jsonLine[MINOR_FACTION_PRESENCES]

    # ================================================================================
    # Stations Methods
    #
    def addStation(self, sta: Station):
        self.stations.append(sta)

    def enemyControlledStations(self):
        ret: List[Station] = []
        for sta in self.stations:
            if sta.isClub():
                ret.append(sta)

    def nonEnemyControlledStations(self):
        ret: List[Station] = []
        for sta in self.stations:
            if not sta.isClub():
                ret.append(sta)

    def getStationsTableString(self) -> str:

        ret: str = "\n\n"
        ret += "|Name | ls | Orb | LPad | Club | Yard | BM | Controlling | \n"
        ret += "| --- | --- |--- | --- | --- | --- | --- | --- |\n"
        for sta in self.stations:
            ret += "| "
            ret += sta.getEddbUrl()  # get_name()
            ret += " | "
            ret += "{:,}".format(sta.getDistanceToStar())
            ret += " | "
            ret += boolToTorBlank(sta.isOrbital())
            ret += " | "
            ret += boolToTorBlank(sta.hasLargePads())
            ret += " | "
            ret += boolToTorBlank(sta.isClub())
            ret += " | "
            ret += boolToTorBlank(sta.hasShipyard())
            ret += "  | "
            ret += boolToTorBlank(sta.hasBlackMarket())
            ret += "  | "
            ret += sta.getControllingFactionName2()
            ret += "  | "
            ret += "\n"

        theret = ret + "\n\n\n"
        # print(theret)
        return theret

    # ================================================================================
    # Templating
    #
    def template(self, msg: str, fix: object) -> str:
        from craid.eddb.FactionInstance import FactionInstance
        fi: FactionInstance = fix

        myDict: PassThroughDict[str, str] = PassThroughDict()

        myDict['system_name'] = self.get_name()
        myDict['allegiance'] = str(self.getAllegiance())
        myDict['government'] = str(self.getGovernment())
        myDict['controlling_faction'] = self.getControllingFactionName2()
        # "{:,}".format(self.getControllingFactionId())
        myDict['population'] = "{:,}".format(self.getPopulation())
        myDict['inara_link'] = "[link](" + self.getInaraSystemUrl() + ")"
        myDict['eddb_link'] = "[link](" + self.getEddbSystemUrl() + ")"

        myDict['nearest_shipyard'] = self.getInaraNearestShipyardUrl()
        myDict['r2r_link'] = self.getRoadToRichesUrl()

        myDict['x'] = "{:,}".format(self.getX())
        myDict['y'] = "{:,}".format(self.getY())
        myDict['z'] = "{:,}".format(self.getZ())

        myDict['octant'] = "{:,}".format(self.getOctant())

        from craid.eddb.SystemAnalyzer import SystemAnalyzer
        # sysA = SystemAnalyzer(self)
        from craid.eddb.SystemAnalyzer import isProbablyAGoodBountyHuntingSystem  # sidestep circ import
        bhVal = isProbablyAGoodBountyHuntingSystem(self)
        # bhVal = self.isProbablyAGoodBHSystem()
        bh = "Unknown"
        if bhVal: bh = "Probably"
        myDict['bounty_hunting'] = bh

        myDict['power'] = self.getPower()
        myDict['power_state'] = self.getPowerState()

        myDict['scouting_msg'] = self.getUpdatedString()

        myDict['station_list'] = self.getStationsTableString()

        myDict['faction_list'] = self.getMinorFactionsAsMarkdown()

        myDict['needs_permit'] = boolToYesOrNo(self.needsPermit())

        myDict['economy'] = self.getEconomy()

        sa = SystemAnalyzer(self, fix)
        rep = sa.toString()
        myDict['system_analysis'] = rep

        myTemplate = string.Template(msg)
        output: str = myTemplate.substitute(myDict)
        return output

    #
    # Return list of club faction names in the given state
    #
    def getClubInState(self, state: int):
        ret: List[str] = []
        from craid.eddb.FactionInstance import FactionInstance
        fi: FactionInstance
        for fi in self.minorFactionPresences:
            if fi.isClub():
                if fi.hasState(state):
                    ret.append(fi.get_name2())

        return ret

    #
    # Return list of club faction names in the given state
    #
    def getNonClubInState(self, state: int):
        ret: List[str] = []
        from craid.eddb.FactionInstance import FactionInstance
        fi: FactionInstance
        for fi in self.minorFactionPresences:
            if fi.isClub():
                if fi.hasState(state):
                    ret.append(fi.get_name2())

        return ret

    def getBestStation(self, orbital: bool, largePads: bool, flag: int, reqBlackMarket=False ) -> Station:
        sta: Station
        # bestStation: Station
        # bestStation: List[Station] = []   #long-ass workaround for standard java technique
        bestStation: Deque[Station] = deque()  # long-ass workaround for standard java technique
        ## FIXME: this method got out of control for stupid reasons

        for sta in self.stations:
            #
            # These conditions match exactly
            #
            if orbital != sta.isOrbital():
                continue
            if largePads != sta.hasLargePads():
                continue

            #
            # For these, if (condition) and if not (state) then skip
            #
            if reqBlackMarket and not (sta.hasBlackMarket()):
                continue

            if len(bestStation) == 0:
                if flag == self.FLAG_CLUB_ONLY:
                    if sta.isClub():
                        bestStation.appendleft(sta)
                        continue
                if flag == self.FLAG_NON_CLUB_ONLY:
                    if not sta.isClub():
                        bestStation.appendleft(sta)
                        continue
                if flag == self.FLAG_EITHER:
                    bestStation.appendleft(sta)
                    continue

            dist = 999999999999999
            if len(bestStation) > 0:
                dist = bestStation[0].getDistanceToStar()

            if sta.getDistanceToStar() <= dist:
                if flag == self.FLAG_CLUB_ONLY:
                    if sta.isClub():
                        bestStation.appendleft(sta)
                        continue
                if flag == self.FLAG_NON_CLUB_ONLY:
                    if not sta.isClub():
                        bestStation.appendleft(sta)
                        continue
                if flag == self.FLAG_EITHER:
                    bestStation.appendleft(sta)
                    continue
        if len(bestStation) < 1:
            return None
        return bestStation.popleft()

    #
    # Orbital only
    #
    def getBestSmugglingStation(self):
        bestStation: Station = self.getBestStation(True, True, self.FLAG_CLUB_ONLY, reqBlackMarket=True)
        if bestStation is not None:
            return bestStation

        bestStation: Station = self.getBestStation(True, False, self.FLAG_CLUB_ONLY, reqBlackMarket=True)
        return bestStation

    #
    #
    #
    def getBestCrimeStation(self):
        bestStation: Station = self.getBestStation(True, True, self.FLAG_CLUB_ONLY)
        if bestStation is not None:
            return bestStation

        bestStation: Station = self.getBestStation(True, False, self.FLAG_CLUB_ONLY)
        return bestStation

    #
    #
    #
    def getBestMissionStation(self):
        bestStation: Station = self.getBestStation(True, True, self.FLAG_EITHER)
        if bestStation is not None:
            return bestStation

        bestStation: Station = self.getBestStation(False, True, self.FLAG_EITHER)
        if bestStation is not None:
            return bestStation

        bestStation: Station = self.getBestStation(True, False, self.FLAG_EITHER)
        if bestStation is not None:
            return bestStation

        bestStation: Station = self.getBestStation(False, False, self.FLAG_EITHER)
        return bestStation

    #
    #
    #
    def getBestTradeStation(self):
        bestStation: Station = self.getBestStation(True, True, self.FLAG_NON_CLUB_ONLY)
        if bestStation is not None:
            return bestStation

        bestStation: Station = self.getBestStation(False, True, self.FLAG_NON_CLUB_ONLY)
        if bestStation is not None:
            return bestStation

        bestStation: Station = self.getBestStation(True, False, self.FLAG_NON_CLUB_ONLY)
        if bestStation is not None:
            return bestStation

        bestStation: Station = self.getBestStation(False, False, self.FLAG_NON_CLUB_ONLY)
        return bestStation
