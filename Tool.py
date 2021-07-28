import dash_html_components as html
import dash_bootstrap_components as dbc
import warnings
import Tab1
import App

warnings.simplefilter(action='ignore', category=FutureWarning)

# Init the app here, use app.get_instance to get the instance app
app = App.App.get_instance()

app.dash_app.layout = html.Div(
    children=[
        # Tabs-environment:
        dbc.Navbar(
            color="secondary",
            dark=True,
            style={'height': '64px'},
            children=[
                html.H2('SMS Group')
            ]
        ),
        dbc.Tabs(style={'fontWeight': 'bold', 'font-size': 24, 'font-family': 'Courier New'},
                 children=[
                     Tab1.layout()
                 ])
    ]
)

# START APP:
if __name__ == '__main__':
    #app.dash_app.run_server(debug=True)
    app.dash_app.run_server(port=8050, debug=True, use_reloader=False)

