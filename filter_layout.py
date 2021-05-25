import dash_html_components as html
from filter_components import *

def filter_layout(days):
    """
    Main layout of filter dashboard.
    """
    
    return html.Div([
        # Date picker range division
        html.Div([
            html.Label(
                children="Date : ",
                style={"display": "inline-block",
                       "marginRight": 10}),
            generate_date_picker_range(days)
        ], style={"marginBottom": 5}),
        
        # Filter fields division
        html.Div([
            
        ], style={"borderTop": "thin lightgrey solid",
                  "borderBottom": "thin lightgrey solid",
                  "paddingTop": 5,
                  "paddingBottom": 5}),
        
        # Data table division
        html.Div([
            # Total visitors label
            generate_total_visitors_label(),
            
            # Data table
            generate_data_table(days)
        ])
    ])