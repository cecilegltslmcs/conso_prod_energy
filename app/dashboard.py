from packages.module_dashboard import *
from pymongo import MongoClient
import packages.authentification as auth
import pandas as pd
import streamlit as st
import time

url = "https://www.data.gouv.fr/fr/datasets/r/d993e112-848f-4446-b93b-0a9d5997c4a4"
region_geojson = loading_geojson(url)

user = auth.mongodb_user
password = auth.mongodb_password
host = auth.mongodb_host
port = auth.mongodb_port
uri = f"mongodb://{user}:{password}@{host}:{port}"

@st.experimental_singleton
def init_connection():
    return MongoClient(uri)

try:
    client = init_connection()
    print("Connection OK")
except:
    print("Connection error")

@st.experimental_memo(ttl=1)
def get_data():
    db = client['electricity_prod']
    items = db['streaming_data'].find()
    items = list(items)
    return items


st.title("Tableau de bord de la consommation et de production d'électricité en France en temps réel")
st.sidebar.title("Analyses par type de production")
option = st.sidebar.selectbox("Choississez une page.", ('Accueil', 'General', 'Consommation', 'Production totale'))

if option == "Accueil":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image("images/logo-odre.svg", width=75)
    with col3:
        st.write(' ')
    st.header("Bienvenue sur cet outil qui vous permet de consulter les consommations et productions d'électricité région par région en France en temps réel.\
               Sélectionnez une analyse sur le menu de gauche pour continuer.")
    st.image("images/power-lines.jpg")
    st.write("Réalisé par Cécile Guillot - Données provenant de l'API Open Data Réseaux électriques")

placeholder = st.empty()
    
while True:
    items = get_data()
    
    with placeholder.container():
        df = pd.DataFrame(items)

        if option == "General":
            counts = len(df.index)
            st.write(df)

        if option == "Consommation":
            counts = len(df.index)
            st.header("Informations concernant la consommation d'énergie en temps réel")
            fig = choropleth_map(df, region_geojson, mean(df.consommation))
            st.write(fig)
        
        if option == "Production totale":
            counts = len(df.index)
            st.header("Informations concernant la production d'énergie en temps réel")
            fig = choropleth_map(df, region_geojson, mean(df.production))
            st.write(fig)

        time.sleep(900)