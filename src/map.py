import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
from vega_datasets import data
alt.data_transformers.disable_max_rows()


# Read in data
#wine_df = pd.read_csv("C:\Users\lihua\MDS\4_532_data_visualization-2\DSCI_532_Group15_wine\data\processed\wine.csv")
wine_df = pd.read_csv("../data/processed/wine.csv")
# print(wine_df)
country_ids = pd.read_csv('../data/geo/country-ids.csv') 

countries = wine_df["country"].dropna().unique()
country_list = list(countries)


# Setup app and layout/frontend
app = dash.Dash(__name__,  external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.layout = html.Div([
        html.Iframe(
            id='scatter',
            #srcDoc=plot_altair(),
            style={'border-width': '0', 'width': '100%', 'height': '400px'}),
        dcc.Dropdown(
            id='country-widget',
            options=[{'label': country, 'value': country} for country in country_list],
            value='US')  ])




# Set up callbacks/backend
@app.callback(
    Output('scatter', 'srcDoc'),
    Input('country-widget', 'value'))
def plot_map(country=None):
    #wine_country = pd.DataFrame()
    #if country:
    #    wine_country = wine_df[wine_df['country'] == country]
    #else:
    #   wine_country = wine_df 
    
    wine_countryid = wine_df.merge(country_ids, left_on='country',right_on='name', how='left')
    wine_countryid = wine_countryid.value_counts(['id']).reset_index(name='wine_count')
    
    alt.renderers.enable('default')
    world = data.world_110m()
    world_map = alt.topo_feature(data.world_110m.url, 'countries')

    chart = (alt.Chart(world_map).mark_geoshape().transform_lookup(
            lookup = 'id',
            from_ = alt.LookupData(wine_countryid, 'id', ['wine_count']))
            .encode(color = 'wine_count:Q')
            .project('equalEarth', scale=90))
    return chart.to_html()

if __name__ == '__main__':
   app.run_server(debug=True)