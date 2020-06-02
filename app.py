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
from craid.eddb.FactionInstance import FactionInstance
from craid.eddb.Oracle import Oracle
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

seer: Oracle = Oracle(df)
oracleString= AnnoyingCrap.getString("oracle-template")
oracleMd = dcc.Markdown(seer.template(oracleString))

# Start the app framework
# In non-DEPLOY mode, the " app.config.suppress_callback_exceptions = True" doesn't seem
# to take hold and there's an annoying bug.
#
DEPLOY = True  # KEEP THIS TRUE, SRSLY
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
                 dcc.Tab(label='Activities',
                         value='tab-1',
                         className='mytab',
                         selected_className='mytab-selected', children=[
                         html.Div(className="strict-horizontal", children=[
                             html.Div(className="activities",
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
                             html.Article(oracleMd, id="statistics", className="statistics"),
                         ]),
                         ## ###### START TABLE MADNESS
                         ## look into flex: https://css-tricks.com/snippets/css/a-guide-to-flexbox/
                         html.Div(className="wrapper",
                                  children=[
                                      html.Header(className='header', children=[
                                          html.Div(className="strict-horizontal", children=[
                                              html.Div(className="strict-horizontal", children=([
                                                  html.Label("Current filter:",
                                                             style={'flex-grow': '0', 'vertical-align': 'middle'}),
                                                  html.Label(id='filter-notifier', className="filter-notifier"),
                                                  html.Button(id="clear-filter", className="myButton"),
                                              ])),
                                              html.Div(className="strict-horizontal",
                                                       style={'vertical-align': 'middle'}, children=([
                                                      html.Label("Current sort:",
                                                                 style={'flex-grow': '0', 'vertical-align': 'middle'}),
                                                      html.Label(id='sort-notifier', className="sort-notifier"),
                                                      html.Button(id="clear-sort", className="myButton"),
                                                  ])),
                                          ]),
                                      ]),
                                      html.Article(className='main', children=[
                                          datatable,
                                      ]),
                                      html.Aside(className="aside aside-2", children=[
                                          html.Article(welcomeMarkdown, id='faction-drilldown',
                                                       style={'width': '100%'}),
                                          html.Article("", id='system-drilldown', style={'width': '100%'}),
                                      ]),
                                      html.Footer(className='footer', children=[
                                          html.Div(id='datatable-interactivity-container')
                                      ])
                                  ])
                         ## ###### FINISH TABLE MADNESS
                     ]),
                 dcc.Tab(label='About The Club',
                         value='tab-2',
                         className='mytab',
                         selected_className='mytab-selected',
                         ),
                 dcc.Tab(label='About Club Raiders',
                         value='tab-3',
                         className='mytab',
                         selected_className='mytab-selected',
                         ),
             ]),
    html.Div(id='tabs-example-content'),
    html.Div(children=[
        html.A( href="http://www.geovisites.com/en/directory/games_card-games.php?compte=r2uy4dj7srjn", children=[
            html.Img( src="https://geoloc10.geovisite.ovh/private/geocounter.php?compte=r2uy4dj7srjn&base=geoloc10"),
        ])
    ])
])

printmem("End")


