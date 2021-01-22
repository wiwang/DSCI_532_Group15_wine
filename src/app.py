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
#wine_df = wine_df.sample(n=1000)
countries = wine_df["country"].dropna().unique()
country_list = list(countries)

def plot_altair(xrange, country=None): # xrange is a list that stores min (xrange[0]) and max (xrange[1])
    wine_country = pd.DataFrame()
    if country:
        wine_country = wine_df[wine_df['country'] == country]
    else:
       wine_country = wine_df

    chart_1 = alt.Chart(wine_df, title='Rating by Price').mark_point().encode(
        x=alt.X('price', title="Price"),
        y=alt.Y('points', title="Score"),
        tooltip=['title','points', 'price','variety']).interactive()

    chart_2 = alt.Chart(wine_df, title="Average Wine Rating by Country").mark_bar().encode(
        x=alt.X('mean(points)', title="Average Rating"),
        y=alt.Y('variety', title="Variety", scale=alt.Scale(zero=False), sort='-x'),
        color='country:N',
        #column=alt.Column('country:N'), 
        tooltip=['mean(points)']).interactive()
    
    chart_3 = alt.Chart(wine_df, title="Average Wine Prices by Country").mark_bar().encode(
        x=alt.X('mean(price)', title="Price", sort='-y'),
        y=alt.Y('variety', scale=alt.Scale(zero=False), sort='-x'),
        color='country', 
        tooltip=['mean(price)']).interactive()

    chart = chart_1 & (chart_2 | chart_3)
    
    return chart.to_html()

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
                srcDoc=plot_altair(xrange=[4, 3300]),
                style={'border-width': '0', 'width': '100%', 'height': '400px'}),           
        ], md=8)
    ])
])



if __name__ == '__main__':
   app.run_server(debug=True)