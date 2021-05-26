from dash.dependencies import Input, Output
import pandas as pd
from datetime import date

def filter_data_by_date(days, start_date, end_date):
    """
    Concatenate data from sheets with date between start date and end date.
    """
    
    if start_date > end_date:
        tmp_end = start_date
        start_date = end_date
        end_date = tmp_end
        
    dt_list = []
    for dt in pd.date_range(start_date, end_date):
        dt_list.append(date(dt.year, dt.month, dt.day))
        
    filtered = pd.concat([days.get(d) for d in dt_list], ignore_index=True)
    
    return filtered

def callback_data_table(app, days):
    """
    Update data in "data-table" table and number of visitors in "total-visitors-label" label.
    """
    
    @app.callback(
        Output("total-visitors-label", "children"),
        Output("data-table", "data"),
        Input("date-picker-range", "start_date"),
        Input("date-picker-range", "end_date"),
        Input("gender-checklist", "value"),
        Input("final-status-checklist", "value")
    )
    def update_data_table(start_date, end_date, gender, final_status):
        # Filter data between given start date and end date.
        filtered = filter_data_by_date(days, start_date, end_date)
        
        # Filter Gender and Final Status
        filtered = filtered[(filtered["gender"].isin(gender)) &
                            (filtered["final_status"].isin(final_status))]
        
        # Change format in datetime columns.
        for col in [col for col in filtered.columns if col.endswith("_dt")]:
            filtered[col] = filtered[col].dt.strftime("%d-%m-%Y%n%H:%M:%S")
        
        return f"Total filtered visitors : {len(filtered)}", filtered.to_dict("records")