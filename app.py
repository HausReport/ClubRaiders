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
from dash.dependencies import Input, Output

import craid.dashbd
import craid.dashbd.AnnoyingCrap as crap
import craid.eddb.loader.CreateDataFrame
import craid.eddb.loader.DataProducer as dp
#
# Set up logging
#
# logging.basicConfig(filename='example.log',level=logging.DEBUG)
from craid.eddb.FactionInstance import FactionInstance
from craid.eddb.Oracle import Oracle

logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().level = logging.DEBUG

#
# Heroku requirements
#
server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
DEPLOY = True


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
clubSystemInstances = currentData['allClubSystemInstances']
sysIdFacIdToFactionInstance = currentData['sysIdFacIdToFactionInstance']

systemNameToXYZ: Dict[str, Tuple[float, float, float]] = currentData['systemNameToXYZ']
playerFactionNameToHomeSystemName: Dict[str, str] = currentData['playerFactionNameToSystemName']
df: pd.DataFrame = craid.eddb.loader.CreateDataFrame.getDataFrame(clubSystemInstances)

#
# Massage data
#
nrows = df.shape[0]
df['distance'] = pd.Series(np.zeros(nrows), index=df.index)

#
# Flotsam
#
colors = {
    'background': 'black',
    'text'      : 'orange'
}

#
# Start the app framework
#
if DEPLOY:
    server = flask.Flask(__name__)
    server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
    app = dash.Dash(__name__, server=server)
else:
    app = dash.Dash(__name__)  # ,requests_pathname_prefix='')
    print(__name__)

#
# Following required for tabs
#
app.config.suppress_callback_exceptions = True

#
# Initialize some UI elements
#
opts = crap.getFirstDropdown(systemNameToXYZ)
fopts = crap.getSecondDropdown(playerFactionNameToHomeSystemName)
theColumns = crap.getTheColumns()

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
    # style_header={
    #     'backgroundColor': 'black',
    #     'color'          : 'gold'},
    # style_cell={
    #     'backgroundColor': 'black',
    #     'color'          : 'orange'
    # }
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
# Layout the header
#
hdr_layout = html.Div([
    # html.Div(
    #     className="app-header",
    #     children=[
    #         html.Div('Plotly Dash', className="app-header--title")
    #     ]
    # ),
    html.Label("Choose a System:", className="myLabel"),
    dcc.Dropdown(
        id='demo-dropdown',
        options=opts,
        value='Alioth',
        placeholder='Select star system',
        className="myDropdown",
        # autoFocus=True,
    ),
    html.Label("or a Squadron:", className="myLabel"),
    dcc.Dropdown(
        id='demo-dropdown2',
        options=fopts,
        value='',  # Anti Xeno Initiative',
        placeholder='Select player faction',
        className="myDropdown",
    ),
], className="strict-horizontal")

# TODO: get a hook to tab1 and print its properties to find color settings
# tab1: dcc.Tab = something

#
# Layout the main application
#
app.layout = html.Div([
    hdr_layout,
    dcc.Tabs(id='tabs-example', value='tab-1',
             parent_className='custom-tabs',
             className='custom-tabs-container',
             style={'primary': 'red',
                    'primaryColor': 'red',
                    'selected': 'red'},
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
                             html.Button("Clear filter", id="clear-filter", className="myButton"),
                         ])),
                         html.Div(className="strict-horizontal", style={'vertical-align': 'middle'}, children=([
                             html.Label("Current sort:", style={'flex-grow': '0', 'vertical-align': 'middle'}),
                             html.Label(id='sort-notifier', className="sort-notifier"),
                             html.Button("Clear sort", id="clear-sort", className="myButton"),
                         ])),
                     ]),
                 ]),
                 html.Article(className='main', children=[
                     datatable,
                 ]),
                 html.Aside(className="aside aside-2", children=[
                     html.Article("Nothing selected.", id='faction-drilldown', style={'width': '100%'}),
                     html.Article("Nothing selected.", id='system-drilldown', style={'width': '100%'}),
                 ]),
                 html.Footer(className='footer', children=[
                     html.Div(id='datatable-interactivity-container')
                 ])
             ])
])
## ###### FINISH TABLE MADNESS

