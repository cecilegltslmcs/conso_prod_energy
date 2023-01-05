import requests
import plotly.express as px

def loading_geojson(url):
    try:
        response = requests.get(url)
        response = response.json()
    except:
        print("Wrong URL")
    return response

def choropleth_map(dataset, geojson, column):
    fig = px.choropleth_mapbox(dataset, 
                               geojson = geojson,
                               featureidkey="properties.reg",
                               locations='code_insee_region',
                               color = column,
                               color_continuous_scale="rdylbu_r",
                               mapbox_style="carto-positron",
                               zoom=4, center = {"lat": 46.2276, "lon": 2.21},
                               opacity=0.6)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

def stack_chart(df):
    fig = px.bar(df, x = "libelle_region", y=["pct_thermique", "pct_nucleaire",
                                              "pct_eolien", "pct_solaire",
                                              "pct_pompage", "pct_bioenergies"])
    return fig
