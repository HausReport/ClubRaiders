#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import logging
from typing import Dict, Tuple

import dash_core_components as dcc
import dash_html_components as html
from dash_table.Format import Format, Scheme, Group
from pkg_resources import resource_string as resource_bytes

from craid.club.regions.RegionFactory import RegionFactory
from craid.eddb.faction.SquadronXYZ import SquadronXYZ
from craid.eddb.system.SystemXYZ import SystemXYZ


class AnnoyingCrap(object):
    # NOTE: Don't use index 0
    cannedActions: Dict[int, Tuple[str, str, str, str]] = \
        {1 : ("find Club Activity near me",
              "{isHomeSystem} contains false",
              [{'column_id': 'distance', 'direction': 'asc'}],
              "overview"),
         2 : ("fight The Club in war zones",
              "{vulnerable} contains War && {isHomeSystem} contains false",
              [{'column_id': 'distance', 'direction': 'asc'}],
              "cz"),
         3 : ("hunt for bounties",
              "{isHomeSystem} contains false && {bountyHuntingScore} >= 50",
              [{'column_id': 'distance', 'direction': 'asc'}],
              "bh"),
         4 : ("smuggle",
              "{isHomeSystem} contains false && {smugglingScore} >= 50",
              [{'column_id': 'distance', 'direction': 'asc'}],
              "smuggle"),
         5 : ("trade",
              "{isHomeSystem} contains false && {salesScore} > 50",
              [{'column_id': 'distance', 'direction': 'asc'}],
              "trade"),
         6 : ("mine",
              "{isHomeSystem} contains false && {mineralSalesScore} > 1",
              [{'column_id': 'distance', 'direction': 'asc'}],
              "mine"),
         7 : ("explore",
              "{isHomeSystem} contains false",
              [{'column_id': 'explorationScore', 'direction': 'desc'}],
              "explore"),
         8 : ("spy behind enemy lines",
              '{isHomeSystem} contains false',
              [{'column_id': 'updated', 'direction': 'asc'}],
              "scouting"),
         9 : ("go on a piracy/murder rampage",
              "{isHomeSystem} contains false && {piracyMurderScore} >= 50",
              [{'column_id': 'piracyMurderScore', 'direction': 'desc'}, {'column_id': 'distance', 'direction': 'asc'}],
              "piracyMurder"),
         10: ("run missions", "{isHomeSystem} contains false && {missionScore} > 120 && {distance} < 100",
              [{'column_id': 'missionScore', 'direction': 'desc'}, {'column_id': 'distance', 'direction': 'asc'}],
              "missions"),
         11: ("beat The Club in an election",
              "{vulnerable} contains Elect && {isHomeSystem} contains false",
              [{'column_id': 'distance', 'direction': 'asc'}],
              "election"),
         12: ("see easy club systems to solo",
              "{isHomeSystem} contains false && {difficulty} < 5",
              [{'column_id': 'difficulty', 'direction': 'asc'}],
              "single"),
         13: ("see hard club systems to solo",
              "{isHomeSystem} contains false && {difficulty} > 5 && {difficulty} < 50",
              [{'column_id': 'difficulty', 'direction': 'asc'}],
              "single"),
         14: ("see systems for small groups",
              "{isHomeSystem} contains false && {difficulty} > 25 && {difficulty} < 150",
              [{'column_id': 'difficulty', 'direction': 'asc'}],
              "group"),
         15: ("see systems for large groups",
              "{isHomeSystem} contains false && {difficulty} > 100 && {difficulty} < 750",
              [{'column_id': 'difficulty', 'direction': 'asc'}],
              "group"),
         16: ("see systems for squadron alliances",
              "{isHomeSystem} contains false && {difficulty} > 750 && {difficulty} < 950000",
              [{'column_id': 'difficulty', 'direction': 'asc'}],
              "group")}

    def __init__(self):
        super().__init__()

    @staticmethod
    def getMarkdown(which: str) -> dcc.Markdown:
        text = resource_bytes('craid.dashbd.text', which + ".md").decode('utf-8')
        return dcc.Markdown(text)

    @staticmethod
    def getString(which: str) -> dcc.Markdown:
        text = resource_bytes('craid.dashbd.text', which + ".md").decode('utf-8')
        return text

    @staticmethod
    def getLocationDropdown():
        # _systemNameToXYZ = SystemXYZ.myDict
        # print("dropdown len=" + str(len(SystemXYZ.myDict)))
        opts = []
        logging.debug("Loading location dropdown")
        # keys: List[str] = sorted(SystemXYZ.myDict)
        for it in SystemXYZ.myDict.keys():
            opts.append({'label': it, 'value': it})
        return opts

    @staticmethod
    def getFilter(val3: int):
        if val3 == 0: val3 = 1
        tup = AnnoyingCrap.cannedActions[val3]
        return tup[1]

    @staticmethod
    def getSort(val3: int):
        if val3 == 0: val3 = 1
        return AnnoyingCrap.cannedActions[val3][2]

    @staticmethod
    def getMessage(val3: int):
        if val3 == 0: val3 = 1
        shortFile: str = AnnoyingCrap.cannedActions[val3][3]
        return AnnoyingCrap.getMarkdown(shortFile)

    @staticmethod
    def getThirdDropdown():
        gopts = []
        keys = AnnoyingCrap.cannedActions.keys()
        key: int
        for key in keys:
            lab = AnnoyingCrap.cannedActions[key][0]
            gopts.append({'label': lab, 'value': key})

        return gopts

    # "hidden": True,  is not a thing, unfortunately
    @staticmethod
    def getTheColumns():
        allowHiddenColumns = False  # INFO: pending a dash bug fix, see https://github.com/plotly/dash-table/issues/789
        return [
            {"name": 'System', "id": 'systemName', "deletable": False, "selectable": False},
            {"name": 'Faction', "id": 'factionName', "deletable": False, "selectable": False},
            # {"name": 'x', "id": 'x', "deletable": False, "selectable": False, "hideable": True, "type": "numeric"},
            # {"name": 'y', "id": 'y', "deletable": False, "selectable": False, "hideable": True, "type": "numeric"},
            # {"name": 'z', "id": 'z', "deletable": False, "selectable": False, "hideable": True, "type": "numeric"},
            {"name"      : 'Home', "id": 'isHomeSystem', "deletable": False, "hideable": allowHiddenColumns,
             "selectable": False},
            {"name"      : 'Population', "id": 'population', "deletable": False, "hideable": allowHiddenColumns,
             "selectable": False,
             "type"      : "numeric", 'format': Format(precision=0, scheme=Scheme.fixed, group=Group.yes)},
            {"name": 'Inf.', "id": 'influence', "deletable": False, "hideable": allowHiddenColumns, "selectable": False,
             "type": "numeric", 'format': Format(precision=2, scheme=Scheme.fixed, group=Group.yes)},
            {"name"  : 'Difficulty', "id": 'difficulty', "deletable": False, "selectable": False, "type": "numeric",
             'format': Format(precision=1, scheme=Scheme.fixed, group=Group.yes)},
            {"name": 'Scouted', "id": 'updated', "deletable": False, "selectable": False, "type": "datetime"},
            {"name"      : 'Control', "id": 'control', "deletable": False, "hideable": allowHiddenColumns,
             "selectable": False},
            {"name": 'Vulnerable', "id": 'vulnerable', "deletable": False, "selectable": False},
            {"name": 'Dist.', "id": 'distance', "deletable": False, "selectable": False, "type": "numeric"},
            {"name"    : 'MissionScore', "id": 'missionScore', "deletable": False, "selectable": False,
             "hideable": allowHiddenColumns, "type": "numeric"},
            {"name"    : 'TradeScore', "id": 'salesScore', "deletable": False, "selectable": False,
             "hideable": allowHiddenColumns, "type": "numeric"},
            {"name": 'ExploreScore', "id": 'explorationScore', "hideable": allowHiddenColumns, "type": "numeric"},
            {"name"    : 'MineralSalesScore', "id": 'mineralSalesScore', "deletable": False, "selectable": False,
             "hideable": allowHiddenColumns, "type": "numeric"},
            {"name": 'BountyHuntScore', "id": 'bountyHuntingScore', "hideable": allowHiddenColumns, "type": "numeric"},
            {"name": 'SmugglingScore', "id": 'smugglingScore', "hideable": allowHiddenColumns, "type": "numeric"},
            {"name": 'PiracyMurderScore', "id": 'piracyMurderScore', "hideable": allowHiddenColumns, "type": "numeric"},
        ]

    #
    # 3d Map Stuff Follows
    #

    @staticmethod
    def getSquadronDropdown():
        print("dropdown len=" + str(len(SquadronXYZ.myDict)))
        opts = []
        logging.debug("Loading squadron dropdown")
        for it in SquadronXYZ.myDict.keys():
            opts.append({'label': it, 'value': it})

        # print("shape= " + str(np.shape(opts)))
        systemDropdown = dcc.Dropdown(
            id='squadronDropdown',
            options=opts,
            # value='Sol',
            placeholder='Select squadron',
            className="dropdown-select",
            # persistence=True,
        )
        return systemDropdown

    @staticmethod
    def getRegionDropdown():
        print("dropdown len=" + str(len(RegionFactory.regionDict)))
        opts = []
        # logging.debug("Loading squadron dropdown")
        for it in RegionFactory.regionDict.keys():
            opts.append({'label': it, 'value': it})

        regionDropdown = dcc.Dropdown(
            id='regionDropdown',
            options=opts,
            # value='Sol',
            placeholder='Select region',
            className="dropdown-select",
            # persistence=True,
        )
        return regionDropdown

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



