import datetime
import json
import logging
from typing import List, Dict, Tuple

import pandas as pd

from craid.eddb.Vulnerability import Vulnerability
from craid.club import FactionNameFilter
from craid.eddb.Faction import Faction
from craid.eddb.FactionInstance import FactionInstance
from craid.eddb.InhabitedSystem import InhabitedSystem
from craid.eddb.LoadDataFromEDDB import LoadDataFromEDDB


# all_stations_dict : Station = {}
# def desiredState(state_dict):
#     ret = []
#     if STATE_RETREAT in state_dict: ret.append(STATE_RETREAT) #96
#     STATE_WAR = 73
#     STATE_CIVIL_WAR = 64
#     STATE_ELECTION = 65
#
#     STATE_OUTBREAK = 72
#     STATE_INFRASTRUCTURE_FAILURE = 104
#     STATE_EXPANSION = 67
#
#     ','.join(ret)
#     #STATE_BOOM = 16
#     #STATE_BUST = 32
#     #STATE_FAMINE = 37
#     #STATE_CIVIL_UNREST = 48
#     #STATE_CIVIL_LIBERTY = 66
#     #STATE_LOCKDOWN = 69
#     #STATE_NONE = 80
#     #STATE_PIRATE_ATTACK = 81
#     #STATE_INVESTMENT = 101
#     #STATE_BLIGHT = 102
#     #STATE_DROUGHT = 103
#     #STATE_NATURAL_DISASTER = 105
#     #STATE_PUBLIC_HOLIDAY = 106
#     #STATE_TERRORIST_ATTACK = 107
#
#     for state in state_dict:
#         if (state['id'] == 64):
#             return 64
#         if (state['id'] == 65):
#             return 65
#         if (state['id'] == 73):
#             return 73
#         if (state['id'] == 96):
#             return 96
#         if (state['id'] == 104):
#             return 104
#
#     return 0


#
# Expensive function - run once, use result many times
#
def getDataArrays() -> Dict[str,object]:
    # all_factions_dict: Faction                     = {}    #private
    playerFactionIdToInfo: Dict[int, Faction] = {}  # private
    clubFactionIdToInfo: Dict[int, Faction] = {}  # private
    systemIdToInfo: Dict[int, InhabitedSystem] = {}  # private
    allClubSystemInstances: List[FactionInstance] = []  # make this one avaiable
    playerFactionNameToSystemName: Dict[str, str] = {}
    systemNameToXYZ: Dict[str, Tuple[float, float, float]] = {}
    sysIdFacIdToFactionInstance: Dict[ Tuple[int,int], FactionInstance] = {}


    #with open("../data/factions.jsonl", 'r') as handle:
    #with LoadDataFromEDDB.find_data_file('factions.jsonl') as handle:
    nLines: int = 0
    for thing in LoadDataFromEDDB.find_data_file('factions.jsonl'):
        logging.debug("Back in dp")
        line = thing.readline()
        while line:
            nLines +=1
            facLine: dict = json.loads(line)
            lCurFactionId = int(facLine['id'])
            curFaction = Faction(facLine)
            # all_factions_dict[ lCurFactionId ] = curFaction
            if curFaction.is_player():
                playerFactionIdToInfo[lCurFactionId] = curFaction
            if FactionNameFilter.proClubFaction(curFaction):
                clubFactionIdToInfo[lCurFactionId] = curFaction
            line = thing.readline()

    logging.info("Read %s lines of faction data", str(nLines))
    # with open(stations_file, 'r') as handle:
    #      for line in handle:
    #         station = json.loads(line)
    #         system_id = station[ SYSTEM_ID ]
    #         current_station = stations_dict.get(system_id)

    #with open("../data/systems_populated.jsonl", 'r') as handle:
    nLines = 0
    for thing in LoadDataFromEDDB.find_data_file('systems_populated.jsonl'):
        logging.debug("Back in dp")
        line = thing.readline()
        while line:
            nLines +=1
            sysLine: dict = json.loads(line)
            tid = int(sysLine['id'])
            foo = InhabitedSystem(sysLine)
            systemIdToInfo[tid] = foo
            line = thing.readline()


    logging.info("Read %s lines of systems data", str(nLines))
    #
    # Populate dict of player factions & home system names
    #
    fac: Faction
    for fac in playerFactionIdToInfo.values():
        sid: int = fac.get_homesystem_id()
        tSys: InhabitedSystem = systemIdToInfo.get(sid)
        if tSys is None:
            continue
        factionName: str = fac.get_name()
        systemName: str = tSys.get_name()
        if systemName is None:
            continue
        # x: float = tSys.getX()
        # y: float = tSys.getY()
        # z: float = tSys.getZ()
        # item = (sName, (x, y, z))
        playerFactionNameToSystemName[factionName] = systemName  # (x, y, z)  # .append(item)

    #
    # Populate dict of system name & x,y,zs
    #
    tSys: InhabitedSystem
    for tSys in systemIdToInfo.values():
        if tSys is None:
            continue
        factionName: str = tSys.get_name()
        x: float = tSys.getX()
        y: float = tSys.getY()
        z: float = tSys.getZ()
        systemNameToXYZ[factionName] = (x, y, z)  # .append(item)


    #
    # Make nifty list of club faction presences
    #
    cSystem: InhabitedSystem
    for cSystem in systemIdToInfo.values():
        mfp = cSystem.getMinorFactionPresences()
        for faction_ptr in mfp:
            if faction_ptr is None:
                continue
            faction_id = int(faction_ptr['minor_faction_id'])
            if faction_id is None:
                continue
            if faction_id in clubFactionIdToInfo:
                fac = clubFactionIdToInfo[faction_id]
                factionName: str = fac.get_name2()
                if factionName.startswith("*"):
                    continue  # filters player factions

                # sysname = cSystem.get_name()
                # factionHomeSystemId: int = fac.get_homesystem_id()
                # vulnerable = True
                # if (systemId == factionHomeSystemId): vulnerable = False

                # systemId = cSystem.get_id()
                # vulnerable = not fac.isHomeSystem(systemId)

                govt = cSystem.getGovernment()
                # allg = fac.get_allegiance()

                inf = faction_ptr['influence']
                # sinf = '{:04.2f}'.format(inf)
                # print(sinf)

                # updated = cSystem.getUpdated();
                # date = datetime.datetime.utcfromtimestamp(updated)
                # ds = date.strftime("%m/%d/%Y %H:%M:%S")

                vuln : Vulnerability = Vulnerability(govt, inf, faction_ptr['active_states'])
                # HERE
                # # active_states = json.dumps(faction_ptr[ 'active_states' ])
                # hasWar = desiredState(faction_ptr['active_states'])
                # if (govt == "Anarchy"):
                #     hasWar = -16
                # if (hasWar == 0 and 4.5 >= inf > 0.0):
                #     hasWar = -15
                # if (hasWar == 104 and inf > 10.0):
                #     hasWar = 0

                sysIns = FactionInstance(fac, cSystem, inf, vuln)
                allClubSystemInstances.append(sysIns)
                system_id : int = cSystem.get_id()
                sysIdFacIdToFactionInstance[ (system_id, faction_id)] = sysIns

    return {'playerFactionIdToInfo'        : playerFactionIdToInfo,
            'clubFactionIdToInfo'          : clubFactionIdToInfo,
            'systemIdToInfo'               : systemIdToInfo,
            'allClubSystemInstances'       : allClubSystemInstances,
            'systemNameToXYZ'              : systemNameToXYZ,
            'playerFactionNameToSystemName': playerFactionNameToSystemName,
            'sysIdFacIdToFactionInstance'  : sysIdFacIdToFactionInstance
            }


