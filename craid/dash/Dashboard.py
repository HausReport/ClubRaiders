import math
from typing import Dict, Tuple, List

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output

# import dash_core_components.Markdown as md
import craid.eddb.DataProducer as dp

currentData = dp.getDataArrays()
clubSystemInstances = currentData[ 'allClubSystemInstances' ]

systemNameToXYZ: Dict[ str, Tuple[ float, float, float ] ] = currentData[ 'systemNameToXYZ' ]
playerFactionNameToHomeSystemName: Dict[ str, str ] = currentData[ 'playerFactionNameToSystemName' ]
df = dp.getDataFrame(clubSystemInstances)

nrows = df.shape[ 0 ]


#
# load a markdown file from /data
#
def getMarkdown(which: str) -> dcc.Markdown:
    with open("text/" + which + ".md", "r", encoding="utf-8") as input_file:
        text = input_file.read()
        return dcc.Markdown(text)


# suppress_callback_exceptions=True

df[ 'distance' ] = pd.Series(np.zeros(nrows), index=df.index)

colors = {
    'background': 'black',
    'text': 'orange'
}

external_stylesheets = [ 'https://raw.githubusercontent.com/HausReport/ClubRaiders/master/craid/css/Raiders.css' ]
# ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# filter_query = "{country} contains ol && {lifeExp} < 10"


# name = __name__
name: str = "Club Raiders"
app = dash.Dash(__name__)
print(__name__)
#, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
app.config[ 'suppress_callback_exceptions' ] = True
app.config.suppress_callback_exceptions = True

opts = [ ]
keys: List[ str ] = sorted(systemNameToXYZ.keys())
for it in keys:
    opts.append({'label': it, 'value': it})

fopts = [ ]
keys: List[ str ] = sorted(playerFactionNameToHomeSystemName.keys())
for it in keys:
    val: str = playerFactionNameToHomeSystemName.get(it)
    if val is not None:
        fopts.append({'label': it, 'value': val})

theColumns = [
    {"name": 'systemName', "id": 'systemName', "deletable": False, "selectable": False},
    {"name": 'factionName', "id": 'factionName', "deletable": False, "selectable": False},
    #{"name": 'x', "id": 'x', "deletable": False, "selectable": False, "hideable": True, "type": "numeric"},
    #{"name": 'y', "id": 'y', "deletable": False, "selectable": False, "hideable": True, "type": "numeric"},
    #{"name": 'z', "id": 'z', "deletable": False, "selectable": False, "hideable": True, "type": "numeric"},
    {"name": 'isHomeSystem', "id": 'isHomeSystem', "deletable": False, "selectable": False},
    {"name": 'population', "id": 'population', "deletable": False, "selectable": False, "type": "numeric"},
    {"name": 'influence', "id": 'influence', "deletable": False, "selectable": False, "type": "numeric"},
    {"name": 'updated', "id": 'updated', "deletable": False, "selectable": False, "type": "datetime"},
    {"name": 'control', "id": 'control', "deletable": False, "selectable": False},
    {"name": 'vulnerable', "id": 'vulnerable', "deletable": False, "selectable": False},
    {"name": 'distance', "id": 'distance', "deletable": False, "selectable": False, "type": "numeric"},
]
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
    selected_columns=[ ],
    selected_rows=[ ],
    page_action="native",
    page_current=0,
    page_size=100,
    style_header={
        'backgroundColor': 'black',
        'color': 'gold'},
    #style_header_conditional={
        #'backgroundColor': 'green',
        #'color': 'gold'},
    #style_filter_conditional={
        #'backgroundColor': 'black',
        #'color': 'gold'},
    style_cell={
        'backgroundColor': 'black',
        'color': 'orange'
    },
)

# tput("datatable-interactivity", "filtering_settings"),
# tab.available_properties['filter_query'] = "{control} contains false && {influence} < 25"
datatable.filter_query = "{isHomeSystem} contains false && {influence} < 25"
# datatable.filter_query = "{isHomeSystem} contains false && {vulnerable} contains War"
# datatable.hidden_columns = {'x','y','z'}
# for x1 in tab.available_properties:
# print( str(x1) )


hdr_layout = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.Div('Plotly Dash', className="app-header--title")
        ]
    ),
    html.Label("Choose a System:"),
    dcc.Dropdown(
        id='demo-dropdown',
        options=opts,
        value='Alioth',
        placeholder='Select star system',
        style = { 'backgroundColor': 'black',
                   'color': 'gold'},
    ),
    html.Label("or a Squadron:"),
    dcc.Dropdown(
        id='demo-dropdown2',
        options=fopts,
        value='',#Anti Xeno Initiative',
        placeholder='Select player faction'
    ),

    html.Div(id='system-notifier'),
    html.Div(id='filter-notifier'),
    html.Div(id='sort-notifier'),

], style={'width': '99%', 'display': 'inline-block'})

tab1_layout = html.Div([
    getMarkdown("overview")
])

