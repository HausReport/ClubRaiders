#   Copyright (c) 2020 Club Raiders Project
#   https://github.com/HausReport/ClubRaiders
#
#   SPDX-License-Identifier: BSD-3-Clause
import urllib
from urllib.parse import parse_qs, urlsplit

import dash
import urllib3
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import flask
import pandas as pd
import time
import os
import requests


#
#
# Python/dash/flask to get the url
# https://community.plotly.com/t/dash-flask-request-args/25760/2
#
# JS to copy widget to clipboard
# https://www.w3schools.com/howto/howto_js_copy_clipboard.asp

prevUrl = "xxxfoobarnomatchlalala"
baseUrl = None

app = dash.Dash(__name__)#, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    dcc.Link('Navigate to "/"', href='/activities?name=bob&age=14'),
    html.Br(),
    dcc.Link('Navigate to "/page-2"', href='/activities?name=fred&age=22'),

    # content will be rendered in this element
    html.Div(id='page-content')
])

def handle_crap(obj, default):
    if not obj:
        return default
    if obj is None:
        return default
    if len(obj) <1:
        return default
    obj = obj[0]
    if len(obj)<1:
        return default
    return obj[0]

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'href')])
def display_page(href):
    global prevUrl, baseUrl

    if href is not None:
        o = urllib3.util.parse_url(href)
        print(str(o))
        scheme = o.scheme

        netloc = o.netloc
        path = o.path
        if (path == "/"):
            path = "/activities"
        query = o.query
        #
        print("scheme = " + scheme)
        print("netloc = " + netloc)
        print("path = " + path)
        print("query = " + str(query))

        # stupid to have to use 2 libs for this but....
        q2 = urlsplit(href).query
        params = parse_qs(query)

        #
        # Make any updates on the dict
        #
        # params['name'] = "Hildigard"
        # params['age'] = '77'

        newQuery = urllib.parse.urlencode(params)
        baseUrl = scheme + "://" + netloc + path
        newUrl = baseUrl + "?" + newQuery

        print("newUrl = " + newUrl)
        if not prevUrl:
            pass
        elif prevUrl == newUrl:
            print("Matched!")
        else:
            print("Didn't match.")
        prevUrl = newUrl
    else:
        print("href is none")



    #print("params=" + str(req.__getattribute__("params")))
    # #
    # # Parse the url and get the query
    # #

    # #
    # # See if the query provided values
    # #

    #
    # #
    # # If not, provide defaults
    # #
    # if path=="/":
    #     path = "/activities"

    #
    # url_endpoint = base
    # mydict = parsed_query
    # resp = requests.get(url_endpoint, params=mydict)
    #
    # print("resp=" + str(resp))

    return html.Div([
        html.H3('You are on page {}'.format(href))
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


# FIXME: it'd be nice to let users link directly to certain factions, systems, etc...
# getting the url isn't trivial, see
# https://dash.plotly.com/dash-core-components/location
# https://community.plotly.com/t/get-full-url-string-instead-of-only-pathname/23376
# loc = dcc.Location(id="location-url")
# print(loc.href)
# if flask.has_request_context():
# print(" url = " + str(flask.request.host_url))A

#
# NOTE: Links related to url handling
#
# Set browser url via JS: https://stackoverflow.com/questions/18396501/how-to-get-set-current-page-url-which-works-across-space-time-browsers-versions
#
# Dash/flask parsing url: https://community.plotly.com/t/dash-flask-request-args/25760
#
# Url shortener: https://pypi.org/project/gdshortener/