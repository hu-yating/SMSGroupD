import dash
import dash_bootstrap_components as dbc


class App:
    __instance = None
    dash_app = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if App.__instance is None:
            App()
        return App.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if App.__instance is not None:
            raise Exception("This class is a singleton, call get_instance to access the App.")
        else:
            App.__instance = self
            self.init_dash_app()

    def init_dash_app(self):
        self.dash_app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

    def start_app(self):
        self.dash_app.run_server(debug=True, use_reloader=False)
