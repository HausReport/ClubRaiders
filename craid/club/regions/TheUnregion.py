#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
from craid.club.regions.Region import Region


class TheUnregion(Region):

    def __init__(self, ):
        super().__init__("UnRegion", 0, 'rgb(0,0,0)')

    def contains(self, x, y, z):
        return True

    def distanceFrom(self, x, y, z):
        dist = 999999
        return dist