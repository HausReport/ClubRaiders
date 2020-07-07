#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
# from craid.club.regions.SphericalRegion import _name, num, color
# from craid.club.regions.MultiSphericalRegion import MultiSphericalRegion
# from craid.club.regions.SphericalRegion import SphericalRegion
# from craid.club.regions.TheUnregion import TheUnregion
from abc import ABC, abstractmethod

import plotly.graph_objs as go

class Region(ABC):

    def __init__(self, _name, num, color):
        self.color = color
        self.num = num
        self._name = _name

    @abstractmethod
    def contains(self, x, y, z) -> bool:
        pass

    @abstractmethod
    def distanceFrom(self, x, y, z) -> bool:
        pass

    @abstractmethod
    def getVolume(self) -> bool:
        pass

    def getTitle(self):
        return "The " + self._name + " Region"

    def getNumber(self):
        return self.num

    def getColor(self):
        return self.color

    def getView(self, dataFrame):
        return dataFrame[dataFrame.apply(lambda x: self.contains(x.x, x.y, x.z), axis=1)]

    def getFigure(self, theFrame):

        from craid.club.regions.TheUnregion import TheUnregion
        if isinstance(self, TheUnregion):
            title = "Club Activity Galaxy-Wide"
            view = theFrame
        else:
            title = "Club Activity near " + self.getTitle()
            view = self.getView(theFrame)

        simpleTrace = Region.getTrace(view)
        myLayout = Region.getLayout(title)
        return go.Figure(data=[simpleTrace], layout=myLayout)

    @staticmethod
    def getLayout(theTitle):
        return go.Layout(title=theTitle,
                         scene=Region.getScene(),
                         width=800,
                         height=900,
                         autosize=False,
                         paper_bgcolor='rgb(0,0,0)',
                         plot_bgcolor='rgb(0,0,0)',
                         clickmode='event+select',
                         font=dict(
                             family="Courier New, monospace",
                             size=12,
                             color="#ffffff"),
                         margin=dict(t=100, b=0, l=0, r=0),
                         )

    @staticmethod
    def getScene():
        return dict(
            xaxis=dict(
                backgroundcolor="rgb(0,0,0)",
                gridcolor="grey",
                showbackground=False,
                zerolinecolor="white", ),
            yaxis=dict(
                backgroundcolor="rgb(0,0,0)",
                gridcolor="grey",
                showbackground=False,
                zerolinecolor="white", ),
            zaxis=dict(
                backgroundcolor="rgb(0,0,0)",
                gridcolor="grey",
                showbackground=False,
                zerolinecolor="white", ),
            aspectratio=dict(x=1, y=1, z=0.7),
            aspectmode="manual"
        )

    @staticmethod
    def getTrace(theFrame):
        return go.Scatter3d(x=theFrame['x'],
                            y=theFrame['z'],
                            z=theFrame['y'],
                            text=theFrame['systemName'],
                            hoverinfo="text",
                            hovertext=theFrame['htext'],
                            mode='markers+text',
                            marker=dict(size=theFrame["marker_size"],
                                        color=theFrame["color"]))
