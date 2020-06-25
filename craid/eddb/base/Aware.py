#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
#
#   SPDX-License-Identifier: BSD-3-Clause

from typing import Dict

from craid.eddb.base.NamedItem import NamedItem


class Aware(NamedItem):
    systemsDict: Dict[int, object] = None  # Sidestepping circular imports
    factionsDict: Dict[int, object] = None  # Sidestepping circular imports

    # # getters/setters for id & name in superclass
    # def __init__(self, jsonString):
    #     super().__init__(jsonString[NamedItem.NAME], jsonString[NamedItem.ID])

    # getters/setters for id & name in superclass
    def __init__(self, name: str, _id: int):
        super().__init__(name, _id)

    @staticmethod
    def setSystemsDict(foo: Dict):  # [int, craid.eddb.InhabitedSystem]):
        from craid.eddb.system.InhabitedSystem import InhabitedSystem
        Aware.systemsDict: Dict[int, InhabitedSystem] = foo

    @staticmethod
    def setFactionsDict(foo: Dict):
        from craid.eddb.faction.Faction import Faction
        Aware.factionsDict: Dict[int, Faction] = foo

    @staticmethod
    def getSystemNameById(sysId: int):
        from craid.eddb.system.InhabitedSystem import InhabitedSystem
        sys: InhabitedSystem = Aware.systemsDict.get(sysId)
        if sys is None:
            return "Unknown-" + str(sysId)
        # assert sys is not None, "Invalid system, id: " + str(sysId)
        return sys.get_name()

    @staticmethod
    def getSystemById(sysId: int):
        from craid.eddb.system.InhabitedSystem import InhabitedSystem
        sys: InhabitedSystem = Aware.systemsDict.get(sysId)
        return sys

    @staticmethod
    def getFactionNameById(facId: int):
        from craid.eddb.faction.Faction import Faction
        # sd Dict[int, Faction] = Aware.factionsDict
        fac: Faction = Aware.factionsDict.get(facId)
        if fac is None:
            return "Unknown-" + str(facId)
        # assert fac is not None, "Invalid faction, id: " + str(facId)
        return fac.get_name()

    @staticmethod
    def getFactionById(facId: int):
        from craid.eddb.faction.Faction import Faction
        # sd Dict[int, Faction] = Aware.factionsDict
        fac: Faction = Aware.factionsDict.get(facId)
        return fac
