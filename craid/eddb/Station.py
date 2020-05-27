from craid.eddb.NamedItem import NamedItem

# Currently known Types

# Usually good for us
#"type_id": 3, "type": "Coriolis Starport",
#"type_id": 8, "type": "Orbis Starport",
#"type_id": 7, "type": "Ocellus Starport",
#"type_id": 19, "type": "Megaship",
#"type_id": 20, "type": "Asteroid Base",

# I think these are medium orbital + planetary
#"type_id": 13, "type": "Planetary Outpost",
#"type_id": 4, "type": "Industrial Outpost",
#"type_id": 1, "type": "Civilian Outpost",
#"type_id": 16, "type": "Planetary Settlement",
#"type_id": 6, "type": "Mining Outpost",
#"type_id": 14, "type": "Planetary Port",
#"type_id": 2, "type": "Commercial Outpost",
#"type_id": 9, "type": "Scientific Outpost",
#"type_id": 5, "type": "Military Outpost",

# No Good for us
#"type_id": 23, "type": "Non-Dockable Orbital",

class Station(NamedItem):

    # getters/setters for id & name in superclass
    def __init__(self, jsonString):
        super().__init__(jsonString[NamedItem.NAME], jsonString[NamedItem.ID])
        self.jsonLine = jsonString

    def getDistanceToStar(self) -> int:
        return int(self.jsonLine['distance_to_star'])

    def hasLargePads(self) -> bool:
        return self.jsonLine['max_landing_pad_size'] == "L"

    def hasMarket(self) -> bool:
        return self.jsonLine['has_market'] == "true"

    def hasBlackMarket(self) -> bool:
        return self.jsonLine['has_black_market'] == "true"

    def hasShipyard(self) -> bool:
        return self.jsonLine['has_shipyard'] == "true"

    def hasDocking(self) -> bool:
        return self.jsonLine['has_docking'] == "true"

    def isOrbital(self) -> bool:
        return not self.isPlanetary()

    def isPlanetary(self) -> bool:
        if self.jsonLine['is_planetary']: return True
        return False
        #return self.jsonLine['body'] is not None

    def okCandidate(self) -> bool:
        if not self.hasDocking(): return False

    def getTypeString(self) -> str:
        return self.jsonLine['type']

    def getTypeString(self) -> str:
        return self.jsonLine['type']



    # def getc_allegiance(self):
    #     return self.jsonLine['allegiance']
    # def getc_allegiance(self):
    #     return self.jsonLine['allegiance']
    # def getc_allegiance(self):
    #     return self.jsonLine['allegiance']