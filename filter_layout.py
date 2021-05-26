from dash_core_components.Checklist import Checklist
import dash_html_components as html
from filter_components import *

marginBottom = {"marginBottom": 10}

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
            # First division
            html.Div([
                # Gender checklist division
                html.Div([
                    html.Label(children="Gender : "),
                    generate_gender_checklist(days)
                ], style=marginBottom),
                
                # Final status checklist division
                html.Div([
                    html.Label(children="Final Status : "),
                    generate_final_status_checklist(days)
                ], style=marginBottom),
                
                # Appointment checklist division
                html.Div([
                    html.Label(children="Appointment : "),
                    generate_appointment_checklist()
                ], style=marginBottom),
                
                # Age division
                html.Div([
                    html.Label(children="Age : "),
                    generate_two_inputs_components(
                        min_id="min-age-input",
                        max_id="max-age-input"
                    )
                ], style=marginBottom),
                
                # ช่วงเวลาที่ visitors เริ่มเข้าสู่ระบบ division
                html.Div([
                    html.Label(children="ช่วงเวลาที่ visitors เริ่มเข้าสู่ระบบ (hrs) : "),
                    generate_two_inputs_components(
                        min_id="min-start-input",
                        max_id="max-start-input",
                        min=0,
                        max=24
                    )
                ])
            ], style={"width": "20%"})
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