import datetime

from craid.eddb.Vulnerability import Vulnerability
from craid.eddb.Faction import Faction
from craid.eddb.InhabitedSystem import InhabitedSystem


class FactionInstance(Faction):

    # getters/setters for id & name in superclass
    def __init__(self, par, inhabSys: InhabitedSystem, inf: float, vuln: Vulnerability):
        super().__init__(par.jsonLine)
        self.mySystem: InhabitedSystem = inhabSys
        self.influence: float = inf
        self.vulnerable: Vulnerability = vuln
        # print("Hi")

    def getInaraFactionUrl(self):
        return "https://inara.cz/galaxy-minorfaction/" + self.getFactionID()

    def getFactionID(self):
        return self.get_id()

    def getPopulation(self):
        return self.mySystem.getPopulation()

    def getSystemID(self):
        return self.mySystem.get_id()

    def getSystemName(self):
        return self.mySystem.get_name()

    def getUpdated(self):
        return self.mySystem.getUpdated()

    # <1, A single player can easily retreat
    # 1-100, A single player can retreatA
    # >50, Recommended for small groups
    # >100, requires significant team
    # excel formula = (D10/15000)*(E10^2)/ 1000
    # d=pop, e = inf
    def getDifficulty(self) -> float:
        max = 999999.0
        if not self.canRetreat():
            return max
        e10 = self.getInfluence()
        if e10 == 0.0:
            return max
        d10 = self.getPopulation()
        ret = (d10 / 15000.0) * (e10 ** 2.0) / 1000.0

        if(ret<0.0): ret = 0.0
        if(ret>max): ret = max
        return round(ret,1)  #TODO: trimmed to 3 decimals since no format support

    def getDifficultyString(self) -> str:
        val = self.getDifficulty()
        # "Forcing a retreat from this system would "
        if val<.5   : return "be extremely easy for one commander"
        if val<1   : return "be very easy for one commander"
        if val<10   : return "be easy for one commander"
        if val<25   : return "be easy"
        if val<50   : return "take some work for one commander"
        if val<100   : return "be possible for one commander"
        if val<1000   : return "require group effort"
        if val<10000 : return "require a gargantuan effort"
        if val<100000 : return "be well-nigh impossible"
        return "seem an impossibility"

    def canRetreat(self) -> bool:
        if self.isHomeSystem(): return False

        # TODO: handle special cases here

        return True

    def getUpdatedDateTime(self):
        return datetime.datetime.fromtimestamp(int(self.mySystem.getUpdated()))

    def getX(self):
        return self.mySystem.getX()

    def getY(self):
        return self.mySystem.getY()

    def getZ(self):
        return self.mySystem.getZ()

    def getInfluence(self):
        return self.influence

    #
    # Vulnerability is a Frankenstein's Monster atm,
    # but it will take some thought to work out.
    #
    # At the moment, it's determined on data load.
    #
    #def isVulnerable(self):
    #    return self.vulnerable is not 0

    def getVulnerableString(self):
        assert self.vulnerable is not None, 'null vulnerable'
        retval: str = self.vulnerable.getShortString()
        assert retval is not None, 'null vulnerable 2'
        return retval


        # if (self.vulnerable == 0): return ""
        # war = "Civil War"
        # if (self.vulnerable == 104): war = "LowInf+Inf Fail"
        # if (self.vulnerable == -15): war = "Low Influence"
        # if (self.vulnerable == -16): war = "Anarchy"
        # if (self.vulnerable == 73): war = "War"
        # if (self.vulnerable == 65): war = "Election"
        # if (self.vulnerable == 96): war = war + "/Retreat"
        # return war
        #
        # # "16,Boom"
        # # "32,Bust"
        # # "37,Famine"
        # # "48,Civil Unrest"
        # # "64,Civil War"
        # # "65,Election"
        # # "66,Civil Liberty"
        # # "67,Expansion"
        # # "69,Lockdown"
        # # "72,Outbreak"
        # # "73,War"
        # # "80,None"
        # # "81,Pirate Attack"
        # # "101,Investment"
        # # "102,Blight"
        # # "103,Drought"
        # # "104,Infrastructure Failure"
        # # "105,Natural Disaster"
        # # "106,Public Holiday"
        # # "107,Terrorist Attack"

    def getUpdatedString(self):
        updated = self.getUpdated()
        date = datetime.datetime.utcfromtimestamp(updated)
        ds = date.strftime("%d-%b-%Y %H:%M")
        return ds

    def printCSV(self):
        facname = self.get_name2()
        war = self.getVulnerableString()
        sysname = self.getSystemName()
        x = '{:04.2f}'.format(self.getX())
        y = '{:04.2f}'.format(self.getY)
        z = '{:04.2f}'.format(self.getZ)
        sinf = '{:04.2f}'.format(self.getInfluence)
        allg = self.get_allegiance()
        ds = self.getUpdatedString()
        print(f"{facname},{sysname},{x},{y},{z},{allg},{sinf},{war},{ds}")
        #    facname + "," + sysname + "," + x + "," + y + "," + z + "," + allg +
        #    "," + sinf + "," + war + "," + ds)  # + "," + allg)

    def asArray(self):
        facname = self.get_name2()
        war = self.getVulnerableString()
        sysname = self.getSystemName()
        x = '{:04.2f}'.format(self.getX())
        y = '{:04.2f}'.format(self.getY)
        z = '{:04.2f}'.format(self.getZ)
        sinf = '{:04.2f}'.format(self.getInfluence)
        allg = self.get_allegiance()
        ds = self.getUpdatedString()
        return [facname, sysname, x, y, z, allg, sinf, war, ds]

    def isHomeSystem(self):
        factionHomeSystemId: int = self.get_homesystem_id()
        systemId = self.getSystemID()
        return systemId == factionHomeSystemId

    def controlsSystem(self):
        cid = self.mySystem.getControllingFactionId()
        mid: int = int(self.get_id())
        return cid == mid
