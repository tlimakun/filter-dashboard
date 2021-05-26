from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
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

def callback_age_inputs(app, days):
    """
    Update max, min and initial values of age inputs.
    """
    
    @app.callback(
        Output("min-age-input", "min"),
        Output("min-age-input", "value"),
        Output("max-age-input", "max"),
        Output("max-age-input", "value"),
        Input("date-picker-range", "start_date"),
        Input("date-picker-range", "end_date")
    )
    def update_age_inputs(start_date, end_date):
        filtered = filter_data_by_date(days, start_date, end_date)
        
        min_age = min(filtered["age"])
        max_age = max(filtered["age"])
        
        return min_age, min_age, max_age, max_age
    
def callback_clinics_checklist(app, days):
    """
    Update clinics checklist options and initial values.
    """
    
    @app.callback(
        Output("clinics-checklist", "options"),
        Output("clinics-checklist", "value"),
        Input("date-picker-range", "start_date"),
        Input("date-picker-range", "end_date")
    )
    def update_clinics_checklist(start_date, end_date):
        filtered = filter_data_by_date(days, start_date, end_date)
        
        all_clinics = set()
        for day in days.values():
            all_clinics = all_clinics.union(day["clinic"].unique())
            
        available_clinics = filtered["clinic"].unique()
        disabled_clinics = all_clinics.difference(available_clinics)
        
        options = [{"label": clinic, "value": clinic, "disabled": True} if clinic in disabled_clinics
                   else {"label": clinic, "value": clinic, "disabled": False} for clinic in all_clinics]
        options = sorted(options, key=(lambda key: key["label"]))
        options = sorted(options, key=(lambda key: key["disabled"]))
        
        return options, available_clinics

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
        Input("final-status-checklist", "value"),
        Input("appointment-checklist", "value"),
        Input("min-age-input", "value"),
        Input("max-age-input", "value"),
        Input("min-start-time-input", "value"),
        Input("max-start-time-input", "value"),
        Input("min-total-time-input", "value"),
        Input("max-total-time-input", "value")
    )
    def update_data_table(start_date, end_date, gender, final_status, appointment, min_age, max_age,
                          min_start_time, max_start_time, min_total_time, max_total_time):
        # Filter data between given start date and end date.
        filtered = filter_data_by_date(days, start_date, end_date)
        
        # Filter appointment
        if len(appointment) == 1:
            if 1 in appointment:
                filtered = filtered[(filtered["visit_dt"].dt.minute.isin([0, 30])) & (filtered["visit_dt"].dt.second == 0)]
            elif 0 in appointment:
                filtered = filtered[(~filtered["visit_dt"].dt.minute.isin([0, 30])) | (filtered["visit_dt"].dt.second != 0)]
        elif len(appointment) == 0:
            filtered = filtered[filtered["vn"] == -1]
        
        # Filter gender, final status, and age
        filtered = filtered[(filtered["gender"].isin(gender)) &
                            (filtered["final_status"].isin(final_status)) &
                            (filtered["age"] >= min_age) & (filtered["age"] <= max_age)]
        
        # Filter visitors with start time between min_start_time and max_start_time
        filtered["start_time"] = filtered[[col for col in filtered.columns if col.endswith("_dt") and col != "visit_dt"]].min(axis=1)
        filtered = filtered[(filtered["start_time"].dt.hour >= min_start_time) & (filtered["start_time"].dt.hour < max_start_time)]
        
        # Filter visitors with total time in process between min_total_time and max_total_time
        filtered["end_time"] = filtered[[col for col in filtered.columns if col.endswith("_dt") and col != "visit_dt"]].max(axis=1)
        filtered["total_time"] = (filtered["end_time"] - filtered["start_time"]) / np.timedelta64(1, 'h')
        filtered = filtered[(filtered["total_time"] >= min_total_time) & (filtered["total_time"] < max_total_time )]
        
        # Drop unused columns
        filtered.drop(["start_time", "end_time", "total_time"], axis=1)
        
        # Change format in datetime columns.
        for col in [col for col in filtered.columns if col.endswith("_dt")]:
            filtered[col] = filtered[col].dt.strftime("%d-%m-%Y%n%H:%M:%S")
        
        return f"Total filtered visitors : {len(filtered)}", filtered.to_dict("records")