# =============================================================
# Tab handlers
# =============================================================
app.layout = html.Div([
    hdr_layout,
    dcc.Tabs(id='tabs-example', value='tab-1',
             parent_className='custom-tabs',
             className='custom-tabs-container',
             children=[
                dcc.Tab(label='Overview',
                        value='tab-1',
                        className='custom-tab',
                        selected_className='custom-tab--selected'
                        ),
                dcc.Tab(label='Combat Zones',
                        value='tab-2',
                        className='custom-tab',
                        selected_className='custom-tab--selected'
                        ),
                dcc.Tab(label='Bounty Hunting',
                        value='tab-3',
                        className='custom-tab',
                        selected_className='custom-tab--selected'
                        ),
                dcc.Tab(label='Trade/Exploration/Missions',
                        value='tab-4',
                        className='custom-tab',
                        selected_className='custom-tab--selected'
                        ),
                dcc.Tab(label='Scouting',
                        value='tab-5',
                        className='custom-tab',
                        selected_className='custom-tab--selected'
                        ),
            ]),
    html.Div(id='tabs-example-content'),
    datatable,
    html.Div(id='datatable-interactivity-container')
])


@app.callback(Output('tabs-example-content', 'children'),
              [ Input('tabs-example', 'value') ])
def render_content(tab):
    if tab == 'tab-1':
        return tab1_layout
        # return html.Div([
        #    html.H3('Tab content 1')
        # ])
    elif tab == 'tab-2':
        return html.Div([
            getMarkdown("cz")
        ])
    elif tab == 'tab-3':
        return html.Div([
            getMarkdown("bh")
        ])
    elif tab == 'tab-4':
        return html.Div([
            getMarkdown("tem")
        ])
    elif tab == 'tab-5':
        return html.Div([
            getMarkdown("scouting")
        ])
    elif tab == 'tab-6':
        return html.Div([
            html.H3('Tab content 6')
        ])
    elif tab == 'tab-7':
        return html.Div([
            html.H3('Tab content 7')
        ])


def fSystemNameToXYZ(sName: str):  # -> tuple(3): #float, float, float):
    #
    # value should be a valid system name
    #
    # pos: Tuple[ float, float, float ]
    pos = systemNameToXYZ.get(sName)
    if (pos is None): pos = (0, 0, 0)
    return pos


# =============================================================
# Callback handlers below
# =============================================================
@app.callback(
    [ Output('datatable-interactivity', 'data'), Output('datatable-interactivity', 'columns') ],
    [ Input('demo-dropdown', 'value') ])
def update_output(val1):
    value = val1
    pos = fSystemNameToXYZ(value)
    x = pos[ 0 ]
    y = pos[ 1 ]
    z = pos[ 2 ]

    for ind in df.index:
        x1: float = df.at[ ind, 'x' ]
        y1: float = df.at[ ind, 'y' ]
        z1: float = df.at[ ind, 'z' ]
        dis: float = math.sqrt((x - x1) ** 2 + (y - y1) ** 2 + (z - z1) ** 2)
        df.at[ ind, 'distance' ] = dis

    # print(df[ 'distance' ].dtypes)
    #print(datatable.sort_by)
    _cols = theColumns
    # [
    #     {"name": i, "id": i} for i in df.columns
    # ]
    return df.to_dict('records'), _cols


@app.callback(
    dash.dependencies.Output('system-notifier', 'children'),
    [ dash.dependencies.Input('demo-dropdown', 'value') ])
def update_output2(value):
    return 'Selected system "{}" '.format(value)


@app.callback(
    dash.dependencies.Output('demo-dropdown', 'value'),
    [ dash.dependencies.Input('demo-dropdown2', 'value') ])
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
    Output('datatable-interactivity-container', "children"),
    [ Input('datatable-interactivity', "derived_virtual_data"),
      Input('datatable-interactivity', "derived_virtual_selected_rows"),
      Input('datatable-interactivity', 'active_cell') ])
def update_graphs(rows, derived_virtual_selected_rows, active_cell):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncracy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = [ ]

    dff = df if rows is None else pd.DataFrame(rows)

    #colors = [ '#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
               #for i in range(len(dff)) ]

    if active_cell:
        print("You selected row " + str(active_cell))
    # active_row_id = active_cell['row_id'] if active_cell else None
    # if( active_row_id != None):
    # print("You selected row " + active_row_id)
    # print("You selected row " + dff["systemName"][0])
    return [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff[ "systemName" ],
                        "y": dff[ column ],
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column},
                        "type": "log"
                    },
                    "height": 250,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        for column in [ "influence", "population", "gdpPercap" ] if column in dff
    ]


@app.callback(
    dash.dependencies.Output('sort-notifier', 'children'),
    [Input('datatable-interactivity', 'sort_by')])
def update_table(sort_by):
    if sort_by is None:
        return("Sort empty")
    if len(sort_by) == 0:
        return("Sort empty")
    else:
        return "Current sort: " + str(sort_by)

@app.callback(
    dash.dependencies.Output('filter-notifier', 'children'),
    [Input('datatable-interactivity', 'filter_query')])
def update_table(query):
    if query is None:
        return("Sort empty")
    if len(query) == 0:
        return("Sort empty")
    else:
        return "Current filter: " + str(query)


if __name__ == '__main__':
    app.run_server(debug=True)
