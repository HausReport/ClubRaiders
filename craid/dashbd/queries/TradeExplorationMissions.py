class TradeExplorationMissions:

    @staticmethod
    def getFilter(self):
        return "{isHomeSystem} contains false && {distance} < 125"

    @staticmethod
    def getSort(self):
        return [{'column_id': 'influence', 'direction': 'asc'}]
