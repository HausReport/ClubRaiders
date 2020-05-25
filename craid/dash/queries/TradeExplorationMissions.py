class TradeExplorationMissions:

    def getFilter(self):
        return "{isHomeSystem} contains false && {distance} < 125"

    def getSort(self):
        return [{'column_id': 'influence', 'direction': 'asc'}]

