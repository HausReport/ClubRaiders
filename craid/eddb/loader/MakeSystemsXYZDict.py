#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import os
import tempfile
from typing import Dict
from typing import Tuple

import json_lines

shortName = "systems_populated.jsonl"
tmpDir = tempfile.gettempdir()
fName = os.path.join(tmpDir, shortName) + ".gz"

systemNameToXYZ: Dict[str, Tuple[int, int, int]] = {}
nLines: int = 0
with json_lines.open(fName, broken=True) as handle:
    for sysLine in handle:
        nLines += 1

        tName = sysLine['name']
        tX = int(sysLine['x'])
        tY = int(sysLine['y'])
        tZ = int(sysLine['z'])
        systemNameToXYZ[tName]  = (tX, tY, tZ)

        #if(nLines>10):
            #break

print( "myDict = \\ \n{")
for tName in sorted(systemNameToXYZ):
    tT = systemNameToXYZ[tName]
    tX = tT[0]
    tY = tT[1]
    tZ = tT[2]

    msg = f' "{tName}": ({tX},{tY},{tZ}),'
    print(msg)


print( "}")

