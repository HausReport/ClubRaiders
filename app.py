#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import logging
import math
import os
import sys
from random import randint
from typing import Dict, Tuple, List
from multiprocessing import Process

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
from DailyUpdate import DailyUpdate
from appHelpers import AnnoyingCrap, tab_style, tab_selected_style, enCard, makeArticleCard, my_meta_tags, \
    makeDiscordIframe
from craid.club.regions.RegionFactory import RegionFactory
from craid.club.regions.TheUnregion import TheUnregion
from craid.eddb.Oracle import Oracle
from craid.eddb.faction.FactionInstance import FactionInstance
from craid.eddb.system.SystemXYZ import SystemXYZ
from craid.eddb.util.Printmem import printmem

#
# Set up logging
#
logging.basicConfig(
    format='APP - %(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')



styles = {
    'pre': {
        'border'    : 'thin lightgrey solid',
        'overflowX' : 'scroll',
        'height'    : '200px',
        'min-height': '200px',
        'width'     : '200px',
        'min-width' : '200px',
    }
}

#
# Get data
# NOTE: It's built into Dash that this will run twice, see  https://community.plotly.com/t/why-global-code-runs-twice/12514
#
currentData = dp.getDataArrays()
sysIdFacIdToFactionInstance = currentData['sysIdFacIdToFactionInstance']
systemNameToXYZ: Dict[str, Tuple[float, float, float]] = SystemXYZ.myDict  # currentData['systemNameToXYZ']
# playerFactionNameToHomeSystemName: Dict[str, str] = currentData['playerFactionNameToSystemName']
annoyingCrap: AnnoyingCrap = AnnoyingCrap()
df: pd.DataFrame = currentData['dataFrame']
printmem("4")

AnnoyingCrap.setMarkerColors(df)
AnnoyingCrap.setMarkerSize(df)
AnnoyingCrap.setHovertext(df)

#
# Massage data
#
nrows = df.shape[0]
df['distance'] = pd.Series(np.zeros(nrows), index=df.index)

seer: Oracle = Oracle(df)
oracleString = AnnoyingCrap.getString("oracle-template")
oracleMd = dcc.Markdown(seer.template(oracleString))
newsString = AnnoyingCrap.getString("news")
newsString = seer.template(newsString)
newsMarkdown = dcc.Markdown(newsString)
mapOracleMd = oracleMd

#
# Start up Dash
#
appName = __name__
DEPLOY = True  # KEEP THIS TRUE, SRSLY
if DEPLOY:
    #
    # Heroku requirements
    #
    server = flask.Flask(appName)
    server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
    app = dash.Dash(appName, server=server, meta_tags=my_meta_tags )  # , external_stylesheets=[dbc.themes.CYBORG])
    app.scripts.config.serve_locally = False
    app.scripts.append_script({
        'external_url': 'https://www.googletagmanager.com/gtag/js?id=UA-61576455-2'
    })
    app.scripts.append_script({
        'external_url': 'https://erlaed.s3.us-east-2.amazonaws.com/gtag.js'
        # https://raw.githubusercontent.com/HausReport/ClubRaiders/master/assets/gtag.js'
    })
else:
    app = dash.Dash(appName)  # , external_stylesheets=[dbc.themes.CYBORG])
    app.scripts.config.serve_locally = True
    # print(appName)

app.title = "Club Raiders - fighting the BGS war against The Club in Elite: Dangerous"
#
# Following required for tabs
#
app.config.suppress_callback_exceptions = True

#
# Url encoding/parsing stuff
#
urlParameters: Dict = {}

#
# Initialize some UI elements
#
systemDropdown = dcc.Dropdown(
    id='locationDropdown',
    options=AnnoyingCrap.getLocationDropdown(),
    value='Sol',
    placeholder='Select star system',
    className="dropdown-select",
    # persistence=True,
)

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
    # hidden cols seems to cause problems with searches
    # hidden_columns=['salesScore','explorationScore','mineralSalesScore','bountyHuntingScore','smugglingScore','piracyMurderScore'],
    page_action="native",
    page_current=0,
    page_size=30,
    style_cell={
        'backgroundColor': '#2c2e2f',
        'color'          : '#a3a3a3'
    },
    style_header={
        'backgroundColor': '#2c2e2f',
        'color'          : '#a3a3a3'
    },
)

datatable.filter_query = "{isHomeSystem} contains false && {influence} < 25"

