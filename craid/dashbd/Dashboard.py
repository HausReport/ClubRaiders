import logging
import math
from typing import Dict, Tuple

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output

import craid.dashbd
import craid.dashbd.AnnoyingCrap as crap
import craid.eddb.DataProducer as dp
#
# Set up logging
#
# logging.basicConfig(filename='example.log',level=logging.DEBUG)
from FactionInstance import FactionInstance
from Oracle import Oracle

logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().level = logging.DEBUG

#
# Load data
# https://community.plotly.com/t/why-global-code-runs-twice/12514
#
#currentData:  Dict[str,object]
#if currentData is None:
currentData = dp.getDataArrays()
clubSystemInstances = currentData['allClubSystemInstances']
sysIdFacIdToFactionInstance = currentData['sysIdFacIdToFactionInstance']

systemNameToXYZ: Dict[str, Tuple[float, float, float]] = currentData['systemNameToXYZ']
playerFactionNameToHomeSystemName: Dict[str, str] = currentData['playerFactionNameToSystemName']
df: pd.DataFrame = dp.getDataFrame(clubSystemInstances)

#
# Massage data
#
nrows = df.shape[0]
df['distance'] = pd.Series(np.zeros(nrows), index=df.index)

#
# Flotsam
#
colors = {
    'background': 'black',
    'text'      : 'orange'
}
# external_stylesheets = ['https://raw.githubusercontent.com/HausReport/ClubRaiders/master/craid/css/Raiders.css']
# ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# filter_query = "{country} contains ol && {lifeExp} < 10"

#
# Start the app framework
#
app = dash.Dash(__name__)  # ,requests_pathname_prefix='')
print(__name__)
# , external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
# app.config['suppress_callback_exceptions'] = True
app.config.suppress_callback_exceptions = True

#
# Initialize some UI elements
#
opts = crap.getFirstDropdown(systemNameToXYZ)
fopts = crap.getSecondDropdown(playerFactionNameToHomeSystemName)
theColumns = crap.getTheColumns()

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
    selected_columns=[],
    selected_rows=[],
    page_action="native",
    page_current=0,
    page_size=100,
    style_header={
        'backgroundColor': 'black',
        'color'          : 'gold'},
    # style_header_conditional={
    # 'backgroundColor': 'green',
    # 'color': 'gold'},
    # style_filter_conditional={
    # 'backgroundColor': 'black',
    # 'color': 'gold'},
    style_cell={
        'backgroundColor': 'black',
        'color'          : 'orange'
    }
)

#
# Holding place for filter query logic
#
# tput("datatable-interactivity", "filtering_settings"),
# tab.available_properties['filter_query'] = "{control} contains false && {influence} < 25"
datatable.filter_query = "{isHomeSystem} contains false && {influence} < 25"
# datatable.filter_query = "{isHomeSystem} contains false && {vulnerable} contains War"
# datatable.hidden_columns = {'x','y','z'}
# for x1 in tab.available_properties:
# print( str(x1) )


#
# Layout the header
#
hdr_layout = html.Div([
    # html.Div(
    #     className="app-header",
    #     children=[
    #         html.Div('Plotly Dash', className="app-header--title")
    #     ]
    # ),
    html.Label("Choose a System:"),
    dcc.Dropdown(
        id='demo-dropdown',
        options=opts,
        value='Alioth',
        placeholder='Select star system',
        style={'backgroundColor': 'black',
               'color'          : 'gold'},
    ),
    html.Label("or a Squadron:"),
    dcc.Dropdown(
        id='demo-dropdown2',
        options=fopts,
        value='',  # Anti Xeno Initiative',
        placeholder='Select player faction'
    ),

    html.Div(id='system-notifier'),
    html.Div(id='filter-notifier'),
    html.Div(id='sort-notifier'),

], style={'width': '99%', 'display': 'inline-block'})

# TODO: get a hook to tab1 and print its properties to find color settings
# tab1: dcc.Tab = something

