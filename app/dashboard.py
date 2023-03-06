import os
from dash import Dash, dcc, html
import pandas as pd
import plotly.io as pio
from pymongo import MongoClient
import packages.authentification as auth
from packages.module_dashboard import *

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

map_conso = choropleth_map(df, region_geojson, "consommation")
map_prod = choropleth_map(df, region_geojson, "production")
map_diff = choropleth_map(df, region_geojson, "diff")
stack_prod = stack_chart(df)

app.layout = html.Div([
        html.H1(children="Tableau de bord de la consommation et de la production d'énergie en France en temps réel",
                style={
                    'textAlign' : 'center',
                }),
        html.Div(children="Cette application permet de visualiser les données de consommation et de production d'énergie région par région. Les données présentées sont actualisées toutes les 15 minutes.",
                 style={
                     'textAlign': 'justify',
                 }),
        html.Div(children="Source : https://opendata.reseaux-energies.fr/",
                 style={
                     'textAlign' : 'justify',
                     'fontStyle' : 'italic'
                 }),
        html.H3(children="Carte de la consommation en temps réel"),
        dcc.Graph(id="graph-conso",
                  figure=map_conso),
        html.H3(children="Données de production en temps réel"),
        dcc.Graph(id="map-prod",
                  figure=map_prod),
        html.H3(children="Différence entre consommation et production"),
        dcc.Graph(id="diff",
                  figure=map_diff)
])


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port="8050", debug=debug)
