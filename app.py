import dash
from data_preprocessing import load_data

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

filename = "../data/sample-data-1-7Mar.xlsx"
days = load_data(filename)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True)