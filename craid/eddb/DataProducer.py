import datetime
import logging
from typing import List, Dict, Tuple, Set

import json_lines
import pandas as pd

from Aware import Aware
from Station import Station
from craid.club import FactionNameFilter
from craid.eddb.Faction import Faction
from craid.eddb.FactionInstance import FactionInstance
from craid.eddb.InhabitedSystem import InhabitedSystem
from craid.eddb.LoadDataFromEDDB import LoadDataFromEDDB
from craid.eddb.Vulnerability import Vulnerability


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
def getDataArrays() -> Dict[str, object]:
    all_systems_dict: Dict[int, InhabitedSystem] = {}  # private
    all_factions_dict: Dict[int, Faction] = {}  # private

    playerFactionIdToInfo: Dict[int, Faction] = {}  # private
    playerFactionNameToSystemName: Dict[str, str] = {}

    clubFactionIdToInfo: Dict[int, Faction] = {}  # private
    allClubSystemInstances: List[FactionInstance] = []  # make this one avaiable
    clubSystemLookup: Set[int] = set()
    sysIdFacIdToFactionInstance: Dict[Tuple[int, int], FactionInstance] = {}

    systemNameToXYZ: Dict[str, Tuple[float, float, float]] = {}

    #
    # Load factions
    #
    nLines: int = 0
    fName = LoadDataFromEDDB.find_data_file('factions.jsonl')
    with json_lines.open(fName, broken=True) as handle:
        for facLine in handle:
            nLines += 1
            lCurFactionId = int(facLine['id'])
            curFaction = Faction(facLine)
            all_factions_dict[lCurFactionId] = curFaction

            if curFaction.is_player():
                playerFactionIdToInfo[lCurFactionId] = curFaction
            if FactionNameFilter.proClubFaction(curFaction):
                clubFactionIdToInfo[lCurFactionId] = curFaction

    logging.info("Read %s lines of faction data", str(nLines))

    #
    # Load all inhabited systems
    #
    nLines = 0
    fName = LoadDataFromEDDB.find_data_file('systems_populated.jsonl')
    with json_lines.open(fName, broken=True) as handle:
        for sysLine in handle:
            nLines += 1
            tid = int(sysLine['id'])
            foo = InhabitedSystem(sysLine)
            all_systems_dict[tid] = foo

    logging.info("Read %s lines of systems data", str(nLines))
    Aware.setSystemsDict(all_systems_dict)
    Aware.setFactionsDict(all_factions_dict)

    #
    # Populate dict of player factions & home system names
    #
    fac: Faction
    for fac in playerFactionIdToInfo.values():
        sid: int = fac.get_homesystem_id()
        tSys: InhabitedSystem = all_systems_dict.get(sid)
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
    for tSys in all_systems_dict.values():
        if tSys is None:
            continue
        systemName: str = tSys.get_name()
        x: float = tSys.getX()
        y: float = tSys.getY()
        z: float = tSys.getZ()
        systemNameToXYZ[systemName] = (x, y, z)

    #
    # Make nifty list of club faction presences
    #
    cSystem: InhabitedSystem
    for cSystem in all_systems_dict.values():
        mfp = cSystem.getMinorFactionPresences()
        for faction_ptr in mfp:
            if faction_ptr is None:
                continue
            faction_id: int = int(faction_ptr['minor_faction_id'])
            if faction_id is None:
                continue
            if faction_id in clubFactionIdToInfo:
                fac = clubFactionIdToInfo[faction_id]
                factionName: str = fac.get_name2()
                if factionName.startswith("*"):
                    continue  # filters player factions
                govt = cSystem.getGovernment()
                inf = faction_ptr['influence']
                vulnerabilities: Vulnerability = Vulnerability(govt, inf, faction_ptr['active_states'])

                factionInstance = FactionInstance(fac, cSystem, inf, vulnerabilities)
                allClubSystemInstances.append(factionInstance)
                system_id: int = cSystem.get_id()

                clubSystemLookup.add(system_id)  # it's a set
                sysIdFacIdToFactionInstance[(system_id, faction_id)] = factionInstance

    logging.info("Populated club faction presences")
    logging.debug("nitems in CSL {%d} ", len(clubSystemLookup))

    #
    # Only now, can we populate lists of stations in **club** systems
    #
    nLines: int = 0
    nAdded: int = 0
    fName = LoadDataFromEDDB.find_data_file('stations.jsonl')
    with json_lines.open(fName, broken=True) as handle:
        for staLine in handle:
            nLines += 1
            if (nLines % 50000 == 0):
                logging.debug("Read %d lines...", nLines)

            # I didn't appreciate how many stations there were...
            # hard coding the weeding out of non-faction, non-dockable
            # stations before the clubSystemLookout
            if True is True:  # staLine['has_docking']:  show assets?
                cmf = staLine.get('controlling_minor_faction_id')
                if cmf is not None:
                    lCurSystemId = int(staLine['system_id'])
                    if lCurSystemId in clubSystemLookup:

                        curSys: InhabitedSystem = all_systems_dict[lCurSystemId]
                        if curSys is not None:
                            # lCurStationId = int(staLine['id'])
                            sta: Station = Station(staLine)

                            controlFacId: int = sta.getControllingFactionId()
                            # controlFac is not none at this point    c
                            nAdded += 1
                            if nAdded % 100 == 0:
                                logging.debug("Adding station %d...", nAdded)

                            if controlFacId in clubSystemLookup:
                                sta.setClub(True)

                            curSys.addStation(sta)

    logging.info("Read %s lines of station data", str(nLines))
    logging.info("Added %d stations", nAdded)

    return {'playerFactionIdToInfo'        : playerFactionIdToInfo,
            'clubFactionIdToInfo'          : clubFactionIdToInfo,
            'all_systems_dict'             : all_systems_dict,
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
    difficulty: List[float] = []

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
        updated.append(
            factionInstance.getUpdatedDateTime().date())  # TODO: demoted to date because no formatting in datatable
        controlsSystem.append(factionInstance.controlsSystem())
        vulnerableString.append(factionInstance.getVulnerableString())
        sysId.append(factionInstance.getSystemID())
        facId.append(factionInstance.getFactionID())
        difficulty.append(factionInstance.getDifficulty())

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
        'facId'       : facId,
        'difficulty'  : difficulty
    }

    #
    # Main dataframe of all club factions
    #
    df = pd.DataFrame(data=data)
    return df

# if __name__ == '__main__':
# csa = getDataArrays()
