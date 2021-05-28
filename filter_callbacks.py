from dash.dependencies import Input, Output, State, MATCH, ALL
import dash
import pandas as pd
import numpy as np
from datetime import date
from filter_components import generate_time_between_checkpoints_division

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

def datetime_columns_dict(kios_g_dt, kios_dt, screen_dt, send_doc_dt, doc_call_dt, doc_begin_dt,
                          doc_submit_dt, nurse_dt, payment_dt, pharmacy_dt):
    """
    Generate datetime columns dictionary.
    """
    
    datetime_dict = {"kios_g_dt": kios_g_dt, "kios_dt": kios_dt, "screen_dt": screen_dt, "send_doc_dt": send_doc_dt,
                     "doc_call_dt": doc_call_dt, "doc_begin_dt": doc_begin_dt, "doc_submit_dt": doc_submit_dt,
                     "nurse_dt": nurse_dt, "payment_dt": payment_dt, "pharmacy_dt": pharmacy_dt}
    
    return datetime_dict

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
        Input("max-total-time-input", "value"),
        Input("clinics-checklist", "value"),
        Input("kios-g-column-radioItems", "value"),
        Input("kios-column-radioItems", "value"),
        Input("screen-column-radioItems", "value"),
        Input("send-doc-column-radioItems", "value"),
        Input("doc-call-column-radioItems", "value"),
        Input("doc-begin-column-radioItems", "value"),
        Input("doc-submit-column-radioItems", "value"),
        Input("nurse-column-radioItems", "value"),
        Input("payment-column-radioItems", "value"),
        Input("pharmacy-column-radioItems", "value"),
        Input("checkpoints-ordering-dropdown", "value"),
        Input("checkpoints-ordering-radioItems", "value"),
        Input({"type": "start-checkpoint-dropdown", "index": ALL}, "value"),
        Input({"type": "end-checkpoint-dropdown", "index": ALL}, "value"),
        Input({"type": "min-btw-time-input", "index": ALL}, "value"),
        Input({"type": "max-btw-time-input", "index": ALL}, "value")
    )
    def update_data_table(start_date, end_date, gender, final_status, appointment, min_age, max_age,
                          min_start_time, max_start_time, min_total_time, max_total_time, clinics,
                          kios_g_dt, kios_dt, screen_dt, send_doc_dt, doc_call_dt, doc_begin_dt,
                          doc_submit_dt, nurse_dt, payment_dt, pharmacy_dt, checkpoints, isOrdered,
                          start_checkpoints, end_checkpoints, min_btw, max_btw):
        # Filter data between given start date and end date
        filtered = filter_data_by_date(days, start_date, end_date)
        
        # Filter appointment
        if len(appointment) == 1:
            if 1 in appointment:
                filtered = filtered[(filtered["visit_dt"].dt.minute.isin([0, 30])) & (filtered["visit_dt"].dt.second == 0)]
            elif 0 in appointment:
                filtered = filtered[(~filtered["visit_dt"].dt.minute.isin([0, 30])) | (filtered["visit_dt"].dt.second != 0)]
        elif len(appointment) == 0:
            filtered = filtered[filtered["vn"] == -1]
            
        # Filter datetime columns
        for col, value in datetime_columns_dict(kios_g_dt, kios_dt, screen_dt, send_doc_dt, doc_call_dt, doc_begin_dt,
                                                doc_submit_dt, nurse_dt, payment_dt, pharmacy_dt).items():
            if value == 1:
                filtered = filtered[~filtered[col].isna()]
            elif value == 0:
                filtered = filtered[filtered[col].isna()]
        
        # Filter gender, final status, age, and clinics
        filtered = filtered[(filtered["gender"].isin(gender)) &
                            (filtered["final_status"].isin(final_status)) &
                            (filtered["age"] >= min_age) & (filtered["age"] <= max_age) &
                            (filtered["clinic"].isin(clinics))]
        
        # Filter visitors with start time between min_start_time and max_start_time
        filtered["start_time"] = filtered[[col for col in filtered.columns if col.endswith("_dt") and col != "visit_dt"]].min(axis=1)
        filtered = filtered[(filtered["start_time"].dt.hour >= min_start_time) & (filtered["start_time"].dt.hour < max_start_time)]
        
        # Filter visitors with total time in process between min_total_time and max_total_time
        filtered["end_time"] = filtered[[col for col in filtered.columns if col.endswith("_dt") and col != "visit_dt"]].max(axis=1)
        filtered["total_time"] = (filtered["end_time"] - filtered["start_time"]) / np.timedelta64(1, 'h')
        filtered = filtered[(filtered["total_time"] >= min_total_time) & (filtered["total_time"] < max_total_time )]
        
        # Drop unused columns
        filtered.drop(["start_time", "end_time", "total_time"], axis=1)
        
        # Filter visitors with time between two checkpoints is between min_btw and max_btw
        def generate_time_btw(columns):
            if pd.isnull(columns[0]) or pd.isnull(columns[1]):
                return np.nan
            
            return abs((columns[0] - columns[1]) / np.timedelta64(1, 'h'))
        
        for index in range(max(len(start_checkpoints), len(end_checkpoints))):
            if start_checkpoints[index] == None or end_checkpoints[index] == None:
                continue
            
            filtered["time_btw"] = filtered[[start_checkpoints[index], end_checkpoints[index]]].apply(lambda columns: generate_time_btw(columns),
                                                                                                      axis=1)
            filtered = filtered[(filtered["time_btw"] >= min_btw[index]) &
                                (filtered["time_btw"] < max_btw[index]) |
                                (filtered["time_btw"].isna())]
            
            filtered.drop(["time_btw"], axis=1)
        
        # Filter visitors that have same checkpoint order with desired checkpoint ordering
        def order_checkpoints(columns, checkpoints):
            sequence = []
            for index in range(len(columns)):
                if not pd.isnull(columns[index]):
                    sequence.append((checkpoints[index], columns[index]))
            
            sequence = sorted(sequence, key=(lambda x: x[1]))
            sequence = list(map(lambda x: x[0], sequence))
            
            sequence_index = []
            for checkpoint in checkpoints:
                if checkpoint in sequence:
                    sequence_index.append(sequence.index(checkpoint))
            
            if sorted(sequence_index) == sequence_index:
                return True
            else:
                return False
            
        if checkpoints is not None:
            filtered["sequence"] = filtered[checkpoints].apply(lambda columns: order_checkpoints(columns, checkpoints), axis=1)
            if isOrdered == 1:
                filtered = filtered[filtered["sequence"]]
            else:
                filtered = filtered[~filtered["sequence"]]
            
            # Drop unused columns
            filtered.drop(["sequence"], axis=1)
        
        # Change format in datetime columns
        for col in [col for col in filtered.columns if col.endswith("_dt")]:
            filtered[col] = filtered[col].dt.strftime("%d-%m-%Y%n%H:%M:%S")
        
        return f"Total filtered visitors: {len(filtered)}", filtered.to_dict("records")

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
    
