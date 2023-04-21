import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

# Chargement des données
df = pd.read_csv('C:/Users/Sibylle Mathieu/Desktop/ESME/Hands on Data science tools/TP Data Visualization/trafic-annuel-entrant-par-station-du-reseau-ferre-2021.csv', sep=';')

# Aggrégation des données
grouped_data = df.groupby('Station')['Trafic'].sum().reset_index()
top10 = grouped_data.sort_values('Trafic', ascending=False).head(10)

# Création bar chart TOP 10 trafic en fonction des stations
fig= px.bar(top10, x='Station', y='Trafic', title='Top 10 Station with Biggest Trafic',width=1200, height=600)

# Aggrégation des données
grouped_data2 = df.groupby('Ville')['Trafic'].sum().reset_index()
top5 = grouped_data2.sort_values('Trafic', ascending=False).head(5)

# Création bar chart  TOP 5 trafic par ville
fig2 = px.pie(top5, values='Trafic', names='Ville', title='Top 5 Cities with Biggest Trafic',width=1000, height=600)

# Création de l'application Dash
app = Dash(__name__)

# Définition de la mise en page
app.layout = html.Div(children=[
    html.H1("Dashboard de visualisation de données", style={'color': 'blue'}),

    html.Div(className='row', style={'display' : 'flex'}, children=[
        html.Div(className='col-md-6', children=[
            html.H2("Top 10 stations avec le plus grand trafic", style={'color': 'green'}),
            dcc.Graph(id='bar-chart', figure=fig)
        ]),

        html.Div(className='col-md-6', children=[
            html.H2("Top 5 villes avec le plus grand trafic", style={'color': 'red'}),
            dcc.Graph(id='pie-chart', figure=fig2)
        ])
    ])
], style={'width': '100%'})

if __name__ == '__main__':
    app.run_server(debug=True)
