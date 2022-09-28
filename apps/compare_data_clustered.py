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

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("result_clustered.csv"))
df2 = pd.read_csv(DATA_PATH.joinpath("game_questionnaire1.csv"))
dff = pd.concat([df.reset_index(drop=True), df2.reset_index(drop=True)], axis=1)

d = deque(maxlen=2)

layout = html.Div(
    [
        html.H1('Compare Data', style={"textAlign": "center"}),

        html.Div([
            dcc.Interval(id='load_interval2',
                         n_intervals=0,
                         max_intervals=0,  # <-- only run once
                         interval=1
                         ),

            dcc.Graph(id='my_graph2', figure={}, clickData=None, hoverData=None, animate=False,
                      # I assigned None for tutorial purposes. By defualt, these are None, unless you specify otherwise.
                      config={
                          'staticPlot': True,  # True, False
                          'scrollZoom': False,  # True, False
                          'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                          'showTips': True,  # True, False
                          'displayModeBar': True,  # True, False, 'hover'
                          'watermark': False,
                          'showEditInChartStudio': True,
                          # 'modeBarButtonsToRemove': ['pan2d', 'select2d'],
                      },
                      className='six columns'
                      ),
            html.Div(id='output_container2', children=[], className='three columns'),
            dcc.Dropdown(id='Column_list2', clearable=True, placeholder="Select a Column", className='three columns')
        ]),
        html.Div(id='visual2', children=[], className='six columns')

    ])


@app.callback(
    Output('my_graph2', 'figure'),
    Input('load_interval2', 'n_intervals'),
)
def update_graph(country_chosen):
    print(country_chosen)
    df["Cluster"] = df["Cluster"].astype(str)
    fig = px.sunburst(
        data_frame=df,
        path=["Cluster"],  # Root, branches, leaves
        color="Cluster",
        color_discrete_map={
            "0": '#702251',
            "1": '#4C78A8',
            "2": '#E45756',
            "3": '#d46431',
            "4": '#B279A2',
            "5": '#9D755D',
            "6": '#54A24B',
            "7": '#8fa389',
            "8": '#66b391',
            "9": '#3f8cd9',
        },
        maxdepth=-1,
    )
    return fig


