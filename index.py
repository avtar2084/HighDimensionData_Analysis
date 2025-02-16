import dash
from dash.dependencies import Input, Output
from dash import dcc, html
import dash_bootstrap_components as dbc

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import compare_data, compare_data_clustered, visualization1

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#333333",

}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.Div(
            [
                # width: 3rem ensures the logo is the exact width of the
                # collapsed sidebar (accounting for padding)
                html.H3("Dashboard", style={'color': 'white', 'text-decoration': 'none'}),

            ],
            className="sidebar-header",
        ),
        html.Div([
            dcc.Link(
                html.A('Visualization1', className="button no-print print", style={'color': 'white', 'width': '165px'}),
                href='/apps/visualization 1',
                style={'color': 'white', 'text-decoration': 'none', 'margin-bottom': '3em', 'margin-top': '3em'}),

            # dcc.Link(html.A('Sunburst Vis', className="button no-print print", style={'color': 'white', 'width':'165px'}), href='/apps/sunburst'
            #          , style={'color': 'white', 'text-decoration': 'none','margin-bottom': '3em'}),
            # html.Br(hidden=True),
            dcc.Link(html.A('visualization 2', className="button no-print print",
                            style={'color': 'white', 'width': '165px', 'text-align': 'left'}),
                     href='/apps/compare_data',
                     style={'color': 'white', 'text-decoration': 'none', 'margin-bottom': '3em', 'text-align': 'left'}),
            # dcc.Link(html.A('Clustered', className="button no-print print",
            #                 style={'color': 'white', 'width': '165px', 'text-align': 'left'}),
            #          href='/apps/compare_data_clustered'),
        ], className="row"),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    # if pathname == '/apps/sunburst':
    #     return sunburst.layout
    if pathname == '/apps/compare_data':
        return compare_data.layout
    # if pathname == '/apps/compare_data_clustered':
    #     return compare_data_clustered.layout
    if pathname == '/apps/visualization1':
        return visualization1.layout
    else:
        return visualization1.layout


if __name__ == '__main__':
    app.run_server(debug=False)
