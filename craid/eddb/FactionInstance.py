#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

import datetime
import string

from PassThroughDict import PassThroughDict
from craid.eddb.Faction import Faction
from craid.eddb.InhabitedSystem import InhabitedSystem
from craid.eddb.States import States


class FactionInstance(Faction):

    # getters/setters for id & name in superclass
    def __init__(self, par, inhabSys: InhabitedSystem, inf: float, vuln: States):
        super().__init__(par.jsonLine)
        self.mySystem: InhabitedSystem = inhabSys
        self.influence: float = inf
        self.states: States = vuln

    def getSystem(self):
        return self.mySystem

    def getFactionID(self):
        return self.get_id()

    def getPopulation(self):
        return self.mySystem.getPopulation()

    def getSystemID(self):
        return self.mySystem.get_id()

    def getSystemName(self):
        return self.mySystem.get_name()

    def getSystemNameById(self, _id):
        return super().getSystemNameById()

    #def getUpdated(self):
    #    return self.mySystem.getUpdated()

    # <1, A single player can easily retreat
    # 1-100, A single player can retreatA
    # >50, Recommended for small groups
    # >100, requires significant team
    # excel formula = (D10/15000)*(E10^2)/ 1000
    # d=pop, e = inf
    def getDifficulty(self) -> float:
        theMax = 999999.0
        if not self.canRetreat():
            return theMax
        e10 = self.getInfluence()
        if e10 == 0.0:
            return theMax
        d10 = self.getPopulation()
        ret = (d10 / 15000.0) * (e10 ** 2.0) / 1000.0

        if ret < 0.0:
            ret = 0.0
        if ret > theMax:
            ret = theMax
        return round(ret, 1)  # TODO: trimmed to 3 decimals since no format support

    def getDifficultyString(self) -> str:
        val = self.getDifficulty()
        # "Forcing a retreat from this system would "
        if val < .5: return "be extremely easy for one commander"
        if val < 1: return "be very easy for one commander"
        if val < 10: return "be easy for one commander"
        if val < 25: return "be easy"
        if val < 50: return "take some work for one commander"
        if val < 100: return "be possible for one commander"
        if val < 1000: return "require group effort"
        if val < 10000: return "require a gargantuan effort"
        if val < 100000: return "be well-nigh impossible"
        return "seem an impossibility"

    def canRetreat(self) -> bool:
        if self.isHomeSystem(): return False

        # TODO: handle special cases here

        return True

    def getUpdatedDateTime(self) -> datetime:
        return self.mySystem.getUpdatedDateTime()

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
    # def isVulnerable(self):
    #    return self.vulnerable is not 0

    def getVulnerableString(self):
        assert self.states is not None, 'null vulnerable'
        retval: str = self.states.getShortString()
        assert retval is not None, 'null vulnerable 2'
        return retval

    def getUpdatedString(self):
        date = self.mySystem.getUpdatedDateTime()
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

    def isHomeSystem(self) -> bool:
        factionHomeSystemId: int = self.get_homesystem_id()
        systemId = self.getSystemID()
        return systemId == factionHomeSystemId

    def controlsSystem(self) -> bool:
        cid = self.mySystem.getControllingFactionId()
        mid: int = int(self.get_id())
        return cid == mid

    def template(self, msg: str) -> str:
        myDict: PassThroughDict[str, str] = PassThroughDict()

        myDict['home_system'] = self.get_homesystem_name()
        myDict['allegiance'] = str(self.get_allegiance())
        myDict['government'] = str(self.get_government())
        #myDict['inara_link'] = self.getInaraFactionUrl()
        myDict['faction_name'] = self.get_name2()

        template = string.Template(msg)
        output = template.substitute(myDict)
        return output

    def hasSate(self, state: int):
        return self.states.hasState(state)
