#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

import plotly.graph_objs as go
from numpy import *
from craid.club.regions.Region import Region

class SphericalRegion(Region):

    def __init__(self, _name, num, x0, y0, z0, r, color):
        super().__init__(_name, num, color)
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.r = r

    def contains(self, x, y, z):
        dist = math.sqrt((x - self.x0) ** 2 + (y - self.y0) ** 2 + (z - self.z0) ** 2)
        return dist <= self.r

    def distanceFrom(self, x, y, z):
        dist = math.sqrt((x - self.x0) ** 2 + (y - self.y0) ** 2 + (z - self.z0) ** 2)
        dist = dist - self.r
        if dist < 0:
            dist = 0
        return dist

    # def regionDistance(self, otherRegion: Region) -> float:
    #     d1 = self.distanceFrom()
    #     d2 = otherRegion._regionDistance(self)
    #     return min(d1, d2)

    def getSurface(self):
        theta = linspace(0, 2 * pi, 100)
        phi = linspace(0, pi, 100)
        x = self.x0 + self.r * outer(cos(theta), sin(phi))
        y = self.y0 + self.r * outer(sin(theta), sin(phi))
        z = self.z0 + self.r * outer(ones(100), cos(phi))  # note this is 2d now

        colorScale = [[0, self.color], [1, self.color]]
        data = go.Surface(
            x=x,
            y=y,
            z=z,
            opacity=0.2,
            showlegend=False,
            showscale=False,
            hoverinfo='skip',
            colorscale=colorScale,
            text=self._name
        )
        return data

    def getVolume(self):
        # 4/3 pi r^2
        return (4.0 * math.pi / 3.0) * self.r * self.r

    def __str__(self):
        msg2 = f"Sphere: {self._name} at ( {self.x0}, {self.y0}, {self.z0}) radius {self.r} color {self.color}"
        return msg2

    def getX(self):
        return self.x0

    def getY(self):
        return self.y0

    def getZ(self):
        return self.z0
