import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

# Chargement des données
df = pd.read_csv('emplacement-des-gares-idf.csv', sep=';')

df[['lat', 'lng']] = df['Geo_Point'].str.split(',', expand=True)
df['lat'] = df['lat'].str.strip().astype(float)
df['lng'] = df['lng'].str.strip().astype(float)

# Ajout de la carte avec les positions des stations
fig_map = px.scatter_mapbox(df, lat="lat", lon="lng", hover_name="nom_long", hover_data=["Geo_Point", "exploitant"],
                            color_discrete_sequence=["fuchsia"], zoom=9, height=600)
fig_map.update_layout(mapbox_style="open-street-map")
fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Création de l'application Dash
app = Dash(__name__)

# Définition de la mise en page
app.layout = html.Div(children=[
    html.H1("Dashboard de visualisation de données 4", style={'color': 'blue'}),
    
    html.Div(children=[
        html.H2("Position des stations sur une carte", style={'color': 'red'}),
        dcc.Graph(id='map-chart', figure=fig_map)
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
