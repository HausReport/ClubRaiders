#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

from Aware import Aware


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

# No Good for us
# "type_id": 23, "type": "Non-Dockable Orbital",

class Station(Aware):

    # getters/setters for id & name in superclass
    def __init__(self, jsonString: str):
        super().__init__(jsonString)  # [NamedItem.NAME], jsonString[NamedItem.ID])
        # self.jsonLine: Dict[str, str] = jsonString
        # self.jsonLine = jsonString
        self.club: bool = False

    def getDistanceToStar(self) -> int:
        xxx = self.jsonLine.get('distance_to_star')
        if xxx is None: return -999999
        return int(xxx)

    def hasLargePads(self) -> bool:
        # if not self.hasDocking() : return False
        xxx = self.jsonLine.get('max_landing_pad_size')
        if xxx is None: return False
        return xxx == "L"

    def hasMarket(self) -> bool:
        xxx: bool = self.jsonLine.get("has_market")
        return xxx

    def hasBlackMarket(self) -> bool:
        xxx: bool = self.jsonLine.get('has_black_market')
        return xxx

    def hasShipyard(self) -> bool:
        xxx: bool = self.jsonLine.get('has_shipyard')
        return xxx

    def hasDocking(self) -> bool:
        xxx: bool = self.jsonLine.get('has_docking')
        return xxx

    def isOrbital(self) -> bool:
        return not self.isPlanetary()

    def isPlanetary(self) -> bool:
        xxx: bool = self.jsonLine.get('is_planetary')
        return xxx
        # return self.jsonLine['body'] is not None

    def okCandidate(self) -> bool:
        if not self.hasDocking():
            return False
        if self.jsonLine['controlling_minor_faction'] is None:
            return False
        return True

    def getTypeString(self) -> str:
        return self.jsonLine['type']

    # def getTypeString(self) -> str:
    # return self.jsonLine['type']

    def getControllingFactionId(self) -> int:
        zzz: int = int(self.jsonLine['controlling_minor_faction_id'])
        ##print("cf id: " + str(zzz))
        return zzz

    def getControllingFactionName(self) -> str:
        return Aware.getFactionNameById(self.getControllingFactionId())

    def getControllingFactionName2(self) -> str:
        from Faction import Faction
        fac: Faction = Aware.getFactionById(self.getControllingFactionId())
        return fac.get_name2()

    def setClub(self, param: bool):
        #print("setting club to :" + str(param))
        self.club = param

    def isClub(self) -> bool:
        return self.club

    ## FIXME: miners_tool urls are pretty obfuscated, too
    # FIXME: this is pretty obfuscated, don't see how it works yet
    #    def getEddbSellToUrl(self):
    #        https: // eddb.io / trade / single / sellSystemId = & sellStationId =
    def getEddbUrl(self):
        return '[' + self.get_name() + "](https://eddb.io/station/" + str(self.get_id()) + ")"

    def getEddbUrlHtml(self):
        return '<a href="https://eddb.io/station/' + str(self.get_id()) + '">' + self.get_name() + '</a>'
