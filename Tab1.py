import App

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

app = App.App.get_instance()

lst_str_cols = ['R_OS_ID', 'MATERIAL_ID', 'STEEL_GRADE']
dict_dtypes = {x : 'str' for x in lst_str_cols}
df = pd.read_csv('final_data.csv', dtype=dict_dtypes)

# Converting Date column to string format to make it work with the animation
df["END_DATE"] = pd.to_datetime(df['END_DATE'], format='%Y/%m/%d %H:%M:%S')
df["DATE"] = df['END_DATE'].dt.date
df['Date_str'] = df['DATE'].astype(str)
dates_list_dates = df['DATE'].drop_duplicates().sort_values()
dates_list_numbers = [i for i in range(len(df['DATE'].unique()))]
map_date_to_number = {date: number for date, number in zip(dates_list_dates, dates_list_numbers)}
df['Date_num'] = [map_date_to_number[date] for date in df['DATE']]

# Date range slider
dates_list_numbers_marks = {number: date.strftime('%d/%m/%y') for number, date in zip(dates_list_numbers, dates_list_dates)}
dates_list_numbers_marks = {(number if (number % 10 == 0) else "remove"):
                                {'label': date.strftime('%Y/%m/%d'), 'style': {'writing-mode': 'vertical-rl', 'text-orientation': 'sideways'}}
                            for number, date in zip(dates_list_numbers, dates_list_dates)}
dates_list_numbers_marks[dates_list_numbers[-1]] = {'label': dates_list_dates.iloc[-1].strftime('%Y/%m/%d'),
                                                    'style': {'writing-mode': 'vertical-rl',
                                                              'text-orientation': 'sideways'}}
dates_list_numbers_marks.pop('remove', None)

@app.dash_app.callback(
    dash.dependencies.Output('bar_small', 'figure'),
    dash.dependencies.Input('timing', 'value'),
)
def update_graph(time):
    sub = df[(df['Date_num'] >= time[0]) & (df['Date_num'] <= time[-1])]
    agg_weight = sub.groupby(["PRODUCTION_LINE_NAME"])["WEIGHT"].sum().reset_index()
    agg_weight = agg_weight.sort_values(['WEIGHT'], ascending=False)
    small_weight = agg_weight[agg_weight["WEIGHT"] <= 100]
    fig = px.bar(small_weight, x="PRODUCTION_LINE_NAME", y="WEIGHT")
    return fig

@app.dash_app.callback(
    dash.dependencies.Output('bar_big', 'figure'),
    dash.dependencies.Input('timing', 'value'),
)
def update_graph(time):
    sub = df[(df['Date_num'] >= time[0]) & (df['Date_num'] <= time[-1])]
    agg_weight = sub.groupby(["PRODUCTION_LINE_NAME"])["WEIGHT"].sum().reset_index()
    agg_weight = agg_weight.sort_values(['WEIGHT'], ascending=False)
    big_weight = agg_weight[agg_weight["WEIGHT"] > 100]
    fig = px.bar(big_weight, x="PRODUCTION_LINE_NAME", y="WEIGHT")
    return fig

@app.dash_app.callback(
    dash.dependencies.Output('output_timing', 'children'),
    [dash.dependencies.Input('timing', 'value')])
def update_output(t):
    start = df[df["Date_num"] == t[0]]
    end = df[df["Date_num"] == t[1]]
    return "{} until {}".format(list(start["DATE"])[0], list(end["DATE"])[0])

def layout():
    return dbc.Tab(label="Weight per Production Line", children=[
        html.Div([
            html.Div([
                html.Div([
                    html.Div(id='output_timing'),
                    html.Div([
                dcc.Graph(id='bar_big'),
                        ], className="five columns"),
                html.Div([
                dcc.Graph(id='bar_small'),
                    ], className="five columns"),
                    ], className="row"),

            html.Div([
                html.Div([
                dcc.RangeSlider(
                    id="timing",
                    min=dates_list_numbers[0],
                    max=dates_list_numbers[-1],
                    value=[dates_list_numbers[0], dates_list_numbers[-1]],
                    marks=dates_list_numbers_marks,
                    tooltip={'always_visible': False}),
                ], className="eleven columns"),
                ], className="row"
            ),
                ], style={'margin-left': 50, 'margin-right': 50}
            ),
        ]),
    ])

