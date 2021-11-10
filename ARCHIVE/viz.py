import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import gspread
import plotly.express as px

gc = gspread.oauth()

wks = gc.open("2021 Player Data as of 2021_04_21").sheet1

sheet = wks.get_all_values()
headers = sheet.pop(0)

data = pd.DataFrame(sheet, columns=headers)
data = data.head(20)

app = dash.Dash(__name__)

fig = px.scatter(data, x="on_base_percentage", y="on_base_percentage",text = 'name')

app.layout = dcc.Graph(figure=fig)

if __name__ == "__main__":
    app.run_server(debug=True)