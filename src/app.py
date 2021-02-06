import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
import numpy as np
import re
from vega_datasets import data
alt.data_transformers.disable_max_rows()


# Read in data

wine_df = pd.read_csv("data/processed/wine.csv")

wine_df = wine_df.sample(n=10000)

wine_df = wine_df[wine_df['country'].notna()]
wine_df = wine_df[wine_df['year'].notna()]

def shorten_title(text):
    #match = re.search(r'\d{4}', text) 
    shorter_name = re.split(r'\s+(?=\d)|(?<=\d)\s+', text)[0]
    if shorter_name:
        return shorter_name
    else:
        return text

wine_df['title_short'] = wine_df['title'].apply(shorten_title)

countries = wine_df["country"].dropna().unique() # 
country_list = list(countries)

varieties = wine_df["variety"].dropna().unique()
variety_list = list(varieties)

country_ids = pd.read_csv('data/geo/country-ids-revised.csv') 




#### GENERATING LIST FOR SLIDER TICKS ####
slider_range_price = np.arange(300, 1501, 300).tolist()
slider_range_5 = [5]
slider_range_price = slider_range_5 + slider_range_price
slider_range_price2 = []
for digit in slider_range_price:
    slider_range_price2.append('$' + str(digit))
slider_range_price_dic = {} 
slider_range_price_dic = {slider_range_price[i]: slider_range_price2[i] for i in range(len(slider_range_price))}
#### END ####

table_cols = ["variety", "winery", "country", "price", "points", "year"]
results_table_cols = ["Detailed Information"]

results_table_temp = pd.DataFrame(np.array([
        ["No wine selected. Click on a row in the table to the left to see detailed information about a selection."],
                                ]),
                    columns=['Detailed Information'])


