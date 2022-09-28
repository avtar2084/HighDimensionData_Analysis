import pathlib
import dash
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State
from dash import dcc, html
from collections import deque
from app import app
import numpy as np
import parse
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("result1.csv"))
df2 = pd.read_csv(DATA_PATH.joinpath("game_questionnaire1.csv"))
dff = pd.concat([df.reset_index(drop=True), df2.reset_index(drop=True)], axis=1)

d = deque(maxlen=2)

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('Visualization Prototype V2', style={"textAlign": "center"}),

        ], width='12')

    ]),

    dbc.Row([
        dbc.Col([

            dcc.Graph(id='my_graph', figure={}, clickData=None, hoverData=None, animate=False,
                      # I assigned None for tutorial purposes. By default, these are None, unless you specify otherwise.
                      config={
                          'staticPlot': True,  # True, False
                          'scrollZoom': False,  # True, False
                          'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                          'showTips': True,  # True, False
                          'displayModeBar': True,  # True, False, 'hover'
                          'watermark': False,
                          'showEditInChartStudio': True,
                          # 'modeBarButtonsToRemove': ['pan2d', 'select2d'],
                      }
                      ),

        ], width=6),
        dbc.Col([
            dbc.Row([
                dbc.Col(html.Div(id='output_container1', children=[])),
                dbc.Col(dcc.Dropdown(id='Column_list', clearable=True, placeholder="Select a Column"))
            ]),
            dbc.Row([
                dbc.Col(html.Div(id='visual', children=[]))
            ])

        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Button(id='btn1',
                           children=[html.I(className="fa fa-download mr-1"), "Download Csv File"],
                           color="info",
                           className="mt-1"
                           ),

                dcc.Download(id="download-component1"),
                dcc.Interval(id='load_interval1',
                             n_intervals=0,
                             max_intervals=0,  # <-- only run once
                             interval=1
                             ),
            ]),
        ])
    ], align="end")
], fluid=True)


@app.callback(
    Output('my_graph', 'figure'),
    Input('load_interval1', 'n_intervals'),
)
def update_graph(country_chosen):
    print(country_chosen)
    df["Label"] = df["Label"].astype(str)
    fig = px.sunburst(
        data_frame=df,
        path=["first", "second", "Label"],  # Root, branches, leaves
        color="Label",
        # color_discrete_sequence=px.colors.qualitative.Pastel,
        color_discrete_map={
            "1": '#4C78A8',
            "2": '#E45756',
            "3": '#72B7B2',
            "4": '#B279A2',
            "5": '#9D755D',
            "6": '#54A24B'},
        maxdepth=-1,
    )
    return fig


@app.callback(
    [Output(component_id='output_container1', component_property='children'),
     Output(component_id='Column_list', component_property='options')],
    [Input(component_id='my_graph', component_property='hoverData'),
     Input(component_id='my_graph', component_property='clickData'),
     Input(component_id='my_graph', component_property='selectedData')],
    prevent_initial_call=True,
)
def update_side_graph(hov_data, clk_data, slct_data):
    arr = np.empty((0, 2))
    if clk_data is None:
        print('none')
        return dash.no_update, dash.no_update
    else:
        clk_label = clk_data['points'][0]['id']
        try:
            ind = d.index(clk_label)
            # print("@@@", ind)
        except ValueError:
            print("List does not contain value")
            d.append(clk_label)
        container = "Selected Label is: {}".format(d)
        container = container.strip(", maxlen=2)")
        container = container.replace("deque(", "")
        try:
            if (d[0] is not None) & (d[1] is not None):
                st1 = str(d[0])
                st2 = str(d[1])
                first_label = st1.split("/")
                second_label = st2.split("/")
                temp1 = dff[(dff["first"] == int(first_label[0])) & (dff["second"] == int(first_label[1]))
                            & (dff["Label"] == int(first_label[2]))]
                temp2 = dff[(dff["first"] == int(second_label[0])) & (dff["second"] == int(second_label[1]))
                            & (dff["Label"] == int(second_label[2]))]
                for (columnName, columnData) in temp1.iteritems():
                    if (columnName != 'name') & (columnName != 'Address') & (columnName != 'postcode') \
                            & (columnName != 'first') & (columnName != 'second') & (columnName != 'Label') & (
                            columnName != 'credit_card_number'):
                        x1 = temp1[columnName].values.tolist()
                        x2 = temp2[columnName].values.tolist()
                        all1 = list(set(x1) | set(x2))
                        diff = list(set(x1) & set(x2))
                        ratio = len(diff) / len(all1)
                        arr = np.append(arr, np.array([[columnName, ratio]]), axis=0)
                arr2 = arr[arr[:, 1].argsort()]
                return container, [{'label': i[0], 'value': i[0]} for i in arr2]
        except IndexError:
            print("!!!!!IndexError")
        arr1 = arr[arr[:, 1].argsort()]
        # print("array:", arr1[:10])
        return container, dash.no_update


