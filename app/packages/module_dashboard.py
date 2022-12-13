import plotly.express as px
import requests

def loading_geojson(url):
    try:
        response = requests.get(url)
        response = response.json()
    except:
        print("Wrong URL")
    return response

def choropleth_map(dataset, geojson, color):
    fig = px.choropleth_mapbox(dataset, geojson=geojson,
                               featureidkey="properties.reg",
                               locations='code_insee_region',
                               color=color,
                               color_continuous_scale="rdylbu_r",
                               mapbox_style="carto-positron",
                               zoom=4, center = {"lat": 46.2276, "lon": 2.21},
                               opacity=0.6)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