tab_style = {
    'borderBottom'   : '1px solid #d6d6d6',
    'padding'        : '6px',
    'backgroundColor': '#3c3f41',
    'color'          : 'whitesmoke',
}
tab_selected_style = {
    'borderTop'      : '1px solid #d6d6d6',
    'borderBottom'   : '1px solid #d6d6d6',
    'fontWeight'     : 'bold',
    'backgroundColor': '#4e5254',
    'color'          : 'white',
    'padding'        : '6px'
}


def enCard(contents) -> html.Div:
    return html.Div(className="card", children=[
        contents,
    ])


def makeArticleCard(contents, id_) -> html.Div:
    return enCard(html.Article(contents, id=id_, className="simpleColItem"))


def makeDiscordCard(msg, _id, _idnum) -> html.Div:
    return html.Div(className="card", children=[
        dcc.Markdown(msg),
        html.Iframe(id=f"{_id}", src=f"https://discordapp.com/widget?id={_idnum}&theme=dark",
                    width="350", height="400"),
    ])

def makeDiscordIframe(_id, _idnum) -> html.Iframe:
    return html.Iframe(id=f"{_id}", src=f"https://discordapp.com/widget?id={_idnum}&theme=dark",
                    width="350", height="400")


my_meta_tags = [
    # A description of the app, used by e.g.
    # search engines when displaying search results.
    {
        'name'   : 'description',
        'content': 'Tool to help Elite: Dangerous commanders identify, evaluate and eradicate factions linked to the shadowy organization known as The Club.'
    },
    # A tag that tells Internet Explorer (IE)
    # to use the latest renderer version available
    # to that browser (e.g. Edge)
    {
        'http-equiv': 'X-UA-Compatible',
        'content'   : 'IE=edge'
    },
    # A tag that tells the browser not to scale
    # desktop widths to fit mobile screens.
    # Sets the width of the viewport (browser)
    # to the width of the device, and the zoom level
    # (initial scale) to 1.
    #
    # Necessary for "true" mobile support.
    {
        'name'   : 'viewport',
        'content': 'width=device-width, initial-scale=1.0'
    }
]
