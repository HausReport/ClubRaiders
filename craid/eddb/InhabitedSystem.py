#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

import string
from collections import deque
from typing import List, Deque

from PassThroughDict import PassThroughDict
from Station import Station
from System import System
from craid.eddb.Faction import Faction
from craid.eddb.GameConstants import *
from util.TextDecoration import boolToTorBlank, boolToYesOrNo


#
# INFO: Tap-dancing right on the edge of a cyclic import catastrophe with FactionInstance
#
class InhabitedSystem(System):

    FLAG_CLUB_ONLY :int = 0
    FLAG_NON_CLUB_ONLY: int = 1
    FLAG_EITHER: int = 2

    def __init__(self, jsonString: str):
        super().__init__(jsonString)
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

    def getPowerLabel(self):
        power = self.getPower()
        powerState = self.getPowerState()
        return f'{power}-{powerState}'

    def getPopulation(self) -> int:
        return int(self.jsonLine['population'])

    # ================================================================================
    # Factions Methods
    #
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
        from FactionInstance import FactionInstance

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
        from FactionInstance import FactionInstance
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
    def template(self, msg: str) -> str:
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
        sysA = SystemAnalyzer(self)
        from SystemAnalyzer import isProbablyAGoodBountyHuntingSystem  #sidestep circ import
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

        sa = SystemAnalyzer(self)
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
        from FactionInstance import FactionInstance
        fi: FactionInstance
        for fi in self.minorFactionPresences:
            if fi.isClub():
                if fi.hasSate(state):
                    ret.append(fi.get_name2())

        return ret

    #
    # Return list of club faction names in the given state
    #
    def getNonClubInState(self, state: int):
        ret: List[str] = []
        from FactionInstance import FactionInstance
        fi: FactionInstance
        for fi in self.minorFactionPresences:
            if fi.isClub():
                if fi.hasSate(state):
                    ret.append(fi.get_name2())

        return ret

    def getBestStation(self, orbital: bool, largePads: bool, flag: int) -> Station:
        sta: Station
        #bestStation: Station
        #bestStation: List[Station] = []   #long-ass workaround for standard java technique
        bestStation: Deque[Station] = deque()  #long-ass workaround for standard java technique
        ## FIXME: this method got out of control for stupid reasons

        for sta in self.stations:
            if orbital != sta.isOrbital():
                continue
            if largePads != sta.hasLargePads():
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
            if len(bestStation)> 0:
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
        if( len(bestStation)<1):
            return None
        return bestStation.popleft()

    #
    # Orbital only
    #
    def getBestSmugglingStation(self):
        bestStation: Station = self.getBestStation(True, True, self.FLAG_CLUB_ONLY)
        if bestStation is not None:
            return bestStation

        bestStation: Station = self.getBestStation(True, False, self.FLAG_CLUB_ONLY)
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


