import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

# Chargement des données
df = pd.read_csv('C:/Users/Sibylle Mathieu/Desktop/ESME/Hands on Data science tools/TP Data Visualization/emplacement-des-gares-idf.csv', sep=';')

# Aggrégation des données
grouped_data = df.groupby('exploitant')['nom_long'].count().reset_index()
grouped_data = grouped_data.rename(columns={'nom_long': 'nombre_stations'})

# Création bar chart Nombre de stations par exploitant
fig = px.bar(grouped_data, x='exploitant', y='nombre_stations', title='Nombre de stations par exploitant',width=800, height=600)

# Aggrégation des données 2
grouped_data = df.groupby('ligne')['nom_long'].count().reset_index()
grouped_data = grouped_data.rename(columns={'nom_long': 'nombre_stations'})

# Création bar chart Nombre de stations par exploitant 2
fig1 = px.bar(grouped_data, x='ligne', y='nombre_stations', title='Nombre de stations par ligne',width=1400, height=600)

# Création de l'application Dash
app = Dash(__name__)

# Définition de la mise en page
app.layout = html.Div(children=[
    html.H1("Dashboard de visualisation de données 2 ", style={'color': 'blue'}),

    html.Div(className='row', style={'display' : 'flex'}, children=[
        html.Div(className='col-md-6', children=[
            html.H2("Nombre de stations par exploitant", style={'color': 'green'}),
            dcc.Graph(id='bar-chart', figure=fig)
        ]),

        html.Div(className='col-md-6', children=[
            html.H2("Nombre de stations par ligne", style={'color': 'red'}),
            dcc.Graph(id='pie-chart', figure=fig1)
        ])
    ])
], style={'width': '100%'})



if __name__ == '__main__':
    app.run_server(debug=True)
