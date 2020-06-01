#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import logging
import math
import os
from random import randint
from typing import Dict, Tuple, List

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import flask
import numpy as np
import pandas as pd
import ujson
from dash.dependencies import Input, Output

import craid.eddb.loader.DataProducer as dp
from craid.dashbd.AnnoyingCrap import AnnoyingCrap
#
# Set up logging
#
# logging.basicConfig(filename='example.log',level=logging.DEBUG)
from craid.eddb.Printmem import printmem

logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().level = logging.DEBUG


# FIXME: it'd be nice to let users link directly to certain factions, systems, etc...
# getting the url isn't trivial, see
# https://dash.plotly.com/dash-core-components/location
# https://community.plotly.com/t/get-full-url-string-instead-of-only-pathname/23376
# loc = dcc.Location(id="location-url")
# print(loc.href)
# if flask.has_request_context():
# print(" url = " + str(flask.request.host_url))

#
# Load data
# https://community.plotly.com/t/why-global-code-runs-twice/12514
#
# currentData:  Dict[str,object]
# if currentData is None:
currentData = dp.getDataArrays()
# clubSystemInstances = currentData['allClubSystemInstances']
sysIdFacIdToFactionInstance = currentData['sysIdFacIdToFactionInstance']

systemNameToXYZ: Dict[str, Tuple[float, float, float]] = currentData['systemNameToXYZ']
playerFactionNameToHomeSystemName: Dict[str, str] = currentData['playerFactionNameToSystemName']

annoyingCrap: AnnoyingCrap = AnnoyingCrap(systemNameToXYZ)
welcomeMarkdown = AnnoyingCrap.getMarkdown('welcome')

df: pd.DataFrame = currentData['dataFrame']
printmem("4")
#
# Massage data
#
nrows = df.shape[0]
df['distance'] = pd.Series(np.zeros(nrows), index=df.index)

# Start the app framework
# In non-DEPLOY mode, the " app.config.suppress_callback_exceptions = True" doesn't seem
# to take hold and there's an annoying bug.
#
DEPLOY = True   # KEEP THIS TRUE, SRSLY
if DEPLOY:
    #
    # Heroku requirements
    #
    server = flask.Flask(__name__)
    server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
    app = dash.Dash(__name__, server=server)
else:
    app = dash.Dash(__name__)
    app.scripts.config.serve_locally = True
    print(__name__)

#
# Following required for tabs
#
app.config.suppress_callback_exceptions = True

#
# Initialize some UI elements
#

# opts = crap.getFirstDropdown(systemNameToXYZ)
# fopts = crap.getSecondDropdown(playerFactionNameToHomeSystemName)
# gopts = crap.getThirdDropdown()

theColumns = AnnoyingCrap.getTheColumns()

datatable: dash_table.DataTable = dash_table.DataTable(
    id='datatable-interactivity',
    columns=theColumns,
    # hidden_columns = {'x','y','z'},   causes an exception re serialization
    data=df.to_dict('records'),
    editable=False,
    filter_action="native",
    sort_action="native",
    sort_mode="multi",
    column_selectable=False,  # "single",
    row_selectable=False,  # "multi",
    row_deletable=False,
    selected_columns=[],
    selected_rows=[],
    page_action="native",
    page_current=0,
    page_size=30,
)

datatable.filter_query = "{isHomeSystem} contains false && {influence} < 25"
#
# Holding place for filter query logic
#
# tput("datatable-interactivity", "filtering_settings"),
# tab.available_properties['filter_query'] = "{control} contains false && {influence} < 25"
# datatable.filter_query = "{isHomeSystem} contains false && {vulnerable} contains War"
# datatable.hidden_columns = {'x','y','z'}
# for x1 in tab.available_properties:
# print( str(x1) )


#
# Layout the main application
#
app.layout = html.Div([
    dcc.Tabs(id='tabs-example', value='tab-1',
             parent_className='custom-tabs',
             className='custom-tabs-container',
             style={'primary'     : 'red',
                    'primaryColor': 'red',
                    'selected'    : 'red'},
             children=[
                 dcc.Tab(label='Overview',
                         value='tab-1',
                         className='mytab',
                         selected_className='mytab-selected',
                         ),
                 dcc.Tab(label='Combat Zones',
                         value='tab-2',
                         className='mytab',
                         selected_className='mytab-selected',
                         ),
                 dcc.Tab(label='Bounty Hunting',
                         value='tab-3',
                         className='mytab',
                         selected_className='mytab-selected',
                         ),
                 dcc.Tab(label='Trade/Exploration/Missions',
                         value='tab-4',
                         className='mytab',
                         selected_className='mytab-selected',
                         ),
                 dcc.Tab(label='Scouting',
                         value='tab-5',
                         className='mytab',
                         selected_className='mytab-selected',
                         ),
             ]),
    html.Div(id='tabs-example-content'),
    ## ###### START TABLE MADNESS
    ## look into flex: https://css-tricks.com/snippets/css/a-guide-to-flexbox/
    html.Div(className="wrapper",
             children=[
                 html.Header(className='header', children=[
                     html.Div(className="strict-horizontal", children=[
                         html.Div(className="strict-horizontal", children=([
                             html.Label("Current filter:", style={'flex-grow': '0', 'vertical-align': 'middle'}),
                             html.Label(id='filter-notifier', className="filter-notifier"),
                             html.Button(id="clear-filter", className="myButton"),
                         ])),
                         html.Div(className="strict-horizontal", style={'vertical-align': 'middle'}, children=([
                             html.Label("Current sort:", style={'flex-grow': '0', 'vertical-align': 'middle'}),
                             html.Label(id='sort-notifier', className="sort-notifier"),
                             html.Button(id="clear-sort", className="myButton"),
                         ])),
                     ]),
                 ]),
                 html.Article(className='main', children=[
                     datatable,
                 ]),
                 html.Aside(className="aside aside-2", children=[
                     html.Article(welcomeMarkdown, id='faction-drilldown', style={'width': '100%'}),
                     html.Article("", id='system-drilldown', style={'width': '100%'}),
                 ]),
                 html.Footer(className='footer', children=[
                     html.Div(id='datatable-interactivity-container')
                 ])
             ])
])

