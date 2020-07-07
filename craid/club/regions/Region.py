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
        view = dataFrame[dataFrame.apply(lambda x: self.contains(x.x, x.y, x.z), axis=1)]
        Region.setMarkerSize(view)
        Region.setMarkerColors(view)
        Region.setHovertext(view)

    @staticmethod
    def setMarkerSize(dataFrame):
        dataFrame.loc[dataFrame['control'] == True, 'marker_size'] = 8  # Medium is not home/control
        dataFrame.loc[dataFrame['control'] == False, 'marker_size'] = 5  # Small is not home/not control
        dataFrame.loc[dataFrame['isHomeSystem'] == True, 'marker_size'] = 15  # Large is home
        # df["marker_size"] = df["influence"].apply(lambda x: 5+ x/5)

    @staticmethod
    def setMarkerColors(dataFrame):
        dataFrame.loc[dataFrame['control'] == True, 'color'] = "#ffbf00"  # Yellow is control/not home
        dataFrame.loc[dataFrame['control'] == False, 'color'] = "#00ff00"  # Green is not home/not control
        dataFrame.loc[dataFrame['isHomeSystem'] == True, 'color'] = "#ff0000"  # Red is homesystem

    @staticmethod
    def setHovertext(dataFrame):
        dataFrame['htext'] = dataFrame[['systemName', 'factionName']].agg('\n'.join, axis=1)


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
