#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause

import dash
import dash_core_components as dcc
import dash_html_components as html
import flask

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
                makeDiscordIframe( "x-edbgs", "483005833853009950"),
            ]),
            html.Td(className="clean-left", children=[
                AnnoyingCrap.getMarkdown("EliteBGS"),
            ])
        ]),

    ])
], className="container")

if __name__ == '__main__':
    app.run_server()

#discussion about the background game simulation mechanics within game Elite: Dangerous , codename : Extremely Delicious Bubble Gum Simulation
    #