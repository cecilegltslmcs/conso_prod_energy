from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import os
import plotly.io as pio
from pymongo import MongoClient
import packages.authentification as auth
from packages.module_dashboard import *
import pandas as pd

user = auth.mongodb_user
password = auth.mongodb_password
host = auth.mongodb_host
port = auth.mongodb_port
uri = f"mongodb://{user}:{password}@{host}:{port}"

pio.templates.default = "seaborn"
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True

def init_connection():
    return MongoClient(uri)

def get_data():
    db = client['electricity_prod']
    items = db['streaming_data'].find()
    items = list(items)
    return items

try:
    client = init_connection()
    print("Connection OK")
except:
    print("Connection error")

items = get_data()
df = pd.DataFrame(items)

url = "https://www.data.gouv.fr/fr/datasets/r/d993e112-848f-4446-b93b-0a9d5997c4a4"
region_geojson = loading_geojson(url)

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Dashboard de la consommation et de la production d'énergie"

map_conso = choropleth_map(df, region_geojson, df.consommation)
map_prod = choropleth_map(df, region_geojson, df.production)
map_diff = choropleth_map(df, region_geojson, df.diff)
stack_prod = stack_chart(df)


app.layout = html.Div([
    html.Div([
        dcc.H4("""# Tableau de bord de la consommation et de la production d'énergie en France en temps réel
    Cette application permet de visualiser les données de consommation et de production d'énergie région par région. Les données présentées sont actualisées toutes les 15 minutes.
    Source : [Open Data Réseaux-Energies](https://opendata.reseaux-energies.fr/)""")]),
        dcc.Tabs(id="tabs", value='tab-1', children=[
            dcc.Tab(label="Consommation", value="tab-1"),
            dcc.Tab(label="Production", value="tab-2"),
            dcc.Tab(label="Difference ", value="tab-3")
        ]),
        html.Div(id="tabs-content")
        ])

@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == "tab-1":
        return html.Div([
            html.H3("Données de consommation en temps réel (actualisation toutes les 15 minutes)"),
            dcc.Graph(figure=map_conso)
        ])
    elif tab == "tab-2":
        return html.Div([
            html.H3("Données de production en temps réel (actualisation toutes les 15 minutes)"),
            dcc.Graph(figure=map_prod),
            dcc.Graph(figure=stack_prod)
        ])
    elif tab == "tab-3":
        return html.Div([
            html.H3("Données de production en temps réel (actualisation toutes les 15 minutes)"),
            dcc.Graph(figure=map_diff)
        ])

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port="8050", debug=debug)
