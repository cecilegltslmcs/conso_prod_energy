import packages.authentification as auth
import pandas as pd
from pymongo import MongoClient
import streamlit as st
import time

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
    print('Connection OK')
except:
    print('Connection error')

# Pull data from the collection
@st.experimental_memo(ttl=1)
def get_data():
    db = client['electricity_prod']
    items = db['streaming_data'].find()
    items = list(items)
    return items

st.title("Tableau de bord de la consommation et de production d'électricité en France en temps réel")
st.sidebar.title("Analyses par type de production")
option = st.sidebar.selectbox("Choississez une page.", ('Accueil', 'Consommation moyenne'))

if option == "Accueil":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image("images/logo-odre.svg", width=75)
    with col3:
        st.write(' ')
    st.header("Bienvenue sur cet outil qui vous permet de consulter l'historique des consommations et production d'électricité région par région en France en temps réel.\
               Sélectionnez une analyse sur le menu de gauche pour continuer.")
    st.image("images/power-lines.jpg")
    st.write("Réalisé par Cécile Guillot - Données provenant de l'API Open Data Réseaux électriques")

placeholder = st.empty()
    
while True:
    items = get_data()
    
    with placeholder.container():
        df = pd.DataFrame(items)

        if option == "Consommation moyenne":
            counts = len(df.index)
            st.header("Informations concernant la consommation d'énergie")
            st.write("Nombre d'enregistrements:", counts)
            st.dataframe(df)

        time.sleep(1)