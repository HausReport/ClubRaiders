#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import math

from craid.club.regions.Region import Region


class SphericalRegion(Region):


    def __init__(self, _name, num, x0, y0, z0, r, color):
        super().__init__(_name, num, color)
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.r = r

    def contains(self, x,y,z):
        dist = math.sqrt( (x-self.x0)**2 + (y-self.y0)**2 + (z-self.z0)**2)
        return dist <= self.r

