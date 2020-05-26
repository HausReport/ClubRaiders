class CombatZones:

    @staticmethod
    def getFilter(self):
        return "{isHomeSystem} contains false && {distance} < 125 && {vulnerable} contains War"

    @staticmethod
    def getSort():
        return [{'column_id': 'distance', 'direction': 'asc'}]
