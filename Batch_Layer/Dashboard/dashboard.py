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

@st.experimental_singleton
def init_connection():
    return create_engine(f'postgresql://{user}:{password}@localhost:5432/energy_consumption')

try:
    conn = init_connection()
    print('Connection OK')
except (Exception, Error) as error:
    print('Error while connecting to PostgreSQL', error)

sql_query = "SELECT libelle_region, AVG(consommation)\
             FROM consumption\
             INNER JOIN region ON consumption.code_insee_region = region.code_insee_region\
             GROUP BY libelle_region;"
avg_consumption = pd.read_sql_query(sql_query, conn)

st.header('Tableau de bord de la consommation d\'électricité en France')
st.text(time.strftime("%d-%m-%Y %H:%M"))
fig = px.histogram(avg_consumption, x="libelle_region", y="avg")
st.write(fig)
st.write(avg_consumption)

