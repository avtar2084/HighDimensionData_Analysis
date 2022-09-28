import pathlib
import dash
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from dash import dcc, html
from app import app

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("result_kmode.csv"))
df2 = pd.read_csv(DATA_PATH.joinpath("game_questionnaire_sunburst.csv"))
dff = pd.concat([df.reset_index(drop=True), df2.reset_index(drop=True)], axis=1)

dff["first"] = dff["first"].astype(str)
dff["have_a_car"] = dff["have_a_car"].astype(str)
dff["willing_or_not"] = dff["willing_or_not"].astype(str)
dff["interest_in_car_racing"] = dff["interest_in_car_racing"].astype(str)

layout = html.Div(
    [
        html.H1('Visualization Prototype V1', style={"textAlign": "center"}),

        html.Div([

            dcc.Interval(id='load_interval_vis1',
                         n_intervals=0,
                         max_intervals=0,  # <-- only run once
                         interval=1
                         ),

            dcc.Graph(id='my-graph_vis1', figure={}, clickData=None, hoverData=None, responsive='session',
                      className='eight columns'
                      # I assigned None for tutorial purposes. By default, these are None, unless you specify otherwise.
                      ),
            html.Div(id='my-list_vis1', className="ui red horizontal label"),
            # dbc.Alert("", color="info", id='my-list')
        ])
    ])


@app.callback(
    Output('my-graph_vis1', 'figure'),
    Input('load_interval_vis1', 'n_intervals'),
)
def update_graph(country_chosen):
    print(country_chosen)
    # df = pd.read_csv("resultTR.csv")
    fig = px.sunburst(
        data_frame=dff,
        path=["first", "marital_status", "gender", "have_a_car", "willing_or_not",
              "interest_in_car_racing", "age", "salary", "monthly_consumption"],  # Root, branches, leaves
        # values="first",
        # color="first",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    # fig.update_traces(textinfo='label+percent entry')
    # fig.update_layout(margin=dict(t=10, l=10, r=10, b=10), width=400)
    return fig


@app.callback(
    [Output(component_id='my-list_vis1', component_property='children')],
    [Input(component_id='my-graph_vis1', component_property='hoverData')],
)
def update_side_graph(hov_data):
    if hov_data is None:
        print('n')
        return dash.no_update
    else:
        hover_label = str(hov_data['points'][0]['id'])
        print(hover_label)
        lines = hover_label.split("/")
        try:
            if lines[0] is not None:
                lines[0] = 'Cluster : ' + lines[0]
            if lines[1] is not None:
                lines[1] = 'Marital Status : ' + lines[1]
            if lines[2] is not None:
                lines[2] = 'Gender : ' + lines[2]
            if lines[3] is not None:
                if lines[3] == '0':
                    lines[3] = 'Has a car : ' + 'No'
                else:
                    lines[3] = 'Has a car : ' + 'Yes'
            if lines[4] is not None:
                lines[4] = 'Willing or not : ' + lines[4]
            if lines[5] is not None:
                if lines[5] == '0':
                    lines[5] = 'Interest in car racing : ' + 'No'
                else:
                    lines[5] = 'Interest in car racing : ' + 'Yes'
            if lines[6] is not None:
                lines[6] = 'Age : ' + lines[6]
            if lines[7] is not None:
                lines[7] = 'Salary : ' + lines[7]
            if lines[8] is not None:
                lines[8] = 'Monthly Consumption : ' + lines[8]
        except IndexError:
            print("")
        print(lines)
        return [html.Ul([html.Li(x) for x in lines], )]
