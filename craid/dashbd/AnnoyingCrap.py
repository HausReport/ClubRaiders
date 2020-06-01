#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

from typing import List

import dash_core_components as dcc
import dash_html_components as html
from pkg_resources import resource_string as resource_bytes


#
# load a markdown file from /data
# https://importlib-resources.readthedocs.io/en/latest/using.html
#
def getMarkdown(which: str) -> dcc.Markdown:
    text = resource_bytes('craid.dashbd.text', which + ".md").decode('utf-8')
    return dcc.Markdown(text)


def getString(which: str) -> dcc.Markdown:
    text = resource_bytes('craid.dashbd.text', which + ".md").decode('utf-8')
    return text


def getFirstDropdown(_systemNameToXYZ):
    opts = []
    keys: List[str] = sorted(_systemNameToXYZ.keys())
    for it in keys:
        opts.append({'label': it, 'value': it})
    return opts


def getSecondDropdown(playerFactionNameToHomeSystemName):
    fopts = []
    keys: List[str] = sorted(playerFactionNameToHomeSystemName.keys())
    for it in keys:
        val: str = playerFactionNameToHomeSystemName.get(it)
        if val is not None:
            fopts.append({'label': it, 'value': val})
    return fopts


## "hidden": True,  is not a thing, unfortunately
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


def render_content(tab):
    if tab == 'tab-1':
        return html.Div(className="strict-horizontal", children=[
            html.Div(id="activities"),
            html.Div(id="activity"
            ),
            html.Div(id="statistics"),
        ]),
    elif tab == 'tab-2':
        return html.Div([
            getMarkdown("cz")
        ])
    elif tab == 'tab-3':
        return html.Div([
            getMarkdown("bh")
        ])
    elif tab == 'tab-4':
        return html.Div([
            getMarkdown("tem")
        ])
    elif tab == 'tab-5':
        return html.Div([
            getMarkdown("scouting")
        ])
    elif tab == 'tab-6':
        return html.Div([
            html.H3('Tab content 6')
        ])
    elif tab == 'tab-7':
        return html.Div([
            html.H3('Tab content 7')
        ])
