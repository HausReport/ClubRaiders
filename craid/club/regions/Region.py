#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
#from craid.club.regions.SphericalRegion import _name, num, color


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
