import dash_html_components as html
import dash_core_components as dcc
import dash_table as table
from datetime import timedelta


# Checklist and RadioItems labelStyle
checklist_labelStyle = {"marginRight": 8,
                        "display": "inline-block"}

marginBottom = {"marginBottom": 10}

def generate_date_picker_range(label, days):
    """
    Generate date picker using DatePickerRange from Dash Core Components.
    """
    
    dates = list(days.keys())
    
    return html.Div([
        html.Label(children=label,
                   style={"display": "inline-block",
                          "marginRight": 10}),
        dcc.DatePickerRange(
            id="date-picker-range",
            min_date_allowed=min(dates),
            max_date_allowed=max(dates) + timedelta(days=1),
            start_date=min(dates),
            end_date=max(dates),
            minimum_nights=0,
            initial_visible_month=min(dates),
            display_format="D/M/YYYY"
        )
    ], style=marginBottom)
    
def generate_total_visitors_label():
    """
    Generate total visitors label using Label from Dash Html Components.
    """
    
    return html.Label(
        id="total-visitors-label",
        style={
            "marginTop": 5,
            "marginBottom": 5
        }
    )
    
def generate_data_table(days):
    """
    Generate data table using Dash DataTable
    """
    
    columns = days.get(list(days.keys())[0]).columns
    
    return table.DataTable(
        id="data-table",
        columns=[{"name": col, "id": col} for col in columns],
        page_size=5,
        style_cell={
            "whiteSpace": "normal",
            "height": "auto",
            "lineHeight": "20px",
            "minLineHeight": "20px",
            "textAlign": "left"
        },
        style_cell_conditional=[
            {"if": {"column_id": dt_column},
             "width": "6%"} for dt_column in [col for col in columns if col.endswith("_dt")]
        ] + [{"if": {"column_id": "clinic"},
              "width": "10%"},
             {"if": {"column_id": "sex"},
              "width": "2%"}]
    )
    
def generate_possible_values_checklist(label, id, days, column):
    """
    Generate possible values selection using Checklist from Dash Core Components.
    """
    
    values = set()
    for day in days.values():
        values = values.union(day[column].unique())
    
    return html.Div([
        html.Label(children=label),
        dcc.Checklist(
            id=id,
            options=[{"label": value, "value": value} for value in values],
            value=list(values),
            labelStyle=checklist_labelStyle
        )
    ], style=marginBottom)
    
def generate_appointment_checklist(label):
    """
    Generate appointment selection using Checklist from Dash Core Components.
    """
    
    return html.Div([
        html.Label(children=label),
        dcc.Checklist(
            id="appointment-checklist",
            options=[{"label": "?????????????????????", "value": 1},
                    {"label": "walk-in", "value": 0}],
            value=[1, 0],
            labelStyle=checklist_labelStyle
        )
    ], style=marginBottom)
    
def generate_two_inputs_components(label, min_id, max_id, min=None, max=None):
    """
    Generate html component that receive two inputs using Input from Dash Core Components.
    """
    input_style={"display": "inline-block",
                 "width": "25%"}
    
    return html.Div([
        html.Label(children=label),
        html.Div([
            dcc.Input(
                id=min_id,
                min=min,
                value=min,
                type="number",
                step=1,
                style=input_style
            ),
            html.Label(children="to",
                       style={"display": "inline-block",
                              "width": "10%",
                              "textAlign": "center"}
            ),
            dcc.Input(
                id=max_id,
                max=max,
                value=max,
                type="number",
                step=1,
                style=input_style
            )
        ])
    ], style=marginBottom)
    
def generate_clinics_checklist(label):
    """
    Generate clinics selections using Checklist from Dash Core Components.
    """
    
    return html.Div([
        html.Label(children=label),
        dcc.Checklist(
            id="clinics-checklist"
        )
    ], style=marginBottom)
    
def generate_require_datetime_radioItems(label, id):
    """
    Generate require data in datetime columns or not selection using RadioItems from Dash Core Components.
    """
    
    return html.Div([
        html.Label(children=label),
        dcc.RadioItems(
            id=id,
            options=[
                {"label": "?????? / ???????????????", "value": 2},
                {"label": "??????", "value": 1},
                {"label": "???????????????", "value": 0}
            ],
            value=2,
            labelStyle=checklist_labelStyle
        )
    ], style=marginBottom)
    
def generate_checkpoints_ordering_division(label):
    """
    Generate checkpoints ordering division using Dropdown and RadioItems from Dash Core Components.
    """
    
    return html.Div([
        html.Div([
            html.Label(children=label),
            dcc.Dropdown(
                id="checkpoints-ordering-dropdown",
                multi=True
            )
        ], style={"display": "inline-block",
                  "width": "85%",
                  "verticalAlign": "top",
                  "marginRight": "1%"}),
        html.Div([
            html.Label("????????????????????????????????????????????????????????????:"),
            dcc.RadioItems(
                id="checkpoints-ordering-radioItems",
                labelStyle=checklist_labelStyle
            )
        ], style={"display": "inline-block",
                  "width": "14%",
                  "verticalAlign": "top"})
    ], style=marginBottom)
    
def generate_more_button(id):
    """
    Generate more and less button using Buttom from Dash Html Components.
    """
    
    return html.Div([
        html.Button(
            children="MORE",
            id=id,
            n_clicks=0,
            style={
                "width": "20%",
                "textAlign": "center",
                "padding": 0,
                "marginRight": "2%"
            }
        )
    ], style={"textAlign": "right",
              "marginBottom": 10})
    
def generate_time_between_label(label):
    """
    Generate time between checkpoints division label using Label from Dash Html Components.
    """
    
    return html.Label(children=label)
    
def generate_time_between_checkpoints_division(start_checkpoint_id, end_checkpoint_id,
                                               min_id, max_id, min=None, max=None):
    """
    Generate time between checkpoints division using Input and Dropdown from Dash Core Components.
    """
    
    return html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(id=start_checkpoint_id)
            ], style={"display": "inline-block",
                      "width": "45%",
                      "verticalAlign": "middle"}),
            html.Label(children="to",
                       style={"display": "inline-block",
                              "width": "10%",
                              "textAlign": "center",
                              "verticalAlign": "middle"}
            ),
            html.Div([
                dcc.Dropdown(id=end_checkpoint_id)
            ], style={"display": "inline-block",
                      "width": "45%",
                      "verticalAlign": "middle"})
        ], style={"marginBottom": 5}),
        generate_two_inputs_components(
            label=None,
            min_id=min_id,
            max_id=max_id,
            min=min,
            max=max
        )
    ])