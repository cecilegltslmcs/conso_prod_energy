from packages.module_dashboard import *
from packages import authentification as auth
import streamlit as st

user = auth.user
password = auth.password
url = "https://www.data.gouv.fr/fr/datasets/r/d993e112-848f-4446-b93b-0a9d5997c4a4"
region_geojson = loading_geojson(url)

conn = init_connection(user, password)

st.title("Tableau de bord de la consommation et de production d'électricité en France à partir de 2012")
st.sidebar.title("Analyses par type de production")
option = st.sidebar.selectbox("Choississez une page.", ('Accueil', 'Consommation moyenne', 'Pourcentage pour chaque type de production','Production moyenne - Thermique',\
                              'Production moyenne - Nucléaire', 'Production moyenne - Eolien', 'Production moyenne - Solaire', 'Production moyenne - Hydraulique',
                              'Production moyenne - Pompage', 'Production moyenne - Bioénergies'))

if option == "Accueil":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image("images/logo-odre.svg", width=75)
    with col3:
        st.write(' ')
    st.header("Bienvenue sur cet outil qui vous permet de consulter l'historique des consommations et production d'électricité région par région en France.\
               Sélectionnez une analyse sur le menu de gauche pour continuer.")
    st.image("images/power-lines.jpg")
    st.write("Réalisé par Cécile Guillot - Données provenant de l'API Open Data Réseaux électriques")

if option == "Consommation moyenne":
    st.header("Informations concernant la consommation d'énergie")
    avg_consumption = query_mean("consommation", conn)
    fig = choropleth_map_conso(avg_consumption, region_geojson)
    st.write(fig)

    consumption_year = query_time_conso("consommation", conn)
    line_fig = line_chart_conso(consumption_year)
    st.write(line_fig)

if option == "Pourcentage pour chaque type de production":
    st.header("Pourcentage de la production moyenne par région et type d'énergie")
    df = query_pct(conn)
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


if option == "Production moyenne - Thermique":
    st.header("Informations concernant la production d'énergie d'origine hhermique")
    avg_thermique = query_mean("thermique", conn)
    fig = choropleth_map(avg_thermique, region_geojson)
    st.write(fig)

    thermique_year = query_time("thermique", conn)
    line_fig = line_chart(thermique_year)
    st.write(line_fig)

if option == "Production moyenne - Nucléaire":
    st.header("Informations concernant la production d'énergie d'origine nucléaire")
    avg_nucleaire = query_mean("nucleaire", conn)
    fig = choropleth_map(avg_nucleaire, region_geojson)
    st.write(fig)

    nuclear_year = query_time("nucleaire", conn)
    line_fig = line_chart(nuclear_year)
    st.write(line_fig)

if option == "Production moyenne - Eolien":
    st.header("Informations concernant la production d'énergie d'origine éolienne")
    avg_eolien = query_mean("eolien", conn)
    fig = choropleth_map(avg_eolien, region_geojson)
    st.write(fig)

    wind_year = query_time("eolien", conn)
    line_fig = line_chart(wind_year)
    st.write(line_fig)

if option == "Production moyenne - Solaire":
    st.header("Informations concernant la production d'énergie d'origine solaire")
    avg_solaire = query_mean("solaire", conn)
    fig = choropleth_map(avg_solaire, region_geojson)
    st.write(fig)

    sun_year = query_time("solaire", conn)
    line_fig = line_chart(sun_year)
    st.write(line_fig)

if option == "Production moyenne - Hydraulique":
    st.header("Informations concernant la production d'énergie d'origine hydraulique")
    avg_hydraulique = query_mean("hydraulique", conn)
    fig = choropleth_map(avg_hydraulique, region_geojson)
    st.write(fig)

    water_year = query_time("hydraulique", conn)
    line_fig = line_chart(water_year)
    st.write(line_fig)

if option == "Production moyenne - Pompage":
    st.header("Informations concernant la production d'énergie par pompage")
    avg_pompage = query_mean("pompage", conn)
    fig = choropleth_map(avg_pompage, region_geojson)
    st.write(fig)
    
    pompage_year = query_time("pompage", conn)
    line_fig = line_chart(pompage_year)
    st.write(line_fig)

if option == "Production moyenne - Bioénergies":
    st.header("Informations concernant la production d'énergie d'origine bio")
    avg_bioenergies = query_mean("bioenergies", conn)
    fig = choropleth_map(avg_bioenergies, region_geojson)
    st.write(fig)

    bioenergy_year = query_time("bioenergies", conn)
    line_fig = line_chart(bioenergy_year)
    st.write(line_fig)
