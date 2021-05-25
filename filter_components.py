import dash_html_components as html
import dash_core_components as dcc
import dash_table as table
from datetime import timedelta

def generate_date_picker_range(days):
    """
    Generate date picker using DatePickerRange from Dash Core Components.
    """
    
    dates = list(days.keys())
    
    return dcc.DatePickerRange(
        id="date-picker-range",
        min_date_allowed=min(dates),
        max_date_allowed=max(dates) + timedelta(days=1),
        start_date=min(dates),
        end_date=max(dates),
        minimum_nights=0,
        initial_visible_month=min(dates),
        display_format="D/M/YYYY"
    )
    
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