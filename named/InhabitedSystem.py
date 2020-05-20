from named.Constants import MINOR_FACTION_ID, POWER_STATE, GOVERNMENT, MINOR_FACTION_PRESENCES, HAS_ANARCHY

from named.NamedItem import NamedItem


class InhabitedSystem(NamedItem):
    global all_factions_dict

    def __init__(self, name='', id=0):
        super().__init__(name, id)

    def __init__(self, jsonString):
        super().__init__(jsonString[ NamedItem.NAME ], jsonString[ NamedItem.ID ])
        self.jsonLine = jsonString
        self.hasAnarchy = False
        self.powerState = jsonString[ POWER_STATE ]

    def isProbablyAGoodBHSystem(self):
        if not self.jsonLine[ 'primary_economy' ]:
            return False
        if (not self.jsonLine[ 'primary_economy' ].startswith('Extract')) and (
                not self.jsonLine[ 'primary_economy' ].startswith('Refine')):
            return False
        return True

    def getMinorFactionPresences(self):
        return self.jsonLine[ MINOR_FACTION_PRESENCES ]

    def getFactions(self):
        ret = [ ]
        minor_faction_presences = self.jsonLine[ MINOR_FACTION_PRESENCES ]
        # if minor_faction_presences is None
        for faction_ptr in minor_faction_presences:
            if faction_ptr is None:
                continue
            faction_id = faction_ptr[ MINOR_FACTION_ID ]
            if faction_id is None:
                continue
            curFaction = all_factions_dict.get(faction_id)
            if curFaction is None:
                continue
            ret.append(curFaction)
        return ret


    def hasAnarchyFaction(self):
        fList = self.getFactions()
        for fac in fList:
            if fac.is_anarchy():
                return True
        return False

    # ======================================================================
    def getGovernment(self):
        return self.jsonLine[ 'government' ]

    def getUpdated(self):
        return self.jsonLine[ 'updated_at' ]

    def getX(self):
        return self.jsonLine[ 'x' ]

    def getY(self):
        return self.jsonLine[ 'y' ]
        
    def getZ(self):
        return self.jsonLine[ 'z' ]

    def getPowerState(self):
        return self.jsonLine[ POWER_STATE ]

    def getPower(self):
        return self.jsonLine[ 'power' ]

    def getPowerLabel(self):
        power = self.getPower()
        powerState = self.getPowerState()
        return f'{power}-{powerState}'

    def getSystemLine(self):
        name = self.jsonLine[ 'name' ]
        dist = 0  # str(round(self.jsonLine[ 'dist' ], 1))
        # id = str(self.jsonLine[ ID ])
        # nCount = str(self.jsonLine[ NEIGHBOR_COUNT ])
        # hasAnarchy = str(self.jsonLine[ HAS_ANARCHY ])
        # stationString = "empty"
        power = self.getPowerLabel()
        return f'{name} ({dist}ly) - {power}'