#
# Content of tab_1
#
tab_1 = \
    html.Table(className="clean", children=[
        html.Tr(className="clean", children=[
            html.Td(className="left-column", children=[
                html.Div(className="card", children=[
                    html.Label("I want to:", className="simpleColItem"),
                    html.Div(className="dropdown dropdown-dark", children=[
                        dcc.Dropdown(
                            id='activityDropdown',
                            options=AnnoyingCrap.getThirdDropdown(),
                            # persistence=True,
                            placeholder='Select activity',
                            className="dropdown-select",
                        ),
                    ]),
                    html.Label("in the vicinity of", className="simpleColItem"),
                    html.Div(className="dropdown dropdown-dark", children=[
                        systemDropdown,
                    ]),
                ]),
                # html.Button("DarkMode", id="darkModeButton", name="darkModeButton"),
                makeArticleCard(oracleMd, "statistics"),
                makeArticleCard("", "faction-drilldown"),
                makeArticleCard("", "system-drilldown"),
                makeArticleCard(newsMarkdown, "news"),
                # makeDiscordCard(
                #     "## Cabal Operatives\n\nCommanders fighting the BGS war against The Club.",
                #     "cabal-ops",
                #     "439201271174660097"),
                # makeDiscordCard(
                #     "## Elite BGS\n\nFor resources, questions and discussion about the Elite Background Simulation in general.",
                #     "elite-bgs",
                #     "483005833853009950"),
                # End of left column
            ]),  # td closed
            html.Td(className="clean2", children=[
                enCard(html.Div(AnnoyingCrap.getMarkdown('overview'), id="activity")),
                html.Div(className="card", children=[
                    html.Div(className="clean", children=[
                        html.Label("Current filter:", className=''),
                        html.Label(id='filter-notifier', className="code-notifier"),
                        html.Button(id="clear-filter", className="myButton"),
                    ]),
                    html.Div(className="clean", children=[
                        html.Label("Current sort:", className=""),
                        html.Label(id='sort-notifier', className="code-notifier"),
                        html.Button(id="clear-sort", className="myButton"),
                    ]),
                    datatable,
                ]),
            ]),  # td closed
        ]),  # tr closed
    ]),  # table closed

#
# Layout the main application
#

app.layout = html.Div([
    html.Label("placeholder", id='url-holder', style={'display': 'none'}),  # move this into layout to use it
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),
    dcc.Tabs(id='tabs-example', value='tab-1',
             parent_className='custom-tabs',
             className='custom-tabs-container',
             children=[
                 dcc.Tab(label='Activities',
                         value='tab-1',
                         style=tab_style, selected_style=tab_selected_style,
                         ),
                 dcc.Tab(label='Explore ClubSpace',
                         value='tab-2',
                         style=tab_style, selected_style=tab_selected_style,
                         ),
                 dcc.Tab(label='Community',
                         value='tab-3',
                         style=tab_style, selected_style=tab_selected_style,
                         ),
                 dcc.Tab(label='About The Club',
                         value='tab-4',
                         style=tab_style, selected_style=tab_selected_style,
                         ),
                 dcc.Tab(label='About Club Raiders',
                         value='tab-5',
                         style=tab_style, selected_style=tab_selected_style,
                         ),
             ]),
    html.Div(id='tabs-example-content'),
    # html.Script(src="assets/dm.js"),
])

printmem("End")

