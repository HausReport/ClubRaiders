#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import ujson
from dash.dependencies import Output, Input

import craid.eddb.loader.DataProducer as dp
import pandas as pd
import logging
import plotly.graph_objs as go
from numpy import *

from craid.club.regions.RegionFactory import RegionFactory

styles = {
    'pre': {
        'border'   : 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}


def setMarkerSize(df):
    df.loc[df['control'] == True, 'marker_size'] = 8  # Medium is not home/control
    df.loc[df['control'] == False, 'marker_size'] = 5  # Small is not home/not control
    df.loc[df['isHomeSystem'] == True, 'marker_size'] = 15  # Large is home
    # df["marker_size"] = df["influence"].apply(lambda x: 5+ x/5)


def setMarkerColors(df):
    df.loc[df['control'] == True, 'color'] = "#ffbf00"  # Yellow is control/not home
    df.loc[df['control'] == False, 'color'] = "#00ff00"  # Green is not home/not control
    df.loc[df['isHomeSystem'] == True, 'color'] = "#ff0000"  # Red is homesystem


def setHovertext(df):
    df['htext'] = df[['systemName', 'factionName']].agg('\n'.join, axis=1)


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
            zerolinecolor="white", ), )


def getView(key: str, df):
    squad = 'Lavigny\'s Legion'
    squad = 'The Brotherhood of the Dark Circle'
    # squad = 'Anti Xeno Initiative'
    # squad = 'Close Encounters Corps'
    # squad = 'The Silverbacks'
    squad = 'Shadow of the Phoenix'

    # df["marker_size"] = df["difficulty"].apply(lambda x: 1 if x<10 else log(x))       # difficult = larger
    # df["marker_size"] = df["difficulty"].apply(lambda x: 20 if x<10 else 20/log(x))    # easy = larger

    reg = RegionFactory.getSquadronRegion(squad, 64, 'rgba(0,0,255,0.05)')
    axi = df[df.apply(lambda x: reg.contains(x.x, x.y, x.z), axis=1)]
    return axi


logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().level = logging.DEBUG

arrays = dp.getDataArrays()
df: pd.DataFrame = arrays['dataFrame']
setMarkerColors(df)
setMarkerSize(df)
setHovertext(df)
simpleScene = getScene()

squad = "Anti Xeno Initiative"
view = getView(squad, df)

# Create figure
simpleTrace = go.Scatter3d(x=view['x'],
                           y=view['z'],
                           z=view['y'],
                           text=view['systemName'],
                           hoverinfo="text",
                           hovertext=view['htext'],
                           mode='markers+text',
                           marker=dict(size=view["marker_size"],
                                       color=view["color"]))

myLayout = go.Layout(title='Club Activity near ' + squad,
                     paper_bgcolor='rgb(0,0,0)',
                     plot_bgcolor='rgb(0,0,0)',
                     clickmode='event+select',
                     font=dict(
                         family="Courier New, monospace",
                         size=12,
                         color="#ffffff")
                     )
fig = go.Figure(data=[simpleTrace], layout=myLayout)

fig.update_layout(scene=simpleScene)

# Update plot sizing
fig.update_layout(
    width=800,
    height=900,
    autosize=False,
    margin=dict(t=100, b=0, l=0, r=0),
)

# Update 3D scene options
fig.update_scenes(
    aspectratio=dict(x=1, y=1, z=0.7),
    aspectmode="manual"
)

# Add drowdowns
button_layer_1_height = 1.08
fig.update_layout(
    updatemenus=[
        dict(
            buttons=list([
                dict(
                    args=["colorscale", "Viridis"],
                    label="Viridis",
                    method="restyle"
                ),
                dict(
                    args=["colorscale", "Cividis"],
                    label="Cividis",
                    method="restyle"
                ),
                dict(
                    args=["colorscale", "Blues"],
                    label="Blues",
                    method="restyle"
                ),
                dict(
                    args=["colorscale", "Greens"],
                    label="Greens",
                    method="restyle"
                ),
            ]),
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=button_layer_1_height,
            yanchor="top"
        ),
        dict(
            buttons=list([
                dict(
                    args=["reversescale", False],
                    label="False",
                    method="restyle"
                ),
                dict(
                    args=["reversescale", True],
                    label="True",
                    method="restyle"
                )
            ]),
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.37,
            xanchor="left",
            y=button_layer_1_height,
            yanchor="top"
        ),
        dict(
            buttons=list([
                dict(
                    args=[{"contours.showlines": False, "type": "contour"}],
                    label="Hide lines",
                    method="restyle"
                ),
                dict(
                    args=[{"contours.showlines": True, "type": "contour"}],
                    label="Show lines",
                    method="restyle"
                ),
            ]),
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.58,
            xanchor="left",
            y=button_layer_1_height,
            yanchor="top"
        ),
    ]
)

fig.update_layout(
    annotations=[
        dict(text="colorscale", x=0, xref="paper", y=1.06, yref="paper",
             align="left", showarrow=False),
        dict(text="Reverse<br>Colorscale", x=0.25, xref="paper", y=1.07,
             yref="paper", showarrow=False),
        dict(text="Lines", x=0.54, xref="paper", y=1.06, yref="paper",
             showarrow=False)
    ])

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(id="fig", figure=fig),
    html.Div([dcc.Markdown("""
                **Click Data**
                Click on points in the graph.
            """),
              html.Pre(id='click-data', style=styles['pre']), ], )
])

app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter


@app.callback(
    Output('click-data', 'children'),
    [Input('fig', 'clickData')])
def display_click_data(clickData):
    print(ujson.dumps(clickData))
    return ujson.dumps(clickData, indent=2)
