import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc #add
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
import numpy as np #add

alt.data_transformers.disable_max_rows()


# Read in data
wine_df = pd.read_csv("../data/processed/wine.csv")
countries = wine_df["country"].dropna().unique()
country_list = list(countries)

#### GENERATING LIST FOR SLIDER TICKS ####
slider_range_price = np.arange(100, 3400, 400).tolist()
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

app.layout = html.Div([
        'Price',
        dcc.RangeSlider(id = "xslider", min=4, max=3300,
        value=[4, 3300], marks=slider_range_price_dic),
        'Wine Enthusiast Score',
        dcc.RangeSlider(min=80, max=100, value=[80, 100], marks={80: '80',
        85: '85', 90: '90', 95: '95', 100: '100'}),
        'Year',
        dcc.RangeSlider(min=1990, max=2017, value=[1990, 2017], marks={1990: '1990',
        1995: '1995', 2000: '2000', 2005: '2005', 2010: '2010', 2015: '2015', 2017: '2017'}),
        'Country',
        dcc.Dropdown(
            options=[{'label': i, 'value': i} for i in country_list],
            value='SF', multi=True),
        'Variety',
        dcc.Dropdown(
        options=[{'label': i, 'value': i} for i in wine_df["variety"].dropna().unique()],
        value='SF', multi=True)
        
        ])


if __name__ == '__main__':
   app.run_server(debug=True)