#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

from typing import List, Dict, Tuple

import dash_core_components as dcc
from pkg_resources import resource_string as resource_bytes


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

         5: ("trade",
             "{isHomeSystem} contains false",
             [{'column_id': 'salesScore', 'direction': 'desc'}],
             "trade"),
         6: ("mine",
             "{isHomeSystem} contains false",
             [{'column_id': 'mineralSalesScore', 'direction': 'desc'}],
             "mine"),
         7: ("explore",
             "{isHomeSystem} contains false",
             [{'column_id': 'explorationScore', 'direction': 'desc'}],
             "explore"),
    # cannedActions[5] = ("trade", None, None)
    # cannedActions[6] = ("sell mined minerals", None, None)
    # cannedActions[7] = ("explore", None, None)

         9 : ("run missions", "{isHomeSystem} contains false",
              [{'column_id': 'distance', 'direction': 'asc'}],
              "missions"),
         10: ("beat The Club in an election",
              "{vulnerable} contains Elect && {isHomeSystem} contains false",
              [{'column_id': 'distance', 'direction': 'asc'}],
              "election"),
         11: ("find an easy faction for a single commander to attack",
              "{isHomeSystem} contains false && {difficulty} < 5",
              [{'column_id': 'difficulty', 'direction': 'asc'}],
              "single"),
         12: ("find an challenging faction for a single commander to attack",
              "{isHomeSystem} contains false && {difficulty} > 5 && {difficulty} < 100",
              [{'column_id': 'difficulty', 'direction': 'asc'}],
              "single"),
         13: ("find a faction to attack with a small group",
              "{isHomeSystem} contains false && {difficulty} > 50 && {difficulty} < 150",
              [{'column_id': 'difficulty', 'direction': 'asc'}],
              "group")}

    #
    # TODO: work list
    #
    # cannedActions[3] = ("hunt for bounties", None, None)
    # cannedActions[4] = ("smuggle illegal goods", None, None)

    # cannedActions[13] = ("see the welcome message again", None, None)
    # cannedActions[8] = ("go on a murder/piracy rampage", None, None)

    #
    # Implemented
    #

    def __init__(self, systemNameToXYZ):
        super().__init__()
        self.systemNameToXYZ = systemNameToXYZ

    @staticmethod
    def getMarkdown(which: str) -> dcc.Markdown:
        text = resource_bytes('craid.dashbd.text', which + ".md").decode('utf-8')
        return dcc.Markdown(text)

    @staticmethod
    def getString(which: str) -> dcc.Markdown:
        text = resource_bytes('craid.dashbd.text', which + ".md").decode('utf-8')
        return text

    @staticmethod
    def getFirstDropdown(_systemNameToXYZ):
        opts = []
        keys: List[str] = sorted(_systemNameToXYZ.keys())
        for it in keys:
            opts.append({'label': it, 'value': it})
        return opts

    @staticmethod
    def getSecondDropdown(playerFactionNameToHomeSystemName):
        fopts = []
        keys: List[str] = sorted(playerFactionNameToHomeSystemName.keys())
        for it in keys:
            val: str = playerFactionNameToHomeSystemName.get(it)
            if val is not None:
                fopts.append({'label': it, 'value': val})
        return fopts

    @staticmethod
    def getFilter(val3: int):
        if val3==0: val3 = 1
        tup = AnnoyingCrap.cannedActions[val3]
        return tup[1]

    @staticmethod
    def getSort(val3: int):
        if val3==0: val3 = 1
        return AnnoyingCrap.cannedActions[val3][2]

    @staticmethod
    def getMessage(val3: int):
        if val3==0: val3 = 1
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

    ## "hidden": True,  is not a thing, unfortunately
    @staticmethod
    def getTheColumns():
        return [
            {"name": 'System', "id": 'systemName', "deletable": False, "selectable": False},
            {"name": 'Faction', "id": 'factionName', "deletable": False, "selectable": False},
            # {"name": 'x', "id": 'x', "deletable": False, "selectable": False, "hideable": True, "type": "numeric"},
            # {"name": 'y', "id": 'y', "deletable": False, "selectable": False, "hideable": True, "type": "numeric"},
            # {"name": 'z', "id": 'z', "deletable": False, "selectable": False, "hideable": True, "type": "numeric"},
            {"name": 'Home', "id": 'isHomeSystem', "deletable": False, "hideable": True, "selectable": False},
            {"name": 'Population', "id": 'population', "deletable": False, "hideable": True, "selectable": False,
             "type": "numeric"},
            {"name": 'Inf.', "id": 'influence', "deletable": False, "hideable": True, "selectable": False,
             "type": "numeric"},
            {"name": 'Difficulty', "id": 'difficulty', "deletable": False, "selectable": False, "type": "numeric"},
            {"name": 'Scouted', "id": 'updated', "deletable": False, "selectable": False, "type": "datetime"},
            {"name": 'Control', "id": 'control', "deletable": False, "hideable": True, "selectable": False},
            {"name": 'Vulnerable', "id": 'vulnerable', "deletable": False, "selectable": False},
            {"name": 'Dist.', "id": 'distance', "deletable": False, "selectable": False, "type": "numeric"},
        ]
