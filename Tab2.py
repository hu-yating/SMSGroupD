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
df_only_na = data[data.isnull().any(axis=1)]
df_no_na = data.dropna(inplace = False)

# Negative Duration Count Based on Production Line
neg = data[data.DURATION_SECONDS<0].groupby("PRODUCTION_LINE_NAME").count()["R_OS_ID"].sort_values(ascending=False).reset_index()
fig_neg = px.bar(neg, x="PRODUCTION_LINE_NAME", y="R_OS_ID")

# NA Count Based on Production Line
na = df_only_na.groupby("PRODUCTION_LINE_NAME").count()["END_DATE"].sort_values(ascending=False).reset_index()
fig_na = px.bar(na, x="PRODUCTION_LINE_NAME", y="END_DATE")

def layout():
    return dbc.Tab(label="Tab2", children=[
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                dcc.Graph(id='neg', figure=fig_neg),
                        ], className="five columns"),
                html.Div([
                dcc.Graph(id='na', figure=fig_na),
                    ], className="five columns"),
                    ], className="row"),
                ], style={'margin-left': 50, 'margin-right': 50}
            ),
        ]),
    ])

