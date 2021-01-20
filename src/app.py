import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
alt.data_transformers.disable_max_rows()


# Read in data
wine_df = pd.read_csv("./data/processed/wine.csv")

countries = wine_df["country"].dropna().unique()
country_list = list(countries)

# Setup app and layout/frontend
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    html.H1('Wine Valley'),

    #The first row
    dbc.Row([
        #add search criteria
        dbc.Col([
            dcc.Dropdown(
                id='country-widget',
                options=[{'label': country, 'value': country} for country in country_list],
                value='US')
        ], md=4),
        #add search results
        dbc.Col([
            html.Iframe(
                id='search-result',
                srcDoc=alt.Chart(wine_df).mark_bar().encode(
                    x = 'country',
                    y = 'price'
                ).to_html()
            )
        ])
    ]),

    #The second row
    dbc.Row([
        #add geometry map
        dbc.Col([
            html.Iframe(
                id='map-result',
                srcDoc=alt.Chart(wine_df).mark_bar().encode(
                    x = 'country',
                    y = 'price'
                ).to_html()
            )
        ], md=4),
        #add statistic results
        dbc.Col([
            html.Iframe(
                id='scatter',
                #srcDoc=plot_altair(),
                style={'border-width': '0', 'width': '100%', 'height': '400px'})            
        ])
    ])
])

# Set up callbacks/backend
@app.callback(
    Output('scatter', 'srcDoc'),
    Input('country-widget', 'value'))
def plot_altair(country=None):
    wine_country = pd.DataFrame()
    if country:
        wine_country = wine_df[wine_df['country'] == country]
    else:
       wine_country = wine_df 
    chart = alt.Chart(wine_country, title="Wine Price vs Points").mark_point().encode(
        alt.X('points', scale=alt.Scale(domain=(75, 105))),
        alt.Y('price'),
        tooltip=['title','points', 'price','variety']).interactive()
    return chart.to_html()

if __name__ == '__main__':
   app.run_server(debug=True)