from typing import Dict

from NamedItem import NamedItem


class Aware(NamedItem):
    systemsDict : Dict[int, object] = None #=  None #Dict[int, InhabitedSystem] = None  typing this causes a circular import problem
    factionsDict: Dict[int, object] = None #=  None # Dict[int, Faction] = None

    # getters/setters for id & name in superclass
    def __init__(self, jsonString):
        super().__init__(jsonString[NamedItem.NAME], jsonString[NamedItem.ID])
        self.jsonLine = jsonString

    @staticmethod
    def setSystemsDict( foo: Dict): #[int, craid.eddb.InhabitedSystem]):
        from InhabitedSystem import InhabitedSystem
        Aware.systemsDict: Dict[int,InhabitedSystem] = foo

    @staticmethod
    def setFactionsDict(foo: Dict):
        from Faction import Faction
        Aware.factionsDict: Dict[int,Faction] = foo

    @staticmethod
    def getSystemNameById(sysId: int):
        from InhabitedSystem import InhabitedSystem
        sys: InhabitedSystem = Aware.systemsDict.get(sysId)
        if sys is None:
            return "Unknown-" + str(sysId)
        #assert sys is not None, "Invalid system, id: " + str(sysId)
        return sys.get_name()

    @staticmethod
    def getFactionNameById(facId: int):
        from Faction import Faction
        #sd Dict[int, Faction] = Aware.factionsDict
        fac: Faction = Aware.factionsDict.get(facId)
        if fac is None:
            return "Unknown-" + str(facId)
        #assert fac is not None, "Invalid faction, id: " + str(facId)
        return fac.get_name()