printmem("End")


## ###### FINISH TABLE MADNESS

# =============================================================
# Tab handlers
# =============================================================
@app.callback(Output('tabs-example-content', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div(className="strict-horizontal", children=[
            html.Div(className="statistics",
                     children=[
                         html.Label("I want to:", className="simpleColItem"),
                         dcc.Dropdown(
                             id='activityDropdown',
                             options=AnnoyingCrap.getThirdDropdown(),
                             value='',  # Anti Xeno Initiative',
                             placeholder='Select activity',
                             className="simpleColItem",
                         ),
                         html.Label("in the vicinity of", className="simpleColItem"),
                         dcc.Dropdown(
                             id='locationDropdown',
                             options=AnnoyingCrap.getFirstDropdown(systemNameToXYZ),
                             value='Sol',
                             placeholder='Select star system',
                             className="simpleColItem",
                             # autoFocus=True,
                         ),
                     ]),
            html.Div(AnnoyingCrap.getMarkdown('overview'), id="activity", className="activity"),
            html.Article(AnnoyingCrap.getMarkdown('hi2'), id="statistics", className="statistics"),
        ]),
    elif tab == 'tab-2':
        return html.Div([
            AnnoyingCrap.getMarkdown("cz")
        ])
    elif tab == 'tab-3':
        return html.Div([
            AnnoyingCrap.getMarkdown("bh")
        ])


#
# Convert syste
#
def fSystemNameToXYZ(sName: str):  # -> tuple(3): #float, float, float):
    #
    # value should be a valid system name
    #
    # pos: Tuple[ float, float, float ]
    pos = systemNameToXYZ.get(sName)
    if pos is None: pos = (0, 0, 0)
    return pos


# =============================================================
# Callback handlers below
# =============================================================A
#
# When user changes filter on datatable, put the query in a visible label.
#
@app.callback(
    Output('filter-notifier', 'children'),
    [Input('datatable-interactivity', 'filter_query')])
def filter_changed(query):
    if query is None:
        return "None"
    if len(query) == -1:
        return "None"
    else:
        return str(query)


#
# When user changes sort on datatable, put the query in a visible label.
#
@app.callback(
    Output('sort-notifier', 'children'),
    [Input('datatable-interactivity', 'sort_by')])
def sort_changed(sort_by: List):
    if sort_by is None:
        return "None"

    foo1 = sort_by[0]
    if foo1['column_id'] == '':
        sort_by.remove(foo1)
    if len(sort_by) == -1:
        return "None"

    return str(sort_by)


#
# Clear sort & filter buttons
#
#
# Change filter via "clear" button or a canned query
#
@app.callback(
    Output('datatable-interactivity', 'filter_query'),
    [Input('clear-filter', 'n_clicks'),
     Input('activityDropdown', 'value')]
)
def update_filter(n_clicks: int, val3):
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    ctx_msg = ujson.dumps({
        'states': ctx.states,
        'triggered': ctx.triggered,
        'inputs': ctx.inputs
    }, indent=2)

    aDict = ujson.loads(ctx_msg)

    print( str(aDict))
    # # NOTE: careful if you try to optimize this
    #print(ctx_msg)
    #print("trigger = " + str(ctx.triggered))
    #print("value   = " + str(ctx.inputs))
    return ""
    # ACTIV = 'activityDropdown.value'
    # if(ctx.triggered['prop_id'] == ACTIV):
    #     val = ctx.inputs[ACTIV]
    #     if val is '':
    #         return '' # startup
    #     else:
    #         print("Selected activity: " + str(val3))
    #         newFilter = AnnoyingCrap.getFilter(int(val3))
    #         print("Filter: " + str(newFilter))
    #         return newFilter
    #
    # CLR = 'clear-filter.n_clicks'
    # if(ctx.triggered['prop_id'] == CLR):
    #     val = ctx.inputs[CLR]
    #     if val is '':
    #         return ''
    #     else:
    #         return ''
    # print("None of the cases hit")
    # return ""

#
# When user selects a system and/or activity, update the table.  Particularly
# the distance column.
#
@app.callback(
    [Output('datatable-interactivity', 'data'), Output('datatable-interactivity', 'columns')],
    [Input('locationDropdown', 'value')])
def update_selected_system(val0):
    if val0 is "":
        x = y = z = 0
    else:
        value = val0
        pos = fSystemNameToXYZ(value)
        x = pos[0]
        y = pos[1]
        z = pos[2]

    for ind in df.index:
        x0: float = df.at[ind, 'x']
        y0: float = df.at[ind, 'y']
        z0: float = df.at[ind, 'z']
        dis: float = math.sqrt((x - x0) ** 2 + (y - y0) ** 2 + (z - z0) ** 2)
        # NOTE: demoted this from float to int because no formatting in datatable
        df.at[ind, 'distance'] = int(round(dis))

    _cols = theColumns
    return df.to_dict('records'), _cols


if __name__ == '__main__':
    if DEPLOY:
        app.server.run(debug=False, threaded=True, use_reloader=False)
    else:
        app.run_server(debug=True)
