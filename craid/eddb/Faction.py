#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

# from InhabitedSystem import InhabitedSystem
from typing import Dict

from craid.eddb.Aware import Aware
from eddb.NamedItem import NamedItem


class Faction(Aware):

    # getters/setters for id & name in superclass
    def __init__(self, obj, fromFaction: bool=False):

        self.club = False
        if not fromFaction:
            jsonString : Dict = obj
            name = jsonString[NamedItem.NAME]
            id = jsonString[NamedItem.ID]
            super().__init__(name, id)
            self.allegiance = jsonString['allegiance']
            self.government = jsonString['government']
            self.homesystem_id = jsonString['home_system_id']
            self.player = jsonString['is_player_faction']
        else:
            tfac: Faction = obj
            super().__init__(tfac.get_name(), tfac.get_id())
            self.allegiance = tfac.allegiance
            self.government = tfac.government
            self.homesystem_id = tfac.homesystem_id
            self.player = tfac.player

    #
    # Picked off the jsonLine
    #
    def get_allegiance(self):
        return self.allegiance

    def get_government(self):
        return self.government

    def get_homesystem_id(self):
        return self.homesystem_id

    def is_player(self):
        return self.player

    #
    # Don't use the jsonLine
    #
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
        # print("setting club to :" + str(param))
        self.club = param

    def isClub(self) -> bool:
        return self.club
