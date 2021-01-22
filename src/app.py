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

wine_df = pd.read_csv("data/processed/wine.csv")

wine_df = wine_df.sample(n=10000)
countries = wine_df["country"].dropna().unique()
country_list = list(countries)

country_ids = pd.read_csv('data/geo/country-ids-revised.csv') 


def plot_scatter(xrange, country=None):
    wine_country = pd.DataFrame()
    if country:
        wine_country = wine_df[wine_df['country'] == country]
    else:
       wine_country = wine_df

    chart_1 = alt.Chart(wine_df, title='Rating by Price').mark_point().encode(
        x=alt.X('price', title="Price", scale=alt.Scale(zero=False)),
        y=alt.Y('points', title="Score", scale=alt.Scale(zero=False)),
        color='country',
        tooltip=['title','points', 'price','variety']).interactive()

    chart = chart_1

    return chart.to_html()

bar_click = alt.selection_multi(fields=['country'])

def plot_altair(xrange, country=None): # xrange is a list that stores min (xrange[0]) and max (xrange[1])

    wine_country = pd.DataFrame()
    if country:
        wine_country = wine_df[wine_df['country'] == country]
    else:
       wine_country = wine_df

    chart_2 = alt.Chart(wine_df.nlargest(15, 'points'), title="Average Rating of Top 15 Best Rated Wine").mark_bar().encode(
        x=alt.X('mean(points)', title="Rating Score"),
        y=alt.Y('variety', title="Variety", scale=alt.Scale(zero=False), sort='-x'),
        color='country:N',
        #column=alt.Column('country:N'), 
        tooltip=['mean(points)']).interactive()
    
    chart_3 = alt.Chart(wine_df.nlargest(15, 'points'), title="Average Price of Top 15 Best Rated Wine").mark_bar().encode(
        x=alt.X('mean(price)', title="Price", sort='-y', stack=None),
        y=alt.Y('variety', title=" ", scale=alt.Scale(zero=False), sort='-x'),
        color='country:N', 
        row='variety:N',
        tooltip=['mean(price)']).add_selection(bar_click)

    chart = (chart_2 | chart_3)
    
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
app.layout = dbc.Container([
    html.H1('Wine Valley'),

    #The first row
    dbc.Row([
        #add search criteria
        dbc.Col([
            'Country',
            dcc.Dropdown(
                id='country_widget',
                options=[{'label': country, 'value': country} for country in country_list],
                value='US',
                multi=True
            ),
        # 'Variety',
        #     dcc.Dropdown(
        #         id='variety_widget',
        #         options=[{'label': i, 'value': i} for i in wine_df["variety"].dropna().unique()],
        #         value='SF',
        #         multi=True
        #     ),
        'Price',
            dcc.RangeSlider(
                id = "price_slider",
                min=4, max=3300, value=[4, 3300],
                marks=slider_range_price_dic
            ),
        'Wine Enthusiast Score',
            dcc.RangeSlider(
                id = 'score_slider',
                min=80, max=100, value=[80, 100],
                marks={80: '80', 85: '85', 90: '90', 95: '95', 100: '100'}
            ),
        'Year',
            dcc.RangeSlider(
                id = 'year_slider',
                min=1990, max=2017, value=[1990, 2017],
                marks={1990: '1990',1995: '1995', 2000: '2000', 2005: '2005', 2010: '2010', 2015: '2015', 2017: '2017'}
            ),
        ], md=4),
        #add search results
        dbc.Col([
            html.Iframe(
                srcDoc=plot_scatter(xrange=[4, 3300]),
                style={'border-width': '0', 'width': '100%', 'height': '400px'})
        ])
    ]),

    #The second row
    dbc.Row([
        #add geometry map
        dbc.Col([
            html.Iframe(
                id ='map',
                #srcDoc=plot_map(),
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

# Set up callbacks/backend
@app.callback(
    Output('map', 'srcDoc'),
    Input('price_slider', 'value'),
    Input('year_slider', 'value'),
    Input('score_slider', 'value'))
def plot_map(price_range = [4,3300], year_range = [1900, 2017], points_range = [80, 90]):
    wine = wine_df
    # filter by price
    wine = wine[(wine['price'] >= price_range[0]) & (wine_df['price'] <= price_range[1]) &
    (wine['year'] >= year_range[0]) & (wine_df['price'] <= year_range[1]) &
    (wine['points'] >= points_range[0]) & (wine_df['points'] <= points_range[1])]


    wine_countryid = wine.merge(country_ids, left_on='country',right_on='name', how='left')
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


if __name__ == '__main__':
   app.run_server(debug=True)