@app.callback(
    Output("visual", "children"),
    [State(component_id='output_container1', component_property='children'),
     Input(component_id='Column_list', component_property='value')],
    # prevent_initial_call=True,
)
def update_scatter(str2, dropdown):
    if not dropdown:
        raise PreventUpdate
    if not str2:
        raise PreventUpdate
    str1 = str(str2)
    str1 = str1.replace(' ', '')
    substring = parse.parse('SelectedLabelis:[\'{}\',\'{}\']', str1)
    substring1 = str(substring.fixed[0])
    substring2 = str(substring.fixed[1])
    first_label = substring1.split("/")
    second_label = substring2.split("/")
    temp1 = dff[(dff["first"] == int(first_label[0])) & (dff["second"] == int(first_label[1]))
                & (dff["Label"] == int(first_label[2]))]
    temp2 = dff[(dff["first"] == int(second_label[0])) & (dff["second"] == int(second_label[1]))
                & (dff["Label"] == int(second_label[2]))]
    # print(temp1[:5])
    # print(temp2[:5])
    frames = [temp1, temp2]
    result = pd.concat(frames)
    # x_axis = ''
    # for i in range(2, -1, -1):
    #     if first_label[i] != second_label[i]:
    #         if i == 2:
    #             x_axis = "third"
    #             break
    #         elif i == 1:
    #             x_axis = "second"
    #             break
    #         else:
    #             x_axis = "first"
    #             break

    if dropdown == 'salary':
        # print("salary")
        fig_1 = px.box(result, x="Label", y="salary", points="all", color="Label",
                       color_discrete_map={1: '#4C78A8', 2: '#E45756', 3: '#72B7B2', 4: '#B279A2', 5: '#9D755D',
                                           6: '#54A24B'})
    elif dropdown == 'money_spent_on_games':
        fig_1 = px.box(result, x="Label", y="money_spent_on_games", points="all", color="Label",
                       color_discrete_map={1: '#4C78A8', 2: '#E45756', 3: '#72B7B2', 4: '#B279A2', 5: '#9D755D',
                                           6: '#54A24B'})
    elif dropdown == 'monthly_consumption':
        fig_1 = px.box(result, x="Label", y="monthly_consumption", points="all", color="Label",
                       color_discrete_map={1: '#4C78A8', 2: '#E45756', 3: '#72B7B2', 4: '#B279A2', 5: '#9D755D',
                                           6: '#54A24B'})
    elif dropdown == 'age':
        fig_1 = px.box(result, x="Label", y="age", points="all", color="Label",
                       color_discrete_map={1: '#4C78A8', 2: '#E45756', 3: '#72B7B2', 4: '#B279A2', 5: '#9D755D',
                                           6: '#54A24B'})
    elif dropdown == 'gender':
        fig_1 = px.histogram(result, x="gender", color="Label", barmode="group", color_discrete_map={
            1: '#4C78A8',
            2: '#E45756',
            3: '#72B7B2',
            4: '#B279A2',
            5: '#9D755D',
            6: '#54A24B'})
    elif dropdown == 'credit_card_provider':
        fig_1 = px.histogram(result, x="credit_card_provider", color="Label", barmode="group",
                             color_discrete_map={1: '#4C78A8', 2: '#E45756', 3: '#72B7B2', 4: '#B279A2', 5: '#9D755D',
                                                 6: '#54A24B'})
    elif dropdown == 'marital_status':
        fig_1 = px.histogram(result, x="marital_status", color="Label", barmode="group",
                             color_discrete_map={1: '#4C78A8', 2: '#E45756', 3: '#72B7B2', 4: '#B279A2', 5: '#9D755D',
                                                 6: '#54A24B'})
    elif dropdown == 'have_a_car':
        fig_1 = px.histogram(result, x="have_a_car", color="Label", barmode="group",
                             color_discrete_map={1: '#4C78A8', 2: '#E45756', 3: '#72B7B2', 4: '#B279A2', 5: '#9D755D',
                                                 6: '#54A24B'})
    elif dropdown == 'interest_in_car_racing':
        fig_1 = px.histogram(result, x="interest_in_car_racing", color="Label", barmode="group",
                             color_discrete_map={1: '#4C78A8', 2: '#E45756', 3: '#72B7B2', 4: '#B279A2', 5: '#9D755D',
                                                 6: '#54A24B'})
    elif dropdown == 'heard_of_steam':
        fig_1 = px.histogram(result, x="heard_of_steam", color="Label", barmode="group",
                             color_discrete_map={1: '#4C78A8', 2: '#E45756', 3: '#72B7B2', 4: '#B279A2', 5: '#9D755D',
                                                 6: '#54A24B'})
    else:
        fig_1 = px.box(result, x="Label", y=dropdown, points="all", color="Label",
                       color_discrete_map={1: '#4C78A8', 2: '#E45756', 3: '#72B7B2', 4: '#B279A2', 5: '#9D755D',
                                           6: '#54A24B'})
    return dcc.Graph(figure=fig_1)


# credit_card_provider marital_status heard_of_steam

@app.callback(
    Output("download-component1", "data"),
    [Input("btn1", "n_clicks"),
     State(component_id='output_container1', component_property='children')],
    prevent_initial_call=True,
)
def func(n_clicks, value):
    print("button clicked")
    str1 = str(value)
    str1 = str1.replace(' ', '')
    print(len(str1))
    if len(str1) < 26:
        substring = parse.parse('SelectedLabelis:[\'{}\']', str1)
        substring1 = str(substring.fixed[0])
        first_label = substring1.split("/")
        temp1 = dff[(dff["first"] == int(first_label[0])) & (dff["second"] == int(first_label[1]))
                    & (dff["Label"] == int(first_label[2]))]
        return dcc.send_data_frame(temp1.to_csv, "mydf_csv.csv")
    else:
        substring = parse.parse('SelectedLabelis:[\'{}\',\'{}\']', str1)

        substring1 = str(substring.fixed[0])
        substring2 = str(substring.fixed[1])
        first_label = substring1.split("/")
        second_label = substring2.split("/")
        temp1 = dff[(dff["first"] == int(first_label[0])) & (dff["second"] == int(first_label[1]))
                    & (dff["Label"] == int(first_label[2]))]
        temp2 = dff[(dff["first"] == int(second_label[0])) & (dff["second"] == int(second_label[1]))
                    & (dff["Label"] == int(second_label[2]))]
        final = pd.concat([temp1.reset_index(drop=True), temp2.reset_index(drop=True)])
        return dcc.send_data_frame(final.to_csv, "mydf_csv.csv")
