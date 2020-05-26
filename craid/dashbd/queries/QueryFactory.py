from craid.dash.queries.CombatZones import CombatZones
from craid.dash.queries.Scouting import Scouting

from craid.dash.queries.TradeExplorationMissions import TradeExplorationMissions


class QueryFactory:

    def __init__(self):
        self.cz = CombatZones()
        self.sc = Scouting()
        self.tem = TradeExplorationMissions()

    def getCombatZonesSort(self):
        return CombatZones.getSort()

    def getCombatZonesFilter(self):
        return CombatZones.getFilter()

    def getScoutingSort(self):
        return Scouting.getSort()

    def getScoutingFilter(self):
        return Scouting.getFilter()

    def getTradeExplorationMissionsSort(self):
        return TradeExplorationMissions.getSort()

    def getTradeExplorationMissionsFilter(self):
        return TradeExplorationMissions.getFilter()
