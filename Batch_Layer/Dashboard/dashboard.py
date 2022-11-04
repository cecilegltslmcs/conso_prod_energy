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

def query_pct():
    sql_query =  'SELECT libelle_region, AVG(pct_thermique) AS Thermique, AVG(pct_nucleaire) AS Nucleaire,\
                  AVG(pct_eolien) AS Eolien, AVG(pct_solaire) AS Solaire, AVG(pct_hydraulique) AS Hydraulique, AVG(pct_bioenergies) AS Bioenergies\
                  FROM consumption\
                  INNER JOIN region ON consumption.code_insee_region = region.code_insee_region\
                  GROUP BY libelle_region;'
    dataset = pd.read_sql_query(sql_query, conn, dtype={"libelle_region": str})
    dataset.rename(columns={"libelle_region" : "Région"}, inplace=True)
    return dataset

def query_time(feature):
    sql_query = f'SELECT EXTRACT(YEAR FROM date) AS year, libelle_region, AVG({feature})\
                FROM consumption\
                INNER JOIN region ON consumption.code_insee_region = region.code_insee_region\
                GROUP BY year, libelle_region;'
    dataset = pd.read_sql_query(sql_query, conn, dtype={"year":int, "libelle_region": str, 'avg':float})
    dataset.rename(columns={"year" : "Année",
                            "libelle_region" : "Région",
                            "avg": "Consommation Annuelle Moyenne (en MW)"}, inplace=True)
    return dataset

def line_chart(dataset):
    fig = px.line(dataset, x="Année", y="Consommation Annuelle Moyenne (en MW)", color="Région")
    return fig

def bar_chart(dataset, feature):
    fig = px.bar(dataset, x=feature, y='Région',
                color="Région",
                text_auto=True)
    return fig

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
except:
    print('Error while connecting to PostgreSQL')

st.title("Tableau de bord de la consommation d'électricité en France à partir de 2012")
st.sidebar.title("Analyses par type de production")
option = st.sidebar.selectbox("Choississez une page.", ('Accueil', 'Consommation moyenne (toutes sources confondues)', 'Pourcentage pour chaque type de production','Consommation moyenne - Thermique',\
                              'Consommation moyenne - Nucléaire', 'Consommation moyenne - Eolien', 'Consommation moyenne - Solaire', 'Consommation moyenne - Hydraulique',
                              'Consommation moyenne - Pompage', 'Consommation moyenne - Bioénergies'))

if option == "Accueil":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image("img/logo-odre.svg", width=75)
    with col3:
        st.write(' ')
    st.header("Bienvenue sur cet outil qui vous permet de consulter l'historique des consommations d'électricité région par région en France.\
               Sélectionnez une analyse sur le menu de gauche pour continuer.")
    st.image("img/power-lines.jpg")
    st.write("Réalisé par Cécile Guillot - Données provenant de l'API Open Data Réseaux électriques")

if option == "Consommation moyenne (toutes sources confondues)":
    st.header("Informations concernant la consommation d'énergie - Toutes sources confondues")
    avg_consumption = query_mean("consommation")
    fig = choropleth_map(avg_consumption)
    st.write(fig)

    consumption_year = query_time("consommation")
    line_fig = line_chart(consumption_year)
    st.write(line_fig)

if option == "Pourcentage pour chaque type de production":
    st.header("Pourcentage de la consommation moyenne par type de production")
    df = query_pct()
    prod = st.radio(
    "Choississez un type de production",
    ('Thermique', 'Nucléaire', 'Eolien', 'Solaire', 'Hydraulique', 'Bioénergies'))
    if prod == "Thermique":
        fig = bar_chart(df, 'thermique')
        st.write(fig)
    if prod == "Nucléaire":
        fig = bar_chart(df, 'nucleaire')
        st.write(fig)
    if prod == "Eolien":
        fig = bar_chart(df, 'eolien')
        st.write(fig)
    if prod == "Solaire":
        fig = bar_chart(df, 'solaire')
        st.write(fig)
    if prod == "Hydraulique":
        fig = bar_chart(df, 'hydraulique')
        st.write(fig)
    if prod == "Bioénergies":
        fig = bar_chart(df, 'bioenergies')
        st.write(fig)


if option == "Consommation moyenne - Thermique":
    st.header("Informations concernant la consommation d'énergie - Thermique")
    avg_thermique = query_mean("thermique")
    fig = choropleth_map(avg_thermique)
    st.write(fig)

    thermique_year = query_time("thermique")
    line_fig = line_chart(thermique_year)
    st.write(line_fig)

if option == "Consommation moyenne - Nucléaire":
    st.header("Informations concernant la consommation d'énergie - Nucléaire")
    avg_nucleaire = query_mean("nucleaire")
    fig = choropleth_map(avg_nucleaire)
    st.write(fig)

    nuclear_year = query_time("nucleaire")
    line_fig = line_chart(nuclear_year)
    st.write(line_fig)

if option == "Consommation moyenne - Eolien":
    st.header("Informations concernant la consommation d'énergie - Eolien")
    avg_eolien = query_mean("eolien")
    fig = choropleth_map(avg_eolien)
    st.write(fig)

    wind_year = query_time("eolien")
    line_fig = line_chart(wind_year)
    st.write(line_fig)

if option == "Consommation moyenne - Solaire":
    st.header("Informations concernant la consommation d'énergie - Solaire")
    avg_solaire = query_mean("solaire")
    fig = choropleth_map(avg_solaire)
    st.write(fig)

    sun_year = query_time("solaire")
    line_fig = line_chart(sun_year)
    st.write(line_fig)

if option == "Consommation moyenne - Hydraulique":
    st.header("Informations concernant la consommation d'énergie - Hydraulique")
    avg_hydraulique = query_mean("hydraulique")
    fig = choropleth_map(avg_hydraulique)
    st.write(fig)

    water_year = query_time("hydraulique")
    line_fig = line_chart(water_year)
    st.write(line_fig)

if option == "Consommation moyenne - Pompage":
    st.header("Informations concernant la consommation d'énergie - Pompage")
    avg_pompage = query_mean("pompage")
    fig = choropleth_map(avg_pompage)
    st.write(fig)
    
    pompage_year = query_time("pompage")
    line_fig = line_chart(pompage_year)
    st.write(line_fig)

if option == "Consommation moyenne - Bioénergies":
    st.header("Informations concernant la consommation d'énergie - Bioénergies")
    avg_bioenergies = query_mean("bioenergies")
    fig = choropleth_map(avg_bioenergies)
    st.write(fig)

    bioenergy_year = query_time("bioenergies")
    line_fig = line_chart(bioenergy_year)
    st.write(line_fig)