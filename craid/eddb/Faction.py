#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

# from InhabitedSystem import InhabitedSystem
from Aware import Aware


class Faction(Aware):
    # systemsDict: None #Dict[int, InhabitedSystem] = None  typing this causes a circular import problem

    # getters/setters for id & name in superclass
    def __init__(self, jsonString):
        super().__init__(jsonString)
        self.club = False

    def get_allegiance(self):
        return self.jsonLine['allegiance']

    def get_government(self):
        return self.jsonLine['government']

    def get_homesystem_id(self):
        return self.jsonLine['home_system_id']

    def get_homesystem_name(self):
        return Aware.getSystemNameById(self.get_homesystem_id())

    # def get_active_states(self):
    #    return json.dumps(self.jsonLine) #[ 'active_states' ]

    def is_anarchy(self):
        return self.get_government() == 'Anarchy'

    def is_federation(self):
        return self.get_allegiance() == 'Federation'

    def is_alliance(self):
        return self.get_allegiance() == 'Alliance'

    def is_empire(self):
        return self.get_allegiance() == 'Empire'

    def is_independent(self):
        return self.get_allegiance() == 'Independent'

    def is_player(self):
        return self.jsonLine['is_player_faction'] is True

    def get_name2(self):
        ret = self._name
        if self.is_player():
            ret = "*" + ret + "*"  ## first one use programmatically, 2nd is trick for markdowwn
        if self.isClub():
            ret = "~~" + ret + "~~"  ## first one use programmatically, 2nd is trick for markdowwn

        return ret

    def factionStringShort(self):
        name = self.get_name2()
        allegiance = self.get_allegiance()[0:3].upper()
        return f'[{allegiance}] - {name}'

    # # FIXME: inara faction ids are different from eddb's arnie may fix
    # def getInaraFactionUrl(self):
    #     return "https://inara.cz/galaxy-minorfaction/" + str(self.get_id())

    def setClub(self, param: bool) -> None:
        print("setting club to :" + str(param))
        self.club = param

    def isClub(self) -> bool:
        return self.club