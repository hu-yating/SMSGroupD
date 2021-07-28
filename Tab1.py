import App

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import pandas as pd
import numpy as np
from dash.exceptions import PreventUpdate

import plotly.graph_objects as go
import plotly.express as px

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

app = App.App.get_instance()

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

def layout():
    return dbc.Tab(label="Tab", children=[
        html.Div([
            # Scatter plot for one specific day including selector and click value
            html.Div([
                html.Div([
                dcc.Dropdown(id='dropdown',
                             options=[
                                 {'label': 'example1', 'value': 'value1'},
                                 {'label': 'example2', 'value': 'value2'},
                                 {'label': 'example3', 'value': 'value3'},
                             ],
                             value='value1'),
                ], style={'margin-top': 20}),
                dcc.Graph(id='fig', figure=fig),
            ], className="ten columns"
            ),
        ], className="row"),
            ], className="ten columns"
            )

