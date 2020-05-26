from craid.dashbd.queries.CombatZones import CombatZones
from craid.dashbd.queries.Scouting import Scouting

from craid.dashbd.queries.TradeExplorationMissions import TradeExplorationMissions


class QueryFactory:
    cz = CombatZones()
    sc = Scouting()
    tem = TradeExplorationMissions()

    @staticmethod
    def getCombatZonesSort():
        return CombatZones.getSort()

    @staticmethod
    def getCombatZonesFilter():
        return CombatZones.getFilter()

    @staticmethod
    def getScoutingSort():
        return Scouting.getSort()

    @staticmethod
    def getScoutingFilter():
        return Scouting.getFilter()

    @staticmethod
    def getTradeExplorationMissionsSort():
        return TradeExplorationMissions.getSort()

    @staticmethod
    def getTradeExplorationMissionsFilter():
        return TradeExplorationMissions.getFilter()
