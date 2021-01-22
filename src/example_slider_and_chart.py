import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc 
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
import numpy as np

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

def plot_altair(xrange): # xrange is a list that stores min (xrange[0]) and max (xrange[1])
    chart = alt.Chart( wine_df[wine_df['price'].between(xrange[0], xrange[1], inclusive=True )]).mark_point().encode(
        x='price',
        y='points')
    return chart.to_html()

# Setup app and layout/frontend
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
        html.Iframe(
            id='price',
            srcDoc=plot_altair(xrange=[4, 3300]),
            style={'border-width': '0', 'width': '100%', 'height': '400px'}),
        dcc.RangeSlider(id = "price_slider", min=4, max=3300,
        value=[4, 3300], marks=slider_range_price_dic)])

# Set up callbacks/backend
@app.callback(
    Output('price', 'srcDoc'),
    Input('price_slider', 'value'))
def update_output(xrange):
    return plot_altair(xrange)

if __name__ == '__main__':
   app.run_server(debug=True)