# =========================================================!!!!!!!!!!!!!!!
def getDataFrame(csa: List[FactionInstance]) -> pd.DataFrame:
    x_coordinate: List[float] = []
    y_coordinate: List[float] = []
    z_coordinate: List[float] = []
    factionName: List[str] = []
    systemName: List[str] = []
    allegiances: List[str] = []
    isHomeSystem: List[bool] = []
    population: List[int] = []
    influence: List[float] = []
    updated: List[datetime.datetime] = []
    controlsSystem: List[bool] = []
    vulnerableString: List[str] = []
    sysId: List[int] = []
    facId: List[int] = []

    factionInstance: FactionInstance
    for factionInstance in csa:
        factionName.append(factionInstance.get_name())
        systemName.append(factionInstance.getSystemName())
        x_coordinate.append(factionInstance.getX())
        y_coordinate.append(factionInstance.getY())
        z_coordinate.append(factionInstance.getZ())
        allegiances.append(factionInstance.get_allegiance())
        isHomeSystem.append(factionInstance.isHomeSystem())
        population.append(factionInstance.getPopulation())
        influence.append(factionInstance.getInfluence())
        updated.append(factionInstance.getUpdatedDateTime().date())  #TODO: demoted to date because no formatting in datatable
        controlsSystem.append(factionInstance.controlsSystem())
        vulnerableString.append(factionInstance.getVulnerableString())
        sysId.append(factionInstance.getSystemID())
        facId.append(factionInstance.getFactionID())

    data = {
        'systemName'  : systemName,
        'factionName' : factionName,
        'x'           : x_coordinate,
        'y'           : y_coordinate,
        'z'           : z_coordinate,
        'allegiance'  : allegiances,
        'isHomeSystem': isHomeSystem,
        'population'  : population,
        'influence'   : influence,
        'updated'     : updated,
        'control'     : controlsSystem,
        'vulnerable'  : vulnerableString,
        'sysId'       : sysId,
        'facId'       : facId
    }

    #
    # Main dataframe of all club factions
    #
    df = pd.DataFrame(data=data)
    return df
