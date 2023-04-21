import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dependencies

# Chargement des données
df1 = pd.read_csv('trafic-annuel-entrant-par-station-du-reseau-ferre-2021.csv', sep=';')
df2 = pd.read_csv('emplacement-des-gares-idf.csv', sep=';')
df2[['lat', 'lng']] = df2['Geo_Point'].str.split(',', expand=True)
df2['lat'] = df2['lat'].str.strip().astype(float)
df2['lng'] = df2['lng'].str.strip().astype(float)


# Aggrégation des données 1
sort_ratp = df1.sort_values(by=['Trafic'], ascending=False).head(10)
#grouped_data1 = df1.groupby('Station')['Trafic'].sum().reset_index()
#top10 = grouped_data1.sort_values(by=['Trafic'], ascending=False).head(10)
# Création bar chart TOP 10 trafic en fonction des stations
fig1 = px.bar(sort_ratp, x='Station', y='Trafic', title='Top 10 Station with Biggest Trafic',width=1200, height=600)

# Aggrégation des données 2
grouped_data2 = df1.groupby('Ville')['Trafic'].sum().reset_index()
top5 = grouped_data2.sort_values('Trafic', ascending=False).head(5)

# Création bar chart  TOP 5 trafic par ville
fig2 = px.pie(top5, values='Trafic', names='Ville', title='Top 5 Cities with Biggest Trafic',width=1000, height=600)

# Aggrégation des données 3
grouped_data3 = df2.groupby('exploitant')['nom_long'].count().reset_index()
grouped_data3= grouped_data3.rename(columns={'nom_long': 'nombre_stations'})

# Création bar chart Nombre de stations par exploitant
fig3 = px.bar(grouped_data3, x='exploitant', y='nombre_stations', title='Nombre de stations par exploitant',width=800, height=600)

# Aggrégation des données 4
grouped_data4 = df2.groupby('ligne')['nom_long'].count().reset_index()
grouped_data4 = grouped_data4.rename(columns={'nom_long': 'nombre_stations'})

# Création bar chart Nombre de stations par exploitant 2
fig4 = px.bar(grouped_data4, x='ligne', y='nombre_stations', title='Nombre de stations par ligne',width=1400, height=600)

# Ajout de la carte avec les positions des stations
fig5 = px.scatter_mapbox(df2, lat="lat", lon="lng", hover_name="nom_long", hover_data=["Geo_Point", "exploitant"],
                            color_discrete_sequence=["fuchsia"], zoom=9, height=600)
fig5.update_layout(mapbox_style="open-street-map")
fig5.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

#Création d'un filtre
top10_réseau = sort_ratp.groupby('Réseau').head(10)
fig6 = px.bar(top10_réseau, x='Réseau', y='Trafic',title='Top 10 stations with biggest trafic and the filtre "Réseau" ', color='Station',width=800, height=600)

grouped_data5 = df2.groupby('exploitant')['nom_long'].count().reset_index()
fig7 = px.bar(grouped_data5, x='exploitant', y='nom_long',title='Number of station per exploitant with the filtre "Réseau" ',width=1000, height=600, labels={'exploitant': 'Exploitant', 'nom_long': 'nombre_de_stations'})

# Création de l'application Dash
app = Dash(__name__)

# Définition de la mise en page
app.layout = html.Div(children=[
    html.H1("Dashboard de visualisation de données", style={'color': 'blue'}),

    html.Div(className='row', style={'display': 'flex'}, children=[
        html.Div(className='col-md-6', children=[
            html.H2("Top 10 stations avec le plus grand trafic", style={'color': 'green'}),
            dcc.Graph(id='bar-chart-1', figure=fig1)
        ]),

        html.Div(className='col-md-6', children=[
            html.H2("Top 5 villes avec le plus grand trafic", style={'color': 'red'}),
            dcc.Graph(id='pie-chart-1', figure=fig2)
        ])
    ]),

    html.Div(className='row', style={'display': 'flex'}, children=[
        html.Div(className='col-md-6', children=[
            html.H2("Nombre de stations par exploitant", style={'color': 'green'}),
            dcc.Graph(id='bar-chart-2', figure=fig3)
        ]),

        html.Div(className='col-md-6', children=[
            html.H2("Nombre de stations par ligne", style={'color': 'red'}),
            dcc.Graph(id='pie-chart-2', figure=fig4)
        ])
    ]),

    html.Div(children=[
        html.H2("Position des stations sur une carte", style={'color': 'red'}),
        dcc.Graph(id='map-chart', figure=fig5)
    ]),

    html.Div(className='row', style={'display': 'flex'}, children=[
        html.Div(className='col-md-6', children=[
            html.H2("Top 10 stations avec le plus grand trafic avec un filtre réseau", style={'color': 'green'}),
            dcc.Dropdown(
                id='reseau-filter',
                options=[{'label': category, 'value': category} for category in sort_ratp['Réseau'].unique()],
                value=None,
                placeholder='Select a category'
            ),
            dcc.Graph(id='bar-chart_3', figure=fig6)
        ]),
        html.Div(className='col-md-6', children=[
            html.H2("Nombre de lignes par exploitant avec filtre", style={'color': 'green'}),
            dcc.Dropdown(
                id='exploit-filter',
                options=[{'label': category, 'value': category} for category in df2['exploitant'].unique()],
                value=None,
                placeholder='Select a category'
            ),
            dcc.Graph(id='bar-chart4', figure=fig7)
        ])
    ])
])

# Définition du callback

@app.callback(
    dependencies.Output('bar-chart_3', 'figure'),
    dependencies.Input('reseau-filter', 'value')
)
def update_bar_chart1(category):
    if category is None:
        # Keep all categories if no value has been selected
        filtered_df = top10_réseau
    else:
        # Filter the df based on selection
        filtered_df = top10_réseau[top10_réseau['Réseau'] == category]

    return px.bar(filtered_df, x='Station', y='Trafic')

@app.callback(
    dependencies.Output('bar-chart4', 'figure'),
    dependencies.Input('exploit-filter', 'value')
)
def update_bar_chart2(category):
    if category is None:
        # Keep all categories if no value has been selected
        filtered_df = grouped_data5
    else:
        # Filter the df based on selection
        filtered_df = grouped_data5[grouped_data5['exploitant'] == category]

    return px.bar(filtered_df, x='exploitant', y='nom_long')


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)

