import authentification as auth
import pandas as pd
import plotly.express as px
import requests
from sqlalchemy import create_engine
import streamlit as st
from module_dashboard_drawing import *

user = auth.user
password = auth.password

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
