#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

import datetime
from typing import List

import pandas as pd

from craid.eddb.FactionInstance import FactionInstance


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

    # NOTE: hi there
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
