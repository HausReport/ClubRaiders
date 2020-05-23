import datetime
import json
from typing import List

import pandas as pd
from craid import Club
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


def getSystemsArray():
    #all_factions_dict: Faction         = {}    #private
    player_factions_dict: Faction       = {}    #private
    club_factions_dict: Faction         = {}    #private
    all_systems_dict: InhabitedSystem   = {}    #private
    club_systems_arr: FactionInstance   = []    #make this one avaiable

    with open("data/factions.jsonl", 'r') as handle:
        for line in handle:
            lCurFaction = json.loads(line)
            lCurFactionId = int(lCurFaction[ 'id' ])
            curFaction = Faction(lCurFaction)
            #all_factions_dict[ lCurFactionId ] = curFaction
            if curFaction.is_player():
                player_factions_dict[ lCurFactionId ] = curFaction
            if Club.proClubFaction(curFaction):
                club_factions_dict[ lCurFactionId ] = curFaction

    # with open(stations_file, 'r') as handle:
    #      for line in handle:
    #         station = json.loads(line)
    #         system_id = station[ SYSTEM_ID ]
    #         current_station = stations_dict.get(system_id)

    with open("data/systems_populated.jsonl", 'r') as handle:
        for line in handle:
            sys = json.loads(line)
            tid = int(sys[ 'id' ])
            foo = InhabitedSystem(sys)
            all_systems_dict[ tid ] = foo


    #
    # Populate list of player factions & x,y,zs
    #
    xFacList = []
    fac: Faction
    for fac in player_factions_dict.values():
        sid = fac.get_homesystem_id()
        sys: InhabitedSystem = all_systems_dict.get(sid)
        if(sys is None): continue
        sName :str = sys.get_name()
        x :float = sys.getX()
        y :float = sys.getY()
        z :float = sys.getZ()
        item = (sName, (x, y, z))
        xFacList.add(item)
    #
    # Make nifty list of club faction presences
    #
    cSystem: InhabitedSystem
    for cSystem in all_systems_dict.values():
        mfp = cSystem.getMinorFactionPresences()
        for faction_ptr in mfp:
            if faction_ptr is None:
                continue
            faction_id = int(faction_ptr[ 'minor_faction_id' ])
            if faction_id is None:
                continue
            if faction_id in club_factions_dict:
                fac = club_factions_dict[ faction_id ]
                factionName: str = fac.get_name2()
                if factionName.startswith("*"): continue  # filters player factions

                #sysname = cSystem.get_name()
                #factionHomeSystemId: int = fac.get_homesystem_id()
                #vulnerable = True
                #if (systemId == factionHomeSystemId): vulnerable = False


                #systemId = cSystem.get_id()
                #vulnerable = not fac.isHomeSystem(systemId)

                govt = cSystem.getGovernment()
                # allg = fac.get_allegiance()

                inf = faction_ptr[ 'influence' ]
                # sinf = '{:04.2f}'.format(inf)
                # print(sinf)

                # updated = cSystem.getUpdated();
                # date = datetime.datetime.utcfromtimestamp(updated)
                # ds = date.strftime("%m/%d/%Y %H:%M:%S")

                #active_states = json.dumps(faction_ptr[ 'active_states' ])
                hasWar = desiredState(faction_ptr[ 'active_states' ])
                if (govt == "Anarchy"):
                    hasWar = -16
                if (hasWar == 0 and inf <= 3.5 and inf > 0.0):
                    hasWar = -15
                if (hasWar == 104 and inf > 10.0):
                    hasWar = 0

                sysIns = FactionInstance(fac, cSystem, inf, hasWar)
                club_systems_arr.append(sysIns)
                # print(factionName + "," + sysname)
                # print("=====================================================================================")
                # print(factionName + "," + sysname + "," + x + "," + y + "," + z + "," + allg + "," + sinf + "," + war+ "," + ds )  # + "," + allg)

    return [club_systems_arr, xFacList]

#=========================================================!!!!!!!!!!!!!!!
def getDataFrame(csa):

    xCoords:        List[int] = []
    yCoords:        List[int] = []
    zCoords:        List[int] = []
    factionName:    List[str] = []
    systemName:     List[str] = []
    allegiances:    List[str] = []
    isHomeSystem:   List[bool] = []
    population:     List[int] = []
    influence:      List[float] = []
    updated:        List[datetime.datetime] = []
    controlsSystem: List[bool] = []
    vulnerableString: List[str] = []

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


