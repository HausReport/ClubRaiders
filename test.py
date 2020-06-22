#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

import logging

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import ujson
from dash.dependencies import Output, Input

import craid.eddb.loader.DataProducer as dp
from craid.club.regions.RegionFactory import RegionFactory
from craid.eddb.FactionInstance import FactionInstance
from craid.eddb.Oracle import Oracle
from craid.eddb.Printmem import printmem
from craid.dashbd.AnnoyingCrap import AnnoyingCrap

logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().level = logging.DEBUG

# These go away when merging
def enCard(contents) -> html.Div:
    return html.Div(className="card", children=[
        contents,
    ])

def makeArticleCard(contents, id_) -> html.Div:
    return enCard(html.Article(contents, id=id_, className="simpleColItem"))


#########################################################################

printmem("a")
app = dash.Dash(__name__) #, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

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

# df["marker_size"] = df["difficulty"].apply(lambda x: 1 if x<10 else log(x))       # difficult = larger
# df["marker_size"] = df["difficulty"].apply(lambda x: 20 if x<10 else 20/log(x))    # easy = larger
# reg = RegionFactory.getSquadronRegion(regionName, 64, 'rgba(0,0,255,0.05)')


arrays = dp.getDataArrays()
df: pd.DataFrame = arrays['dataFrame']
sysIdFacIdToFactionInstance = arrays['sysIdFacIdToFactionInstance']

AnnoyingCrap.setMarkerColors(df)
AnnoyingCrap.setMarkerSize(df)
AnnoyingCrap.setHovertext(df)

printmem("b")

seer: Oracle = Oracle(df)
oracleString = AnnoyingCrap.getString("oracle-template")
mapOracleMd = dcc.Markdown(seer.template(oracleString))

# Create figure
fig = AnnoyingCrap.getFigure(None, df)

app.layout = \
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
                html.Label("Red: Club home system, Yellow: Club controls system, Green: Club active in system", className="blackColItem"),
                html.Label("Drag mouse to rotate, Ctrl-mouse to pan, Alt-mouse or wheel to zoom.", className="blackColItem"),
                dcc.Graph(id="the-graph", figure=fig),
            ])
        ]),
    ])

def getFacInfoSysInfo(sysId, facId):
    global df
    global sysIdFacIdToFactionInstance

    theFac: FactionInstance = sysIdFacIdToFactionInstance.get((sysId, facId))
    if theFac is not None:
        print("I think that's system %s and faction %s", theFac.getSystemName(), theFac.get_name())
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
                print("sysName = " + sysName)
                systemRows = df[df['systemName'] == sysName]
                if systemRows is not None:
                    facId = systemRows['facId'].iloc[0]
                    facName = systemRows['factionName'].iloc[0]
                    sysId = systemRows['sysId'].iloc[0]
                    print("facName = " + str(facName))
                    print("facId = " + str(facId))
                    print("sysId = " + str(sysId))
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

    print("prop_id=" + str(prop_id))
    inputs = aDict['inputs']  # ['prop_id']
    # activity = inputs['activityDropdown.value']

    if (prop_id == button_id + ".value"):
        value = elt0['value']
        return value

    return None


@app.callback(
    [Output('the-graph', 'figure'), Output('map-statistics','children')],
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
        newFigure = AnnoyingCrap.getFigure(reg, df)

        #
        # Local scoreboard
        #
        view = AnnoyingCrap.getView(reg,df)
        seer: Oracle = Oracle(view)
        oracleString = AnnoyingCrap.getString("oracle-template")
        mapOracleMd = dcc.Markdown(seer.template(oracleString))

        printmem("d")
        return newFigure, mapOracleMd

    return AnnoyingCrap.getFigure(None, df), mapOracleMd


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)
