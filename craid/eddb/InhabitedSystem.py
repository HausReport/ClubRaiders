#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

import string
from typing import Dict, List, Any, Union

from deprecated import deprecated

from PassThroughDict import PassThroughDict
from Station import Station
from System import System
from TextDecoration import boolToTorBlank, boolToYesOrNo
from craid.eddb.Constants import MINOR_FACTION_ID, POWER_STATE, MINOR_FACTION_PRESENCES
from craid.eddb.Faction import Faction

#
# INFO: Tapdancing right on the edge of a cyclic import catastrophe with FactionInstance
#
class InhabitedSystem(System):

    def __init__(self, jsonString: str):
        super().__init__(jsonString)
        self.hasAnarchy: bool = False
        self.powerState: str = jsonString[POWER_STATE]
        self.stations: List[Station] = []
        self.minorFactionPresences: List[object] = []

    #================================================================================
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

    #================================================================================
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
        foo: List[FactionInstance] = self.minorFactionPresences

        ret: str = "\n\n"
        f: FactionInstance
        for f in foo:
            pre: str = f.get_name2()       # decorates name for md
            ret = ret + "\n*  " + pre      # star for bullet

        return ret + "\n\n"



    # def getMinorFactionsAsDict(self):
    #     ret: Dict[int, Faction] = {}
    #     mfp: Dict = self.getMinorFactionPresencesDict()
    #     for faction_ptr in mfp:
    #         faction_id: int = int(faction_ptr['minor_faction_id'])
    #         fac: Faction = super().getFactionById(faction_id)
    #         if fac is not None:
    #             ret[faction_id] = fac
    #
    #     # pprint.pprint( ret )
    #     print(" mfd size = " + str(len(list(mfp))))
    #     print(" ret size = " + str(len(list(ret.keys()))))
    #     return ret

    # def getFactions(self, all_factions_dict: Dict[int, Faction]):
    #     ret = []
    #     minor_faction_presences = self.jsonLine[MINOR_FACTION_PRESENCES]
    #     # if minor_faction_presences is None
    #     for faction_ptr in minor_faction_presences:
    #         if faction_ptr is None:
    #             continue
    #         faction_id: int = int(faction_ptr[MINOR_FACTION_ID])
    #         if faction_id is None:
    #             continue
    #         curFaction = all_factions_dict.get(faction_id)
    #         if curFaction is None:
    #             continue
    #         ret.append(curFaction)
    #     return ret

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

    #================================================================================
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

    #================================================================================
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
        bhVal = SystemAnalyzer.isProbablyAGoodBountyHuntingSystem(self)
        #bhVal = self.isProbablyAGoodBHSystem()
        bh = "Unknown"
        if bhVal: bh = "Probably"
        myDict['bounty_hunting'] = bh

        myDict['power'] = self.getPower()
        myDict['power_state'] = self.getPowerState()

        myDict['scouting_msg'] = self.getUpdatedString()

        myDict['station_list'] = self.getStationsTableString()

        myDict['faction_list'] = self.getMinorFactionsAsMarkdown()

        myDict['needs_permit'] = boolToYesOrNo(self.needsPermit())

        myTemplate = string.Template(msg)
        output: str = myTemplate.substitute(myDict)
        return output