# =============================================================
# Tab handlers
# =============================================================
@app.callback(Output('tabs-example-content', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    return craid.dashbd.AnnoyingCrap.render_content(tab)


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
# =============================================================
@app.callback(
    [Output('datatable-interactivity', 'data'), Output('datatable-interactivity', 'columns')],
    [Input('demo-dropdown', 'value')])
def update_output(val1):
    value = val1
    pos = fSystemNameToXYZ(value)
    x = pos[0]
    y = pos[1]
    z = pos[2]

    for ind in df.index:
        x1: float = df.at[ind, 'x']
        y1: float = df.at[ind, 'y']
        z1: float = df.at[ind, 'z']
        dis: float = math.sqrt((x - x1) ** 2 + (y - y1) ** 2 + (z - z1) ** 2)
        # NOTE: demoted this from float to int because no formatting in datatable
        df.at[ind, 'distance'] = int( round(dis))

    _cols = theColumns
    return df.to_dict('records'), _cols

@app.callback(
    dash.dependencies.Output('demo-dropdown', 'value'),
    [dash.dependencies.Input('demo-dropdown2', 'value')])
def update_outputr3(value):
    return value

# @app.callback(
#     dash.dependencies.Output('dd-output-container', 'children'),
#     [Input('datatable-row-ids', 'active_cell')])
# def update_graphs(row_ids, active_cell):
#     if row_ids is None:
#         dff = df
#         # pandas Series works enough like a list for this to be OK
#         row_ids = df['id']
#     else:
#         dff = df.loc[row_ids]
#
#     active_row_id = active_cell['row_id'] if active_cell else None
#     return "You selected row " + active_row_id

@app.callback(
    [Output('faction-drilldown', 'children'),
     Output('system-drilldown', 'children'),
     Output('datatable-interactivity-container', "children")],
    [Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows"),
     Input('datatable-interactivity', 'active_cell'),
     Input('datatable-interactivity', "page_current"),
     Input('datatable-interactivity', "page_size")])
def update_graphs(rows, derived_virtual_selected_rows, active_cell, page_cur, page_size):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncrasy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df if rows is None else pd.DataFrame(rows)

    dataColors = ['gold' if i in derived_virtual_selected_rows else 'orange'
                  for i in range(len(dff))]

    factionInfo: str = "Nothing selected"
    systemInfo: str = "Nothing selected"

    if active_cell:
        row = active_cell['row']
        logical_row = row + page_cur * page_size
        sysId = rows[logical_row]['sysId']
        facId = rows[logical_row]['facId']
        print(str(sysId) + "/" + str(facId))
        theFac: FactionInstance = sysIdFacIdToFactionInstance.get((sysId, facId))
        if theFac is not None:
            print("I think that's system %s and faction %s", theFac.getSystemName(), theFac.get_name())
            factionInfo = theFac.get_name()
            gg: pd.DataFrame = df[df['factionName'].str.match(factionInfo)]
            seer: Oracle = Oracle(gg)
            factionInfo = crap.getString("faction-template")
            output = seer.template(factionInfo)
            factionInfo = theFac.template(output)

            ts = crap.getString("system-template")
            theSys = theFac.getSystem()
            systemInfo = theSys.template(ts)

    factionWidget = dcc.Markdown(factionInfo)
    systemWidget = dcc.Markdown(systemInfo)

    theGraphs = [
        dcc.Graph(
            id=column,
            figure={
                "data"  : [
                    {
                        "x"     : dff["systemName"],
                        "y"     : dff[column],
                        "type"  : "bar",
                        "marker": {"color": dataColors},
                    }
                ],
                "layout": {
                    "xaxis"        : {"automargin": True},
                    "yaxis"        : {
                        "automargin": True,
                        "title"     : {"text": column},
                        "type"      : "log"
                    },
                    "paper_bgcolor": 'rgba(0,0,0,0)',  # TODO fix color & bg
                    "plot_bgcolor" : 'rgba(0,0,0,0)',  # TODO: fix color & bg
                    "height"       : 250,
                    "margin"       : {"t": 10, "l": 10, "r": 10},
                },
            },
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        for column in ["difficulty", "influence", "population"] if column in dff]

    if len(theGraphs) == 0:
        return factionWidget, systemWidget, [None, None, None]
    return factionWidget, systemWidget, [theGraphs[0], theGraphs[1], theGraphs[2]]


#
# Clear sort button
#
@app.callback(
    Output('datatable-interactivity', 'sort_by'),
    [Input('clear-sort', 'n_clicks')])
def clear_sort(n_clicks):
    # return [ {} ]
    print(str(n_clicks))
    return [{'column_id': '', 'direction': 'asc'}]

#
# Clear sort button
#
@app.callback(
    Output('datatable-interactivity', 'filter_query'),
    [Input('clear-filter', 'n_clicks')])
def clear_sort(n_clicks):
    return ""

@app.callback(
    Output('sort-notifier', 'children'),
    [Input('datatable-interactivity', 'sort_by')])
def update_table(sort_by: List):
    if sort_by is None:
        return "None"

    foo = sort_by[0]
    if foo['column_id'] == '':
        sort_by.remove(foo)
    if len(sort_by) == 0:
        return "None"

    return str(sort_by)


@app.callback(
    dash.dependencies.Output('filter-notifier', 'children'),
    [Input('datatable-interactivity', 'filter_query')])
def update_table(query):
    if query is None:
        return "None"
    if len(query) == 0:
        return "None"
    else:
        return str(query)
#
# app.scripts.config.serve_locally = False
# dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'
#


if __name__ == '__main__':
    if DEPLOY:
        app.server.run(debug=True, threaded=True)
    else:
        app.run_server(debug=True)
