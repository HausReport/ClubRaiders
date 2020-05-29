#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

#
# Populate dict of system name & x,y,zs
# Used by dropdowns in dashboard
#

# FIXME: actually, dashboard has all_systems_dict, this can be moved there

from typing import Dict, Tuple

from InhabitedSystem import InhabitedSystem


def loadSystemNameToPositionMap(all_systems_dict: Dict[int, InhabitedSystem]):
    systemNameToXYZ: Dict[str, Tuple[float, float, float]] = {}
    tSys: InhabitedSystem
    for tSys in all_systems_dict.values():
        if tSys is None:
            continue
        systemName: str = tSys.get_name()
        x: float = tSys.getX()
        y: float = tSys.getY()
        z: float = tSys.getZ()
        systemNameToXYZ[systemName] = (x, y, z)

    return systemNameToXYZ