# Setup app and layout/frontend
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.layout = dbc.Container([

    html.H1('Wine Valley',
                    style={
                        'backgroundColor': '#c50017',
                        'padding': 10,
                        'color': 'white',
                        'margin-top': 20,
                        'margin-bottom': 30,
                        'text-align': 'center',
                        'font-size': '48px',
                        'border-radius': 3,
                        'font-family': 'cursive'}),


    #The first row
    dbc.Row([
        #add search criteria
        dbc.Col([
            'Country',
            dcc.Dropdown(
                className='country_dropdown_class',
                id='country_widget',
                options=[{'label': country, 'value': country} for country in country_list],
                multi=True
            ),
        'Variety',
            dcc.Dropdown(
                className='variety_dropdown_class',
                id='variety_widget',
                options=[{'label': variety, 'value': variety} for variety in variety_list],
                multi=True
            ),
        'Price (USD)',
            dcc.RangeSlider(
                className='price_slider_class',
                id = "price_slider",
                min=4, max=1500, value=[4, 1500],
                marks=slider_range_price_dic
            ),
        'Wine Enthusiast Score (80-100 points)',
            dcc.RangeSlider(
                className='score_slider_class',
                id = 'score_slider',
                min=80, max=100, value=[80, 100],
                marks={80: '80', 85: '85', 90: '90', 95: '95', 100: '100'}
            ),
        'Vintage',
            dcc.RangeSlider(
                className='year_slider_class',
                id = 'year_slider',
                min=1994, max=2017, value=[1994, 2017],
                marks={1994: '1994' ,1998: '1998', 2003: '2003', 2008: '2008', 2013: '2013', 2017: '2017'}
            ),
        ], md=4),
        
        dbc.Col([
            dash_table.DataTable(
                id = "search-table",
                columns=[
                    {"name": i, "id": i, "deletable": False, "selectable": False} for i in table_cols
                ],
                data = wine_df.to_dict('records'),
                editable=False,
                sort_action="native",
                sort_mode="multi",
                column_selectable=False,
                row_selectable="single",
                row_deletable=False,
                filter_action="native",
                selected_columns=[],
                selected_rows=[],
                page_action="native",
                page_current= 0,
                page_size= 10,
                style_data={
                    'width': '20px',
                    'maxWidth': '80px',
                    'minWidth': '5px',
                },
                style_cell={'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'},
                style_data_conditional=[
                    {'if': { "state": "selected"},
                        "backgroundColor": "inherit !important",
                        "border": "inherit !important",}
                    ] + [
                    {'if': {'row_index': 'odd'},
                        'backgroundColor': '#ffeded'
                    }
                ]
            ),
            html.Div(id='datatable-interactivity-container')
        ], md=5),

        dbc.Col([
            dash_table.DataTable(
                id = "results-table",
                style_data={
                    'width': '20px',
                    'maxWidth': '80px',
                    'minWidth': '5px',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
                style_cell_conditional=[
                    {'if': {'column_id': ' '},
                        'width': '1%'}
                    ] + [
                    {'if': { "state": "selected"},
                        "backgroundColor": "inherit !important",
                        "border": "inherit !important",}
                    ] + [
                    {'if': {'row_index': 'odd'},
                        'backgroundColor': '#ffeded'
                    }
                ],
                style_cell={'textAlign': 'left'},
                columns=[
                    {"name": i, "id": i, "deletable": False, "selectable": False} for i in results_table_cols
                ],
                data = results_table_temp.to_dict('records'),
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'}
            ),
            html.Div(id='resultstable-interactivity-container')
        ], md=3)
       
    ]),

    #The second row
    dbc.Row([
        #add geometry map
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Country Produciton Map'),
                dbc.CardBody(
                    html.Iframe(
                        id ='map',
                        #srcDoc=plot_map(),
                        style={'border-width': '0', 'width': '100%', 'height': '400px'}
                )
        )])]),
        #add statistic results

        dbc.Col([
            dcc.Tabs([
                dcc.Tab(label='Rating vs Price Scatterplot', children=[
                    html.Iframe(
                        id = 'plot_altair',
                        style={'border-width': '0', 'width': '100%', 'height': '400px'})
                ]),
                dcc.Tab(label='Top Rated', children=[
                    html.Iframe(
                        id = 'scatter',
                        style={'border-width': '0', 'width': '100%', 'height': '400px'})
                ])

            ])
        ], md=6)

    ]),

    html.Hr(),
    html.P(f'''
    This dashboard was made by Lara Habashy, Huanhuan Li, Matthew Pin, Zhiyong Wang. The data is from https://www.kaggle.com/zynicide/wine-reviews. 
    ''')
], style={'max-width': '80%'})

# Set up callbacks/backend
@app.callback(
    Output('map', 'srcDoc'),
    [Input('country_widget', 'value')],
    [Input('variety_widget', 'value')],
    Input('price_slider', 'value'),
    Input('year_slider', 'value'),
    Input('score_slider', 'value'))
def plot_map(country = None, variety = None, price_range = [4,1500], year_range = [1900, 2017], points_range = [80, 100]):

    wine = wine_df

    if country:
        wine = wine[wine['country'].isin(country)]

    if variety:
        wine = wine[wine['variety'].isin(variety)]

    # filter by price
    wine = wine[(wine['price'] >= price_range[0]) & (wine_df['price'] <= price_range[1]) &
    (wine['year'] >= year_range[0]) & (wine_df['price'] <= year_range[1]) &
    (wine['points'] >= points_range[0]) & (wine_df['points'] <= points_range[1])]


    wine_countryid = wine.merge(country_ids, left_on='country',right_on='name', how='left')
    wine_countryid = wine_countryid.value_counts(['id','country']).reset_index(name='count')
    
    alt.renderers.enable('default')
    world = data.world_110m()
    world_map = alt.topo_feature(data.world_110m.url, 'countries')

    background = (alt.Chart(world_map)
        .mark_geoshape(stroke='black', fill = 'lightgrey', strokeWidth=0.25)
        .project('equalEarth', scale=80)
        .properties(width=425,height=250)
    )

    map_click = alt.selection_multi()
    fill = (alt.Chart(world_map)
            .mark_geoshape(stroke='black', strokeWidth=0.5)
            .transform_lookup(
            lookup = 'id',
            from_ = alt.LookupData(wine_countryid, 'id', ['country','count']))
            .encode(color = alt.Color('count:Q', scale = alt.Scale(scheme = 'goldred')),
                    opacity=alt.condition(map_click, alt.value(1), alt.value(0.2)),
                    tooltip = ['country:N','count:Q'])
            .add_selection(map_click)
            .project('equalEarth', scale=80)
            .properties(width=425,height=250)
            #.configure_legend(orient = 'bottom')
            )
    
    chart = background + fill

    #chart.configure_legend(orient = 'bottom')

    return chart.to_html()