#
# Layout the main application
#
app.layout = html.Div([
    hdr_layout,
    dcc.Tabs(id='tabs-example', value='tab-1',
             parent_className='custom-tabs',
             className='custom-tabs-container',
             style={'primary': 'red'},
             children=[
                 dcc.Tab(label='Overview',
                         value='tab-1',
                         className='custom-tab',
                         selected_className='custom-tab--selected',
                         style={'backgroundColor': '#3C3C3C',
                                'color'          : 'gold',
                                'primary'        : 'red'}
                         ),
                 dcc.Tab(label='Combat Zones',
                         value='tab-2',
                         className='custom-tab',
                         selected_className='custom-tab--selected',
                         style={'backgroundColor': '#3C3C3C',
                                'color'          : 'gold',
                                'primary'        : 'red'}
                         ),
                 dcc.Tab(label='Bounty Hunting',
                         value='tab-3',
                         className='custom-tab',
                         selected_className='custom-tab--selected',
                         style={'backgroundColor': '#3C3C3C',
                                'color'          : 'gold',
                                'primary'        : 'red'}
                         ),
                 dcc.Tab(label='Trade/Exploration/Missions',
                         value='tab-4',
                         className='custom-tab',
                         selected_className='custom-tab--selected',
                         style={'backgroundColor': '#3C3C3C',
                                'color'          : 'gold',
                                'primary'        : 'red'}
                         ),
                 dcc.Tab(label='Scouting',
                         value='tab-5',
                         className='custom-tab',
                         selected_className='custom-tab--selected',
                         style={'backgroundColor': '#3C3C3C',
                                'color'          : 'gold',
                                'primary'        : 'red'}
                         ),
             ]),
    html.Div(id='tabs-example-content', style={'backgroundColor': 'green'}),
    ## ###### START TABLE MADNESS
    ## look into flex: https://css-tricks.com/snippets/css/a-guide-to-flexbox/
    html.Div(className="wrapper",
             children=[
                 html.Header(className='header'),
                 html.Article(className='main', children=[
                    datatable,
                 ]),
                 html.Aside(className="aside aside-2", children=[
                     html.Article("Hi There!", id='faction-drilldown', style={'width': '100%'}),
                     html.Article("Hi There!", id='system-drilldown', style={'width': '100%'}),
                 ]),
                 html.Footer(className='footer', children=[
                    html.Div(id='datatable-interactivity-container')
                 ])
             ])
    ])

# <div class="wrapper">
#   <header class="header">Header</header>
#   <article class="main">
#     <p>Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum tortor quam, feugiat vitae, ultricies eget, tempor sit amet, ante. Donec eu libero sit amet quam egestas semper. Aenean ultricies mi vitae est. Mauris placerat eleifend leo.</p>
#   </article>
#   <aside class="aside aside-2">Aside 2</aside>
#   <footer class="footer">Footer</footer>
# </div>
    ## ###### FINISH TABLE MADNESS

