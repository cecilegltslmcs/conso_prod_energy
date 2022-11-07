import authentification as auth
import pandas as pd
import plotly.express as px
import requests
from sqlalchemy import create_engine
import streamlit as st

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
