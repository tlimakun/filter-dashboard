from dash_core_components.Checklist import Checklist
import dash_html_components as html
from filter_components import *

datetime_style = {"display": "inline-block",
                  "width": "50%",
                  "vecticalAlign": "top"}

def filter_layout(days):
    """
    Main layout of filter dashboard.
    """
    
    return html.Div([
        # Date picker range
        generate_date_picker_range(
            label="Date:",
            days=days
        ),
        
        # Filter fields division
        html.Div([
            # First division
            html.Div([
                # Gender checklist
                generate_possible_values_checklist(
                    label="Gender:",
                    id="gender-checklist",
                    days=days,
                    column="gender"
                ),
                
                # Final status checklist
                generate_possible_values_checklist(
                    label="Final Status:",
                    id="final-status-checklist",
                    days=days,
                    column="final_status"
                ),
                
                # Appointment checklist
                generate_appointment_checklist(label="Appointment:"),
                
                # Age input
                generate_two_inputs_components(
                    label="Age:",
                    min_id="min-age-input",
                    max_id="max-age-input"
                ),
                
                # ช่วงเวลาที่ visitors เริ่มเข้าสู่ระบบ input
                generate_two_inputs_components(
                    label="ช่วงเวลาที่ visitors เริ่มเข้าสู่ระบบ (hrs):",
                    min_id="min-start-time-input",
                    max_id="max-start-time-input",
                    min=0,
                    max=24
                ),
                
                # ระยะเวลาที่ visitors input
                generate_two_inputs_components(
                    label="ระยะเวลาที่ visitors ใช้ทั้งระบบ (hrs):",
                    min_id="min-total-time-input",
                    max_id="max-total-time-input",
                    min=0,
                    max=24
                )
            ], style={"display": "inline-block",
                      "width": "22%",
                      "marginRight": "1%"}),
            
            # Second division
            html.Div([
                # 2-1 sub division
                html.Div([
                    generate_checkpoints_ordering_division(label="ลำดับของ checkpoints:")
                ]),
                
                # 2-2 sub division
                html.Div([
                    # Clinic checklist
                    generate_clinics_checklist(label="Clinics:")
                ], style={"display": "inline-block",
                          "width": "29%",
                          "marginRight": "1%"}),
                
                # 2-3 sub division
                html.Div([
                    # First datetime column radioItems division
                    html.Div([
                        # KIOS G floor datetime column radioItems
                        generate_require_datetime_radioItems(
                            label="KIOS-G Datetime:",
                            id="kios-g-column-radioItems"
                        ),
                        
                        # KIOS datetime column radioItems
                        generate_require_datetime_radioItems(
                            label="KIOS Datetime:",
                            id="kios-column-radioItems"
                        ),
                        
                        # Nurse screen datetime column radioItems
                        generate_require_datetime_radioItems(
                            label="Nurse Screen Datetime:",
                            id="screen-column-radioItems"
                        ),
                        
                        # Send to doctor datetime column radioItems
                        generate_require_datetime_radioItems(
                            label="Send to Doctor Datetime:",
                            id="send-doc-column-radioItems"
                        ),
                        
                        # Doctor call datetime column radioItems
                        generate_require_datetime_radioItems(
                            label="Doctor Call Datetime:",
                            id="doc-call-column-radioItems"
                        )
                    ], style=datetime_style),
                    
                    # Second datetimte column radioItems division
                    html.Div([
                        # Doctor begin datetime column radioItems
                        generate_require_datetime_radioItems(
                            label="Doctor Begin Datetime:",
                            id="doc-begin-column-radioItems"
                        ),
                        
                        # Doctor submit column radioItems
                        generate_require_datetime_radioItems(
                            label="Doctor Submit Datetime:",
                            id="doc-submit-column-radioItems"
                        ),
                        
                        # Nurse response datetime column radioItems
                        generate_require_datetime_radioItems(
                            label="Nurse Response Datetime:",
                            id="nurse-column-radioItems"
                        ),
                        
                        # Payment datetime column radioItems
                        generate_require_datetime_radioItems(
                            label="Payment Datetime:",
                            id="payment-column-radioItems"
                        ),
                        
                        # Pharmacy datetime column radioItems
                        generate_require_datetime_radioItems(
                            label="Receive Pharmacy Datetime:",
                            id="pharmacy-column-radioItems"
                        )
                    ], style=datetime_style)
                ], style={"display": "inline-block",
                          "width": "38%",
                          "verticalAlign": "top",
                          "marginRight": "1%"}),
                
                # 2-4 sub division
                html.Div([
                    # Time between checkpoints label
                    generate_time_between_label(label="ระยะเวลาที่ visitors ใช้ระหว่าง 2 checkpoints (hrs):"),
                    
                    # Time between checkpoints main division
                    html.Div(id="time-btw-checkpoints-main-div"),
                    
                    # More and Less button
                    generate_more_less_button(
                        more_btn_id="more-time-btw-div-btn",
                        less_btn_id="less-time-btw-div-btn"
                    )
                ], style={"display": "inline-block",
                          "width": "29%",
                          "verticalAlign": "top"})
            ], style={"display": "inline-block",
                      "width": "77%",
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