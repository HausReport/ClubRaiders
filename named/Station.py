from named.NamedItem import NamedItem

class Station(NamedItem):

    # getters/setters for id & name in superclass
    def __init__(self, jsonString):
        super().__init__(jsonString[ NamedItem.NAME ], jsonString[ NamedItem.ID ])
        self.jsonLine = jsonString
