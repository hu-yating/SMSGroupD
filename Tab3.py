import App

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

import scipy


import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

app = App.App.get_instance()

app = App.App.get_instance()

lst_str_cols = ['R_OS_ID', 'MATERIAL_ID', 'STEEL_GRADE']
dict_dtypes = {x : 'str' for x in lst_str_cols}
df = pd.read_csv('final_data.csv', dtype=dict_dtypes)


df_BAF = df.copy()
df_BAF.replace(['BAF01', 'BAF02', 'BAF03', 'BAF04', 'BAF05', 'BAF06',
       'BAF07', 'BAF08', 'BAF10', 'BAF11', 'BAF12', 'BAF13', 'BAF14',
       'BAF15', 'BAF16', 'BAF17', 'BAF18', 'BAF19', 'BAF20', 'BAF21',
       'BAF22', 'BAF23', 'BAF24'],"BAF",inplace=True)

@app.dash_app.callback(
    dash.dependencies.Output('distr', 'figure'),
    dash.dependencies.Input('selector_line', 'value'),
    dash.dependencies.Input('selector_par', 'value')
)
def update_graph(select_line, select_par):
    sub = df_BAF[(df_BAF['PRODUCTION_LINE_NAME'] == select_line)]
    arr = []

    if select_par == "THICKNESS":
        X = [i for i in list(sub["THICKNESS"]) if i != 0]
        if X:
            arr.append(X)
    if select_par == "WIDTH":
        X = [i for i in list(sub["WIDTH"]) if i != 0]
        if X:
            arr.append(X)
    if select_par == "LENGTH":
        X = [i for i in list(sub["LENGTH"]) if i != 0]
        if X:
            arr.append(X)
    # Create distplot with custom bin_size
    fig = ff.create_distplot(arr, ["distribution"], bin_size=.1)
    return fig

def layout():
    return dbc.Tab(label="Distribution", children=[
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                dcc.Graph(id='distr'),
                        ], className="ten columns"),
                    ], className="row"),
            html.Div([
                    dcc.Dropdown(id='selector_line',
                        options=[
                            {'label': 'Electr.arc furnace', 'value': 'EAF1'},
                            {'label': 'Ladle furnace', 'value': 'LF1'},
                            {'label': 'Quality check', 'value': 'QC'},
                            {'label': 'Announcement', 'value' : 'ANN'},

                            {'label': 'Attach', 'value': 'ATT'},
                            {'label': 'Book in', 'value': 'B_IN'},
                            {'label': 'Book out', 'value': 'B_OUT'},
                            {'label': 'Set of batch annealing furnaces', 'value': 'BAF'},

                            {'label': 'CSP Caster', 'value': 'CCM1'},
                            {'label': 'Cont.galvanizing line', 'value': 'CGL1'},
                            {'label': 'CGL1 entry reject', 'value': 'CGL1R'},
                            {'label': 'Set of batch annealing furnaces', 'value': 'BAF'},

                            {'label': 'CSP line 1', 'value': 'CSP'},
                            {'label': 'Coil yard', 'value': 'CY'},
                            {'label': 'Manual change', 'value': 'DC3'},
                            {'label': 'Delivery', 'value': 'DEL'},

                            {'label': 'Dispatch', 'value': 'DISP'},
                            {'label': 'Location change', 'value': 'EDTLOC'},
                            {'label': 'Hot mill sample cut', 'value': 'HSC'},
                            {'label': 'CSP Hot strip mill', 'value': 'HSM'},
    ],
                        value='QC'
                    ),
                dcc.Dropdown(id='selector_par',
                             options=[
                                 {'label': 'Thickness', 'value': 'THICKNESS'},
                                 {'label': 'Width', 'value': 'WIDTH'},
                                 {'label': 'Length', 'value': 'LENGTH'}
                             ],
                             value='WIDTH'
                             ),
                ], className="five columns"),
                ], style={'margin-left': 50, 'margin-right': 50}
            ),
        ]),
    ])