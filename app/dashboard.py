import dash
import dash_core_components as dcc
import dash_html_components as html
from flask import Flask
import os
import plotly.io as pio
import plotly.express as px
from pymongo import MongoClient
import packages.authentification as auth
import pandas as pd
import requests

user = auth.mongodb_user
password = auth.mongodb_password
host = auth.mongodb_host
port = auth.mongodb_port
uri = f"mongodb://{user}:{password}@{host}:{port}"

pio.templates.default = "seaborn"
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True

def init_connection():
    return MongoClient(uri)

def get_data():
    db = client['electricity_prod']
    items = db['streaming_data'].find()
    items = list(items)
    return items

def loading_geojson(url):
    try:
        response = requests.get(url)
        response = response.json()
    except:
        print("Wrong URL")
    return response

try:
    client = init_connection()
    print("Connection OK")
except:
    print("Connection error")

items = get_data()
df = pd.DataFrame(items)

url = "https://www.data.gouv.fr/fr/datasets/r/d993e112-848f-4446-b93b-0a9d5997c4a4"
region_geojson = loading_geojson(url)

app = dash.Dash(__name__)
server = app.server
app.title = "Dashboard"

fig = px.choropleth_mapbox(df, geojson=region_geojson,
                               featureidkey="properties.reg",
                               locations='code_insee_region',
                               color=df.consommation,
                               color_continuous_scale="rdylbu_r",
                               mapbox_style="carto-positron",
                               zoom=4, center = {"lat": 46.2276, "lon": 2.21},
                               opacity=0.6)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

app.layout = html.Div([
    html.Div([
        dcc.Markdown("""# Tableau de bord de la consommation et de la production d'énergie en France en temps réel
    Cette application permet de visualiser les données de consommation et de production
    d'énergie région par région. Les données présentées sont actualisées toutes les 15 minutes.
    Source : *[Open Data Réseaux-Energies](https://opendata.reseaux-energies.fr/)*""")]),
        dcc.Graph(figure=fig)
        ])

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port="8050", debug=debug)