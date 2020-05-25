from craid.eddb.NamedItem import NamedItem


class Faction(NamedItem):

    # getters/setters for id & name in superclass
    def __init__(self, jsonString):
        super().__init__(jsonString[NamedItem.NAME], jsonString[NamedItem.ID])
        self.jsonLine = jsonString

    def get_allegiance(self):
        return self.jsonLine['allegiance']

    def get_government(self):
        return self.jsonLine['government']

    def get_homesystem_id(self):
        return self.jsonLine['home_system_id']

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
        p_ind = ""
        if self.is_player():
            p_ind = "*"
        return p_ind + self._name

    def factionStringShort(self):
        name = self.get_name2()
        allegiance = self.get_allegiance()[0:3].upper()
        return f'[{allegiance}] - {name}'
