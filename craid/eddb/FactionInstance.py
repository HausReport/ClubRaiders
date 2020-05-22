from craid.eddb.Faction import Faction
from craid.eddb.InhabitedSystem import InhabitedSystem
import datetime

class FactionInstance(Faction):

      # getters/setters for id & name in superclass
    def __init__(self, par, xtsys, xinfluence, xvulnerable):
        super().__init__(par.jsonLine)
        self.mySystem: InhabitedSystem = xtsys
        self.influence: float = xinfluence
        self.vulnerable: int = xvulnerable
        #print("Hi")

    def getPopulation(self):
        return self.mySystem.getPopulation()

    def getSystemID(self):
      return self.mySystem.get_id()

    def getSystemName(self):
      return self.mySystem.get_name()
    
    def getUpdated(self):
      return self.mySystem.getUpdated()

    def getUpdatedDateTime(self):
      return datetime.datetime.fromtimestamp( int(self.mySystem.getUpdated()))
    
    def getX(self):
      return self.mySystem.getX()

    def getY(self):
        return self.mySystem.getY()
        
    def getZ(self):
        return self.mySystem.getZ()

    def getInfluence(self):
        return self.influence

    def isVulnerable(self):
      if (self.vulnerable == 0): return False
      return True

    def getVulnerableString(self):
      if(self.vulnerable ==0 ): return "-"
      war = "Civil War"
      if (self.vulnerable == 104): war = "LowInf+Inf Fail"
      if (self.vulnerable == -15): war = "Low Influence"
      if (self.vulnerable == -16): war = "Anarchy"
      if (self.vulnerable == 73): war = "War"
      if (self.vulnerable == 65): war = "Election"
      if (self.vulnerable == 96): war = war + "/Retreat"
      return war

    def getUpdatedString(self):
      updated = self.getUpdated();
      date = datetime.datetime.utcfromtimestamp(updated)
      ds = date.strftime("%d-%b-%Y %H:%M")
      return ds

    def printCSV(self):
      facname = self.get_name2()
      war = self.getVulnerableString()
      sysname = self.getSystemName()
      x = '{:04.2f}'.format(self.getX())
      y = '{:04.2f}'.format(self.getY())
      z = '{:04.2f}'.format(self.getZ())
      sinf = '{:04.2f}'.format(self.getInfluence())
      allg = self.get_allegiance()
      ds = self.getUpdatedString();
      print( facname + "," + sysname + "," + x + "," + y + "," + z + "," + allg + "," + sinf + "," + war + "," + ds)  # + "," + allg)

    def asArray(self):
      facname = self.get_name2()
      war = self.getVulnerableString()
      sysname = self.getSystemName()
      x = '{:04.2f}'.format(self.getX())
      y = '{:04.2f}'.format(self.getY())
      z = '{:04.2f}'.format(self.getZ())
      sinf = '{:04.2f}'.format(self.getInfluence())
      allg = self.get_allegiance()
      ds = self.getUpdatedString()
      return [facname,sysname,x,y,z,allg,sinf,war,ds]

    def isHomeSystem(self):
        factionHomeSystemId: int = self.get_homesystem_id()
        systemId = self.getSystemID()
        hs = True
        if (systemId == factionHomeSystemId): hs = False
        return hs

    def controlsSystem(self):
        cid = self.mySystem.getControllingFactionId()
        mid: int = int(self.get_id())
        return cid == mid