def callback_checkpoints_ordering_dropdown(app, days):
    """
    Update items in checkpoints ordering dropdown.
    """
    
    @app.callback(
        Output("checkpoints-ordering-dropdown", "options"),
        Input("kios-g-column-radioItems", "value"),
        Input("kios-column-radioItems", "value"),
        Input("screen-column-radioItems", "value"),
        Input("send-doc-column-radioItems", "value"),
        Input("doc-call-column-radioItems", "value"),
        Input("doc-begin-column-radioItems", "value"),
        Input("doc-submit-column-radioItems", "value"),
        Input("nurse-column-radioItems", "value"),
        Input("payment-column-radioItems", "value"),
        Input("pharmacy-column-radioItems", "value")
    )
    def update_checkpoints_ordering_dropdown(kios_g_dt, kios_dt, screen_dt, send_doc_dt, doc_call_dt, doc_begin_dt,
                                             doc_submit_dt, nurse_dt, payment_dt, pharmacy_dt):
        checkpoints = []
        
        for col, value in datetime_columns_dict(kios_g_dt, kios_dt, screen_dt, send_doc_dt, doc_call_dt, doc_begin_dt,
                                                doc_submit_dt, nurse_dt, payment_dt, pharmacy_dt).items():
            if value == 1:
                checkpoints.append({"label": col, "value": col})
                
        return checkpoints
    
