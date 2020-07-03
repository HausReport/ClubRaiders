#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
# from craid.club.regions.SphericalRegion import _name, num, color
from craid.club.regions.MultiSphericalRegion import MultiSphericalRegion
from craid.club.regions.SphericalRegion import SphericalRegion
from craid.club.regions.TheUnregion import TheUnregion


class Region(object):

    def __init__(self, _name, num, color):
        self.color = color
        self.num = num
        self._name = _name

    def getTitle(self):
        return "The " + self._name + " Region"

    def getNumber(self):
        return self.num

    def getColor(self):
        return self.color

    def regionDistance(self, otherRegion):
        if isinstance(self,TheUnregion) or isinstance(otherRegion,TheUnregion):
            return 0.0
        if isinstance(self, SphericalRegion) and isinstance(otherRegion, SphericalRegion):
            d1 = self.distanceFrom(otherRegion.getX(), otherRegion.getY(), otherRegion.getZ())
            d2 = otherRegion.distanceFrom(self.getX(), self.getY(), self.getZ())
            return min(d1, d2)
        if isinstance(self,MultiSphericalRegion) and isinstance(otherRegion,SphericalRegion):
            d1 = self.distanceFrom(otherRegion.getX(), otherRegion.getY(), otherRegion.getZ())
            dist = 1000000000
            for p in self.points:
                d2 = otherRegion.distanceFrom(p[0], p[1], p[2])
                if d2<dist:
                    dist = d2
            return min(d1,dist)
        if isinstance(self,SphericalRegion) and isinstance(otherRegion,MultiSphericalRegion):
            d1 = otherRegion.distanceFrom(self.getX(), self.getY(), self.getZ())
            dist = 1000000000
            for p in otherRegion.points:
                d2 = self.distanceFrom(p[0], p[1], p[2])
                if d2<dist:
                    dist = d2
            return min(d1,dist)
        if isinstance(self,MultiSphericalRegion) and isinstance(otherRegion,MultiSphericalRegion):
            dist = 1000000000
            for p in self.points:
                d2 = otherRegion.distanceFrom(p[0], p[1], p[2])
                if d2 < dist:
                    dist = d2
            for p in otherRegion.points:
                d2 = self.distanceFrom(p[0], p[1], p[2])
                if d2<dist:
                    dist = d2
            return dist
        assert False, "No region distance case matched"

# def __init__(self, name, labelx, labely, x0, y0, x1, y1, shape, color):
#     self.name = name
#     self.labelx = labelx
#     self.labely = labely
#     self.x0 = x0
#     self.y0 = y0
#     self.x1 = x1
#     self.y1 = y1
#     self.shape = shape
#     self.color = color
