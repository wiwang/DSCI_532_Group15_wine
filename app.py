import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
alt.data_transformers.disable_max_rows()


# Read in data
#wine_df = pd.read_csv("C:/Users/lihua/MDS/4_532_data_visualization-2/DSCI_532_Group15_wine/data/winemag-data-130k-v2.csv",index_col=0)
wine_df = pd.read_csv("./data/winemag-data-130k-v2.csv",index_col=0)
#print(wine_df)
countries = wine_df.country.dropna().unique()
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