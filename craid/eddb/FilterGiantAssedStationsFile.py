import datetime
import logging
from typing import List, Dict, Tuple, Set

import pandas as pd
import ujson

from Station import Station
from craid.club import FactionNameFilter
from craid.eddb.Faction import Faction
from craid.eddb.FactionInstance import FactionInstance
from craid.eddb.InhabitedSystem import InhabitedSystem
from craid.eddb.LoadDataFromEDDB import LoadDataFromEDDB
from craid.eddb.Vulnerability import Vulnerability


#
# Expensive function - run once, use result many times
#
def getDataArrays():
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.getLogger().level = logging.DEBUG

    # all_factions_dict: Faction                     = {}    #private
    # playerFactionIdToInfo: Dict[int, Faction] = {}  # private
    clubFactionIdToInfo: Dict[int, Faction] = {}  # private
    systemIdToInfo: Dict[int, InhabitedSystem] = {}  # private
    # allClubSystemInstances: List[FactionInstance] = []  # make this one avaiable
    # playerFactionNameToSystemName: Dict[str, str] = {}
    # systemNameToXYZ: Dict[str, Tuple[float, float, float]] = {}
    # sysIdFacIdToFactionInstance: Dict[Tuple[int, int], FactionInstance] = {}

    clubSystemLookup: Set[int] = set()

    # with open("../data/factions.jsonl", 'r') as handle:
    # with LoadDataFromEDDB.find_data_file('factions.jsonl') as handle:
    nLines: int = 0
    for thing in LoadDataFromEDDB.find_data_file('factions.jsonl'):
        logging.debug("Back in dp")
        line = thing.readline()
        while line:
            nLines += 1
            facLine: dict = ujson.loads(line)
            lCurFactionId = int(facLine['id'])
            curFaction = Faction(facLine)
            # all_factions_dict[ lCurFactionId ] = curFaction
            if FactionNameFilter.proClubFaction(curFaction):
                clubFactionIdToInfo[lCurFactionId] = curFaction
            line = thing.readline()

    logging.info("Read %s lines of faction data", str(nLines))

    nLines = 0
    for thing in LoadDataFromEDDB.find_data_file('systems_populated.jsonl'):
        logging.debug("Back in dp")
        line = thing.readline()
        while line:
            nLines += 1
            sysLine: dict = ujson.loads(line)
            tid = int(sysLine['id'])
            foo = InhabitedSystem(sysLine)
            systemIdToInfo[tid] = foo
            line = thing.readline()

    logging.info("Read %s lines of systems data", str(nLines))

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

                # govt = cSystem.getGovernment()
                # inf = faction_ptr['influence']
                # vuln: Vulnerability = Vulnerability(govt, inf, faction_ptr['active_states'])

                # sysIns = FactionInstance(fac, cSystem, inf, vuln)
                # allClubSystemInstances.append(sysIns)
                system_id: int = cSystem.get_id()

                clubSystemLookup.add(system_id)  # it's a set
                # sysIdFacIdToFactionInstance[(system_id, faction_id)] = sysIns

    logging.info("Populated club faction presences")

    #
    # Only now, can we populate lists of stations in **club** systems
    #
    bigList: List[str] = []
    nLines: int = 0
    nAdded: int = 0
    for thing in LoadDataFromEDDB.find_data_file('stations.jsonl'):
        logging.debug("Back in dp")
        line = thing.readline()
        while line:
            nLines += 1
            if nLines % 50000 == 0:
                logging.debug("Read %d lines...", nLines)
            staLine: dict = ujson.loads(line)

            # I didn't appreciate how many stations there were...
            # hard coding the weeding out of non-faction, non-dockable
            # stations before the clubSystemLookout
            if staLine['has_docking'] :
                cmf = staLine.get('controlling_minor_faction_id')
                if cmf is not None:
                    lCurSystemId = int(staLine['system_id'])
                    if lCurSystemId in clubSystemLookup:

                        curSys: InhabitedSystem = systemIdToInfo[lCurSystemId]
                        if curSys != None:
                            sta: Station = Station(staLine)
                            logging.debug("Adding station...", nLines)
                            nAdded += 1
                            bigList.append(staLine)

            line = thing.readline()

    logging.info("Read %s lines of station data", str(nLines))
    logging.info("Preparing to write")

    outF = open("../data/smol-stations.jsonl", "w")
    aLine: str
    for aLine in bigList:
        outF.write(line + "\n")
    outF.close()


if __name__ == '__main__':
    csa = getDataArrays()
