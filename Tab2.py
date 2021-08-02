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
dict_dtypes = {x : 'str'  for x in lst_str_cols}
data = pd.read_csv('data_clean.csv', dtype=dict_dtypes)

# Converting Date column to string format to make it work with the animation
data["END_DATE"] = pd.to_datetime(data['END_DATE'], format='%Y/%m/%d %H:%M:%S')
data["DATE"] = data['END_DATE'].dt.date
data['Date_str'] = data['DATE'].astype(str)
dates_list_dates = data['DATE'].drop_duplicates().sort_values()
dates_list_numbers = [i for i in range(len(data['DATE'].unique()))]
map_date_to_number = {date: number for date, number in zip(dates_list_dates, dates_list_numbers)}
data['Date_num'] = [map_date_to_number[date] for date in data['DATE']]

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
    dash.dependencies.Output('bar_na', 'figure'),
    dash.dependencies.Input('times', 'value'),
)
def update_graph(time):
    sub = data[(data['Date_num'] >= time[0]) & (data['Date_num'] <= time[-1])]
    df_only_na = sub[sub.isnull().any(axis=1)]
    # NA Count Based on Production Line
    na = df_only_na.groupby("PRODUCTION_LINE_NAME").count()["END_DATE"].sort_values(ascending=False).reset_index()
    fig_na = px.bar(na, x="PRODUCTION_LINE_NAME", y="END_DATE")
    return fig_na

@app.dash_app.callback(
    dash.dependencies.Output('bar_neg', 'figure'),
    dash.dependencies.Input('times', 'value'),
)
def update_graph(time):
    sub = data[(data['Date_num'] >= time[0]) & (data['Date_num'] <= time[-1])]
    # Negative Duration Count Based on Production Line
    neg = sub[sub.DURATION_SECONDS < 0].groupby("PRODUCTION_LINE_NAME").count()["R_OS_ID"].sort_values(
        ascending=False).reset_index()
    fig_neg = px.bar(neg, x="PRODUCTION_LINE_NAME", y="R_OS_ID")
    return fig_neg

@app.dash_app.callback(
    dash.dependencies.Output('output', 'children'),
    [dash.dependencies.Input('times', 'value')])
def update_output(t):
    start = data[data["Date_num"] == t[0]]
    end = data[data["Date_num"] == t[1]]
    return "{} until {}".format(list(start["DATE"])[0], list(end["DATE"])[0])

def layout():
    return dbc.Tab(label="Pre-Processing", children=[
        html.Div([
            html.Div([
                html.Div([
                    html.Div(id='output'),
                    html.Div([
                        html.Div(children='''
                Negative Duration Count based on Production Line
            '''),
                dcc.Graph(id='bar_neg'),
                        ], className="five columns"),
                html.Div([
                    html.Div(children='''
               Missing Values Count based on Production Line
           '''),
                dcc.Graph(id='bar_na'),
                    ], className="five columns"),
                    ], className="row"),

                html.Div([
                    html.Div([
                        dcc.RangeSlider(
                            id="times",
                            min=dates_list_numbers[0],
                            max=dates_list_numbers[-1],
                            value=[dates_list_numbers[0], dates_list_numbers[-1]],
                            marks=dates_list_numbers_marks,
                            tooltip={'always_visible': False}),
                    ], className="eleven columns"),
                ], className="row"
                )], style={'margin-left': 50, 'margin-right': 50})
        ]),
    ])