@app.callback(
    [Output(component_id='output_container2', component_property='children'),
     Output(component_id='Column_list2', component_property='options')],
    [Input(component_id='my_graph2', component_property='hoverData'),
     Input(component_id='my_graph2', component_property='clickData'),
     Input(component_id='my_graph2', component_property='selectedData')],
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
            clk_label = clk_data['points'][0]['id']
            container = "Selected Label is: {}".format(d)
            container = container.strip(", maxlen=2)")
            container = container.replace("deque(", "")
            try:
                if (d[0] is not None) & (d[1] is not None):
                    st1 = str(d[0])
                    st2 = str(d[1])
                    temp1 = dff[dff["Cluster"] == int(st1)]
                    temp2 = dff[dff["Cluster"] == int(st2)]
                    for (columnName, columnData) in temp1.iteritems():
                        if (columnName != 'name') & (columnName != 'Address') & (columnName != 'postcode') \
                                & (columnName != 'Cluster') :
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
    Output("visual2", "children"),
    [State(component_id='output_container2', component_property='children'),
     Input(component_id='Column_list2', component_property='value')],
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
    temp1 = dff[dff["Cluster"] == int(substring1)]
    temp2 = dff[dff["Cluster"] == int(substring2)]
    # print(temp1[:5])
    # print(temp2[:5])
    frames = [temp1, temp2]
    result = pd.concat(frames)
    if dropdown == 'salary':
        # print("salary")
        fig_1 = px.box(result, x="Cluster", y="salary", points="all", color="Cluster",
                       color_discrete_map={
                           0: '#702251', 1: '#4C78A8', 2: '#E45756',
                           3: '#d46431', 4: '#B279A2', 5: '#9D755D', 6: '#54A24B', 7: '#8fa389',
                           8: '#66b391', 9: '#3f8cd9',
                       })
    elif dropdown == 'money_spent_on_games':
        fig_1 = px.box(result, x="Cluster", y="money_spent_on_games", points="all", color="Cluster",
                       color_discrete_map={
                           0: '#702251', 1: '#4C78A8', 2: '#E45756',
                           3: '#d46431', 4: '#B279A2', 5: '#9D755D', 6: '#54A24B', 7: '#8fa389',
                           8: '#66b391', 9: '#3f8cd9',
                       })
    elif dropdown == 'monthly_consumption':
        fig_1 = px.box(result, x="Cluster", y="monthly_consumption", points="all", color="Cluster",
                       color_discrete_map={
                           0: '#702251', 1: '#4C78A8', 2: '#E45756',
                           3: '#d46431', 4: '#B279A2', 5: '#9D755D', 6: '#54A24B', 7: '#8fa389',
                           8: '#66b391', 9: '#3f8cd9',
                       })
    elif dropdown == 'age':
        fig_1 = px.box(result, x="Cluster", y="age", points="all", color="Cluster",
                       color_discrete_map={
                           0: '#702251', 1: '#4C78A8', 2: '#E45756',
                           3: '#d46431', 4: '#B279A2', 5: '#9D755D', 6: '#54A24B', 7: '#8fa389',
                           8: '#66b391', 9: '#3f8cd9',
                       })
    elif dropdown == 'gender':
        fig_1 = px.histogram(result, x="gender", color="Cluster", barmode="group",
                             color_discrete_map={
                                 0: '#702251', 1: '#4C78A8', 2: '#E45756',
                                 3: '#d46431', 4: '#B279A2', 5: '#9D755D', 6: '#54A24B', 7: '#8fa389',
                                 8: '#66b391', 9: '#3f8cd9',
                             })
    elif dropdown == 'credit_card_provider':
        fig_1 = px.histogram(result, x="credit_card_provider", color="Cluster", barmode="group",
                             color_discrete_map={
                                 0: '#702251', 1: '#4C78A8', 2: '#E45756',
                                 3: '#d46431', 4: '#B279A2', 5: '#9D755D', 6: '#54A24B', 7: '#8fa389',
                                 8: '#66b391', 9: '#3f8cd9',
                             })
    elif dropdown == 'marital_status':
        fig_1 = px.histogram(result, x="marital_status", color="Cluster", barmode="group",
                             color_discrete_map={
                                 0: '#702251', 1: '#4C78A8', 2: '#E45756',
                                 3: '#d46431', 4: '#B279A2', 5: '#9D755D', 6: '#54A24B', 7: '#8fa389',
                                 8: '#66b391', 9: '#3f8cd9',
                             })
    elif dropdown == 'have_a_car':
        fig_1 = px.histogram(result, x="have_a_car", color="Cluster", barmode="group",
                             color_discrete_map={
                                 0: '#702251', 1: '#4C78A8', 2: '#E45756',
                                 3: '#d46431', 4: '#B279A2', 5: '#9D755D', 6: '#54A24B', 7: '#8fa389',
                                 8: '#66b391', 9: '#3f8cd9',
                             })
    elif dropdown == 'interest_in_car_racing':
        fig_1 = px.histogram(result, x="interest_in_car_racing", color="Cluster", barmode="group",
                             color_discrete_map={
                                 0: '#702251', 1: '#4C78A8', 2: '#E45756',
                                 3: '#d46431', 4: '#B279A2', 5: '#9D755D', 6: '#54A24B', 7: '#8fa389',
                                 8: '#66b391', 9: '#3f8cd9',
                             })
    elif dropdown == 'heard_of_steam':
        fig_1 = px.histogram(result, x="heard_of_steam", color="Cluster", barmode="group",
                             color_discrete_map={
                                 0: '#702251', 1: '#4C78A8', 2: '#E45756',
                                 3: '#d46431', 4: '#B279A2', 5: '#9D755D', 6: '#54A24B', 7: '#8fa389',
                                 8: '#66b391', 9: '#3f8cd9',
                             })
    else:
        fig_1 = px.box(result, x="Cluster", y=dropdown, points="all", color="Cluster",
                       color_discrete_map={
                           0: '#702251', 1: '#4C78A8', 2: '#E45756',
                           3: '#d46431', 4: '#B279A2', 5: '#9D755D', 6: '#54A24B', 7: '#8fa389',
                           8: '#66b391', 9: '#3f8cd9',
                       })
    return dcc.Graph(figure=fig_1)

# credit_card_provider marital_status heard_of_steam
