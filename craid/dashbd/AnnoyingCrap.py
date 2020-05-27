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


def getTheColumns():
    return [
        {"name": 'systemName', "id": 'systemName', "deletable": False, "selectable": False},
        {"name": 'factionName', "id": 'factionName', "deletable": False, "selectable": False},
        # {"name": 'x', "id": 'x', "deletable": False, "selectable": False, "hideable": True, "type": "numeric"},
        # {"name": 'y', "id": 'y', "deletable": False, "selectable": False, "hideable": True, "type": "numeric"},
        # {"name": 'z', "id": 'z', "deletable": False, "selectable": False, "hideable": True, "type": "numeric"},
        {"name": 'isHomeSystem', "id": 'isHomeSystem', "deletable": True, "selectable": False},
        {"name": 'population', "id": 'population', "deletable": True, "selectable": False, "type": "numeric"},
        {"name": 'influence', "id": 'influence', "deletable": True, "selectable": False, "type": "numeric"},
        {"name": 'difficulty', "id": 'difficulty', "deletable": False, "selectable": False, "type": "numeric"},
        {"name": 'updated', "id": 'updated', "deletable": False, "selectable": False, "type": "datetime"},
        {"name": 'control', "id": 'control', "deletable": True, "selectable": False},
        {"name": 'vulnerable', "id": 'vulnerable', "deletable": False, "selectable": False},
        {"name": 'distance', "id": 'distance', "deletable": False, "selectable": False, "type": "numeric"},
    ]


def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            getMarkdown("overview")
        ])
        # return html.Div([
        #    html.H3('Tab content 1')
        # ])
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
