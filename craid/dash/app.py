from typing import Dict, Tuple, List

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output
import numpy as np

import craid.eddb.DataProducer as dp

# df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')

arrs = dp.getDataArrays()
csa = arrs[ 0 ]
systems: Dict[ str, Tuple[ float, float, float ] ] = arrs[2]
df = dp.getDataFrame(csa)

nrows = df.shape[0]

df['distance'] = pd.Series(np.zeros(nrows), index=df.index)

#distance = np.zeros(nrows)
#distances: List[float] = [0.0] * nrowslAl
#df.assign(distance=distances)

# @font-face {
# font-family: myFirstFont;
# src: url(sansation_light.woff);
# }
#
# div {
# font-family: myFirstFont;
# }

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


#def generate_table(dataframe: pd.DataFrame, max_rows: int = 10):
    #return html.Table([
        #html.Thead(
            #html.Tr([ html.Th(col) for col in dataframe.columns ])
        #),
        #html.Tbody([
            #html.Tr([
                #html.Td(dataframe.iloc[ i ][ col ]) for col in dataframe.columns
            #]) for i in range(min(len(dataframe), max_rows))
        #])
    #])


external_stylesheets = [ 'https://raw.githubusercontent.com/HausReport/ClubRaiders/master/craid/css/Raiders.css']
#['https://codepen.io/chriddyp/pen/bWLwgP.css' ]


# filter_query = "{country} contains ol && {lifeExp} < 10"
# filter_query = "{control} contains false && {influence} < 25"


name = __name__
name = "Club Raiders"
app = dash.Dash(name, external_stylesheets=external_stylesheets)

opts = []
for it in systems.keys():
   val: Tuple = systems.get(it)
   opts.append({'label': it, 'value': str(it) + "," + str(val[0]) + "," + str(val[1]) + "," + str(val[2])})


#print( df.columns )

tab : dash_table.DataTable =      dash_table.DataTable(
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
            #{"name": i,
             #"id": i,
             #"deletable": False,
             #"selectable": False}
            #for i in df.columns
        ],
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
    )

#for x1 in tab.available_properties:
    #print( str(x1) )

app.layout = html.Div([
    html.Div([
        html.Label("System:"),
        dcc.Dropdown(
            id='demo-dropdown',
            options=opts,
            #[
                #{'label': 'New York City', 'value': 'NYC'},
                #{'label': 'Montreal', 'value': 'MTL'},
                #{'label': 'San Francisco', 'value': 'SF'}
            #],
            value='Alioth',
            placeholder='Select star system'
        ),
        html.Div(id='dd-output-container')
    ],style={'width': '99%', 'display': 'inline-block'}),
    tab,
    html.Div(id='datatable-interactivity-container')
])

@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    spl = value.split(",")
    x = float(spl[1])
    y = float(spl[2])
    z = float(spl[3])
    print( str(x) + str(y) + str(z))
    return 'Selected system "{}" '.format(value)

@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    [ Input('datatable-interactivity', 'selected_columns') ]
)
def update_styles(selected_columns):
    return [ {
        'if': {'column_id': i},
        'background_color': colors[ 'background' ],  # '#D2F3FF'
        'font_color': colors[ 'text' ]
    } for i in selected_columns ]


@app.callback(
    Output('datatable-interactivity-container', "children"),
    [ Input('datatable-interactivity', "derived_virtual_data"),
      Input('datatable-interactivity', "derived_virtual_selected_rows") ])
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
        derived_virtual_selected_rows = [ ]

    dff = df if rows is None else pd.DataFrame(rows)

    colors = [ '#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
               for i in range(len(dff)) ]

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


if __name__ == '__main__':
    app.run_server(debug=True)
