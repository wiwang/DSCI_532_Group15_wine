import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
import numpy as np
from vega_datasets import data
alt.data_transformers.disable_max_rows()


# Read in data
wine_df = pd.read_csv("./data/processed/wine.csv")
wine_df = wine_df.sample(n=10000)
countries = wine_df["country"].dropna().unique()
country_list = list(countries)

country_ids = pd.read_csv('./data/geo/country-ids-revised.csv') 

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

def plot_map(country=None):
    
    wine_countryid = wine_df.merge(country_ids, left_on='country',right_on='name', how='left')
    wine_countryid = wine_countryid.value_counts(['id','country']).reset_index(name='count')
    
    alt.renderers.enable('default')
    world = data.world_110m()
    world_map = alt.topo_feature(data.world_110m.url, 'countries')

    map_click = alt.selection_multi()
    chart = (alt.Chart(world_map, title='Wine Producing Map').mark_geoshape().transform_lookup(
            lookup = 'id',
            from_ = alt.LookupData(wine_countryid, 'id', ['country','count']))
            .encode(color = 'count:Q',
                    opacity=alt.condition(map_click, alt.value(1), alt.value(0.2)),
                    tooltip = ['country:N','count:Q'])
            .add_selection(map_click)
            .project('equalEarth', scale=90))
    return chart.to_html()


#### GENERATING LIST FOR SLIDER TICKS ####
slider_range_price = np.arange(500, 3400, 600).tolist()
slider_range_5 = [5]
slider_range_price = slider_range_5 + slider_range_price
slider_range_price2 = []
for digit in slider_range_price:
    slider_range_price2.append(str(digit))
slider_range_price_dic = {} 
slider_range_price_dic = {slider_range_price[i]: slider_range_price2[i] for i in range(len(slider_range_price))}
#### END ####


# Setup app and layout/frontend
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.layout = dbc.Container([
    html.H1('Wine Valley'),

    #The first row
    dbc.Row([
        #add search criteria
        dbc.Col([
            'Country',
            dcc.Dropdown(
                id='country-widget',
                options=[{'label': country, 'value': country} for country in country_list],
                value='US'),
            'Variety',
            dcc.Dropdown(
                options=[{'label': i, 'value': i} for i in wine_df["variety"].dropna().unique()],
                value='SF', multi=True),
            'Wine Enthusiast Score',
            dcc.RangeSlider(
                min=80, max=100, value=[80, 100], marks={80: '80', 85: '85', 90: '90', 95: '95', 100: '100'}),
            'Price',
            dcc.RangeSlider(
                id = "xslider", min=4, max=3300, value=[4, 3300], marks=slider_range_price_dic),
            'Year',
            dcc.RangeSlider(
                min=1990, max=2017, value=[1990, 2017],
                marks={1990: '1990',1995: '1995', 2000: '2000', 2005: '2005', 2010: '2010', 2015: '2015', 2017: '2017'}),
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
                id ='map',
                srcDoc=plot_map(),
                style={'border-width': '0', 'width': '100%', 'height': '400px'}
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