# =============================================================
# Tab handlers
# =============================================================
@app.callback(Output('tabs-example-content', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    return craid.dashbd.AnnoyingCrap.render_content(tab)


def fSystemNameToXYZ(sName: str):  # -> tuple(3): #float, float, float):
    #
    # value should be a valid system name
    #
    # pos: Tuple[ float, float, float ]
    pos = systemNameToXYZ.get(sName)
    if pos is None: pos = (0, 0, 0)
    return pos


# =============================================================
# Callback handlers below
# =============================================================
@app.callback(
    [Output('datatable-interactivity', 'data'), Output('datatable-interactivity', 'columns')],
    [Input('demo-dropdown', 'value')])
def update_output(val1):
    value = val1
    pos = fSystemNameToXYZ(value)
    x = pos[0]
    y = pos[1]
    z = pos[2]

    for ind in df.index:
        x1: float = df.at[ind, 'x']
        y1: float = df.at[ind, 'y']
        z1: float = df.at[ind, 'z']
        dis: float = math.sqrt((x - x1) ** 2 + (y - y1) ** 2 + (z - z1) ** 2)
        df.at[ind, 'distance'] = int(
            round(dis))  # TODO: demoted this from float to int because no formatting in datatable

    # print(df[ 'distance' ].dtypes)
    # print(datatable.sort_by)
    _cols = theColumns
    # [
    #     {"name": i, "id": i} for i in df.columns
    # ]
    return df.to_dict('records'), _cols


@app.callback(
    dash.dependencies.Output('system-notifier', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output2(value):
    return 'Selected system "{}" '.format(value)


@app.callback(
    dash.dependencies.Output('demo-dropdown', 'value'),
    [dash.dependencies.Input('demo-dropdown2', 'value')])
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
    [ Output('faction-drilldown', 'children'),
      Output('system-drilldown', 'children'),
      Output('datatable-interactivity-container', "children")],
    [Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows"),
     Input('datatable-interactivity', 'active_cell')])
def update_graphs(rows, derived_virtual_selected_rows, active_cell):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncrasy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df if rows is None else pd.DataFrame(rows)

    dataColors = ['gold' if i in derived_virtual_selected_rows else 'orange'
                  for i in range(len(dff))]

    factionInfo: str = "Nothing available"
    systemInfo: str = "Nothing available"


    if active_cell:
        print("You selected row " + str(active_cell))
        # row = rows[active_cell['row']]
        sysId = rows[active_cell['row']]['sysId']
        facId = rows[active_cell['row']]['facId']
        print(str(sysId) + "/" + str(facId))
        theFac: FactionInstance = sysIdFacIdToFactionInstance.get( (sysId,facId))
        if theFac is not None:
            print("I think that's system %s and faction %s", theFac.getSystemName(), theFac.get_name())
            factionInfo = theFac.get_name()
            systemInfo = theFac.getSystemName()


            gg : pd.DataFrame = df[df['factionName'].str.match(factionInfo)]
            seer: Oracle = Oracle(gg)
            factionInfo = crap.getString("faction-template")
            output = seer.template(factionInfo)
            factionInfo = theFac.template(output)

            ts = crap.getString("system-template")
            theSys  = theFac.getSystem()
            systemInfo = theSys.template(ts)
            systemInfo = theSys.appendStationsTableToString(systemInfo)

    factionWidget = dcc.Markdown(factionInfo)
    systemWidget = dcc.Markdown(systemInfo)

    # active_row_id = active_cell['row_id'] if active_cell else None
    # if( active_row_id != None):
    # print("You selected row " + active_row_id)
    # print("You selected row " + dff["systemName"][0])
    theGraphs = [
        dcc.Graph(
            id=column,
            figure={
                "data"  : [
                    {
                        "x"     : dff["systemName"],
                        "y"     : dff[column],
                        "type"  : "bar",
                        "marker": {"color": dataColors},
                    }
                ],
                "layout": {
                    "xaxis"        : {"automargin": True},
                    "yaxis"        : {
                        "automargin": True,
                        "title"     : {"text": column},
                        "type"      : "log"
                    },
                    "paper_bgcolor": 'rgba(0,0,0,0)',  # TODO fix color & bg
                    "plot_bgcolor" : 'rgba(0,0,0,0)',  # TODO: fix color & bg
                    "height"       : 250,
                    "margin"       : {"t": 10, "l": 10, "r": 10},
                },
            },
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        for column in ["difficulty", "influence", "population"] if column in dff]

    return factionWidget, systemWidget, [theGraphs[0], theGraphs[1], theGraphs[2] ]


@app.callback(
    Output('sort-notifier', 'children'),
    [Input('datatable-interactivity', 'sort_by')])
def update_table(sort_by):
    if sort_by is None:
        return "Sort empty"
    if len(sort_by) == 0:
        return "Sort empty"
    else:
        return "Current sort: " + str(sort_by)


@app.callback(
    dash.dependencies.Output('filter-notifier', 'children'),
    [Input('datatable-interactivity', 'filter_query')])
def update_table(query):
    if query is None:
        return "Sort empty"
    if len(query) == 0:
        return "Sort empty"
    else:
        return "Current filter: " + str(query)


if __name__ == '__main__':
    app.run_server(debug=True)
