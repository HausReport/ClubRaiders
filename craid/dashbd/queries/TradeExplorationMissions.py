class TradeExplorationMissions:

    @staticmethod
    def getFilter():
        return "{isHomeSystem} contains false && {distance} < 125"

    @staticmethod
    def getSort():
        return [{'column_id': 'influence', 'direction': 'asc'}]
