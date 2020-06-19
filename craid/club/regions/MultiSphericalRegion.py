#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
from typing import List
from typing import Tuple

from numpy import *

from craid.club.regions.Region import Region
from craid.club.regions.SphericalRegion import SphericalRegion


class MultiSphericalRegion(Region):

    def __init__(self, myName, num, theData: List[Tuple[str, float, float, float]], r: float, color):
        super().__init__(myName, num, color)
        self.points: List[SphericalRegion] = []
        ct: int = 0
        for point in theData:
            theName = point[0]
            px = point[1]
            py = point[2]
            pz = point[3]
            theNumber = -1
            reg = SphericalRegion(theName, theNumber, px, py, pz, r, color)
            ct = ct + 1
            self.points.append(reg)

    def contains(self, x, y, z):
        for reg in self.points:
            if reg.contains(x, y, z):
                return True
        return False

    def distanceFrom(self, x, y, z):
        dist = 1000000000
        for reg in self.points:
            d2 = reg.distanceFrom(x, y, z)
            if (d2 < dist):
                dist = d2
            if dist == 0:
                return 0
        return dist

    def getSurface(self):
        ret = []
        for reg in self.points:
            ret.append(reg.getSurface())

        return ret

    def __str__(self):
        ret = f"Multisphere: {self._name}"

        for reg in self.points:
            msg = str(reg)
            ret = ret + "msg" + "\n"

        return ret