@app.callback(
    Output('plot_altair', 'srcDoc'),
    [Input('country_widget', 'value')],
    [Input('variety_widget', 'value')],
    Input('price_slider', 'value'),
    Input('year_slider', 'value'),
    Input('score_slider', 'value'))
def plot_scatter(country = None, variety = None, price_range = [4, 1500], year_range = [1900, 2017], points_range = [80, 100]):
    
    wine = wine_df

    # filter by price and year
    wine = wine[(wine['price'] >= price_range[0]) & (wine_df['price'] <= price_range[1]) &
                (wine['year'] >= year_range[0]) & (wine_df['year'] <= year_range[1]) ]
    
    if country:
        wine = wine[wine['country'].isin(country)]
    
    if variety:
        wine = wine[wine['variety'].isin(variety)]

    chart_1 = alt.Chart(wine, title='Wine Rating by Price').mark_point().encode(
        x=alt.X('price', title="Price", scale=alt.Scale(zero=False)),
        y=alt.Y('points', title="Score", scale=alt.Scale(zero=False)),
        color= alt.Color('country', scale=alt.Scale(scheme='darkred'), legend=alt.Legend(symbolLimit=18, title="Country")),
        tooltip=['title','points', 'price','variety']).interactive()
        

    chart = chart_1.properties(width=380,height=280)

    return chart.to_html()

@app.callback(
    Output('scatter', 'srcDoc'),
    [Input('country_widget', 'value')],
    [Input('variety_widget', 'value')],
    Input('price_slider', 'value'),
    Input('year_slider', 'value'),
    Input('score_slider', 'value'))