def callback_checkpoints_ordering_radioItems(app, days):
    """
    Update checkpoints ordering radioItems if there is no any checkpoint in dropdown, disable radioItems.
    """
    
    @app.callback(
        Output("checkpoints-ordering-radioItems", "options"),
        Output("checkpoints-ordering-radioItems", "value"),
        Input("checkpoints-ordering-dropdown", "value")
    )
    def update_checkpoints_ordering_radioItems(checkpoints):
        if checkpoints is None or len(checkpoints) <= 1:
            options = [{"label": "ใช่", "value": 1, "disabled": True},
                       {"label": "ไม่ใช่", "value": 0, "disabled": True}]
        else:
            options = [{"label": "ใช่", "value": 1},
                       {"label": "ไม่ใช่", "value": 0}]
        
        return options, 1
    
def callback_all_datetime_columns_radioItems(app, days):
    """
    Update all datetime columns radioItems by "all-datetime-columns" radioItems.
    """
    
    @app.callback(
        Output("kios-g-column-radioItems", "options"),
        Output("kios-column-radioItems", "options"),
        Output("screen-column-radioItems", "options"),
        Output("send-doc-column-radioItems", "options"),
        Output("doc-call-column-radioItems", "options"),
        Output("doc-begin-column-radioItems", "options"),
        Output("doc-submit-column-radioItems", "options"),
        Output("nurse-column-radioItems", "options"),
        Output("payment-column-radioItems", "options"),
        Output("pharmacy-column-radioItems", "options"),
        Output("kios-g-column-radioItems", "value"),
        Output("kios-column-radioItems", "value"),
        Output("screen-column-radioItems", "value"),
        Output("send-doc-column-radioItems", "value"),
        Output("doc-call-column-radioItems", "value"),
        Output("doc-begin-column-radioItems", "value"),
        Output("doc-submit-column-radioItems", "value"),
        Output("nurse-column-radioItems", "value"),
        Output("payment-column-radioItems", "value"),
        Output("pharmacy-column-radioItems", "value"),
        Input("all-datetime-columns", "value")
    )
    def update_all_datetime_columns_radioItems(all_datetime):
        if all_datetime == 2:
            options = [
                {"label": "มี / ไม่มี", "value": 2},
                {"label": "มี", "value": 1},
                {"label": "ไม่มี", "value": 0}
            ]
        else:
            options = [
                {"label": "มี / ไม่มี", "value": 2, "disabled": True},
                {"label": "มี", "value": 1, "disabled": True},
                {"label": "ไม่มี", "value": 0, "disabled": True}
            ]
            
        return (options, options, options, options, options,
                options, options, options, options, options,
                all_datetime, all_datetime, all_datetime, all_datetime, all_datetime,
                all_datetime, all_datetime, all_datetime, all_datetime, all_datetime)
    
def callback_time_between_checkpoints_main_division(app, days):
    """
    Update time between checkpoints main division.
    """
    
    @app.callback(
        Output("btw-time-checkpoints-main-div", "children"),
        Input("more-btw-time-checkpoints-div-btn", "n_clicks"),
        State("btw-time-checkpoints-main-div", "children")
    )
    def update_time_between_checkpoints_main_division(more_btn, main_div):
        new_element = generate_time_between_checkpoints_division(
            start_checkpoint_id={"type": "start-checkpoint-dropdown",
                                "index": more_btn},
            end_checkpoint_id={"type": "end-checkpoint-dropdown",
                            "index": more_btn},
            min_id={"type": "min-btw-time-input",
                    "index": more_btn},
            max_id={"type": "max-btw-time-input",
                    "index": more_btn},
            min=0,
            max=24
        )
        
        main_div.append(new_element)
                
        return main_div
    
