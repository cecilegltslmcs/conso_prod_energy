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

def query_mean(feature):
    sql_query = f"SELECT consumption.code_insee_region, libelle_region, AVG({feature})\
                FROM consumption\
                INNER JOIN region ON consumption.code_insee_region = region.code_insee_region\
                GROUP BY consumption.code_insee_region, libelle_region;"
    dataset = pd.read_sql_query(sql_query, conn, dtype={"code_insee_region":str, "libelle_region": str, "avg":float})
    dataset.rename(columns={"code_insee_region" : "code",
                                    "libelle_region" : "region",
                                    "avg": "consommation moyenne"}, inplace=True)
    return dataset

def choropleth_map(dataset):
    fig = px.choropleth_mapbox(dataset, geojson=region_geojson,
                               featureidkey="properties.reg",
                               locations='code',
                               color='consommation moyenne',
                               color_continuous_scale="rdylbu_r",
                               mapbox_style="carto-positron",
                               zoom=4, center = {"lat": 46.2276, "lon": 2.21},
                               opacity=0.6,
                               labels={'consommation moyenne':'Consommation moyenne (MW)'})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


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

st.title("Tableau de bord de la consommation d'électricité en France à partir de 2012")
st.sidebar.title("Analyses par type d'énergie")
option = st.sidebar.selectbox("Choississez une page.", ('Accueil', 'Consommation moyenne (toutes sources confondues)', 'Consommation moyenne - Thermique', 'Consommation moyenne - Nucléaire'))

if option == "Accueil":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image("img/logo-odre.svg", width=100)
    with col3:
        st.write(' ')
    st.header("Bienvenue sur cet outil qui vous permet de consulter l'historique des consommations d'électricité région par région en France.\
               Sélectionnez une analyse sur le menu de gauche pour continuer.")
    st.image("img/power-lines.jpg")
    st.write("Réalisé par Cécile Guillot - Données provenant de l'API Open Data Réseaux électriques")

if option == "Consommation moyenne (toutes sources confondues)":
    avg_consumption = query_mean("consommation")
    fig = choropleth_map(avg_consumption)
    st.write(fig)

if option == "Consommation moyenne - Thermique":
    avg_thermique = query_mean("thermique")
    fig = choropleth_map(avg_thermique)
    st.write(fig)


if option == "Consommation moyenne - Nucléaire":
    avg_nucleaire = query_mean("nucleaire")
    fig = choropleth_map(avg_nucleaire)
    st.write(fig)

