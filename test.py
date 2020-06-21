#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

import logging

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import ujson
from dash.dependencies import Output, Input

import craid.eddb.loader.DataProducer as dp
from craid.club.regions.RegionFactory import RegionFactory
from craid.eddb.SquadronXYZ import SquadronXYZ

logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().level = logging.DEBUG

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

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


def setMarkerSize(dataFrame):
    dataFrame.loc[dataFrame['control'] == True, 'marker_size'] = 8  # Medium is not home/control
    dataFrame.loc[dataFrame['control'] == False, 'marker_size'] = 5  # Small is not home/not control
    dataFrame.loc[dataFrame['isHomeSystem'] == True, 'marker_size'] = 15  # Large is home
    # df["marker_size"] = df["influence"].apply(lambda x: 5+ x/5)


def setMarkerColors(dataFrame):
    dataFrame.loc[dataFrame['control'] == True, 'color'] = "#ffbf00"  # Yellow is control/not home
    dataFrame.loc[dataFrame['control'] == False, 'color'] = "#00ff00"  # Green is not home/not control
    dataFrame.loc[dataFrame['isHomeSystem'] == True, 'color'] = "#ff0000"  # Red is homesystem


def setHovertext(dataFrame):
    dataFrame['htext'] = dataFrame[['systemName', 'factionName']].agg('\n'.join, axis=1)


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


def getView(reg, dataFrame):
    # df["marker_size"] = df["difficulty"].apply(lambda x: 1 if x<10 else log(x))       # difficult = larger
    # df["marker_size"] = df["difficulty"].apply(lambda x: 20 if x<10 else 20/log(x))    # easy = larger

    #reg = RegionFactory.getSquadronRegion(regionName, 64, 'rgba(0,0,255,0.05)')
    return dataFrame[dataFrame.apply(lambda x: reg.contains(x.x, x.y, x.z), axis=1)]

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

def getLayout(theTitle):
    return go.Layout(title=theTitle,
                     scene=simpleScene,
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

def getFigure(region, theFrame):
    title = "Club Activity Galaxy-Wide"
    view = theFrame

    if region is not None:
        title = "Club Activity near " + region.getTitle()
        view = getView(region, theFrame)

    simpleTrace = getTrace(view)
    myLayout = getLayout(title)
    return go.Figure(data=[simpleTrace], layout=myLayout)

arrays = dp.getDataArrays()
df: pd.DataFrame = arrays['dataFrame']
setMarkerColors(df)
setMarkerSize(df)
setHovertext(df)
simpleScene = getScene()

# squad = 'Lavigny\'s Legion'
# squad = 'The Brotherhood of the Dark Circle'
# squad = 'Anti Xeno Initiative'
# squad = 'Close Encounters Corps'
# squad = 'The Silverbacks'
squad = 'Shadow of the Phoenix'
# squad = "Anti Xeno Initiative"
#view = df getView(squad, df)

# Create figure
fig = getFigure(None,df)

app.layout = \
    html.Table(className="clean", children=[
        html.Tr(className="clean", children=[
            html.Td(className="clean2", children=[
                dcc.Graph(id="the-graph", figure=fig),
            ]),
            html.Td(className="clean", children=[
                html.Div(className='row', children=[
                    getSquadronDropdown(),
                    getRegionDropdown(),
                    html.Div([
                        dcc.Markdown("""
                            **Click Data**

                            Click on points in the graph.
                        """),
                        html.Pre(id='click-data', style=styles['pre']),
                    ], className='three columns'),
                    html.Div([
                        dcc.Markdown("""
                            **Click Data**

                            Click on points in the graph.
                        """),
                    html.Pre(id='dd-data', style=styles['pre']),
                ], className='three columns'),
                ]),
            ])
        ]),
    ])

@app.callback(
    Output('click-data', 'children'),
    [Input('the-graph', 'clickData')])
def display_click_data(clickData):
    if clickData is not None:
        print(ujson.dumps(clickData))
        return ujson.dumps(clickData, indent=2)

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

    print("prop_id=" + str(prop_id))
    inputs = aDict['inputs']  # ['prop_id']
    #activity = inputs['activityDropdown.value']

    if (prop_id == button_id+".value"):
        value = elt0['value']
        return value

    return None


@app.callback(
    [Output('dd-data', 'children'),Output('the-graph','figure')],
    [Input('squadronDropdown', 'value'), Input('regionDropdown', 'value')])
def display_click_data(squadName, regName):
    global df
    ctx = dash.callback_context
    value = was_clicked(ctx, "squadronDropdown")
    reg = None
    val = None

    if value is not None:
        val = squadName
        reg = RegionFactory.getSquadronRegion(val, 64, "rgb(0,0,255)")

    value = was_clicked(ctx, "regionDropdown")
    if value is not None:
        val = regName
        reg = RegionFactory.regionDict.get(val)

    if reg is not None:
        newFigure = getFigure(reg, df)
        #view = getView(reg,df)
        #fig.update_traces(x=view['x'], y=view['y'], z=view['z'], overwrite=True)
        #fig.update_layout(title="Club activity near " + val, overwrite=True)

        print("reg = " + str(reg))
        return val, newFigure
    return None, getFigure(None,df)

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)