def generate_checkpoints_dropdown(kios_g_dt, kios_dt, screen_dt, send_doc_dt, doc_call_dt, doc_begin_dt,
                                  doc_submit_dt, nurse_dt, payment_dt, pharmacy_dt,
                                  first_checkpoints, second_checkpoints, checkpoint, id):
    """
    Generate checkpoints dropdown options.
    """
    
    checkpoints = []
        
    for col, value in datetime_columns_dict(kios_g_dt, kios_dt, screen_dt, send_doc_dt, doc_call_dt, doc_begin_dt,
                                            doc_submit_dt, nurse_dt, payment_dt, pharmacy_dt).items():
        if value == 1:
            checkpoints.append({"label": col, "value": col})
    
    if checkpoint != None:
        checkpoints.remove({"label": checkpoint, "value": checkpoint})
            
        for index, value in enumerate(first_checkpoints):
            if index == id["index"]:
                continue
            
            if first_checkpoints[index] == checkpoint:
                checkpoints.remove({"label": second_checkpoints[index], "value": second_checkpoints[index]})
            elif second_checkpoints[index] == checkpoint:
                checkpoints.remove({"label": first_checkpoints[index], "value": first_checkpoints[index]})
            
    return checkpoints
    
def callback_time_between_checkpoints_start_dropdown(app, days):
    """
    Update time between checkpoints start dropdown.
    """
    
    @app.callback(
        Output({"type": "start-checkpoint-dropdown", "index": MATCH}, "options"),
        Input("kios-g-column-radioItems", "value"),
        Input("kios-column-radioItems", "value"),
        Input("screen-column-radioItems", "value"),
        Input("send-doc-column-radioItems", "value"),
        Input("doc-call-column-radioItems", "value"),
        Input("doc-begin-column-radioItems", "value"),
        Input("doc-submit-column-radioItems", "value"),
        Input("nurse-column-radioItems", "value"),
        Input("payment-column-radioItems", "value"),
        Input("pharmacy-column-radioItems", "value"),
        Input({"type": "start-checkpoint-dropdown", "index": ALL}, "value"),
        Input({"type": "end-checkpoint-dropdown", "index": ALL}, "value"),
        Input({"type": "end-checkpoint-dropdown", "index": MATCH}, "value"),
        State({"type": "start-checkpoint-dropdown", "index": MATCH}, "id")
    )
    def update_time_between_checkpoints_start_dropdown(kios_g_dt, kios_dt, screen_dt, send_doc_dt, doc_call_dt, doc_begin_dt,
                                                       doc_submit_dt, nurse_dt, payment_dt, pharmacy_dt,
                                                       all_start_checkpoints, all_end_checkpoints, end_checkpoint, id):
        return generate_checkpoints_dropdown(kios_g_dt, kios_dt, screen_dt, send_doc_dt, doc_call_dt, doc_begin_dt,
                                             doc_submit_dt, nurse_dt, payment_dt, pharmacy_dt,
                                             all_start_checkpoints, all_end_checkpoints, end_checkpoint, id)
    
def callback_time_between_checkpoints_end_dropdown(app, days):
    """
    Update time between checkpoints end dropdown.
    """
    
    @app.callback(
        Output({"type": "end-checkpoint-dropdown", "index": MATCH}, "options"),
        Input("kios-g-column-radioItems", "value"),
        Input("kios-column-radioItems", "value"),
        Input("screen-column-radioItems", "value"),
        Input("send-doc-column-radioItems", "value"),
        Input("doc-call-column-radioItems", "value"),
        Input("doc-begin-column-radioItems", "value"),
        Input("doc-submit-column-radioItems", "value"),
        Input("nurse-column-radioItems", "value"),
        Input("payment-column-radioItems", "value"),
        Input("pharmacy-column-radioItems", "value"),
        Input({"type": "start-checkpoint-dropdown", "index": ALL}, "value"),
        Input({"type": "end-checkpoint-dropdown", "index": ALL}, "value"),
        Input({"type": "start-checkpoint-dropdown", "index": MATCH}, "value"),
        State({"type": "start-checkpoint-dropdown", "index": MATCH}, "id")
    )
    def update_time_between_checkpoints_end_dropdown(kios_g_dt, kios_dt, screen_dt, send_doc_dt, doc_call_dt, doc_begin_dt,
                                                     doc_submit_dt, nurse_dt, payment_dt, pharmacy_dt,
                                                     all_start_checkpoints, all_end_checkpoints, start_checkpoint, id):
        return generate_checkpoints_dropdown(kios_g_dt, kios_dt, screen_dt, send_doc_dt, doc_call_dt, doc_begin_dt,
                                             doc_submit_dt, nurse_dt, payment_dt, pharmacy_dt,
                                             all_start_checkpoints, all_end_checkpoints, start_checkpoint, id)
        
