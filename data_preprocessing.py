import pandas as pd
from datetime import date

def load_data(filename):
    """
    Load data from file and preprocess it.
    """
    
    # Load data
    days = pd.read_excel(filename, sheet_name=None)
    
    # Change column names to English.
    for day in days.values():
        day.columns = ["vn", "gender", "age", "visit_dt", "clinic_code", "clinic",
                       "kios_g_dt", "kios_dt", "screen_dt", "send_doc_dt",
                       "doc_call_dt", "doc_begin_dt", "doc_submit_dt", "nurse_dt",
                       "payment_dt", "pharmacy_dt", "final_status"]
        
    # Delete sheets that datetime columns don't contain only "datetime64[ns]" type.
    for d in list(days.keys()):
        type = list(set([days.get(d)[col].dtype for col in days.get(d).columns if col.endswith("_dt")]))
        if len(type) != 1 or str(type[0]) != 'datetime64[ns]':
            del days[d]

    # Change "days" dictionary key names.
    for d, day in list(days.items()):
        D = day["visit_dt"].dt.day.unique()[0]
        M = day["visit_dt"].dt.month.unique()[0]
        Y = day["visit_dt"].dt.year.unique()[0]
        sheet_date = date(Y, M, D)
        days[sheet_date] = days.pop(d)

    # Remove visitors with datetime columns that contain different date from sheet date.
    for d in days.keys():
        for col in [col for col in days.get(d).columns if col.endswith("_dt")]:
            days[d] = days.get(d)[(days.get(d)[col].dt.day == d.day) | (days.get(d)[col].isna())]

    return days