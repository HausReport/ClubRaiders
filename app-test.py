#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import flask
import pandas as pd
import time
import os

from appHelpers import makeDiscordIframe, AnnoyingCrap

server = flask.Flask('app')
#server.secret_key = os.environ.get('secret_key', 'secret')

app = dash.Dash('app', server=server)

app.scripts.config.serve_locally = False
#dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'

app.layout = html.Div([
    html.H1('ClubRaiders Community Tools & Resources'),
    html.Table(className="clean", children=[
        html.Tr(className="clean", children=[
            html.Td(className="left-column", children=[
                makeDiscordIframe( "x-cabal-ops", "439201271174660097"),
            ]),
            html.Td(className="clean-left", children=[
                AnnoyingCrap.getMarkdown("CabalOperatives"),
            ])
        ]),
        html.Tr(className="clean", children=[
            html.Td(className="left-column", children=[
                makeDiscordIframe( "x-irh", "530542802032001074"),
            ]),
            html.Td(className="clean-left", children=[
                AnnoyingCrap.getMarkdown("IRH"),
            ])
        ]),
    ])
], className="container")

if __name__ == '__main__':
    app.run_server()