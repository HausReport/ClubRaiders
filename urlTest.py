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
import urllib.parse



#
#
# Python/dash/flask to get the url
# https://community.plotly.com/t/dash-flask-request-args/25760/2
#
# JS to copy widget to clipboard
# https://www.w3schools.com/howto/howto_js_copy_clipboard.asp

app = dash.Dash(__name__)#, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    dcc.Link('Navigate to "/"', href='/'),
    html.Br(),
    dcc.Link('Navigate to "/page-2"', href='/page-2'),

    # content will be rendered in this element
    html.Div(id='page-content')
])


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'href')])
def display_page(pathname):
    print("url = " + str(pathname))
    parsed_url = urllib.parse.urlparse(pathname)
    parsed_query = urllib.parse.parse_qs(parsed_url.query)

    name = parsed_query.get('name')
    age = parsed_query.get('age')

    if name is None:
        name = "None"
    elif len(name) >= 1:
        name = name[0]

    if age is None:
        age = "None"
    elif len(age) >= 1:
        age = age[0]

    print ( str(name) + "/" + str(age))
    return html.Div([
        html.H3('You are on page {}'.format(pathname))
    ])
# NOTE: see also https://dash.plotly.com/urls

# @app.callback(
#     [Output('theName', 'value'), Output('theAge', 'value') ],
#     [Input('url', 'pathname')]
# )
# def load_page(url):
#     print("url = " + str(url))
#     parsed_url = urllib.parse.urlparse(url)
#     parsed_query = urllib.parse.parse_qs(parsed_url.query)
#     name = parsed_query['name'][0]
#     age = parsed_query['age'][0]
#     return name, age

if __name__ == '__main__':
    app.run_server()