from craid.dash.queries.CombatZones import CombatZones
from craid.dash.queries.Scouting import Scouting

from craid.dash.queries.TradeExplorationMissions import TradeExplorationMissions


class QueryFactory:

    def __init__(self):
        self.cz = CombatZones()
        self.sc = Scouting()
        self.tem = TradeExplorationMissions()

    def getCombatZonesSort(self):
        return self.cz.getSort()

    def getCombatZonesFilter(self):
        return self.cz.getFilter()

    def getScoutingSort(self):
        return self.sc.getSort()

    def getScoutingFilter(self):
        return self.sc.getFilter()

    def getTradeExplorationMissionsSort(self):
        return self.tem.getSort()

    def getTradeExplorationMissionsFilter(self):
        return self.tem.getFilter()
