import datetime
import json
from typing import List, Dict, Tuple

import pandas as pd
from pandas import DataFrame

from craid.club import FactionNameFilter
from craid.eddb.Faction import Faction
from craid.eddb.FactionInstance import FactionInstance
from craid.eddb.InhabitedSystem import InhabitedSystem


# all_stations_dict : Station = {}

def desiredState(state_dict):
    for state in state_dict:
        if (state[ 'id' ] == 64): return 64
        if (state[ 'id' ] == 65): return 65
        if (state[ 'id' ] == 73): return 73
        if (state[ 'id' ] == 96): return 96
        if (state[ 'id' ] == 104): return 104

    return 0


#
# Expensive function - run once, use result many times
#
def getDataArrays():
    # all_factions_dict: Faction                     = {}    #private
    playerFactionIdToInfo: Dict[ int, Faction ] = {}  # private
    clubFactionIdToInfo: Dict[ int, Faction ] = {}  # private
    systemIdToInfo: Dict[ int, InhabitedSystem ] = {}  # private
    allClubSystemInstances: List[ FactionInstance ] = [ ]  # make this one avaiable
    playerFactionNameToSystemName: Dict[ str, str ] = {}
    systemNameToXYZ: Dict[ str, Tuple[ float, float, float ] ] = {}

    with open("../data/factions.jsonl", 'r') as handle:
        for line in handle:
            facLine: dict = json.loads(line)
            lCurFactionId = int(facLine[ 'id' ])
            curFaction = Faction(facLine)
            # all_factions_dict[ lCurFactionId ] = curFaction
            if curFaction.is_player():
                playerFactionIdToInfo[ lCurFactionId ] = curFaction
            if FactionNameFilter.proClubFaction(curFaction):
                clubFactionIdToInfo[ lCurFactionId ] = curFaction

    # with open(stations_file, 'r') as handle:
    #      for line in handle:
    #         station = json.loads(line)
    #         system_id = station[ SYSTEM_ID ]
    #         current_station = stations_dict.get(system_id)

    with open("../data/systems_populated.jsonl", 'r') as handle:
        for line in handle:
            sysLine: dict = json.loads(line)
            tid = int(sysLine[ 'id' ])
            foo = InhabitedSystem(sysLine)
            systemIdToInfo[ tid ] = foo

    #
    # Populate dict of player factions & home system names
    #
    fac: Faction
    for fac in playerFactionIdToInfo.values():
        sid: int = fac.get_homesystem_id()
        tSys: InhabitedSystem = systemIdToInfo.get(sid)
        if (tSys is None): continue
        factionName: str = fac.get_name()
        systemName: str = tSys.get_name()
        if (systemName is None): continue
        # x: float = tSys.getX()
        # y: float = tSys.getY()
        # z: float = tSys.getZ()
        # item = (sName, (x, y, z))
        playerFactionNameToSystemName[ factionName ] = systemName  # (x, y, z)  # .append(item)

    #
    # Populate dict of system name & x,y,zs
    #
    tSys: InhabitedSystem
    for tSys in systemIdToInfo.values():
        if (tSys is None): continue
        factionName: str = tSys.get_name()
        x: float = tSys.getX()
        y: float = tSys.getY()
        z: float = tSys.getZ()
        systemNameToXYZ[ factionName ] = (x, y, z)  # .append(item)

    #
    # Make nifty list of club faction presences
    #
    cSystem: InhabitedSystem
    for cSystem in systemIdToInfo.values():
        mfp = cSystem.getMinorFactionPresences()
        for faction_ptr in mfp:
            if faction_ptr is None:
                continue
            faction_id = int(faction_ptr[ 'minor_faction_id' ])
            if faction_id is None:
                continue
            if faction_id in clubFactionIdToInfo:
                fac = clubFactionIdToInfo[ faction_id ]
                factionName: str = fac.get_name2()
                if factionName.startswith("*"): continue  # filters player factions

                # sysname = cSystem.get_name()
                # factionHomeSystemId: int = fac.get_homesystem_id()
                # vulnerable = True
                # if (systemId == factionHomeSystemId): vulnerable = False

                # systemId = cSystem.get_id()
                # vulnerable = not fac.isHomeSystem(systemId)

                govt = cSystem.getGovernment()
                # allg = fac.get_allegiance()

                inf = faction_ptr[ 'influence' ]
                # sinf = '{:04.2f}'.format(inf)
                # print(sinf)

                # updated = cSystem.getUpdated();
                # date = datetime.datetime.utcfromtimestamp(updated)
                # ds = date.strftime("%m/%d/%Y %H:%M:%S")

                # active_states = json.dumps(faction_ptr[ 'active_states' ])
                hasWar = desiredState(faction_ptr[ 'active_states' ])
                if (govt == "Anarchy"):
                    hasWar = -16
                if (hasWar == 0 and 3.5 >= inf > 0.0):
                    hasWar = -15
                if (hasWar == 104 and inf > 10.0):
                    hasWar = 0

                sysIns = FactionInstance(fac, cSystem, inf, hasWar)
                allClubSystemInstances.append(sysIns)
                # print(factionName + "," + sysname)
                # print("=====================================================================================")
                # print(factionName + "," + sysname + "," + x + "," + y + "," + z + "," + allg + "," + sinf + "," + war+ "," + ds )  # + "," + allg)

    # return [ allClubSystemInstances, xFacList, xSysList, systemIdToInfo ]
    return {'playerFactionIdToInfo': playerFactionIdToInfo,
            'clubFactionIdToInfo': clubFactionIdToInfo,
            'systemIdToInfo': systemIdToInfo,
            'allClubSystemInstances': allClubSystemInstances,
            'systemNameToXYZ': systemNameToXYZ,
            'playerFactionNameToSystemName': playerFactionNameToSystemName
            }


# =========================================================!!!!!!!!!!!!!!!
def getDataFrame(csa: List[ FactionInstance ]) -> object:
    xCoords: List[ int ] = [ ]
    yCoords: List[ int ] = [ ]
    zCoords: List[ int ] = [ ]
    factionName: List[ str ] = [ ]
    systemName: List[ str ] = [ ]
    allegiances: List[ str ] = [ ]
    isHomeSystem: List[ bool ] = [ ]
    population: List[ int ] = [ ]
    influence: List[ float ] = [ ]
    updated: List[ datetime.datetime ] = [ ]
    controlsSystem: List[ bool ] = [ ]
    vulnerableString: List[ str ] = [ ]

    cs: FactionInstance
    for cs in csa:
        factionName.append(cs.get_name())
        systemName.append(cs.getSystemName())
        xCoords.append(cs.getX())
        yCoords.append(cs.getY())
        zCoords.append(cs.getZ())
        allegiances.append(cs.get_allegiance())
        isHomeSystem.append(cs.isHomeSystem())
        population.append(cs.getPopulation())
        influence.append(cs.getInfluence())
        updated.append(cs.getUpdatedDateTime())
        controlsSystem.append(cs.controlsSystem())
        vulnerableString.append(cs.getVulnerableString())

    data = {
        'systemName': systemName,
        'factionName': factionName,
        'x': xCoords,
        'y': yCoords,
        'z': zCoords,
        'allegiance': allegiances,
        'isHomeSystem': isHomeSystem,
        'population': population,
        'influence': influence,
        'updated': updated,
        'control': controlsSystem,
        "vulnerable": vulnerableString
    }

    #
    # Main dataframe of all club factions
    #
    df = pd.DataFrame(data=data)
    return df
