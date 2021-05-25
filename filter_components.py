import dash_html_components as html
import dash_core_components as dcc
import dash_table as table
from datetime import timedelta

def generate_date_picker_range(days):
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