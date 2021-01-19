import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
alt.data_transformers.disable_max_rows()


# Read in data
#wine_df = pd.read_csv("C:\Users\lihua\MDS\4_532_data_visualization-2\DSCI_532_Group15_wine\data\processed\wine.csv")
wine_df = pd.read_csv("../data/processed/wine.csv")
print(wine_df)

countries = wine_df["country"].dropna().unique()
country_list = list(countries)


# Setup app and layout/frontend
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    html.H1('My mudplank'),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='xcol-widget',
                value='Horsepower',  # REQUIRED to show the plot on the first page load
                options=[{'label': col, 'value': col} for col in cars.columns]),
            dcc.Dropdown(
                id='ycol-widget',
                value='Displacement',  # REQUIRED to show the plot on the first page load
                options=[{'label': col, 'value': col} for col in cars.columns])],
            md=4),
        dbc.Col([
            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5('Key value')),
                        color='warning')),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(html.H5('Key value')),
                        color='info', inverse=True, style={'text-align': 'center'}))]),
            html.Iframe(
                id='scatter',
                style={'border-width': '0', 'width': '100vw', 'height': '100vh'})])])])

# Setup app and layout/frontend
# app = dash.Dash(__name__,  external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
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