def change_checkpoint_dropdown_values(kios_g_dt, kios_dt, screen_dt, send_doc_dt, doc_call_dt, doc_begin_dt,
                                      doc_submit_dt, nurse_dt, payment_dt, pharmacy_dt, checkpoint):
    """
    Change checkpoint dropdown value to None if that datetime column radioItem changed to 2 or 0.
    """
      
    for col, value in datetime_columns_dict(kios_g_dt, kios_dt, screen_dt, send_doc_dt, doc_call_dt, doc_begin_dt,
                                            doc_submit_dt, nurse_dt, payment_dt, pharmacy_dt).items():
        if value == 0 and col == checkpoint:
            return None
        else:
            return checkpoint
        
def callback_time_between_checkpoints_start_dropdown_values(app, days):
    """
    Update time between checkpoints start dropdown values.
    """
    
    @app.callback(
        Output({"type": "start-checkpoint-dropdown", "index": MATCH}, "value"),
        Input("kios-g-column-radioItems", "value"),
        Input("kios-column-radioItems", "value"),
        Input("screen-column-radioItems", "value"),
        Input("send-doc-column-radioItems", "value"),
        Input("doc-call-column-radioItems", "value"),
        Input("doc-begin-column-radioItems", "value"),
        Input("doc-submit-column-radioItems", "value"),
        Input("nurse-column-radioItems", "value"),
        Input("payment-column-radioItems", "value"),
        Input("pharmacy-column-radioItems", "value"),
        State({"type": "start-checkpoint-dropdown", "index": MATCH}, "value")
    )
    def update_time_between_checkpoints_start_dropdown_values(kios_g_dt, kios_dt, screen_dt, send_doc_dt, doc_call_dt, doc_begin_dt,
                                                              doc_submit_dt, nurse_dt, payment_dt, pharmacy_dt, checkpoint):
        return change_checkpoint_dropdown_values(kios_g_dt, kios_dt, screen_dt, send_doc_dt, doc_call_dt, doc_begin_dt,
                                                 doc_submit_dt, nurse_dt, payment_dt, pharmacy_dt, checkpoint)
        
def callback_time_between_checkpoints_start_dropdown_values(app, days):
    """
    Update time between checkpoints end dropdown values.
    """
    
    @app.callback(
        Output({"type": "end-checkpoint-dropdown", "index": MATCH}, "value"),
        Input("kios-g-column-radioItems", "value"),
        Input("kios-column-radioItems", "value"),
        Input("screen-column-radioItems", "value"),
        Input("send-doc-column-radioItems", "value"),
        Input("doc-call-column-radioItems", "value"),
        Input("doc-begin-column-radioItems", "value"),
        Input("doc-submit-column-radioItems", "value"),
        Input("nurse-column-radioItems", "value"),
        Input("payment-column-radioItems", "value"),
        Input("pharmacy-column-radioItems", "value"),
        State({"type": "end-checkpoint-dropdown", "index": MATCH}, "value")
    )
    def update_time_between_checkpoints_start_dropdown_values(kios_g_dt, kios_dt, screen_dt, send_doc_dt, doc_call_dt, doc_begin_dt,
                                                              doc_submit_dt, nurse_dt, payment_dt, pharmacy_dt, checkpoint):
        return change_checkpoint_dropdown_values(kios_g_dt, kios_dt, screen_dt, send_doc_dt, doc_call_dt, doc_begin_dt,
                                                 doc_submit_dt, nurse_dt, payment_dt, pharmacy_dt, checkpoint)