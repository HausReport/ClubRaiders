class CombatZones:

    def getFilter(self):
        return "{isHomeSystem} contains false && {distance} < 125 && {vulnerable} contains War"

    def getSort(self):
        return [{'column_id': 'distance', 'direction': 'asc'}]

