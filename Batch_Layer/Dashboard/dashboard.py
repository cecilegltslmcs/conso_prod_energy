import json
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from sqlalchemy import create_engine
import streamlit as st
import time
user = "postgres"
password = "password42!"

def loading_geojson(url):
    try:
        response = requests.get(url)
        response = response.json()
    except:
        print("Wrong URL")
    return response

url = "https://www.data.gouv.fr/fr/datasets/r/d993e112-848f-4446-b93b-0a9d5997c4a4"
region_geojson = loading_geojson(url)

@st.experimental_singleton
def init_connection():
    return create_engine(f'postgresql://{user}:{password}@localhost:5432/energy_consumption')

try:
    conn = init_connection()
    print('Connection OK')
except (Exception, Error) as error:
    print('Error while connecting to PostgreSQL', error)

sql_query = "SELECT consumption.code_insee_region, libelle_region, AVG(consommation)\
             FROM consumption\
             INNER JOIN region ON consumption.code_insee_region = region.code_insee_region\
             GROUP BY consumption.code_insee_region, libelle_region;"
avg_consumption = pd.read_sql_query(sql_query, conn, dtype={"code_insee_region":str, "libelle_region": str, "avg":float})
avg_consumption.rename(columns={"code_insee_region" : "code",
                                "libelle_region" : "region",
                                "avg": "consommation moyenne"}, inplace=True)

st.header('Tableau de bord de la consommation d\'électricité en France de 2013 à 2022')
st.text(time.strftime("%d-%m-%Y %H:%M"))

fig = px.choropleth_mapbox(avg_consumption, geojson=region_geojson,
                           featureidkey="properties.reg",
                           locations='code',
                           color='consommation moyenne',
                           color_continuous_scale="Viridis",
                           mapbox_style="carto-positron",
                           zoom=4, center = {"lat": 46.2276, "lon": 2.21},
                           opacity=0.5,
                           labels={'consommation monyenne':'Consommation moyenne'})

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.write(fig)

