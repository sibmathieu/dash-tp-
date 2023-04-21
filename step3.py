import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dependencies

# Create a dataframe with RATP Data
df_ratp = pd.read_csv("trafic-annuel-entrant-par-station-du-reseau-ferre-2021.csv", sep=";")
sort_ratp = df_ratp.sort_values(by=['Trafic'], ascending=False)
top_bar = sort_ratp.groupby('Réseau').head(5)
top_pie = df_ratp.head(20)

# Create a dataframe with IDF Data
df_idf = pd.read_csv("emplacement-des-gares-idf.csv", sep=";")
exploit_counts = df_idf.groupby('exploitant')['nom'].count().reset_index()
stations_counts = df_idf.groupby('ligne')['nom'].count().reset_index()

app = Dash(__name__)
app.layout = (html.Div(children=[
    html.H1("Data visualization with Plotly Dash", style={'text-align': 'center', 'text-decoration':'underline'}),
    dcc.Dropdown(
        id='reseau-filter',
        options=[{'label': category, 'value': category} for category in sort_ratp['Réseau'].unique()],
        value=None,
        placeholder='Select a category'),

    dcc.Graph(
        id='bar-chart1',
        figure=px.bar(top_bar, x='Réseau', y='Trafic', color='Station'),
        style={'width': '48%', 'align': 'right', 'display': 'inline-block'},
    ),
     html.Div(children=[
        html.H1("Graphs for IDF dataset"),
        dcc.Dropdown(
            id='exploit-filter',
            options=[{'label': category, 'value': category} for category in df_idf['exploitant'].unique()],
            value=None,
            placeholder='Select a category'),
        dcc.Graph(
            id='bar-chart2',
            figure=px.bar(exploit_counts, x='exploitant', y='nom',
                          title='Number of Stations per Exploitant',
                          labels={'exploitant': 'Exploitant', 'nom': 'Number of stations'}),
        ),])
]))

# Define callback for updating the bar chart based on the category filter
@app.callback(
    dependencies.Output('bar-chart1', 'figure'),
    dependencies.Input('reseau-filter', 'value')
)
def update_bar_chart1(category):
    if category is None:
        # Keep all categories if no value has been selected
        filtered_df = top_bar
    else:
        # Filter the df based on selection
        filtered_df = top_bar[top_bar['Réseau'] == category]

    return px.bar(filtered_df, x='Station', y='Trafic')


@app.callback(
    dependencies.Output('bar-chart2', 'figure'),
    dependencies.Input('exploit-filter', 'value')
)
def update_bar_chart2(category):
    if category is None:
        # Keep all categories if no value has been selected
        filtered_df = exploit_counts
    else:
        # Filter the df based on selection
        filtered_df = exploit_counts[exploit_counts['exploitant'] == category]

    return px.bar(filtered_df, x='exploitant', y='nom')


if __name__ == '__main__':
    app.run_server(debug=True)
