#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
from pprint import pprint

from craid.eddb.loader.CreateFactions import load_factions
from craid.eddb.loader.CreateSystems import load_systems
from craid.eddb.loader.DataProducer import getDataArrays
from craid.eddb.loader.strategy.DirectoryLoader import DirectoryLoader

loader = DirectoryLoader()
#fName = loader.find_data_file("jul8.gz")
#print(fName)

prod = getDataArrays(loader= loader, clubSystemsOnly=False)

theDict = prod['sysIdFacIdToFactionInstance']

for facInst in theDict.values():
    pprint(facInst.getANNRow())