def plot_altair(country = None, variety = None, price_range = [4, 1500], year_range = [1900, 2017], points_range = [80, 100]): # xrange is a list that stores min (xrange[0]) and max (xrange[1])
    
    wine = wine_df
 
    # filter by price and year
    wine = wine[(wine['price'] >= price_range[0]) & (wine_df['price'] <= price_range[1]) &
                (wine['year'] >= year_range[0]) & (wine_df['year'] <= year_range[1]) ]

    if country:
        wine = wine[wine['country'].isin(country)]
    
    if variety:
        wine = wine[wine['variety'].isin(variety)]

    chart_2 = alt.Chart(wine.nlargest(35, 'points'), title="Average Rating of Top Rated Wine").mark_point(filled=True, size=40, opacity=0.9).encode(
        x=alt.X('mean(points)', title="Rating Score", scale=alt.Scale(zero=False), stack=None),
        y=alt.Y('variety:N', title="Variety", scale=alt.Scale(zero=False), sort='-x', stack=None),
        color=alt.Color('country:N', scale=alt.Scale(scheme='goldred')), 
        tooltip=alt.Tooltip(['mean(points)', 'mean(price)'], format=",.0f")).properties(
            width=250,
            height=120
        ).interactive()
    #alt.layer(chart_2.mark_line(color='blue').encode(y='mean'))
    chart_21 = alt.Chart(wine.nlargest(35, 'points'), title="Average Rating of Top Rated Wine").mark_line(opacity=0.9).encode(
        x=alt.X('points:Q', title="Rating Score", scale=alt.Scale(zero=False), stack=None),
        y=alt.Y('variety:N', title="Variety", scale=alt.Scale(zero=False), sort='-x', stack=None),
        color=alt.Color('variety:N', scale=alt.Scale(scheme='darkred'))).properties(
            width=250,
            height=120
        )#.interactive()

    #chart_2 = chart_21 + chart_21.mark_line()
    
    chart_3 = alt.Chart(wine.nlargest(35, 'points'), title="Average Price of Top Rated Wine").mark_point(filled=True, size=40, opacity=0.9).encode(
        x=alt.X('mean(price)', title="Price", sort='-y', stack=None),
        y=alt.Y('variety', title=" ", scale=alt.Scale(zero=False), sort='-x'),
        color=alt.Color('country:N', scale=alt.Scale(scheme='goldred'), legend=alt.Legend(title="Country")), 
        tooltip=alt.Tooltip(['mean(price)', 'mean(points)'], format=",.0f")
        #tooltip=['country', alt.Tooltip(['mean(price)', 'mean(points)'], format=",.0f")]
        #tooltip=[ alt.Tooltip(['country:N']), alt.Tooltip(['mean(price)', 'mean(points)'], format=",.0f")]
        ).properties(
            width=250,
            height=120
        ).interactive()

    chart = alt.vconcat(chart_2, chart_3)
    
    return chart.to_html()


@app.callback(
    Output('search-table', 'data'),
    [Input('country_widget', 'value')],
    [Input('variety_widget', 'value')],
    Input('price_slider', 'value'),
    Input('year_slider', 'value'),
    Input('score_slider', 'value'))
def update_table(country = None, variety = None, price_range = [4,1500], year_range = [1900, 2017], points_range = [80, 100]):
    wine = wine_df
    # filter by price
    wine = wine[(wine['price'] >= price_range[0]) & (wine_df['price'] <= price_range[1]) &
                (wine['year'] >= year_range[0]) & (wine_df['year'] <= year_range[1]) &
                (wine['points'] >= points_range[0]) & (wine_df['points'] <= points_range[1])]
    
    # def price_format(x):
    #         return "${:,.4f}".format(x/1)
    
    # wine['price'] = wine['price'].apply(price_format)

    if country:
        wine = wine[wine['country'].isin(country)]
    
    if variety:
        wine = wine[wine['variety'].isin(variety)]
    
    return wine.to_dict('records')


@app.callback(
    Output('results-table', 'data'),
    Input('search-table', "derived_virtual_data"),
    Input('search-table', "selected_rows"),
    Input('search-table', "derived_virtual_selected_rows"))
def update_results(rows, selected_rows, derived_virtual_selected_rows):
    if derived_virtual_selected_rows:
        row = int(derived_virtual_selected_rows[0])

        row_name = pd.DataFrame(rows).loc[row]['title']
        row_winery = pd.DataFrame(rows).loc[row]['winery']
        row_province = "Province: " + pd.DataFrame(rows).loc[row]['province']
        row_taster = pd.DataFrame(rows).loc[row]['taster_name']
        row_review = "Review: " + pd.DataFrame(rows).loc[row]['description']

        if pd.DataFrame(rows).loc[row]['designation']:
            row_designation = "Designation: " + pd.DataFrame(rows).loc[row]['designation']
        else:
            row_designation = "No Designation"
        

        results_table = pd.DataFrame(np.array([[row_name],
                                [row_province],
                                [row_designation],
                                [row_review]
                                ]),
                    columns=['Detailed Information'])

    else: results_table = pd.DataFrame(np.array([
        ["", "No wine selected. Click on a row in the table to the left to see detailed information about a selection."],
                                ]),
                    columns=[' ', 'Detailed Information'])

    return results_table.to_dict('records')




if __name__ == '__main__':
   app.run_server()
