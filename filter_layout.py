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
        generate_date_picker_range(label="Date:",
                                   days=days),
        
        # Filter fields division
        html.Div([
            # First division
            html.Div([
                # Gender checklist division
                generate_possible_values_checklist(
                    label="Gender:",
                    id="gender-checklist",
                    days=days,
                    column="gender"
                ),
                
                # Final status checklist division
                generate_possible_values_checklist(
                    label="Final Status:",
                    id="final-status-checklist",
                    days=days,
                    column="final_status"
                ),
                
                # Appointment checklist division
                generate_appointment_checklist(label="Appointment:"),
                
                # Age division
                generate_two_inputs_components(
                    label="Age:",
                    min_id="min-age-input",
                    max_id="max-age-input"
                ),
                
                # ช่วงเวลาที่ visitors เริ่มเข้าสู่ระบบ division
                generate_two_inputs_components(
                    label="ช่วงเวลาที่ visitors เริ่มเข้าสู่ระบบ (hrs):",
                    min_id="min-start-time-input",
                    max_id="max-start-time-input",
                    min=0,
                    max=24
                ),
                
                # ระยะเวลาที่ visitors ใช้ทั้งระบบ
                generate_two_inputs_components(
                    label="ระยะเวลาที่ visitors ใช้ทั้งระบบ (hrs):",
                    min_id="min-total-time-input",
                    max_id="max-total-time-input",
                    min=0,
                    max=24
                )
            ], style={"display": "inline-block",
                      "width": "20%",
                      "marginRight": "1%"}),
            
            # Second division
            html.Div([
                # Clinic checklist division
                generate_clinics_checklist(label="Clinics:")
            ], style={"display": "inline-block",
                      "width": "79%",
                      "verticalAlign": "top",})
        ], style={"borderTop": "thin lightgrey solid",
                  "borderBottom": "thin lightgrey solid",
                  "paddingTop": 5}),
        
        # Data table division
        html.Div([
            # Total visitors label
            generate_total_visitors_label(),
            
            # Data table
            generate_data_table(days=days)
        ])
    ])