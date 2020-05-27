import string
import urllib.parse
from typing import Dict

from PassThroughDict import PassThroughDict
from craid.eddb.Faction import Faction
from craid.eddb.Constants import MINOR_FACTION_ID, POWER_STATE, MINOR_FACTION_PRESENCES
from craid.eddb.NamedItem import NamedItem


class InhabitedSystem(NamedItem):
    # global all_factions_dict

    # idef __init__(self, name='', eddbId=0):
    #    super().__init__(name, eddbId)
    #    self.jsonLine = None

    def __init__(self, jsonString: str):
        #        """
        #
        #        :type jsonString: str
        #        """
        super().__init__(jsonString[NamedItem.NAME], jsonString[NamedItem.ID])
        self.jsonLine = jsonString
        self.hasAnarchy = False
        self.powerState = jsonString[POWER_STATE]

    def getMinorFactionPresences(self):
        return self.jsonLine[MINOR_FACTION_PRESENCES]

    def getFactions(self, all_factions_dict: Dict[int, Faction]):
        ret = []
        minor_faction_presences = self.jsonLine[MINOR_FACTION_PRESENCES]
        # if minor_faction_presences is None
        for faction_ptr in minor_faction_presences:
            if faction_ptr is None:
                continue
            faction_id = faction_ptr[MINOR_FACTION_ID]
            if faction_id is None:
                continue
            curFaction = all_factions_dict.get(faction_id)
            if curFaction is None:
                continue
            ret.append(curFaction)
        return ret

    def hasAnarchyFaction(self, all_factions_dict):
        fList = self.getFactions(all_factions_dict)
        for fac in fList:
            if fac.is_anarchy():
                return True
        return False

    # ======================================================================
    def getAllegiance(self):
        return self.jsonLine['allegiance']

    def getGovernment(self):
        return self.jsonLine['government']

    def getUpdated(self):
        return self.jsonLine['updated_at']

    def getX(self):
        return self.jsonLine['x']

    def getY(self):
        return self.jsonLine['y']

    def getZ(self):
        return self.jsonLine['z']

    def getPowerState(self):
        return self.jsonLine[POWER_STATE]

    def getPower(self):
        return self.jsonLine['power']

    def getPowerLabel(self):
        power = self.getPower()
        powerState = self.getPowerState()
        return f'{power}-{powerState}'

    #
    # Octant of galaxy measured from Etionses
    #
    def getOctant(self) -> int:
        tmp: int = 0
        if self.getX() > 49.5:
            tmp += 1
        if self.getY() > -104:
            tmp += 2
        if self.getZ() > 6.3:
            tmp += 4
        return tmp

    def getPopulation(self):
        return self.jsonLine['population']

    def getControllingFactionId(self):
        return int(self.jsonLine['controlling_minor_faction_id'])

    def isProbablyAGoodBHSystem(self):
        econ = self.jsonLine['primary_economy']
        if not econ:
            return False
        if (not econ.startswith('Extract')) and (
                not econ.startswith('Refine')):
            return False
        return True

    def getInaraNearestShipyardUrl(self):
        return "https://inara.cz/galaxy-nearest/14/" + str(self.get_id())

    def getInaraSystemUrl(self):
        return "https://inara.cz/galaxy-starsystem/" + str(self.get_id()) + "/"

    def getEddbSystemUrl(self):
        return "https://eddb.io/system/" + str(self.get_id())

    def getRoadToRichesUrl(self):
        return "http://edtools.ddns.net/expl.php?s=" + urllib.parse.quote(self.get_name())

    def template(self, msg: str) -> str:
        myDict: PassThroughDict[str, str] = PassThroughDict()

        myDict['system_name'] = self.get_name()
        myDict['allegiance'] = str(self.getAllegiance())
        myDict['government'] = str(self.getGovernment())
        ## FIXME: need faction name
        myDict['controlling_faction'] = "{:,}".format(self.getControllingFactionId())
        myDict['population'] = "{:,}".format(self.getPopulation())
        myDict['inara_link'] = self.getInaraSystemUrl()
        myDict['eddb_link'] = self.getEddbSystemUrl()

        myDict['nearest_shipyard'] = self.getInaraNearestShipyardUrl()
        myDict['r2r_link'] = self.getRoadToRichesUrl()

        myDict['x'] = "{:,}".format(self.getX())
        myDict['y'] = "{:,}".format(self.getY())
        myDict['z'] = "{:,}".format(self.getZ())

        myDict['octant'] = "{:,}".format(self.getOctant())

        bhVal = self.isProbablyAGoodBHSystem()
        bh = "Unknown"
        if bhVal: bh = "Probably"
        myDict['bounty_hunting'] = bh

        myDict['power']       = self.getPower()
        myDict['power_state'] = self.getPowerState()

        template = string.Template(msg)
        output = template.substitute(myDict)
        return output
