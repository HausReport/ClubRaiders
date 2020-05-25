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

arrs = dp.getDataArrays()
csa = arrs[0]
systems: Dict[str, Tuple[float, float, float]] = arrs[2]
pFactions: Dict[str, Tuple[float, float, float]] = arrs[1]
df = dp.getDataFrame(csa)

nrows = df.shape[0]

#
# load a markdown file from /data
#
def getMarkdown(which: str) -> dcc.Markdown:
    with open("text/"+which+".md", "r", encoding="utf-8") as input_file:
        text = input_file.read()
        return dcc.Markdown(text)


# suppress_callback_exceptions=True

df['distance'] = pd.Series(np.zeros(nrows), index=df.index)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

external_stylesheets = ['https://raw.githubusercontent.com/HausReport/ClubRaiders/master/craid/css/Raiders.css']
# ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# filter_query = "{country} contains ol && {lifeExp} < 10"


# name = __name__
name: str = "Club Raiders"
app = dash.Dash(name, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
app.config['suppress_callback_exceptions'] = True
app.config.suppress_callback_exceptions = True

opts = []
for it in systems.keys():
    val: Tuple = systems.get(it)
    opts.append({'label': it, 'value': str(it) + "," + str(val[0]) + "," + str(val[1]) + "," + str(val[2])})

fopts = []
for it in pFactions.keys():
    val: Tuple = systems.get(it)
    if( val != None):
        opts.append({'label': it, 'value': str(it) + "," + str(val[0]) + "," + str(val[1]) + "," + str(val[2])})

theColumns = [
        {"name": 'systemName', "id": 'systemName', "deletable": False, "selectable": False},
        {"name": 'factionName', "id": 'factionName', "deletable": False, "selectable": False},
        {"name": 'x', "id": 'x', "deletable": False, "selectable": False, "hideable": True, "type": "numeric"},
        {"name": 'y', "id": 'y', "deletable": False, "selectable": False, "hideable": True, "type": "numeric"},
        {"name": 'z', "id": 'z', "deletable": False, "selectable": False, "hideable": True, "type": "numeric"},
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
    columns= theColumns,
    #hidden_columns = {'x','y','z'},   causes an exception re serialization
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
    page_size=100,
)

# tput("datatable-interactivity", "filtering_settings"),
# tab.available_properties['filter_query'] = "{control} contains false && {influence} < 25"
datatable.filter_query = "{isHomeSystem} contains false && {influence} < 25"
#datatable.filter_query = "{isHomeSystem} contains false && {vulnerable} contains War"
#datatable.hidden_columns = {'x','y','z'}
# for x1 in tab.available_properties:
# print( str(x1) )


hdr_layout = html.Div([
    html.Label("System:"),
    dcc.Dropdown(
        id='demo-dropdown',
        options=opts,
        value='Alioth',
        placeholder='Select star system'
    ),
    dcc.Dropdown(
        id='demo-dropdown2',
        options=fopts,
        value='Anti Xeno Initiative',
        placeholder='Select player faction'
    ),

    html.Div(id='dd-output-container')
], style={'width': '99%', 'display': 'inline-block'})

tab1_layout = html.Div([
    getMarkdown("bh")
])

# =============================================================
# Tab handlers
# =============================================================
app.layout = html.Div([
    hdr_layout,
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Overview', value='tab-1'),
        dcc.Tab(label='Combat Zones', value='tab-2'),
        dcc.Tab(label='Bounty Hunting', value='tab-3'),
        dcc.Tab(label='Trade/Exploration/Missions', value='tab-4'),
        dcc.Tab(label='Scouting', value='tab-5'),
    ]),
    html.Div(id='tabs-example-content'),
    datatable,
    html.Div(id='datatable-interactivity-container')
])



@app.callback(Output('tabs-example-content', 'children'),
              [Input('tabs-example', 'value')])
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
            html.H3('Tab content 3')
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Tab content 4')
        ])
    elif tab == 'tab-5':
        return html.Div([
            html.H3('Tab content 5')
        ])
    elif tab == 'tab-6':
        return html.Div([
            html.H3('Tab content 6')
        ])
    elif tab == 'tab-7':
        return html.Div([
            html.H3('Tab content 7')
        ])


# =============================================================
# Callback handlers below
# =============================================================
@app.callback(
    [dash.dependencies.Output('datatable-interactivity', 'data'),
    dash.dependencies.Output('datatable-interactivity', 'columns')],
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    x, y, z = 0.0, 0.0, 0.0
    try:
        spl = value.split(",")
        x = float(spl[1])
        y = float(spl[2])
        z = float(spl[3])
    except:
        print("woops")

    for ind in df.index:
        x1: float = df.at[ind, 'x']
        y1: float = df.at[ind, 'y']
        z1: float = df.at[ind, 'z']
        dis: float = math.sqrt((x - x1) ** 2 + (y - y1) ** 2 + (z - z1) ** 2)
        df.at[ind, 'distance'] = dis

    print(df['distance'].dtypes)
    _cols = theColumns
    # [
    #     {"name": i, "id": i} for i in df.columns
    # ]
    return df.to_dict('records'), _cols

@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    return 'Selected system "{}" '.format(value)


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
    [Input('datatable-interactivity', "derived_virtual_data"),
    Input('datatable-interactivity', "derived_virtual_selected_rows"),
    Input('datatable-interactivity', 'active_cell')])
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
        derived_virtual_selected_rows = []

    dff = df if rows is None else pd.DataFrame(rows)

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
               for i in range(len(dff))]

    if active_cell:
        print("You selected row " + str(active_cell))
    #active_row_id = active_cell['row_id'] if active_cell else None
    #if( active_row_id != None):
        #print("You selected row " + active_row_id)
    #print("You selected row " + dff["systemName"][0])
    return [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff["systemName"],
                        "y": dff[column],
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
        for column in ["influence", "population", "gdpPercap"] if column in dff
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
