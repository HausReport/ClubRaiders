#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import logging

import craid.eddb.base.GameConstants as gconst
from craid.eddb.base.Aware import Aware
# No Good for us
# "type_id": 23, "type": "Non-Dockable Orbital",
from craid.eddb.base.NamedItem import NamedItem


# Currently known Types
# Usually good for us
# "type_id": 3, "type": "Coriolis Starport",
# "type_id": 8, "type": "Orbis Starport",
# "type_id": 7, "type": "Ocellus Starport",
# "type_id": 19, "type": "Megaship",
# "type_id": 20, "type": "Asteroid Base",
# I think these are medium orbital + planetary
# "type_id": 13, "type": "Planetary Outpost",
# "type_id": 4, "type": "Industrial Outpost",
# "type_id": 1, "type": "Civilian Outpost",
# "type_id": 16, "type": "Planetary Settlement",
# "type_id": 6, "type": "Mining Outpost",
# "type_id": 14, "type": "Planetary Port",
# "type_id": 2, "type": "Commercial Outpost",
# "type_id": 9, "type": "Scientific Outpost",
# "type_id": 5, "type": "Military Outpost",


class Station(Aware):

    # getters/setters for id & name in superclass
    def __init__(self, jsonLine):
        super().__init__(jsonLine[NamedItem.NAME], jsonLine[NamedItem.ID])
        # self.jsonLine: Dict[str, str] = jsonString
        self.club: bool = False
        self.distance_to_star: int = jsonLine.get('distance_to_star')
        self.has_large_pads: bool = False
        hm: str = jsonLine.get('max_landing_pad_size')
        if hm is not None:
            if hm == "L":
                self.has_large_pads = True
        self.has_market: bool = jsonLine.get("has_market")
        self.has_blackmarket: bool = jsonLine.get("has_blackmarket")
        self.has_shipyard: bool = jsonLine.get("has_shipyard")
        self.has_docking: bool = jsonLine.get("has_docking")
        self.is_planetary: bool = jsonLine.get("is_planetary")
        self.system_id: int = jsonLine.get("system_id")
        self.stationType: str = jsonLine.get("type")
        self.controlling_minor_faction_id: int = jsonLine.get("controlling_minor_faction_id")
        self.is_fleet_carrier: bool = True
        if not self.stationType.startswith("Fleet"):
            self.is_fleet_carrier = False

    def isFleetCarrier(self) -> bool:
        return self.is_fleet_carrier

    def getSystemId(self) -> int:
        return self.system_id

    def getDistanceToStar(self) -> int:
        return self.distance_to_star

    def hasLargePads(self) -> bool:
        return self.has_large_pads

    def hasMarket(self) -> bool:
        return self.has_market

    def hasBlackMarket(self) -> bool:
        return self.has_blackmarket

    def hasShipyard(self) -> bool:
        return self.has_shipyard

    def hasDocking(self) -> bool:
        return self.has_docking

    def isOrbital(self) -> bool:
        return not self.is_planetary

    def isPlanetary(self) -> bool:
        return self.is_planetary

    def okCandidate(self) -> bool:
        if not self.hasDocking():
            return False
        if self.controlling_minor_faction_id is None:
            return False
        return True

    def getTypeString(self) -> str:
        return self.stationType

    def getSystem(self):
        from craid.eddb.system.InhabitedSystem import InhabitedSystem
        tid: int = self.getSystemId()
        tsys: InhabitedSystem = Aware.getSystemById(tid)
        return tsys

    def getControllingFactionInstance(self):
        from craid.eddb.faction.FactionInstance import FactionInstance

        tSys = self.getSystem()
        fid: int = self.getControllingFactionId()
        fac: FactionInstance = tSys.getFactionInstanceById(fid)
        return fac

    def hasState(self, state: int):
        if self.isFleetCarrier():
            return False
        fac = self.getControllingFactionInstance()
        name = self.get_name()
        if fac is None:
            logging.info("station controlling faction nexist" + name)
            return False
        return fac.hasState(state)

    def getControllingFactionId(self) -> int:
        return self.controlling_minor_faction_id

    def getControllingFactionName(self) -> str:
        return Aware.getFactionNameById(self.getControllingFactionId())

    def getControllingFactionName2(self) -> str:
        from craid.eddb.faction.Faction import Faction
        fac: Faction = Aware.getFactionById(self.getControllingFactionId())
        if fac is None:
            return ("~~Unknown~~")
        return fac.get_name2()

    def setClub(self, param: bool):
        # print("setting club to :" + str(param))
        self.club = param

    def isClub(self) -> bool:
        return self.club

    # a little experimental, but should be close
    def getMineralSalesScore(self) -> int:
        from craid.eddb.system.InhabitedSystem import InhabitedSystem
        tSys: InhabitedSystem = self.getSystem()
        econ: str = tSys.getEconomy()
        if not econ.startswith("Indust") and not econ.startswith("Refin"):
            return 0

        ct: int = 0
        if self.hasState(gconst.STATE_BOOM) or self.hasState(gconst.STATE_INVESTMENT):
            if self.hasState(gconst.STATE_CIVIL_LIBERTY): ct += 1
            if self.hasState(gconst.STATE_EXPANSION): ct += 1
            if self.hasState(gconst.STATE_PUBLIC_HOLIDAY): ct += 1
            if ct < 2:
                return 0
            if self.hasState(gconst.STATE_PIRATE_ATTACK): ct += 1

        return ct

    ## FIXME: miners_tool urls are pretty obfuscated, too
    # FIXME: this is pretty obfuscated, don't see how it works yet
    #    def getEddbSellToUrl(self):
    #        https: // eddb.io / trade / single / sellSystemId = & sellStationId =
    def getEddbUrl(self):
        return '[' + self.get_name() + "](https://eddb.io/station/" + str(self.get_id()) + ")"

    def getEddbUrlHtml(self):
        return '<a href="https://eddb.io/station/' + str(self.get_id()) + '">' + self.get_name() + '</a>'
