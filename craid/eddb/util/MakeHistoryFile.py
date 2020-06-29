#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

# Read big factions file
# Read small systems file
# Construct factioninstances
# output to jsonl
import gzip
import logging
from typing import Dict
import pandas as pd
import ujson

from craid.eddb.loader.CreateClubSystemKeys import getClubSystemKeys
from craid.eddb.loader.CreateFactionInstances import getFactionInstances
from craid.eddb.loader.CreateFactions import load_factions
from craid.eddb.loader.CreateSystems import load_systems
from craid.eddb.loader.strategy.EDDBLoader import LoadDataFromEDDB
from craid.eddb.loader.strategy.GithubLoader import LoadDataFromGithub

oldRevs = ["444f58522e81c3ad6477eefa398f39c2edfc1ea9",
           "7cd6abc33aafab80cace0c13c2beb6e1d8f1779b",
           "ebbdc4e809cc446bbe35b1a540b3480006be4e67",
           "50eb68e359a444de0cec194a603a3a9a339855fa",
           "43f0480c50e9b69c0506a30e366c9f34d4fa60f8",
           "4b7ead2c26999e9736ff179a38f38c5677c2423c",
           "c337e9261161bbfc1be99e1a9e1a31d9b01159f0",
           "ea8d0b6db656cd5802e5fc4595e6f364b455153e",
           "3adfece26c3c8f7a829540fbe6e0f8b109ac8357",
           "92578fe5ebf412523ee9fef68266dc4f7d8874f2",
           "2fdb0b11640577d1900fd3b6ba318ec0d5bffd55",
           "7ccef973cb7ddf50ca6124df78fa0ccbd9256aeb",
           "d3755d00457e86102a9a79db85c1359bea6a227a",
           "7e8ba2b9a6697fc1f01cf3c72a0d48cfff075e8e",
           "8bb9f02d56f9653a60f6e0b69eeeef7ade9bef89",
           "3d1e47b4ca7d2ade4259d040a0aa5261e9fecf7c",
           "a32a807f0cb3efeb8eba568050a7c4eec0af6820",
           "8cd07a52abeb3c0c50c67a88fcbfad03a675fec5",
           "fdcf2cf690ada3cd1cfb801fdfcdfee9fd4d4d75",
           "832e3fc83b2663a128fc84403202faea6f16f0ae",
           "84851ceedc1725a2d5b35f13cd7450e8f76237c3",
           "99aff5ca88e908dcddeb7611623ca7a40f79dffa",
           "5e1e658849098444a10d7aec6a2f0e13542be725",
           "4f848d61f92f772744304aeef49c7e7d0e5e9c63",
           "066c92ef24354305b1dd94ae0e12596afc3a6fd6"]

fName = '../../../data/history.jsonl.gz'

def appendTodaysData():
    global fName
    myLoader = LoadDataFromEDDB()

    playerFactionNameToSystemName: Dict[str, str] = {}
    all_factions_dict, player_faction_keys, club_faction_keys = load_factions(myLoader)

    json_str = ""

    myLoader = LoadDataFromGithub() #True, rev, True)
    all_systems_dict = load_systems(myLoader)

    club_system_keys = getClubSystemKeys(all_systems_dict, club_faction_keys)

    allClubSystemInstances, sysIdFacIdToFactionInstance, factions_of_interest_keys \
        = getFactionInstances(all_systems_dict, club_system_keys, all_factions_dict, club_faction_keys)

    for val in sysIdFacIdToFactionInstance.values():
        if val.isClub():
            hl = val.getHistoryLine()
            #print(hl)
            json_str += hl + "\n"

    json_bytes = json_str.encode('utf-8')
    with gzip.GzipFile(fName, 'a+b') as fout:  # 4. gzip
        fout.write(json_bytes)


def cleanHistoryFile():
    global fName
    dataframe = pd.read_json(fName, lines=True, compression='infer')

    # data cleaning
    dataframe = dataframe.drop_duplicates()
    dataframe = dataframe[dataframe['faction'] != 'Aegis of Federal Democrats']
    dataframe = dataframe[dataframe['faction'] != 'Aegis Imperium']
    dataframe = dataframe[dataframe['faction'] != "Emperor's Dawn"]

    json_str = ""
    for index, row in dataframe.iterrows():
        #print(row.to_dict())
        json_str += ujson.dumps(row.to_dict()) + "\n"

    json_bytes = json_str.encode('utf-8')
    with gzip.GzipFile(fName, 'wb') as fout:  # 4. gzip
        fout.write(json_bytes)


def makeHistoryFromEddbRevisions():
    myLoader = LoadDataFromEDDB()

    playerFactionNameToSystemName: Dict[str, str] = {}
    all_factions_dict, player_faction_keys, club_faction_keys = load_factions(myLoader)

    json_str = ""

    for rev in oldRevs:
        myLoader = LoadDataFromGithub(True, rev, True)
        all_systems_dict = load_systems(myLoader)

        club_system_keys = getClubSystemKeys(all_systems_dict, club_faction_keys)

        allClubSystemInstances, sysIdFacIdToFactionInstance, factions_of_interest_keys \
            = getFactionInstances(all_systems_dict, club_system_keys, all_factions_dict, club_faction_keys)

        for val in sysIdFacIdToFactionInstance.values():
            if val.isClub():
                json_str += val.getHistoryLine() + "\n"
                # print(val.getHistoryLine())

    json_bytes = json_str.encode('utf-8')
    with gzip.GzipFile('../../../data/history.jsonl.gz', 'a+b') as fout:  # 4. gzip
        fout.write(json_bytes)

if __name__ == '__main__':
    #
    # Fire up logger
    #
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.getLogger().level = logging.DEBUG

    appendTodaysData()
    cleanHistoryFile()
    #makeHistoryFiles()
