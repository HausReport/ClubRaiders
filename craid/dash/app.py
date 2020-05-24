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

# df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')

arrs = dp.getDataArrays()
csa = arrs[0]
systems: Dict[str, Tuple[float, float, float]] = arrs[2]
df = dp.getDataFrame(csa)

nrows = df.shape[0]

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

# print( df.columns )

tab: dash_table.DataTable = dash_table.DataTable(
    id='datatable-interactivity',
    columns=[
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
    ],
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
    html.Div(id='dd-output-container')
], style={'width': '99%', 'display': 'inline-block'})

tab1_layout = html.Div([
    tab,
    html.Div(id='datatable-interactivity-container')
])

# =============================================================
# Tab handlers
# =============================================================
app.layout = html.Div([
    hdr_layout,
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Overview', value='tab-1'),
        dcc.Tab(label='Bounty Hunting', value='tab-2'),
        dcc.Tab(label='Combat Zones', value='tab-3'),
        dcc.Tab(label='Trade/Exploration', value='tab-4'),
        dcc.Tab(label='Missions', value='tab-5'),
    ]),
    html.Div(id='tabs-example-content')
])


#
# load a markdown file from /data
#
def getCZMarkdown():
    with open("../data/cz.md", "r", encoding="utf-8") as input_file:
        text = input_file.read()
        return dcc.Markdown(text)


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
            getCZMarkdown()
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
    _cols: List[Dict[str, str]] = [{"name": 'distance', "id": 'distance'}]
    x, y, z = 0.0, 0.0, 0.0
    try:
        spl = value.split(",")
        x = float(spl[1])
        y = float(spl[2])
        z = float(spl[3])
    except:
        print("woops")

    for ind in df.index:
        # print(df['Name'][ind], df['Stream'][ind])
        x1: float = df.at[ind, 'x']
        y1: float = df.at[ind, 'y']
        z1: float = df.at[ind, 'z']
        dis: float = math.sqrt((x - x1) ** 2 + (y - y1) ** 2 + (z - z1) ** 2)
        df.at[ind, 'distance'] = dis

    print(df['distance'].dtypes)
    _cols = [
        {"name": i, "id": i} for i in df.columns
    ]
    return df.to_dict('records'), _cols


# @app.callback(
#     [dash.dependencies.Output('datatable-interactivity', 'data'),
#      dash.dependencies.Output('datatable-interactivity', 'columns')],
#     [dash.dependencies.Input('demo-dropdown', 'value')])
# def update_output(value):
#     nrows = df.shape[0]
#     #ret = df['distance'] #'[1] * nrows
#     columns = [{"name": 'distance', "id": 'distance'}]
#     #tab['data']
#     x = 0.0
#     y = 0.0
#     z = 0.0
#     try:
#         spl = value.split(",")
#         x = float(spl[1])
#         y = float(spl[2])
#         z = float(spl[3])
#     except:
#         print("woops")
#         #print( str(x) + str(y) + str(z))
#
#     for i in range(0, nrows):
#         x1= df.at[i,'x']
#         dis = math.sqrt( (x-x1)**2)
#         df.at[i,'distance'] = dis
#         #ret[i]= str(dis)
#         #ret = df['distance']  # '[1] * nrows
#     print(dis)
#     #for row in df.itertuples():
#         #val: float = df.get(row.Index,'distance')
#         #dis = abs( x-val)
#         #df.set_value(row.Index, dis, 'distance' )
#     #for i in range(0, nrows):
#         #df['distance'] = df
#     #return [ret.to_list(), columns]
#     return [df['distance'].to_dict(), columns]

@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    return 'Selected system "{}" '.format(value)


# @app.callback(
# Output('datatable-interactivity', 'style_data_conditional'),
# [Input('datatable-interactivity', 'selected_columns')] )
# def update_styles(selected_columns):
# return [{
# 'if': {'column_id': i},
# 'background_color': colors['background'],  # '#D2F3FF'
# 'font_color': colors['text']
# } for i in selected_columns]


@app.callback(
    Output('datatable-interactivity-container', "children"),
    [Input('datatable-interactivity', "derived_virtual_data"),
      Input('datatable-interactivity', "derived_virtual_selected_rows")])
def update_graphs(rows, derived_virtual_selected_rows):
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