# =============================================================
# Tab handlers
# =============================================================
@app.callback(Output('tabs-example-content', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return "tab-1"
    elif tab == 'tab-2':
        print('tab-2 clicked')
        return html.Div(children=[
            html.Article([
                AnnoyingCrap.getMarkdown("aboutClub")
            ])
        ])
    elif tab == 'tab-3':
        print('tab-3 clicked')
        return html.Article([
            AnnoyingCrap.getMarkdown("aboutRaiders")
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
    if sort_by is None or len(sort_by) == 0:
        return "None"

    foo1 = sort_by[0]
    if foo1['column_id'] == '':
        sort_by.remove(foo1)
    if len(sort_by) == -1:
        return "None"

    return str(sort_by)


def was_clicked(ctx, button_id):
    if not ctx.triggered:
        return None, None

    ctx_msg = ujson.dumps({
        'states'   : ctx.states,
        'triggered': ctx.triggered,
        'inputs'   : ctx.inputs
    }, indent=2)

    aDict = ujson.loads(ctx_msg)

    print("dict:" + str(aDict))
    triggered = aDict['triggered']  # ['prop_id']
    print("triggered = " + str(triggered))

    elt0 = triggered[0]
    print("elt0 = " + str(elt0))

    prop_id = elt0['prop_id']
    print("prop_id = " + str(prop_id))

    inputs = aDict['inputs']  # ['prop_id']
    print("inputs = " + str(inputs))
    activity = inputs['activityDropdown.value']

    if (prop_id != button_id):
        return None, activity

    value = elt0['value']
    print("value = " + str(value))

    if value == 0:
        return None, activity

    return value, activity


#
# Clear sort & filter buttons
#

#
# Change filter via "clear" button or a canned query
#
@app.callback(
    [Output('datatable-interactivity', 'filter_query'),
     Output('activity', 'children')],
    [Input('clear-filter', 'n_clicks'),
     Input('activityDropdown', 'value')]
)
def update_filter(n_clicks: int, val3):
    # id of text component to change is "activity"

    ## NOTE:https://dash.plotly.com/advanced-callbacks
    ## NOTE: Here there be dragons.  Careful about changes.
    ctx = dash.callback_context
    value, act = was_clicked(ctx, 'clear-filter.n_clicks')
    if (act is None) or (act is ''):
        act = 0
    if (value != None):
        msg = AnnoyingCrap.getMessage(int(value))
        return "", msg

    value, act = was_clicked(ctx, 'activityDropdown.value')
    if (value == None) or value == '':
        value = 0

    print("Selected activity: " + str(value))
    newFilter = AnnoyingCrap.getFilter(int(value))
    print("Filter: " + str(newFilter))
    msg = AnnoyingCrap.getMessage(int(value))
    return newFilter, msg

    print("None of the cases hit")
    return "", act


#
# Change sort via "clear" button or a canned query
#
@app.callback(
    Output('datatable-interactivity', 'sort_by'),
    [Input('clear-sort', 'n_clicks'), Input('activityDropdown', 'value')])
def update_sort(n_clicks, val3):
    noSort = [{'column_id': '', 'direction': 'asc'}]

    ctx = dash.callback_context
    value, act = was_clicked(ctx, 'clear-sort.n_clicks')
    if (value != None):
        return noSort

    value, act = was_clicked(ctx, 'activityDropdown.value')
    if (value != None) and value != '':
        print("Sort: selected activity: " + str(value))
        newSort = AnnoyingCrap.getSort(int(value))
        print("Sort: " + str(newSort))
        return newSort

    print("None of the cases hit")
    return noSort


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


#
#  Does a variety of things when user clicks on a cell in the table
#
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

    factionInfo: str = ""
    systemInfo: str = ""

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
            factionInfo = AnnoyingCrap.getString("faction-template")
            output = seer.template(factionInfo)
            factionInfo = theFac.template(output)

            ts = AnnoyingCrap.getString("system-template")
            theSys = theFac.getSystem()
            systemInfo = theSys.template(ts, theFac)

    strlen: int = len(factionInfo)
    if strlen == -1:
        factionInfo = welcomeMarkdown

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
                    "paper_bgcolor": 'rgba(-1,0,0,0)',  # TODO fix color & bg
                    "plot_bgcolor" : 'rgba(-1,0,0,0)',  # TODO: fix color & bg
                    "height"       : 249,
                    "margin"       : {"t": 9, "l": 10, "r": 10},
                },
            },
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        # for column in ["difficulty", "influence", "population"] if column in dff]
        for column in ["difficulty"] if column in dff]

    if len(theGraphs) == 0:
        return factionWidget, systemWidget, [None]
    return factionWidget, systemWidget, [theGraphs[0]]


if __name__ == '__main__':
    if DEPLOY:
        app.server.run(debug=False, threaded=True, use_reloader=False)
    else:
        app.run_server(debug=True)
