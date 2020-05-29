import math
import pprint
import string
import urllib.parse
from datetime import datetime, timedelta
from typing import Dict, List

from Aware import Aware
from PassThroughDict import PassThroughDict
from Station import Station
from TextDecoration import boolToTorBlank, boolToYesOrNo
from craid.eddb.Constants import MINOR_FACTION_ID, POWER_STATE, MINOR_FACTION_PRESENCES
from craid.eddb.Faction import Faction


class InhabitedSystem(Aware):

    def __init__(self, jsonString: str):
        super().__init__(jsonString)  # [NamedItem.NAME], jsonString[NamedItem.ID])
        # self.jsonLine: str = jsonString
        self.hasAnarchy: bool = False
        self.powerState: str = jsonString[POWER_STATE]
        self.stations: List[Station] = []

    def getControllingFactionName(self):
        cf: int = self.getControllingFactionId()
        return super().getFactionNameById(cf)

    def getMinorFactionPresences(self):
        return self.jsonLine[MINOR_FACTION_PRESENCES]

    def getMinorFactionsAsMarkdown(self):
        foo: Dict[int, Faction] = self.getMinorFactionsAsDict()

        ret: str = "\n\n"
        f: Faction
        for f in foo.values():
            pre: str = f.get_name2()  # adds * for pf
            if pre.startswith("*"):
                pre = pre + "*"  # italicize it

            # TODO: signify club factions somehow..  interesting idea
            # was to redefine strikethru (s in css) to display as orangered
            # with no decoration - tilde and <s> don't work </s>
            ret = ret + "\n*  " + pre

        return ret + "\n\n"

    def getMinorFactionsAsDict(self):
        ret: Dict[int, Faction] = {}
        mfp: Dict = self.getMinorFactionPresences()
        for faction_ptr in mfp:
            faction_id: int = int(faction_ptr['minor_faction_id'])
            fac: Faction = super().getFactionById(faction_id)
            if fac is not None:
                ret[faction_id] = fac

        #pprint.pprint( ret )
        print(" mfd size = " + str(len(list(mfp))))
        print(" ret size = " + str(len(list(ret.keys()))))
        return ret

    def getFactions(self, all_factions_dict: Dict[int, Faction]):
        ret = []
        minor_faction_presences = self.jsonLine[MINOR_FACTION_PRESENCES]
        # if minor_faction_presences is None
        for faction_ptr in minor_faction_presences:
            if faction_ptr is None:
                continue
            faction_id: int = int(faction_ptr[MINOR_FACTION_ID])
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
    def getAllegiance(self) -> str:
        return self.jsonLine['allegiance']

    def getGovernment(self) -> str:
        return self.jsonLine['government']

    def getX(self) -> float:
        return float(self.jsonLine['x'])

    def getY(self) -> float:
        return float(self.jsonLine['y'])

    def getZ(self) -> float:
        return float(self.jsonLine['z'])

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

    def getPopulation(self) -> int:
        return int(self.jsonLine['population'])

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

    def getUpdated(self) -> str:
        return self.jsonLine['updated_at']

    def needsPermit(self) -> bool:
        prm :bool = self.jsonLine.get('needs_permit')
        return prm

    def getUpdatedDateTime(self) -> datetime:
        return datetime.utcfromtimestamp(self.getUpdated())

    def getUpdatedString(self) -> str:
        upd = self.getUpdatedDateTime()
        now = datetime.utcnow()  # timezone.utc)
        time_elapsed: timedelta = now - upd
        days = time_elapsed.days

        if days <= 1:
            return "Scouted within the last day."

        if days <= 6:
            return "Scouted within the last " + str(days) + " days."

        weeks = math.ceil(days / 7)
        if weeks <= 6:
            return "*Scouted " + str(weeks) + " weeks ago.*"

        return "**Really, really needs to be scouted.**"

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
        myDict['controlling_faction'] = self.getControllingFactionName()
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

        bhVal = self.isProbablyAGoodBHSystem()
        bh = "Unknown"
        if bhVal: bh = "Probably"
        myDict['bounty_hunting'] = bh

        myDict['power'] = self.getPower()
        myDict['power_state'] = self.getPowerState()

        myDict['scouting_msg'] = self.getUpdatedString()

        myDict['station_list'] = self.getStationsTableString()

        myDict['faction_list'] = self.getMinorFactionsAsMarkdown()

        myDict['needs_permit'] = boolToYesOrNo(self.needsPermit())



        template = string.Template(msg)
        output  = template.substitute(myDict)
        return output

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
        ret += "|Name | ls | Orb | LPad | Club | Yard | BM | CF | \n"
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
            ret += sta.getControllingFactionName()
            ret += "  | "
            ret += "\n"

        theret = ret + "\n\n\n"
        # print(theret)
        return theret

    # def appendStationsTableToStringOld(self, targ: str) -> str:
    #     ret: str = ""
    #
    #     ret = "\n\n\n<table>\n"
    #     for sta in self.stations:
    #         ret += "\t<tr>\n"
    #         ret += "\t\t<td>"
    #         ret += sta.get_name()
    #         ret += "</td>\n"
    #         ret += "\t\t<td>"
    #         ret += str(sta.get_id())
    #         ret += "</td>\n"
    #         ret += "\t\t<td>"
    #         ret += str(sta.getDistanceToStar())
    #         ret += "</td>\n"
    #         ret += "\t\t<td>"
    #         ret += str(sta.hasLargePads())
    #         ret += "</td>\n"
    #         ret += "\t\t<td>"
    #         ret += str(sta.isClub())
    #         ret += "</td>\n"
    #         ret += "\t\t<td>"
    #         ret += str(sta.hasShipyard())
    #         ret += "</td>\n"
    #         ret += "\t\t<td>"
    #         ret += str(sta.hasBlackMarket())
    #         ret += "</td>\n"
    #         ret += "\t</tr>\n"
    #
    #     ret += "</table>\n"
    #     theret = targ + ret  + "\n\n\n"
    #     print(theret)
    #     return theret
