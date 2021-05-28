import dash
from data_preprocessing import load_data
from filter_layout import filter_layout
import filter_callbacks

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets)

filename = "../data/sample-data-1-7Mar.xlsx"
days = load_data(filename)

app.layout = filter_layout(days)

# Call all callback functions from filter_callbacks.py
for i in dir(filter_callbacks):
    item = getattr(filter_callbacks, i)
    
    if callable(item) and i.startswith("callback_"):
        item(app, days)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True)