# =============================================================
# Tab handlers
# =============================================================
@app.callback([Output('url', 'pathname'), Output('tabs-example-content', 'children')],
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return "activities", tab_1
    if tab == 'tab-2':
        unreg = TheUnregion()
        fig = unreg.getFigure(df)
        tab_2 = \
            html.Table(className="clean", children=[
                html.Tr(className="clean", children=[
                    html.Td(className="left-column", children=[
                        html.Div(className="card", children=[
                            html.Label("Select squadron:", className="simpleColItem"),
                            AnnoyingCrap.getSquadronDropdown(),
                            html.Label("or galactic region:", className="simpleColItem"),
                            AnnoyingCrap.getRegionDropdown(),
                        ]),
                        makeArticleCard(mapOracleMd, "map-statistics"),
                        makeArticleCard("", "map-faction-drilldown"),
                        makeArticleCard("", "map-system-drilldown"),
                    ]),
                    html.Td(className="clean", children=[
                        html.Label("Red: Club home system, Yellow: Club controls system, Green: Club active in system",
                                   className="blackColItem"),
                        html.Label("Drag mouse to rotate, Ctrl-mouse to pan, Alt-mouse or wheel to zoom.",
                                   className="blackColItem"),
                        dcc.Graph(id="the-graph", figure=fig),
                    ])
                ]),
            ])
        return "clubSpace", tab_2
    elif tab == 'tab-3':
        #print('tab-3 clicked')
        return "community", html.Div([
            html.H1('ClubRaiders Community Tools & Resources'),
            html.Table(className="clean", children=[
                html.Tr(className="clean", children=[
                    html.Td(className="left-column", children=[
                        makeDiscordIframe("x-cabal-ops", "439201271174660097"),
                    ]),
                    html.Td(className="clean-left", children=[
                        AnnoyingCrap.getMarkdown("CabalOperatives"),
                    ])
                ]),
                html.Tr(className="clean", children=[
                    html.Td(className="left-column", children=[
                        makeDiscordIframe("x-irh", "530542802032001074"),
                    ]),
                    html.Td(className="clean-left", children=[
                        AnnoyingCrap.getMarkdown("IRH"),
                    ])
                ]),
                html.Tr(className="clean", children=[
                    html.Td(className="left-column", children=[
                        dcc.Markdown("![](https://github.com/HausReport/ClubRaiders/raw/master/assets/FdevForum.jpg)")
                    ]),
                    html.Td(className="clean-left", children=[
                        AnnoyingCrap.getMarkdown("FrontierForum"),
                    ])
                ]),
                html.Tr(className="clean", children=[
                    html.Td(className="left-column", children=[
                        makeDiscordIframe("x-edbgs", "483005833853009950"),
                    ]),
                    html.Td(className="clean-left", children=[
                        AnnoyingCrap.getMarkdown("EliteBGS"),
                    ])
                ]),

            ])
        ], className="container")
    elif tab == 'tab-4':
        #print('tab-4 clicked')
        return "aboutTheClub", html.Div(children=[
            html.Article([
                AnnoyingCrap.getMarkdown("aboutClub")
            ]),
            seer.getFactionTable()
        ])
    elif tab == 'tab-5':
        #print('tab-5 clicked')
        return "aboutClubRaiders", html.Article([
            AnnoyingCrap.getMarkdown("aboutRaiders")
        ])


#
# Convert system name to coordinates
#
def fSystemNameToXYZ(sName: str):  # -> tuple(3): #float, float, float):
    pos = systemNameToXYZ.get(sName)
    if pos is None: pos = (0, 0, 0)
    return pos


# =============================================================
# Callback handlers below
# =============================================================
def updateUrl(key: str, val: str) -> str:
    global urlParameters
    if key is None:
        return str(urlParameters)
    newVal = str(val)
    if newVal == '':
        try:
            urlParameters.pop(key)
        except KeyError:
            pass
    else:
        urlParameters[key] = newVal
    # return str(key) + "=" + str(newVal)
    return str(urlParameters)  # {key: val})


#
# When user changes sort on datatable, put the query in a visible label.
#
@app.callback(
    [Output('url-holder', 'children'), Output('filter-notifier', 'children'), Output('sort-notifier', 'children')],
    [Input('datatable-interactivity', 'filter_query'), Input('datatable-interactivity', 'sort_by')])
def sort_changed(query: str, sort_by: List):
    if query is None or len(query) == 0:
        updateUrl('filter', '')
    else:
        logging.debug("Updating filter: " + str(query))
        updateUrl('filter', str(query))

    if sort_by is None or len(sort_by) == 0:
        updateUrl('sort', '')
    else:
        foo1 = sort_by[0]
        if foo1['column_id'] == '':
            sort_by.remove(foo1)
        if len(sort_by) == 0:
            updateUrl('sort', '')
        else:
            logging.debug("Updating sort: " + str(sort_by))
            updateUrl('sort', sort_by)

    ssb: str = str(sort_by)
    logging.info(f"Query=[{query}], Sort=[{ssb}]")
    # theUrl = updateUrl(None,None)
    # print("theUrl: " + theUrl)
    # import craid.eddb.util.GzipString
    # comp =  str(craid.eddb.util.GzipString.gzip_str( theUrl))
    # print("compressed: " + comp)
    # print("decompressed: " + gunzip_str(comp))

    return updateUrl(None, None), str(query), ssb


#
# Determines which control was used.  Perhaps the most ridiculous part of Dash.
#
def was_clicked(ctx, button_id):
    if not ctx.triggered:
        return None, None

    ctx_msg = ujson.dumps({
        'states'   : ctx.states,
        'triggered': ctx.triggered,
        'inputs'   : ctx.inputs
    }, indent=2)

    aDict = ujson.loads(ctx_msg)
    triggered = aDict['triggered']  # ['prop_id']
    elt0 = triggered[0]
    prop_id = elt0['prop_id']
    inputs = aDict['inputs']  # ['prop_id']
    activity = inputs['activityDropdown.value']

    if prop_id != button_id:
        return None, activity

    value = elt0['value']

    if value == 0:
        return None, activity

    return value, activity


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
    # TODO: add url to input and output
    # check url (& change) url _after_ checking buttons

    ## NOTE:https://dash.plotly.com/advanced-callbacks
    ## NOTE: Here there be dragons.  Careful about changes.
    ctx = dash.callback_context
    value, act = was_clicked(ctx, 'clear-filter.n_clicks')
    if (act is None) or (act == ''):
        logging.debug("No act state (1), going with default 0")
        # act = 0

    # clear filter button was clicked
    if value is not None:
        msg = AnnoyingCrap.getMessage(int(value))
        logging.debug("Cleared filter, Act state: " + str(value))
        return "", msg

    value, act = was_clicked(ctx, 'activityDropdown.value')
    # activity was selected
    if value is None or value == '':
        logging.debug("No act state (2), going with default 0")
        value = 0

    # print("Selected activity: " + str(value))
    newFilter = AnnoyingCrap.getFilter(int(value))
    # print("Filter: " + str(newFilter))
    msg = AnnoyingCrap.getMessage(int(value))
    return newFilter, msg

    # logging.warning("None of the filter cases hit")
    # return "", act


#
# Change sort via "clear" button or a canned query
#
@app.callback(
    Output('datatable-interactivity', 'sort_by'),
    [Input('clear-sort', 'n_clicks'), Input('activityDropdown', 'value')])
def update_sort(n_clicks, val3):
    # TODO: add url to input and output
    # check url (& change) url _after_ checking buttons

    defaultSort = [{'column_id': 'distance', 'direction': 'asc'}]
    noSort = []

    ctx = dash.callback_context
    value, act = was_clicked(ctx, 'clear-sort.n_clicks')

    # clear sort button was clicked
    if value is not None:
        logging.debug("Clear sort button was clicked.")
        return noSort

    value, act = was_clicked(ctx, 'activityDropdown.value')
    # activity was clicked
    if value is not None and value != '':
        logging.debug("Sort: selected activity: " + str(value))
        newSort = AnnoyingCrap.getSort(int(value))
        logging.debug("Sort: " + str(newSort))
        return newSort

    logging.warning("None of the sort cases hit")
    return defaultSort


#
# When user selects a system and/or activity, update the table.  Particularly
# the distance column.
#
@app.callback(
    [Output('datatable-interactivity', 'data'), Output('datatable-interactivity', 'columns')],
    [Input('locationDropdown', 'value')])
def update_selected_system(val0):
    if val0 == "":
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


def getFacInfoSysInfo(sysId, facId):
    global df
    global sysIdFacIdToFactionInstance

    theFac: FactionInstance = sysIdFacIdToFactionInstance.get((sysId, facId))
    if theFac is not None:
        logging.debug("I think that's system %s and faction %s", theFac.getSystemName(), theFac.get_name())
        factionInfo = theFac.get_name()

        factionRows: pd.DataFrame = df[df['factionName'].str.match(factionInfo)]
        tmpSeer: Oracle = Oracle(factionRows)
        factionInfo = AnnoyingCrap.getString("faction-template")
        output = tmpSeer.template(factionInfo)
        factionInfo = theFac.template(output)

        ts = AnnoyingCrap.getString("system-template")
        theSys = theFac.getSystem()
        systemInfo = theSys.template(ts, theFac)
        return factionInfo, systemInfo

    return "", ""


#
#  Does a variety of things when user clicks on a cell in the table
#
# , Output('datatable-interactivity-container', "children")],
@app.callback(
    [Output('faction-drilldown', 'children'),
     Output('system-drilldown', 'children')],
    [Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows"),
     Input('datatable-interactivity', 'active_cell'),
     Input('datatable-interactivity', "page_current"),
     Input('datatable-interactivity', "page_size")])
def update_graphs(rows, derived_virtual_selected_rows, active_cell, page_cur, page_size):
    # From https://dash.plotly.com/datatable/interactivity
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    factionInfo: str = ""
    systemInfo: str = ""

    if active_cell:
        row = active_cell['row']
        logical_row = row + page_cur * page_size
        # NOTE: if a row is selected, then a filter is applied and that rownumber
        # is higher than the number of visible rows, this would cause an error.
        # setting log_row to 0 sidesteps that case
        if logical_row >= len(rows):
            logical_row = 0
        sysId = rows[logical_row]['sysId']
        facId = rows[logical_row]['facId']
        logging.debug(str(sysId) + "/" + str(facId))
        factionInfo, systemInfo = getFacInfoSysInfo(sysId, facId)

    factionWidget = dcc.Markdown(factionInfo)
    systemWidget = dcc.Markdown(systemInfo)
    return factionWidget, systemWidget


@app.callback(
    [Output('map-faction-drilldown', 'children'),
     Output('map-system-drilldown', 'children')],
    [Input('the-graph', 'clickData')])
def display_click_data(clickData):
    global df

    factionInfo: str = ""
    systemInfo: str = ""

    if clickData is not None:
        pts = clickData["points"]
        if pts is not None:
            pts0 = pts[0]
            if pts0 is not None:
                sysName = pts0["text"]
                logging.debug("sysName = " + sysName)
                systemRows = df[df['systemName'] == sysName]
                if systemRows is not None:
                    facId = systemRows['facId'].iloc[0]
                    facName = systemRows['factionName'].iloc[0]
                    sysId = systemRows['sysId'].iloc[0]
                    logging.debug("facName = " + str(facName))
                    logging.debug("facId = " + str(facId))
                    logging.debug("sysId = " + str(sysId))
                    factionInfo, systemInfo = getFacInfoSysInfo(sysId, facId)

    factionWidget = dcc.Markdown(factionInfo)
    systemWidget = dcc.Markdown(systemInfo)
    return factionWidget, systemWidget


#
# Determines which control was used.  Perhaps the most ridiculous part of Dash.
#
def was_clicked2(ctx, button_id):
    if not ctx.triggered:
        return None, None

    ctx_msg = ujson.dumps({
        'states'   : ctx.states,
        'triggered': ctx.triggered,
        'inputs'   : ctx.inputs
    }, indent=2)

    aDict = ujson.loads(ctx_msg)
    triggered = aDict['triggered']  # ['prop_id']
    elt0 = triggered[0]
    prop_id = elt0['prop_id']

    #print("prop_id=" + str(prop_id))
    inputs = aDict['inputs']  # ['prop_id']
    # activity = inputs['activityDropdown.value']

    if prop_id == button_id + ".value":
        value = elt0['value']
        return value

    return None


@app.callback(
    [Output('the-graph', 'figure'), Output('map-statistics', 'children')],
    [Input('squadronDropdown', 'value'), Input('regionDropdown', 'value')])
def display_click_data(squadName, regName):
    global df
    global mapOracleMd

    ctx = dash.callback_context
    value = was_clicked2(ctx, "squadronDropdown")
    reg = None
    val = None

    if value is not None:
        val = squadName
        reg = RegionFactory.getSquadronRegion(val, 64, "rgb(0,0,255)")

    value = was_clicked2(ctx, "regionDropdown")
    if value is not None:
        val = regName
        reg = RegionFactory.regionDict.get(val)

    if reg is not None:
        newFigure = reg.getFigure( df)
        #
        # Local scoreboard
        #
        view = reg.getView(df)
        seer2: Oracle = Oracle(view)
        oracleString2 = AnnoyingCrap.getString("region-oracle")
        mapOracleMd = dcc.Markdown(seer2.template(oracleString2))

        printmem("d")
        return newFigure, mapOracleMd

    unreg = TheUnregion()
    return unreg.getFigure(df), mapOracleMd

#
# Unfortunately, this doesn't help.... need to restart all dynos.
#
# @app.server.route('/shutdown', methods=['GET','POST'])
# def shutdown():
#     #shutdown_server()
#     print('Server shutting down...')
#     sys.exit(0)

if __name__ == '__main__':
    print('-----------> TOP OF MAIN <-----------------')
    #
    # Start Daily Update Daemon
    #
    dup = DailyUpdate()
    p = Process(target=dup.run)  # , args=('bob',))
    p.start()
    #dup.run()
    if DEPLOY:
        app.server.run(debug=False, threaded=True, use_reloader=True)
    else:
        app.run_server(debug=True)
