import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
#from vega_datasets import data


# Read in data
wine_1 = pd.read_csv("C:/Users/lihua/MDS/4_532_data_visualization-2/DSCI_532_Group15_wine/data/winemag-data_first150k.csv",index_col=0)
wine_2 = pd.read_csv("C:/Users/lihua/MDS/4_532_data_visualization-2/DSCI_532_Group15_wine/data/winemag-data-130k-v2.csv",index_col=0)
#wine_1 = pd.read_csv("./data/winemag-data_first150k.csv",index_col=0)
#wine_2 = pd.read_csv("./data/winemag-data-130k-v2.csv",index_col=0)
wine_2 = wine_2.drop(columns=['taster_name', 'taster_twitter_handle','title'], axis=1)

wine_df = pd.concat([wine_1,wine_2], ignore_index = True)
#print(wine_df)

def plot_altair():
    chart = alt.Chart(wine_df).mark_point().encode(
        x='country',
        y='point')
    return chart.to_html()

app.layout = html.Div([
        html.Iframe(
            srcDoc=plot_altair(),
            style={'border-width': '0', 'width': '100%', 'height': '400px'})])


# Setup app and layout/frontend
# app = dash.Dash(__name__,  external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
# app.layout = html.Div([
#     html.Iframe(
#         id='scatter',
#         style={'border-width': '0', 'width': '100%', 'height': '400px'}),
#     dcc.Dropdown(
#         id='xcol-widget',
#         value='Horsepower',  # REQUIRED to show the plot on the first page load
#         options=[{'label': col, 'value': col} for col in cars.columns])])

# # Set up callbacks/backend
# @app.callback(
#     Output('scatter', 'srcDoc'),
#     Input('xcol-widget', 'value'))
# def plot_altair(xcol):
#     chart = alt.Chart(cars).mark_point().encode(
#         x=xcol,
#         y='Displacement',
#         tooltip='Horsepower').interactive()
#     return chart.to_html()

if __name__ == '__main__':
   app.run_server(debug=True)