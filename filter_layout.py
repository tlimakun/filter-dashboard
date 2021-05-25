import dash_html_components as html
from filter_components import *

def filter_layout(days):
    return html.Div([
        html.Div([
            html.Label(children="Date : ",
                       style={"display": "inline-block",
                              "marginRight": 10}),
            generate_date_picker_range(days)
        ], style={"marginBottom": 5})
    ])